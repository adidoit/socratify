---
title: "Reinforcement Learning for Modeling Marketplace Balance"
author: "Unknown"
url: "https://www.uber.com/blog/reinforcement-learning-for-modeling-marketplace-balance/"
published_date: "None"
downloaded_date: "2025-09-15T09:38:03.261771"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for Reinforcement Learning for Modeling Marketplace Balance](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/cover-17514078235579-1024x683.jpg)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Freinforcement-learning-for-modeling-marketplace-balance%2F&t=Reinforcement+Learning+for+Modeling+Marketplace+Balance)
  * [X social](https://twitter.com/share?text=Reinforcement+Learning+for+Modeling+Marketplace+Balance&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Freinforcement-learning-for-modeling-marketplace-balance%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Freinforcement-learning-for-modeling-marketplace-balance%2F)
  * [Envelope](mailto:?subject=Reinforcement+Learning+for+Modeling+Marketplace+Balance&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Freinforcement-learning-for-modeling-marketplace-balance%2F)
  * Link

# Introduction
This blog describes how we apply reinforcement learning techniques to make the Uber network more efficient, helping the world move and creating magical experiences for riders and drivers. We discuss how we apply reinforcement learning in our matching algorithm to improve driver and demand balance in our mobility marketplace.
* * *
## Motivation
In a real-time two-sided marketplace like Uber, the balance between drivers and demand for rides is constantly fluctuating depending on external factors like demand variations as well as internal contributors like how Uber moves drivers by matching them to riders. The core challenge for matching algorithms is how to match riders with drivers in the most efficient way, minimizing wait times for riders while maximizing earnings for drivers. Matching drivers to the right places at the right time can be a difficult task, especially when trying to optimize for immediate and long-term efficiency. 
We specifically view this problem from the lens of balance. A greedy matching algorithm without an understanding of subsequent likely outcomes might create balance at the time of the match, but may cause imbalances in other parts of the city in the future, leading to longer wait times or surge pricing elsewhere. This sequential decision making problem creates an opportunity to use reinforcement learning techniques in the ridesharing marketplace.
* * *
## Exploring Approaches to Reinforcement Learning in the Marketplace
We model the Uber matching system in an MDP (Markov Decision Process) framework where the agent takes collective decisions to match drivers to riders in a particular order. The environment is one where the market reacts to the sequence of collective decisions. The MDP system tracks collective rewards from the environment in the shape of utilization and throughput. 
Modeling our matching stack with MDP enables us to use reinforcement learning for longer term optimization with some important caveats. First, our decisions impact people in the real world and how they move. This makes this space challenging for online reinforcement learning as well as experimentation, since the stability of our algorithms is first-order.
Uber is also a global marketplace with intrinsically heterogenous market conditions in different cities. Finding the right balance between modeling heterogeneity and operational complexity turns out to be non-trivial.
Further, the presence of strong network effects and behavioral drifts makes simulation a tough challenge, and makes it difficult to apply state-of-the-art on-policy learning algorithms, which leverage [Gymnasium](https://gymnasium.farama.org/)-like simulation environments to rollout sufficiently accurate MDP episodes indefinitely. On the other hand, leveraging offline reinforcement learning comes with its own challenges of slow convergence.
The Uber marketplace is a nonstationary environment evolving based on market conditions, seasonality, underlying economics, and more. Given that, we should find the right balance between building complex models with data from longer periods of time versus simple models fitted on the most recent market data.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/fig1-17514123566288-1024x788.png)Figure 1: Uber’s matching engine interfacing with the environment.
Comparing the real constraints of deploying an advanced ML solution at scale to the existing literature, we very soon learned that our solution should be a blend of techniques grounded in the theoretical foundations of reinforcement learning with practical design choices to go beyond R&D.
* * *
## Policy Iteration and Policy Evaluation Loop
Considering the mentioned constraints, we decided to focus on the value iteration family of methods, and used the learned value function as a signal in our online matching algorithms instead of learning a policy directly. We formulated our problem as an infinite-horizon MDP tied to driver states. 
In this setting, we don’t learn direct policy representation, but use a feedback loop on policy evaluation and improvement through periodic re-training. In offline training, we learn the value function corresponding to our most recent version of production policy to learn which states are more valuable than others. Next, we use our online matching algorithms to nudge matches towards higher-value states and away from low-value states. 
This led to a new distribution of trips and balance in different locations and times, leading to a new version of the production policy. We learn a new value function through the re-training process.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/fig2-17514123988929-1024x529.png)Figure 2: Policy iteration and policy evaluation loop. 
* * *
## Learning Value Functions Through Temporal Difference
![Image](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeGfX57xx3x6rTuU7qFYjOTYa_XU-h9z0BMmPXvvzGRb5dFzPztUq5TMFMWzFA6AWNYil68mweL95eOuBGfkMp7fKqA5Tl6q8Me0Gj-a-me9u95dceAUeJaAykNFoaUXztqmqvWJA?key=xQuv_TYy519sFtAUeoDS3mEe)Figure 3: Trajectory of a driver through completing multiple trips. 
We use a DQN-like approach to learn a value function via the temporal difference principle. The temporal difference principle in our context works as follows:
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/image-7-1-25-at-5.41pm-17514169308384.jpeg)1
We update our estimation of value function V evaluated at the state S with a driver event from state S to the next state S’. Note that this state representation of both S and S’ is not tabular, and itself is represented through embedding a more enriched context in the deep neural network.
A driver state transition is accompanied with a collected reward of size r that’s realized after pickup (discounted by ETA). ETD is the time to destination, which is the temporal gap at which the value of the next state (S’) will incur. is the discount factor in the return which is a numerical trick for having a bounded value for an infinite horizon sequence.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/fig4-17514125892938.png)Figure 4: Example of target value function in Los Angeles
This recursive update converges to the exact V function under stationary conditions (Reference 1). In the DQN approach, we estimate this V function with a deep neural network in which the input would be a given driver context and the output is driver value estimation:
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/image-7-1-25-at-5.38pm-17514167647152.jpeg)2
Given these logics, the training algorithm is designed as follows:
  * Initialize the DNN model, batch size B and
  * For i = {1, 2, …, N} where N is the number of iterations: 
    1. Take random samples with size B from the table of driver state transitions {S1, r, ETA, ETD, S2}
    2. _V p1 = DNN(S1) _
    3. _V 1 = YETAr + YETD**.****** DNN(S2)_
    4. StateLoss = MSELoss _(V 1, Vp1)_
    5. Optimization with Gradient Step

In this setup, we procure a table of driver state transitions {S1, r,ETA, ETD, S2} from actual completed trips by Uber, as well as the driver unutilized intervals. We mapped these events respectively to transitions with positive and negative rewards. More on that in the following section.
* * *
## Reward Modeling for Unutilized States
One of the key innovations in solving for balance is identifying states which lead to un-utilized drivers idling in locations where there’s scarce demand and/or deemed undesirable for the drivers. This is a strong signal for imbalance, which we wanted value estimates to learn from.
From a data perspective, we call completed trips as positive signals as they train the model based on desired events of completion. However, if training is only focused on positive signals, the model is agnostic to idling or unfulfillment events in which lack of demand or improper positioning of drivers resulted in extended unutilized driver hours (negative signals). 
By learning trip transitions that lead to times and places where a lot of idling sessions occur, the temporal difference model naturally discounts the value estimates for trips that lead to dead-end locations. This lets us identify low-value destinations effectively in addition to learning from trajectories which increase the value estimates of states through positive reward accumulation.
To incorporate this signal into the learning process, we consider a zero reward for an idling event:
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/image-7-1-25-at-5.40pm-17514168807332.jpeg)3
* * *
## Geospatial Smoothing
The driver context is the input to our reinforcement learning model. At the high level, it comprises two important dimensions: time and the geolocation of the driver. To learn a spatially smooth value function, we use an additional contrastive loss term, which supervises the geo-embeddings that are learned from geohash strings. For example, unique identifiers of spatial coordinates (learn more in Reference 2). This loss encourages the pairwise distances between embeddings to reflect real-world geographic distances, ensuring the learned embeddings are spatially sensible. By training these geo-embeddings alongside the value function, we enable the model to generalize better across locations and capture geographic structure more effectively.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/image-7-1-25-at-4.14pm-17514116995221.jpeg)
* * *
## Evaluations and Analysis Using Ground Truths
Since we use a deep network to estimate the values, and our context space is non-tabular, creating ground-truth labels for trajectories is challenging, especially in high cardinality state space with sparse observations.
To address this problem, we designed a new evaluation approach to evaluate the efficacy of ‌value estimates in production and in training. The primary evaluation method bucketizes predictions from the model at a coarse spatiotemporal resolution, and compares driver state values against ground truths derived with the Monte Carlo approach, using regression metrics like correlation coefficients. In the Monte Carlo approach, we estimate the value of a state by simply averaging returns across agent rollouts (like driver trajectories) initiated from a given state (see Reference 3). 
We designed a custom pipeline for curating Monte Carlo ground truths, allowing for comparison with the model predictions, model evaluations, online monitoring and tracking performance improvements and regressions.
Additionally, model performance is tracked in real time along with weekly retraining of the model. We defined tunable thresholds for graceful adjustments to the signal contribution in proportional to the goodness of regression metrics. If model performance degrades, the matching system automatically incorporates this signal less frequently in decision making. This plays a critical role in scaling deployments globally without manual interventions. 
We also created anomaly detection tools and observability dashboards are in place to ensure smooth operation and timely updates.
Apart from monitoring metrics for the model performance, we used a variety of internal simulation tools to validate the usage of the model inside our production systems.
* * *
## Results 
We incorporate this value function directly into the ranking metric of Uber’s ride matching algorithm. After successful offline simulations, a series of global switchback experiment (AB experiments with time randomization as described in Reference 4) showed promising results: a 0.52% increase in driver earnings by positioning drivers where demand is expected, and a 2.2% reduction in rider cancellations thanks to faster driver assignments fueled by proactive driver placement.
Following the success of deployment in the rides matching algorithm, we applied the signal to boost the utilization and efficiency of AVs (Autonomous Vehicles) on Uber platform. We use this value function to guide AV matching and repositioning. This ensures AVs are proactively placed where feasible demand is expected, enhancing rider experience and maximizing fleet productivity on Uber platform.
* * *
## Next Steps 
A key challenge ahead is handling delayed feedback, as the true impact of matching decisions often unfolds hours later. To address this, we’re exploring real-time TD learning pipelines, a trajectory feedback mechanism, and robust loss functions to better attribute long-term rewards as well as modeling uncertainty in value estimates.
Additionally, we’re also exploring pathways toward direct policy learning, moving beyond the pure value-based methods described above. While our current system leverages value functions to influence decisions, learning explicit policies could allow for faster adaptation to dynamic conditions and enable more flexible optimization across objectives.
* * *
# Conclusion
In this blog, we explored how Uber uses reinforcement learning, specifically a DQN inspired approach, to learn value functions and optimize driver matching and balance driver and demand in real-time.
We’ve deployed this approach in over 400 cities globally. To our knowledge, this is the largest production deployment of a reinforcement learning algorithm for matching in the ridesharing marketplace. 
By focusing on long-term driver value, we’ve been able to make smarter, more sustainable matching decisions that improve the overall health of the marketplace. As we continue to scale this technology, we anticipate even greater improvements in efficiency and user satisfaction.
* * *
### Acknowledgments
This work was a collaboration between the Marketplace Matching ML, Engineering, Applied Science, and Product teams who worked tirelessly to ship this bleeding-edge tech to production. We’re grateful for the opportunity to work with such talented peers. If you’re interested in working at the intersection of reinforcement learning, operations research, and product, please [reach out to us](https://www.uber.com/us/en/careers/list/?query=Mobility%20Matching&location=USA-California-San%20Francisco&location=USA-New%20York-New%20York&location=USA-Washington-Seattle&location=CAN-Ontario-Toronto&department=Engineering). 
###   
References
  1. Sutton, Richard S. “Learning to predict by the methods of temporal differences.” _Machine learning_ 3 (1988): 9-44.
  2. <https://www.uber.com/blog/h3/>[H3]()
  3. Sutton, R. S., & Barto, A. G. (2018). _Reinforcement Learning: An Introduction (2nd ed.)_. MIT Press. (See Chapter 5: “Monte Carlo Methods” for detailed methodology and theory.
  4. Bojinov, Iavor, David Simchi-Levi, and Jinglong Zhao. “Design and analysis of switchback experiments.” Management Science 69, no. 7 (2023): 3759-3777.
  5. [Reinforcement Learning in the Wild](https://arxiv.org/abs/2202.05118)

Cover Photo Attribution: “POTD 2014-06-15 – Boston Skyline from Malone Park – HDR” by Bill Damon, CC BY 2.0. Colors modified.
Stay up to date with the latest from Uber Engineering—follow us on [LinkedIn](https://p.uber.com/eng-linkedin) for our newest blog posts and insights.
* * *
![Prateek Jain](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/prateekj-17514292131453.jpeg)
Prateek Jain
Prateek Jain is an ML systems architect with expertise in building ML infrastructure for internet scale applications. His current focus is on applying reinforcement learning techniques to operations research problems in the Matching and Driver Pricing organization at Uber.
![Soheil Sadeghi](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/soheil-17514294232938-1024x956.png)
Soheil Sadeghi
Soheil Sadeghi is an ML Tech Lead at Uber. His area of expertise is mobility matching algorithms with a focus on reinforcement learning and multi-objective optimization.
![Mehrdad Bakhtiari](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/mehrdad-17514296144037-1024x1024.jpeg)
Mehrdad Bakhtiari
Mehrdad Bakhtiari is an ML Engineering Manager at Uber, leading the Matching ML team. He focuses on advancing ML modeling techniques and systems to optimize mobility matching, improve earner earnings, and enhance rider experiences. His team drives ML ownership, monitoring, and best practices across the marketplace, and supports newer ML teams.
* * *
Posted by Prateek Jain, Soheil Sadeghi, Mehrdad Bakhtiari 
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
[English](/en-CA/blog/reinforcement-learning-for-modeling-marketplace-balance/)
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
[English](/en-CA/blog/reinforcement-learning-for-modeling-marketplace-balance/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
