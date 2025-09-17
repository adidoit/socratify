---
title: "uReview: Scalable, Trustworthy GenAI for Code Review at Uber"
author: "Unknown"
url: "https://www.uber.com/blog/ureview/"
published_date: "None"
downloaded_date: "2025-09-15T09:37:54.001547"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for uReview: Scalable, Trustworthy GenAI for Code Review at Uber](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/figure-header-option3-17549520285216-1024x494.png)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fureview%2F&t=uReview%3A+Scalable%2C+Trustworthy+GenAI+for+Code+Review+at+Uber)
  * [X social](https://twitter.com/share?text=uReview%3A+Scalable%2C+Trustworthy+GenAI+for+Code+Review+at+Uber&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fureview%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fureview%2F)
  * [Envelope](mailto:?subject=uReview%3A+Scalable%2C+Trustworthy+GenAI+for+Code+Review+at+Uber&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fureview%2F)
  * Link

# Introduction
Code reviews are a core component of software development that help ensure the reliability, consistency, and safety of our codebase across tens of thousands of changes each week. However, as services grow more complex, traditional peer reviews face new challenges. Reviewers are overloaded with the increasing volume of code from AI-assisted code development, and have limited time to identify subtle bugs, security issues, or consistently enforce best practices. These limitations can lead to missed errors, slower feedback loops, and other issues, ultimately resulting in production incidents, wasted resources, and slow release cycles.
To address these pain points at scale, we developed uReview, an AI code review platform designed to augment the code review process with a second AI reviewer. At the core of this system is Commenter, a modular, multi-stage GenAI system review system to identify functional bugs, error handling issues, security vulnerabilities, and adherence to internal coding standards. Building on this, Fixer proposes actual code changes in response to comments, whether those comments come from humans or AI. In this blog, we’ll focus on Commenter and refer to it simply as uReview. 
The main challenge of AI code review is false positives from two sources: LLM hallucinations that generate incorrect comments and issues that are generally valid but not important in that specific scenario (like a performance issue in code that isn’t performance sensitive). A high false‑positive rate undermines engineers’ perception of the tool’s accuracy and usefulness—when they encounter many false-positive comments, they start to tune out and ignore them. We delve into how uReview tackles these challenges to achieve its main goals: to raise the signal-to-noise ratio in code reviews, minimize human effort, and provide Uber engineers with timely, high-quality feedback.
uReview today analyzes over 90% of the weekly ~65,000 diffs (equivalent of pull requests) landed at Uber. Engineers who interact with the tool mark 75% of its comments as useful, and we see over 65% of its posted comments addressed. Figure 1 shows an example of an incorrect metric bug caught by uReview.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/figure-1-17549522301065-974x1024.png)Figure 1: Incorrect metric bug caught by uReview.
* * *
## How It Works
uReview is a modular, multi-stage GenAI system designed to automate and enhance code reviews across Uber’s engineering platforms. Its prompt-chaining-based architecture breaks down the code-review task into four simpler sub-tasks, and allows each sub-task—comment generation, filtering, validation, and deduplication—to evolve independently. We now discuss each in turn. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/figure2-llm-17549522932245-1024x417.png)Figure 2: uReview pipeline.
### **Ingestion and Preprocessing**
When a developer submits a change on Uber’s code review platform, uReview first determines which files are eligible for automated review. It filters out low-signal targets such as configuration files, generated code, and experimental directories.
For the remaining files, the system builds a structured prompt that includes surrounding code context such as nearby functions, class definitions, and import statements. This context helps the language model produce precise and relevant suggestions.
### **Comment Generation by Specialized Assistants**
uReview uses a pluggable assistant framework, where each assistant focuses on a specific class of issues. This pluggable framework allows each assistant to be developed and evaluated independently, and use customized prompts and context. uReview currently has three assistants in operation, but is‌ actively expanding the list.
  * The Standard Assistant detects bugs, incorrect exception handling, or logic flaws.
  * The Best Practices Assistant enforces Uber-specific coding conventions by referencing a shared registry of style rules.
  * The AppSec Assistant targets application-level security vulnerabilities.

### **Post-Processing and Quality Filtering**
The main challenge with GenAI code reviews is that a simple standalone prompt results in many false-positive comments and many low-value true-positive comments that developers don’t address. A key piece for tackling this challenge is robust post-processing and quality filtering.
Once comments are generated, uReview runs them through a multi-layered filtering process:
  1. A secondary prompt evaluates each comment’s quality and assigns a confidence score. The prompt is customized for each assistant type, and confidence thresholds for pruning are set at a fine-grained level (per assistant, per language, and comment category) based on developer feedback and evaluations.
  2. Next, a semantic similarity filter merges overlapping suggestions.
  3. Finally, a category classifier tags each comment (for example, _correctness:null-check_ or _readability:naming_) and suppresses those from categories with historically low developer value. 

These filters work together to surface only high-quality, actionable feedback.
### **Comment Delivery and Feedback Collection**
The system posts validated comments directly on the code review platform, in line with the code. Developers can rate each comment as “Useful” or “Not Useful” and optionally add a note. All comments, along with their associated metadata—including assistant origin, category, confidence score, and developer feedback—are streamed to Apache Hive™ via Apache Kafka®. This data supports long-term tracking, experimentation, and operational dashboards. For example, files that contain negative comments provide clear benchmark cases that future versions of uReview should avoid reproducing. Moreover, by assigning a predicted category to each comment, comment‑category filters can automatically eliminate categories that have historically attracted negative feedback within Uber. 
### **Evaluation and Continuous Improvement**
uReview evaluates its performance through automated and manual methods.
It automatically evaluates if a given posted comment has been addressed by re-running uReview five times on the final commit. Because LLM is stochastic, a single rerun might skip a lingering issue or revive one that is already fixed, so we invoke it five times—the minimal count that virtually eliminates missed detections while keeping cost and latency low. A comment is considered addressed if none of the re-runs reproduce a semantically similar comment (with adjustments for cases when code referenced in the comment is deleted).
Manually, a curated benchmark of commits with known issues is used to evaluate comment [precision, recall](https://en.wikipedia.org/wiki/Precision_and_recall), and [F1](https://en.wikipedia.org/wiki/F-score) scores against human-labeled annotations.
The advantage of ‌automatic feedback is that it runs on thousands of commits in production daily. In contrast, the advantage of the manually curated benchmark set is that it allows us to evaluate and iterate on uReview locally before deploying a new feature. 
Feedback from both methods informs adjustments to confidence thresholds, prompts, and filtering logic. We aim to maintain a usefulness rate above 75% as the system expands to cover more languages and services.
* * *
## Impact and Evaluation
uReview is now deployed across all six of Uber’s monorepos (Go, Java, Android, iOS, Typescript, and Python), and reviews every commit as part of our CI process within a median of 4 minutes. We now briefly discuss its impact in terms of its usefulness rate, time savings, and our evaluation of third-party models and review tools.
### High Usefulness in Production
uReview maintains a sustained usefulness rate above 75% across all deployed generators. In terms of our automated evaluation that checks if each review comment is addressed, we see on average 65% of comments being addressed in the same changeset.
This performance significantly exceeds that of human reviewers. Internal audits show that only 51% of human-written comments are considered as bugs by the author and addressed in the same changeset. By focusing on precision and suppressing low-confidence or low-value suggestions, uReview has established itself as a trustworthy tool.
### Time Savings for Developers
Each week, uReview processes over 10,000 commits, excluding configuration files. Internal benchmarks indicate that having a second human reviewer look for the kinds of issues identified by uReview would require 10 minutes per commit. This translates to approximately 1,500 hours saved weekly, equivalent to nearly 39 developer years annually. Further, uReview’s feedback appears minutes after the commit is posted for review, thereby allowing the code author to address these bugs before the commit reaches a human reviewer.
### Empirical Model Evaluation
To identify the optimal configuration for LLM performance, we conducted benchmark tests on a curated suite of commits containing annotated ground-truth issues (that is, a golden comments dataset). The evaluation compares uReview’s identified issues against the ground-truth and computes standard metrics: precision, recall, and F-score.
The most effective configuration paired Anthropic® Claude-4-Sonnet as the primary comment generator with OpenAI® o4-mini-high as the review grader. This combination achieved the highest F1 score across all tested setups, outperforming OpenAI® GPT-4.1, O3, and O1, Meta® Llama-4, and DeepSeek® R1. Claude‑4‑Sonnet as the comment generator paired with OpenAI® GPT‑4.1 as the review grader was the runner-up with 4.5 points below the leading setup. We periodically evaluate newer models using this approach and use the model combination with the highest F1 score.
### Third-Party Tools
There are three main reasons why Uber invests in building an in-house AI code reviewer agent instead of using third-party tools. 
First, most third-party AI code-review tools require code to be hosted on GitHub®. Uber currently uses Phabricator™ instead of GitHub as its primary code review platform. This architectural constraint limits our ability to deploy many off-the-shelf AI code review solutions, which are often tightly coupled with GitHub. 
Secondly, our evaluation of third-party tools on Uber code showed that they suffered from three main issues: many false positives, low-value true positives, and being unable to interact with internal systems at Uber. uReview, in comparison, doesn’t face these issues because of its prioritization of precision, feedback loop, specialization to what works well at Uber, and ability to pull information from internal Uber systems.
A third minor point is that given the scale of diffs at Uber (65,000 per month), we see that the AI-related costs of running uReview are an order of magnitude less than what typical third-party tools charge.
* * *
## **Lessons Learned**
Building uReview at Uber offered deep insights into what it takes to create scalable, trustworthy AI tools for engineers. The most important lessons span model behavior, system design, developer experience, and organizational strategy.
### **Precision Is More Valuable than Volume**
Early in development, we learned that comment quality matters far more than quantity. Developers quickly lose confidence in a tool that generates low-quality or irrelevant suggestions. To preserve trust, we focused on delivering fewer but more useful comments. By automatically rating every comment’s confidence, pruning whole categories that historically add little value, and collapsing near‑duplicate remarks into a single concise note, we stripped away noise and surfaced only the insights that matter. This strategy led to stronger engagement and wider adoption.
### **Feedback Must Be Built-in**
Real-time developer feedback proved essential for tuning the system. We embedded simple rating links into every comment, and our automated evaluation marked which comments were addressed by the final commit. These allowed us to collect feedback at scale, directly from users. By linking feedback to metadata like language, comment category, and assistant variant, we uncovered granular patterns and made targeted improvements, including better prompting, better model selection, and pruning underperforming comment types. 
### **Guardrails Are Just as Important as Prompts**
Even with high-performing models like o4-mini-high and Claude 4 Sonnet, single-shot prompting wasn’t enough. Unfiltered outputs led to hallucinated issues, duplicate suggestions, and inconsistent quality. We introduced multi-stage chained prompts: one step to generate comments, another to grade them, and others to filter or consolidate. This pipeline approach improved reliability. Prompt design helped, but system architecture, and post-processing were even more critical.
### **Developers Don’t Like Readability and Stylistic Comments**
Developers don’t like certain categories of comments from AI tools. Readability nits, minor logging tweaks, low-impact performance optimizations, and stylistic issues consistently received poor ratings. In contrast, correctness bugs, missing error handling, and coding best-practice violations—especially when paired with examples or links to internal docs—scored well. By focusing on high-signal categories, we increased value while avoiding developer fatigue.
### **Better at Catching Bugs than Assessing System Design**
uReview today only has access to the code, and not to other artifacts like past PRs, feature flag configurations, database schemas, technical documentation, and so on, because of which it can’t correctly assess overall correctness and review the system design. It’s much better at catching bugs that are evident from analyzing the source code alone. However, we foresee that this may change in the future with MCP servers being built to access these other resources.
### **Trust Grows with Gradual Rollout**
We introduced uReview in phases, one team or assistant at a time, instrumenting each stage with precision‑recall dashboards, comment‑address‑rate logs, and user‑reported false-positive counts. This allowed quick, data‑driven iteration and limited the scope of regressions. When early users surfaced issues—such as noisy stylistic suggestions or missed security checks—we A/B‑tested candidate fixes, tuned thresholds, and shipped improvements within a day. Early users gave precise feedback that we correlated with the metrics to make objective go/hold decisions for each release. This gradual approach helped us build credibility, adjust based on real‑world use, and scale with confidence.
### **AI Reviews in the IDE Versus the Code Review Platform**
Even though some IDEs (or extensions) offer code reviews, we still want AI reviews on the code review platform (CI time) because we have less control over what the developer does locally. They may not use the AI code-review features or may ignore its warnings. This is analogous to the concept of running build and test at CI time in addition to making build and test available for developers locally.
### **Enforcing Best Practices Using GenAI Versus Linters**
Traditionally, linters (or static analysis tools) have been used to enforce certain best practices. For simple or syntactic patterns, linters are accurate, reliable, and cheap—we should continue using them. However, some properties are hard to check with linters. For example, the Uber Go [style guide](https://github.com/uber-go/guide/blob/master/style.md) recommends using the _time_ library for time-related operations. Here, one needs some semantic code understanding to know that a certain integer variable represents time, and LLMs perform far better in these cases. So, best practices that aren’t checkable by linters are often a great fit for LLMs.
* * *
# What’s Next
The product ceiling for AI code review is high and the scope of impact is very large. So looking ahead, we plan to expand support for richer context, cover more review categories like performance and test coverage, and develop reviewer-focused tools to help with code understanding and identifying potential risks. These efforts aim to push AI-assisted review further while keeping engineers firmly in control.
* * *
# Conclusion
uReview marks a meaningful shift in Uber’s approach to code quality. It treats automation not as a substitute for human insight, but as a scalable partner that enhances engineering productivity. By pairing LLMs with carefully designed prompt-chaining, multi-stage grading, duplicate suppression, and integrated user feedback, uReview delivers high-quality, actionable review comments at scale.
Its modular architecture and evaluation framework allow it to evolve rapidly, while the platform integrates seamlessly into developer workflows. Most importantly, it allows engineers to spend less time on repetitive checks and more time on higher-order tasks like system design and architectural decisions.
With a usefulness rate consistently above 75%, thousands of developer hours saved each year, and steady adoption across teams, uReview has proven itself as both a technical solution and a product experience. The project also underscores broader lessons in GenAI deployment: prioritize precision, build trust through transparency, and design systems that invite feedback.
## **Acknowledgments**
The progress described in this post wouldn’t have been possible without the contributions of engineers across the Development Platform and Michelangelo teams. We’re grateful to the early adopters of uReview, whose feedback and advocacy helped shape the system. Specifically, we’d like to thank Kaia Lang and Uday Kiran Medisetty for championing uReview across our product teams. We’d also like to thank former team members, Stefan Heule, Raajay Viswanathan, and Shrey Tiwari for their contributions to uReview.
_Anthropic ® is a registered trademark of Anthropic PBC. _
_Apache ®, Apache Hive™, Apache Kafka®, HDFS™, and the star logo are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries. No endorsement by The Apache Software Foundation is implied by the use of these marks._
_Cursor ™ is a trademark of Anysphere, Inc._
_GitHub and GitHub Copilot are registered trademarks or trademarks of GitHub, Inc. in the United States and/or other countries._
_Llama 4 ® and its logos are registered trademarks of Meta® in the United States and other countries. No endorsement by Meta is implied by the use of these marks._
_OpenAI ® and its logos are registered trademarks of OpenAI._
Stay up to date with the latest from Uber Engineering—follow us on [LinkedIn](https://p.uber.com/eng-linkedin) for our newest blog posts and insights.
* * *
![Sonal Mahajan](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2023/11/sonal_mahajan-1024x1024.jpg)
Sonal Mahajan
Sonal Mahajan is a Staff Engineer in the Programming Systems team at Uber. Her research interests cover software engineering and artificial intelligence, with a particular focus on using program analysis and AI/ML to develop automated tools for improving code quality, reliability, and developer productivity.
![Shauvik Roy Choudhary](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/03/shauvik-17418444984488.jpg)
Shauvik Roy Choudhary
Shauvik Roy Choudhary is the Engineering Manager of the Programming Systems team at Uber. He’s an experienced leader in the developer tools and AI/ML space, building innovative solutions to improve software quality and performance.
![Akshay Utture](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/akshayphoto-17460432006943-983x1024.jpg)
Akshay Utture
Akshay Utture is a former software engineer on the Programming System team at Uber. He has been focused on building AI Code Review tools at Uber, but is more broadly interested in AI developer tools and program analysis.
![Will Bond](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/willbond-17549530578029.jpeg)
Will Bond
Will Bond is a Staff Engineer on the AI Foundations team within the Development Platform organization at Uber.
![Joseph Wang](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/03/josephwangsmall-17531376456816.jpeg)
Joseph Wang
Joseph Wang serves as a Principal Software Engineer on the AI Platform team at Uber, based in San Francisco. His notable achievements encompass designing the Feature Store, expanding the real-time model inference service, developing a model quality platform, and improving the performance of key models, along with establishing an evaluation framework. Presently, Wang is focusing his expertise on advancing the domain of generative AI.
* * *
Posted by Sonal Mahajan, Shauvik Roy Choudhary, Akshay Utture, Will Bond, Joseph Wang 
Category:
[Engineering](/en-CA/blog/engineering/)
[Data / ML](/en-CA/blog/engineering/data/)
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
[English](/en-CA/blog/ureview/)
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
[English](/en-CA/blog/ureview/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
