---
title: "Slashing CI Costs at Uber"
author: "Unknown"
url: "https://www.uber.com/blog/slashing-ci-costs-at-uber/"
published_date: "None"
downloaded_date: "2025-09-15T09:38:08.103720"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for Slashing CI Costs at Uber](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/blogcover-17507196944018-1024x604.jpg)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fslashing-ci-costs-at-uber%2F&t=Slashing+CI+Costs+at+Uber)
  * [X social](https://twitter.com/share?text=Slashing+CI+Costs+at+Uber&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fslashing-ci-costs-at-uber%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fslashing-ci-costs-at-uber%2F)
  * [Envelope](mailto:?subject=Slashing+CI+Costs+at+Uber&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fslashing-ci-costs-at-uber%2F)
  * Link

# Introduction
Hundreds of engineers can commit changes to a single repository in modern software development, particularly within large and fast-paced technology companies [1]. This situation presents a significant challenge: efficiently managing these changes, quickly resolving conflicts, and ensuring that the mainline remains green. A mainline is considered green if all build steps—compilation, unit tests, and UI tests—successfully execute for every commit point in the repository history. Maintaining a green mainline is critical for enabling rapid development and deployment cycles. However, as highlighted in the Bernardo and Alenca study [2], landing changes rapidly while keeping the mainline green becomes increasingly difficult as the codebase grows in size and complexity, further compounded by the concurrency of changes submitted by numerous developers.
CI (Continuous Integration) systems enable rapid iteration while safeguarding the stability of production systems. As organizations scale, so do the challenges in managing code integration, resolving conflicts, and minimizing the risk of regressions. Without robust CI systems, teams face delayed releases, increased operational overhead, and decreased developer velocity.
[SubmitQueue](https://www.uber.com/blog/bypassing-large-diffs-in-submitqueue/) is designed to continuously land changes efficiently while maintaining a green mainline. More than 4,500 engineers across Uber’s global development centers rely on it every day, contributing to thousands of microservices and tens of mobile apps. This system processes tens of thousands of changes each month. This scale involves managing hundreds of millions of lines of code across six major monorepos and seven programming languages. SubmitQueue facilitates hundreds of thousands of deployments and handles millions of configuration changes monthly. In this high-velocity development environment, ensuring the efficient integration of changes while landing them quickly into the mainline is crucial for maintaining service reliability, operational stability, and maximizing developer productivity.
SubmitQueue operates by speculating on the outcomes of all pending changes and constructing a speculation tree that outlines all possible builds for changes currently in the system. It uses a combination of a probabilistic model and a machine learning model to prioritize the builds most likely to succeed, executing them in parallel to minimize land times. This ensures that only changes passing all required checks are landed, thereby preserving the integrity of the mainline. Additionally, SubmitQueue performs conflict analysis between changes to prune the speculation tree, allowing independent changes to be built concurrently.
This blog describes how Uber enhanced SubmitQueue to slash CI resource usage by 53% and speed up wait times by 37%—all while keeping mainlines green. 
* * *
## Problem
While SubmitQueue addresses many challenges in maintaining a green mainline, it still has certain limitations. As highlighted in [a previous blog](https://www.uber.com/blog/research/keeping-master-green-at-scale), SubmitQueue has a strategy where it ends ongoing builds of changes when the builds of the newly arrived changes are predicted to have a higher likelihood of success than those already in progress. This leads to two key issues:
  * **High resource utilization:** A significant number of builds are prematurely ended, with an estimated 40-65 % of builds being affected across major monorepos at Uber, which in turn leads to the need for scheduling additional builds for the changes whose builds ended.
  * **Increased waiting times:** SubmitQueue processes changes in the order they’re submitted. As a result, changes with shorter build times that arrive after a large, time-consuming change must wait for the larger change to either commit or reject before proceeding.

The introduction of [BLRD (Bypassing Large Diffs)](https://www.uber.com/en-US/blog/bypassing-large-diffs-in-submitqueue/) has partly addressed the issue of increased waiting times by introducing the concept of commutativity in change ordering. According to BLRD, if all the speculative builds for a smaller change, when blocked by a larger, time-consuming conflicting change, have been evaluated and yield consistent outcomes, the smaller change can safely bypass the larger change and be landed or rejected based on the outcome. However, not all speculative builds for the smaller change are evaluated in most cases, as they aren’t prioritized. This occurs because SubmitQueue’s probabilistic model assumes that only a single build is required to make a decision for each change and can’t distinguish between smaller and larger time-consuming changes to prioritize the builds accordingly. As a result, smaller changes continue to experience long waiting times when their speculative builds aren’t prioritized, even though they could ‌bypass the larger changes ahead in the queue.
Addressing these limitations is crucial for two reasons. First, resource utilization directly impacts operational costs, especially in fast-paced companies with high development velocity. Estimates suggest that large-scale CI systems incur costs in the millions annually [4]. Inefficient build prioritization can further escalate these costs. For companies with limited budgets, this poses a significant barrier to adopting CI practices. Additionally, long waiting times reduce system efficiency and hinder developer productivity, as engineers face delays in landing their changes.
* * *
## Architecture
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/figure1-17507206349934-1024x352.png)Figure 1: Architecture of SubmitQueue.
When a change is submitted to SubmitQueue via the API service, it’s added to a distributed queue for processing. The service broadly consists of four core components responsible for executing all necessary build steps for each enqueued change. It ultimately decides whether to land or reject the change and the reason for the rejection. Figure 1 shows the high-level architecture of SubmitQueue, described below.
The Enumerator processes the queue of pending changes by constructing a speculation tree that outlines all possible builds for changes currently in the system. Using a target analyzer to identify potential conflicts between changes, the Enumerator prunes unnecessary speculations to increase the likelihood of executing the remaining ones and identifies independent changes that can be built in parallel, improving throughput.
The Profiler takes the speculation trees generated by the enumerator to create a profile for each tree, capturing information about the bypassing changes linked to each change within the tree. By predicting the build times of the nodes in the speculation tree, the build-time analyzer enables the Profiler to accurately identify the bypassing changes associated with each change.
The Prioritizer calculates the probability of build needed for each node in the speculation tree by using change-bypassing data from the speculation tree profile and the success likelihood score of each change within SubmitQueue. It then ranks the builds based on these probabilities. The success likelihood score is predicted using a machine-learning-powered success predictor, enabling the Prioritizer to make more informed build prioritization decisions.
The Selector processes the prioritized builds and performs these actions: 
  * Schedules high-probability builds for execution in the CI
  * Ends ongoing builds that don’t exist in the latest set of prioritized builds
  * Safely commits changes to the monorepo once they meet all criteria for landing

* * *
## Bypassing Large Diffs (BLRD)
SubmitQueue executes builds in parallel to precompute results. However, it only decides whether to commit or reject a change once its corresponding build finishes and reaches the head of the tree. As a result, smaller changes that arrive after larger conflicting changes are often delayed, even if their builds are completed earlier. Large changes affecting many build targets can conflict with nearly every subsequent change processed by SubmitQueue. As shown in Figure 3, conflicts are frequent in ‌monorepos, and as the number of conflicts increases, the speculation tree grows deeper, further exacerbating delays.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/figure-2-17507206533373-1024x974.png)Figure 2: Monthly conflict rates across Go, iOS, and Android monorepos from January to June 2024.
BLRD can expedite the landing of smaller changes if all of their speculative builds with the conflicting larger changes ahead yield the same outcome.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/figure-3-17507206809575-1024x593.png)Figure 3: Speculation tree of builds for conflicting changes C1, C2, and C3 arrived in the order mentioned.
In Figure 3, let _H_ represent the current repository HEAD and C1, C2, and C3 represent conflicting changes to be committed. Here C1 is a large, time-consuming change, while C2 is smaller and faster. For these changes, the following build steps are defined:
  * B1 – Build steps for C1 against H
  * B2 – Build steps for C2 against H
  * B1.2 – Build steps for C2 against H + C1
  * B1.2.3 – Build steps for C3 against H + C1 \+ C2
  * B1.3 – Build steps for C3 against H + C1
  * B2.3 – Build steps for C3 against H + C2
  * B3 – Build steps for C3 against H

Let _M (S, C)_ represent the state of the mainline after applying change C to state S. SubmitQueue tests C2 both on the current HEAD (B2) and against C1 (B1.2). If both speculative builds B2 and B1.2 produce identical results, then the outcome of landing C2 is independent of whether C1 lands before or after. In this case, C2 can be safely landed while C1 is still in progress, ensuring:
 _M (M (H, C_ _1_ _), C_ _2_ _) = M (M (H, C_ _2_ _), C_ _1_ _)_
The order of landing C1 and C2 behaves commutatively. For more details and a complete proof of the BLRD concept, refer to the [blog about bypassing large diffs](https://www.uber.com/en-US/blog/bypassing-large-diffs-in-submitqueue/). 
* * *
## Probabilistic Model
SubmitQueue prioritizes builds based on their likelihood of being needed to optimize resource utilization. The probability _P BC_ represents the likelihood that the result of build BC will be used to decide whether to commit or reject the change C. The probabilistic model proposed in ‌prior research at Uber was based on the assumptions that only one build is necessary to determine the fate of a change and that changes are landed onto the mainline in the order they arrive in the queue.
However, these assumptions no longer hold with the introduction of BLRD. BLRD allows smaller changes to bypass larger, conflicting ones if all speculative builds of the smaller change are evaluated and produce consistent outcomes before the larger change completes. This requires SubmitQueue to evaluate multiple builds per change, ensuring smaller changes can bypass larger ones when eligible. The previous model’s assumption of a single build determining a change’s outcome is insufficient, as BLRD demands equal prioritization of all speculative builds to assess eligibility to bypass. However, evaluating all builds is expensive because the number of builds grows exponentially with the depth of the speculation tree. Therefore, after the introduction of BLRD, the probabilistic model needs to prioritize builds to expedite the landing of the changes while optimizing resource usage. The new model should focus on two key objectives:
  * **Prioritize speculative builds for possible bypasses:** When changes can bypass larger conflicting changes ahead in the queue, all speculative builds of the eligible changes must be prioritized equally to allow smaller changes to land quickly.

  * **Schedule builds for most likely paths in the speculation tree for non-bypassing changes:** When a change’s builds are likely to finish after the conflicting changes ahead in the queue are landed or rejected, only the most necessary speculative builds should be prioritized, as one build is sufficient to determine the outcome.

Putting the above two objectives into a mathematical notation, we could derive the following formulae:
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/image-6-23-25-at-5.33pm-17507252313777-1024x206.jpeg)
[](https://www.codecogs.com/eqnedit.php?latex=P%5E%7B%5Ctext%7Bneeded%7D%7D_%7BB_C%7D%20%3D%20%5Cprod_%7BC_i%20%5Cin%20%5Cmathcal%7BF%7D%7D%20P%5E%7B%5Ctext%7Boutcome%7D%7D_%7BB_%7BC_i%7D%7D%20%5Ctimes%20%5Cprod_%7BC_j%20%5Cin%20%5Cmathcal%7BB%7D%7D%20P\(FT_C%20%3C%20FT_%7BC_j%7D\)#0)
where:
  * [](https://www.codecogs.com/eqnedit.php?latex=P%5E%7B%5Ctext%7Bneeded%7D%7D_%7BB_C%7D#0) _P BC_ represents the probability of a build being needed for a change C
  * [](https://www.codecogs.com/eqnedit.php?latex=%5Cmathcal%7BF%7D#0) _F_ is the set of conflicting changes ahead of C in the queue that C doesn’t bypass
  * [](https://www.codecogs.com/eqnedit.php?latex=%5Cmathcal%7BB%7D#0) _B_ is the set of conflicting changes ahead that C may bypass
  * [](https://www.codecogs.com/eqnedit.php?latex=%20P%5E%7B%5Ctext%7Boutcome%7D%7D_%7BB_%7BC_i%7D%7D#0) PBCi represents the probability of the build outcome BCi [](https://www.codecogs.com/eqnedit.php?latex=%20B_%7BC_i%7D#0) for change Ci in _F_. The estimation of this probability is explained in [the prior blog](https://www.uber.com/blog/research/keeping-master-green-at-scale/)
  * [](https://www.codecogs.com/eqnedit.php?latex=P\(FT_C%20%3C%20FT_%7BC_j%7D\)#0) P(FTc < FTCj) represents the probability that the finish time of C is less than the finish time of the change Cj in  _B_ [](https://www.codecogs.com/eqnedit.php?latex=%5Cmathcal%7BB%7D%20#0), allowing C to bypass Cj

In extreme cases, when the speculation depth increases in the tree, the system defaults to the original probabilistic model, prioritizing the most likely build needed for the change, that is,
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/image-6-23-25-at-5.34pm-17507252695749-1024x134.jpeg)
where _A_[](https://www.codecogs.com/eqnedit.php?latex=%20%5Cmathcal%7BA%7D#0) is the set of all changes ahead of C in the queue. This ensures efficient build prioritization and resource usage while minimizing unnecessary scheduling.
* * *
## Estimating the Build Completion Order
Given two conflicting changes, Cx and Cy, arriving at times ATx and ATy ( ATx < ATy), with respective finish times FTx and FTy , and predicted build times Tx and Ty, our goal is to estimate the probability that the build for Cy will finish before the build for Cx, expressed as:
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/image-6-23-25-at-5.34pm-17507253017815.jpeg)
The predicted build times, Tx and Ty can be approximated as normally distributed random variables. We use the NGBoost model [5], which is well-suited for probabilistic modeling, to predict build times. NGBoost learns patterns from historical builds to capture both the central tendency (mean) and variability (variance) in build times, smoothing out data irregularities and representing the predicted build times as a normal distribution. So,
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/image-6-23-25-at-5.35pm-17507253398563.jpeg)
[](https://www.codecogs.com/eqnedit.php?latex=T_x%20%5Csim%20%5Cmathcal%7BN%7D\(%5Cmu_x%2C%20%5Csigma_x%5E2\)%2C%20%5Cquad%20T_y%20%5Csim%20%5Cmathcal%7BN%7D\(%5Cmu_y%2C%20%5Csigma_y%5E2\)#0)
  * [](https://www.codecogs.com/eqnedit.php?latex=%5Cmu_x#0) ux and uy represent the combined mean build times
  * [](https://www.codecogs.com/eqnedit.php?latex=%5Csigma_x%5E2#0)o2x and o2y[](https://www.codecogs.com/eqnedit.php?latex=%20%5Csigma_y%5E2#0) represent the combined variances of the builds for changes Cx and Cy

The combined mean and variance are computed by averaging the individual builds’ means and variances. We seek to compute:
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/image-6-23-25-at-5.36pm-17507253793548-1024x96.jpeg)
[](https://www.codecogs.com/eqnedit.php?latex=P\(FT_y%20%3C%20FT_x\)%20%3D%20P\(\(T_y%20%2B%20AT_y\)%20%3C%20\(T_x%20%2B%20AT_x\)\)#0)
This expression can be rewritten as:
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/image-6-23-25-at-5.36pm-17507254212154.jpeg)
[](https://www.codecogs.com/eqnedit.php?latex=P\(T_y%20-%20T_x%20%3C%20AT_x%20-%20AT_y\)#0)
We aim to compute the probability that the difference in build times Ty – Tx , is less than the difference in arrival times ATx – ATy . The random variables Tx and Ty are normally distributed, so the difference D = Ty – Tx is also normally distributed. The mean and variance of D are given by:
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/image-6-23-25-at-5.38pm-17507255434313.jpeg)
The Z-score formula is used to standardize this difference:
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/image-6-23-25-at-5.40pm-17507256619878.jpeg)
[](https://www.codecogs.com/eqnedit.php?latex=Z%20%3D%20%5Cfrac%7B\(AT_x%20-%20AT_y\)%20-%20\(%5Cmu_y%20-%20%5Cmu_x\)%7D%7B%5Csqrt%7B%5Csigma_x%5E2%20%2B%20%5Csigma_y%5E2%7D%7D#0)
The Z-score measures how far the difference between arrival times is from the difference in build times, in standard deviations. Using the cumulative distribution function (CDF) of the standard normal distribution, the cumulative probability gives the likelihood that Cy finishes before Cx
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/image-6-23-25-at-5.41pm-17507257061492.jpeg)
Φ(_Z_) represents the value of the CDF for the Z-score.
For more details on the working of the new probabilistic and machine learning models, refer to [the prior blog](https://www.uber.com/blog/research/keeping-master-green-at-scale/) and the original Juloori and Lin paper [3].
* * *
## Speculation Threshold
Setting a minimum threshold of _P BC_ [](https://www.codecogs.com/eqnedit.php?latex=P%5E%7Bneeded%7D_%7BB_C%7D#0)can ensure that only the most probable nodes are selected for building. The threshold score should be informed by historical build data and adjusted based on the specific characteristics of the monorepos. However, setting the threshold too high can negatively impact land times, especially during high-load conditions. In such cases, more changes may be forced to wait for their builds, particularly if they conflict with larger changes ahead in the queue. Additionally, simply setting the speculation threshold could still leave smaller changes blocked by larger ones if the speculative builds of the smaller changes receive a _P_ _ BC_ [](https://www.codecogs.com/eqnedit.php?latex=P%5E%7Bneeded%7D_%7BB_C%7D#0)score less than the threshold.
By leveraging the new probabilistic model, ‌scores of speculative builds for smaller changes can be boosted if those changes are likely to bypass larger conflicting changes ahead. So, setting an appropriate speculation threshold, combined with the probabilistic model, strikes an optimal balance between resource usage and land times, ensuring efficient build scheduling without compromising throughput.
* * *
## Evaluation
SubmitQueue has been in production at Uber for several years. In 2024, we rolled out a new strategy across three of Uber’s largest monorepos—Go, iOS, and Android—which consist of hundreds of millions of lines of code and handle thousands of daily changes submitted by hundreds of developers. To evaluate the effectiveness of this strategy, we tracked key performance metrics—weekly CPU hours, build-to-changes ratio, and P95 waiting times—over a 21-week period, capturing both pre- and post-rollout data. While our evaluation focused on Uber’s monorepos, the techniques presented here are language-agnostic and platform-independent. The following subsections summarize the performance improvements observed for each metric across the Go, iOS, and Android monorepos.
* * *
## Resource Usage
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/figure-4-17507207106361.png)Figure 4: Weekly trend of builds-to-changes ratio across Go, iOS, and Android monorepos.
The build-to-changes ratio is a critical metric for assessing resource efficiency in our CI pipeline. Figure 4 shows the ratio trends over the 21-week evaluation period.
In the first 10 weeks before the rollout, the ratio fluctuated between 3 and 6, with iOS and Android showing greater variability. The Android monorepo peaked at a ratio of 6 in Week 7, highlighting inefficiencies in resource utilization due to excessive builds per change.
After the rollout, a sharp decline in the ratio was observed across all monorepos. The Go monorepo saw a reduction of 45.45% (from a pre-rollout average of 3.39 to a post-rollout average of 1.85), iOS decreased by 47.86% (from 4.93 to 2.57), and Android achieved the largest reduction of 64.02%, dropping from 5.43 to 1.96. These results demonstrate improved resource allocation and more efficient build scheduling post-rollout.
* * *
## CPU Hours Consumption
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/figure-5-17507207268521.png)Figure 5: Weekly CPU hours consumption across Go, iOS, and Android monorepos.
Before the rollout, CPU usage was consistently high, particularly in the Go monorepo, which peaked at around 2,000 hours in Week 8. Android and iOS fluctuated between 500 and 800 hours and 400 to 600 hours, respectively.
Following the rollout, CPU hours dropped significantly across all monorepos. Go’s CPU consumption fell by 44.70% (from a pre-rollout average of 1,485 to a post-rollout average of 821 hours), iOS decreased by 34.86% (from 472 to 307 hours), and Android saw a reduction of 52.23% (from 729 to 348 hours). These reductions highlight the efficiency gains from minimizing unnecessary builds, leading to substantial cost savings and improved scalability.
* * *
## P95 Waiting Times
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/figure-6-17507207422556.png)Figure 6: Weekly p95 waiting times for changes in Go, iOS, and Android monorepos.
CI resource usage isn’t the only metric to optimize in this work. Trivially, we can set the speculation threshold so high that SubmitQueue rarely speculates more than one path, which would reduce CI resource usage too. However, that would also reduce the efficiency of SubmitQueue, because BLRD, which requires multiple speculation paths, wouldn’t be used. When the conditions for BLRD aren’t met, a change has to wait in SubmitQueue, even though all its speculative builds have finished. We monitor P95 waiting times before and after the rollout to make sure the reduction in resource usage doesn’t reduce ‌efficiency. Figure 7 shows the weekly P95 waiting times across the Go, iOS, and Android monorepos.
Initially, waiting times fluctuated significantly, with the Go monorepo showing peaks around weeks 5 and 10. After the new strategy was implemented in Week 11, all monorepos showed stabilization, particularly on iOS and Android, where waiting times consistently dropped to lower levels than pre-rollout. Go also showed reduced variability, with more stable waiting times after Week 15.
Overall, the P95 waiting times were reduced by 44.67% for Go (from a pre-rollout average of 33.69 minutes to a post-rollout average of 18.64 minutes), 33.32% for iOS (from 14.86 minutes to 9.91 minutes), and 31.66% for Android (from 25.36 minutes to 17.33 minutes). This reduction signifies the impact of the new build prioritization strategy in expediting smaller changes landing using BLRD.
* * *
# Conclusion
There have been doubts about how far we can go in keeping the main branch green while having the land time and resource usage under control. The new enhancement to SubmitQueue once again proved it possible in repositories as large as what we have at Uber, which are among the largest in the world. Building on [BLRD’s shorter build times](https://www.uber.com/en-US/blog/bypassing-large-diffs-in-submitqueue/) and earlier work, we leverage machine learning for build-time predictions within a novel probabilistic framework. This approach mitigates inefficiencies caused by resource contention and larger conflicting changes. A speculation threshold further streamlines the process by scheduling only the most probable builds. The result is a highly efficient solution for managing software changes—adaptable from small teams to large enterprises—leading to faster releases, reduced costs, and higher software quality.
As the business grows, the size of the engineering team grows too, which in turn produces a higher rate of commits to the repositories. As we improve our developer tooling, especially with the recent usage of AI coding assistants, engineers’ productivity increases too, further increasing the commit rate, which reaches its peak during business hours in the United States. Even if we manage to maintain the build and test time (which isn’t easy as the repo size grows), higher commit rate means new conflict commits arrive before SubmitQueue process the commits in the queue, leading to deeper speculation trees, to a point that BLRD become more and more expensive. We have to come up with new scheduling algorithms to increase the throughput of SubmitQueue without requiring more resources. 
Stay tuned!
* * *
### References
[1] R. Potvin, J. LevenBerg: [Why Google Stores Billions of Lines of Code in a Single Repository](https://dl.acm.org/doi/pdf/10.1145/2854146)
[2] J. Bernardo, D. Alenca: [Studying the impact of adopting CI on the delivery time of pull requests](https://doi.org/10.1145/3196398.3196421)
[3] D. Juloori, Z. Lin: [CI at Scale: Lean, Green and Fast](https://arxiv.org/pdf/2501.03440)
[4] X. Jin, F. Servant: [A cost-efficient approach to building in continuous integration](https://dl.acm.org/doi/10.1145/3377811.3380437)[5] D. Tony and A. Anand: [NGBoost: Natural Gradient Boosting for Probabilistic Prediction](https://stanfordmlgroup.github.io/projects/ngboost/)
Stay up to date with the latest from Uber Engineering—follow us on [LinkedIn](https://p.uber.com/eng-linkedin) for our newest blog posts and insights.
* * *
![Dhruva Juloori](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/dhruvajuloori-17507248191847.jpeg)
Dhruva Juloori
Dhruva Juloori is a Senior Software Engineer at Uber, specializing in machine learning and algorithms. He’s the key engineer behind Uber’s SubmitQueue, a transformative CI scheduling system that guarantees an always-green mainline at scale by handling hundreds of changes per hour across Uber’s diverse monorepos. Dhruva’s work empowers thousands of engineers to deliver high-quality code efficiently. His work focuses on building scalable distributed and ML systems that enhance developer productivity and streamline CI/CD processes.
![Matthew Williams](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2023/08/Matthew-Williams-771x1024.jpg)
Matthew Williams
Matthew Williams is a Staff Software Engineer for Developer Platform. He is the Technical Lead for SubmitQueue, and especially interested in improving performance and reliability for large monorepos. Matthew is also the Technical Lead for TargetAnalyzer, a service that computes changed targets in both Buck and Bazel based monorepos.
![Zhongpeng Lin](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2023/08/zhongpenglin-17507249715733-1024x1024.jpg)
Zhongpeng Lin
Zhongpeng Lin is a Staff Software Engineer for Developer Platform. He is one of the founding members of Uber’s Go Monorepo, and has been the Tech Lead of its build system since then. Over the years, he also worked on various areas that improved the developer experience for Go Monorepo, such as code coverage, Git sparse checkout, and dependency management. He is also a maintainer of Bazel’s Go rule set (a.k.a. rules_go) and Gazelle, as well as a frequent contributor to open source projects used by Uber.
* * *
Posted by Dhruva Juloori, Matthew Williams, Zhongpeng Lin 
Category:
[Engineering](/en-CA/blog/engineering/)
[Backend](/en-CA/blog/engineering/backend/)
[Uber AI](/en-CA/blog/engineering/ai/)
* * *
### Related articles
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/09/cover-photo-clock-gears-17575284883091-1024x680.jpg)Engineering, Backend, Data / MLOpen-Sourcing Starlark Worker: Define Cadence Workflows with StarlarkSeptember 11 / Global](/en-CA/blog/starlark/)
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/09/cover-photo-17569388153419-1024x683.jpg)Engineering, Data / MLBuilding Uber’s Data Lake: Batch Data Replication Using HiveSyncSeptember 4 / Global](/en-CA/blog/building-ubers-data-lake-batch-data-replication-using-hivesync/)
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/cover-photo-2-17563345896014-1024x629.jpg)Engineering, BackendControlling the Rollout of Large-Scale Monorepo ChangesAugust 28 / Global](/en-CA/blog/controlling-the-rollout-of-large-scale-monorepo-changes/)
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/cover-1-17561626024808-1024x683.jpg)Engineering, BackendHow Uber Serves over 150 Million Reads per Second from Integrated Cache with Stronger Consistency GuaranteesAugust 26 / Global](/en-CA/blog/how-uber-serves-over-150-million-reads/)
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/cover-photo-17557274589976.jpg)Engineering, BackendLightweight Office Infrastructure: Transitioning from Backbone to SD-WANAugust 21 / Global](/en-CA/blog/lightweight-office-infrastructure/)
## Most popular
[![Post thumbnail](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/cropped-17508030478819-1024x512.png)EarnJune 30 / CanadaHelping you stay informed about risks to your account status](/en-CA/blog/new-reports-experience/)[![Post thumbnail](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/cover-17514078235579-1024x683.jpg)Engineering, Data / ML, Uber AIJuly 2 / GlobalReinforcement Learning for Modeling Marketplace Balance](/en-CA/blog/reinforcement-learning-for-modeling-marketplace-balance/)[![Post thumbnail](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/41577658914f37d9ff4d8o-17525304449657-1024x499.jpg)Engineering, BackendJuly 15 / GlobalHow Uber Processes Early Chargeback Signals](/en-CA/blog/how-uber-processes-early-chargeback-signals/)[![Post thumbnail](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/02/UberIM_009076-1024x684.jpg)TransitJuly 15 / GlobalYour guide to NJ TRANSIT’s Access Link Riders’ Choice Pilot 2.0](/en-CA/blog/your-guide-to-access-link-riders-choice-pilot-2-0/)
[View more stories](/en-CA/blog/engineering/)
## Select your preferred language
[English](/en-CA/blog/slashing-ci-costs-at-uber/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
  * ### Products
    * [EarnResources for driving and delivering with Uber](/en-CA/blog/earn/)
    * [RideExperiences and information for people on the move](/en-CA/blog/ride/)
    * [EatOrdering meals for delivery is just the beginning with Uber Eats](/en-CA/blog/eat/)
    * [MerchantsPutting stores within reach of a world of customers](/en-CA/blog/merchants/)
    * [BusinessTransforming the way companies move and feed their people](/en-CA/blog/business/)
    * [FreightTaking shipping logistics in a new direction](/en-CA/blog/freight/)
    * [Higher EducationEnhancing campus transportation](/en-CA/blog/higher-education/)
    * [TransitExpanding the reach of public transportation](/en-CA/blog/transit/)
  * ### Company
    * [CareersExplore how Uber employees from around the globe are helping us drive the world forward at work and beyond](/en-CA/blog/careers/)
    * [EngineeringThe technology behind Uber Engineering](/en-CA/blog/engineering/)
    * [NewsroomUber news and updates in your country](https://uber.com/newsroom)
    * [Uber.comProduct, how-to, and policy content—and more](https://uber.com)

EN
## Select your preferred language
[English](/en-CA/blog/slashing-ci-costs-at-uber/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
