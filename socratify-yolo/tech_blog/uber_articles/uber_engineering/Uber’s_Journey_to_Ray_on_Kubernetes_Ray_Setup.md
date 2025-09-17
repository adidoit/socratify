---
title: "Uber’s Journey to Ray on Kubernetes: Ray Setup"
author: "Unknown"
url: "https://www.uber.com/blog/ubers-journey-to-ray-on-kubernetes-ray-setup/"
published_date: "None"
downloaded_date: "2025-09-15T09:38:29.331835"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for Uber’s Journey to Ray on Kubernetes: Ray Setup](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/ai-technology-brain-background-digital-transformation-concept-17436212664293-1024x683.jpg)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fubers-journey-to-ray-on-kubernetes-ray-setup%2F&t=Uber%E2%80%99s+Journey+to+Ray+on+Kubernetes%3A+Ray+Setup)
  * [X social](https://twitter.com/share?text=Uber%E2%80%99s+Journey+to+Ray+on+Kubernetes%3A+Ray+Setup&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fubers-journey-to-ray-on-kubernetes-ray-setup%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fubers-journey-to-ray-on-kubernetes-ray-setup%2F)
  * [Envelope](mailto:?subject=Uber%E2%80%99s+Journey+to+Ray+on+Kubernetes%3A+Ray+Setup&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fubers-journey-to-ray-on-kubernetes-ray-setup%2F)
  * Link

# Introduction
Uber’s taken steps to enhance and modernize its machine learning platform. As part of this enhancement, in early 2024, Uber migrated its machine learning workloads to Kubernetes®. This blog is the first in a two-part series that describes our experiences building this new capability, how we leveraged existing open-source components, unique problems we faced in adopting them, and new tech that we built in-house for resource management.
* * *
## Motivation 
Machine learning workloads are typically modeled as a sequence of steps. Most of these steps, especially in model training pipelines, tend to be heavy in data processing. This is because the amount of data fed into machine learning pipelines generally correlates well with the quality of the output model ([Hestness et al. 2017](https://ar5iv.labs.arxiv.org/html/1712.00409); [Banko and Brill 2001](https://www.microsoft.com/en-us/research/publication/scaling-to-very-very-large-corpora-for-natural-language-disambiguation/); [Goodfelltscoow et al. 2016](https://www.deeplearningbook.org/)). For this reason, these jobs usually run in [batch](https://en.wikipedia.org/wiki/Batch_processing) processing mode. Each step is modeled as a large distributed job that forms a graph of jobs that execute the pipeline.
Until mid–2023, Uber ran its machine learning workloads primarily using a job gateway service called MADLJ (Michelangelo Deep Learning Jobs service). It ran Apache Spark™–based ETL jobs and Ray®-based machine learning training jobs. While this served us well, it had some pain points:  

  * **Difficult and manual resource management**. ML engineers had to be aware of the heterogeneity of the compute resource where their jobs ran. They had to figure out the region, zone, and cluster in our compute fleet best suited for a given job. This included factors like GPU availability and the requirement for a specific GPU SKU. They also had to find a cluster that had enough available resources. In our minds, ML engineers handling resource management themselves constituted a leaky abstraction.
  * **Inefficient resource utilization**. Users needed to specify the resource and cluster specifications as part of their job configurations. Once determined, these would get committed to the code base. However, such static configurations caused a high load on some of the compute clusters, while other clusters went underutilized.
  * **Inflexible capacity planning**. As ML engineers experimented with new techniques and models, the capacity required varied. It was bursty at times when running large experiments. This led to capacity planning either overforecasting or under-funding. Uber is cost-aware and therefore has limited headroom for resources. This led to a chicken-and-egg problem where turnaround times for experimentation became long.
  * **Tight coupling with underlying infrastructure**. There was a tight coupling between our service and the underlying infrastructure, especially between compute and data services. This made any migration hard since we had to alter hard-coded configurations.

While trying to tackle the above problems, we also wanted to look at the underlying compute tech stack. MADLJ gateway relied on [Peloton](https://www.uber.com/blog/resource-scheduler-cluster-management-peloton/) as a resource manager. Although this setup was effective, its foundation on Apache Mesos® was outdated. This forced us to develop custom integrations to support newer technologies. Meanwhile, Kubernetes has emerged as the de-facto container orchestration platform in the industry boasting strong community support and open-source backing. Numerous data processing and machine learning frameworks like [Spark](https://github.com/kubeflow/spark-operator) and [Ray](https://github.com/ray-project/kuberay)—both critical to our machine learning workflows—now offer native Kubernetes support. This made transitioning to Kubernetes as the orchestration platform for our machine learning pipelines a clear and strategic decision.
However, to ensure a smooth transition and reuse battle-tested practices where external solutions still have gaps, we kept around some of the custom abstractions that we built on top of Peloton and adapted them to work on Kubernetes. Some examples of these include the concepts of resource pools and elastic resource sharing. We’ll describe these in detail in the second part of this blog series.
* * *
## Objective
Our goal was to simplify the user experience by abstracting away the complexity of the underlying infrastructure. We aimed to offer a declarative interface where users could specify the type of jobs (such as Spark or Ray) and the required hardware resources, without needing to worry about the low-level details of where the jobs would run. The platform would provide a unified, federated view of resources across Uber’s fleet. The system would automatically determine the optimal cluster and resources based on the job’s requirements, and when multiple options met those requirements, it’d prioritize them based on factors like current load.
On the infrastructure side, we saw this as an opportunity to transition from Mesos to Kubernetes. We worked closely with Uber’s Compute Infrastructure team to build Kubernetes support for our technology stack, with the long-term goal of migrating production workloads to this new platform. The remainder of this blog describes the architecture of what we built.
* * *
## Federated Resource Management
The architecture we designed for machine learning pipeline orchestration incorporates federated resource management. Federated resource management helps provide an abstracted view of resources to ‌end users. It also allows us to effectively manage and optimize our usage of resources behind this abstraction.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/ma-2.0-job-layers-17436211301307-1024x722.png)Figure 1: Federated Resource Management. 
For federated resource management, we built the layered architecture shown in Figure 1. The layers include: 
  * **User application layer**. This layer comprises user applications that represent ‌machine learning pipelines. It interacts with the provided APIs to wrap this logic into a declarative job request.
  * **Global control plane**. This layer is our platform that runs on Kubernetes. It’s represented as a [standard Kubernetes architecture](https://kubernetes.io/docs/concepts/overview/components/).
  * **Local control plane**. This layer comprises the Kubernetes clusters where the jobs run.

* * *
## Global Control Plane
The global control plane consists of an API server and a controller manager. The API server consists of [custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) that represent machine learning artifacts. The controller manager consists of optional [controllers](https://kubernetes.io/docs/concepts/architecture/controller/#controller-pattern) that can watch these custom resources and take action on them. Focusing on the jobs aspect, we built a CRD (Custom Resource Definition) that represents a job. We also added a job controller to watch the job requests and find an appropriate cluster and resource pool to run that job on. It’ll mount any secrets that the job requires to access data sources and launch the job on the chosen compute cluster. It’ll then monitor the job to termination and manage the job lifecycle. This includes making sure that ‌resources get released after the job terminates.
###   
Cluster Management
The underlying compute clusters where jobs execute are also represented in a Kubernetes-idiomatic manner as custom resources in the API server. This resource definition encodes properties like the region and the zone a cluster is in and the types of hardware it supports. A cluster controller monitors these clusters and periodically performs health checks on them. This helps with cluster management in case of any cluster maintenance or downtimes.
The cluster controller also populates a cached view of the resource pools across clusters and periodically updates it. The job scheduler uses this view to schedule jobs.
###   
Job Execution and Monitoring
The job controller watches the job CRD in the global API server. It executes a state machine by transitioning the job from one state to the next. The job controller works on each of these transitions in a reconcile step. In other words, the job controller reads a job CRD object from the head of the job event queue. It figures out its current state and [reconciles](https://kubernetes.io/docs/concepts/architecture/controller/#desired-vs-current) it by performing an action. If this action is successful, it updates the job CRD object status to note that it was successful.
When the user creates a new job request, the job controller reconciles the request by adding it to the job queue. This queue represents all the jobs waiting to get assigned to a local cluster with the necessary resources available. The job scheduler dequeues the head of this job queue and works on assigning a suitable local cluster to the dequeued job object. This assignment is modeled as a sequence of filtering and scoring plugins.
The filtering plugins filter out ‌resource pools that don’t support the affinities specified on the job. These affinities represent ‌job characteristics like the requirement for a GPU per worker or running on a specific environment for data locality. The scoring plugins then score the filtered candidate set to find the most suitable resource pool match for the job among them. Typically the scoring is done on factors like existing workloads or higher availability of a dominant resource like available memory. The existing workload on candidate resource pools is determined dynamically by fetching the current load in all the resource pools and scoring them to find the best pool for a given job. This operation is optimized by maintaining an in-memory representation of resource pools updated asynchronously by the cluster controller and consumed by the job scheduler. The job queue and the job scheduler are agnostic to the type of the job. As ‌job assignment is dependent purely on its affinities and resource requirements, we can abstract all jobs behind a common interface that exposes these properties for the scheduler to work on.
After a job is assigned to a local cluster, the job controller provisions the appropriate dependent resources on the assigned local cluster and creates the job on that cluster. An example of dependent resources are secrets required to access data resources that the job needs to access (like Apache Hive™ access tokens). The job controller also ensures that such secrets are refreshed when they’re close to expiration.
Once a job launches, the job controller monitors the job to completion. It does so by adding a special label to all the launched jobs and setting a watch on the API servers of the local Kubernetes clusters using that label as a selector. This way, it subscribes to ‌changes made to ‌local job CRDs. When the local operator updates the local job CRD object as part of the job execution, that update is caught by the job controller. It then augments that information with more contextual information and updates the job. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/joblifecycle-17436321287311-1024x712.png)Figure 2: Flow of the job lifecycle.
### Job Routing
Like other companies, Uber Engineering is broken into organizations. These organizations typically have ‌separate operating budgets that determine the amount of resources that can be accessed for their engineering consumption. Our job scheduler needed to be aware of these organizational hierarchies and smartly route jobs that belonged to a particular team or organization to the resource pools that they own.
For representing this organizational hierarchy, Uber uses an asset management service called uOwn. This system organizes all Uber assets into a tree structure where the nodes of the tree represent an owning team or an asset that’s owned by a team. This ownership model is used for both access control and cost showback.
Our job scheduler uses the uOwn service to match workloads to the resource pools owned by the teams that run those workloads. To achieve this, we do two things. First, we make sure that jobs are organized into projects and that every job belongs to a project. We also make sure that every project has an owner team with a unique uOwn identifier. Second, whenever a new resource pool is created on any of the clusters, it’s required to have an owner team identifier to indicate the team that requested those resources.
Not every project requires a provisioned resource pool. For example, new efforts in the early phases of experimentation may not have any resource pools for them. To address this use case, we provisioned several centrally-owned shared resource pools that are spread across clusters.
Given this context, we now describe how our job scheduler uses this organizational information to schedule jobs. This is done as part of the candidate resource pool selection process described in the section above. We use this order of preference to select the candidate set of resource pools for a given job:
  1. Find resource pools owned by the project that the job belongs to. The same uOwn identifier owns both the project and the resource pool.
  2. Find resource pools owned by a parent uOwn identifier of the project. For example, resource pools owned by the Applied AI organization uOwn identifier can be used by multiple projects from that organization. In this case, each project must have an owner uOwn identifier that’s a child of the Applied AI uOwn identifier in the uOwn hierarchy tree.
  3. If both first and second preference fail to find any resource pools, then the job is scheduled on one of the shared pools. If more than one shared pool matches the job requirements, then they are scored by the scoring plugins described above and the highest scored pool is chosen.

From an implementation perspective, ‌resource pools are represented as an in-memory cache maintained by the cluster controller. This helps remove ‌resource pools fetching operations from the hot path of job scheduling and execution.
In this manner, we can use ‌organizational resources dedicated to certain lines of business while still providing the benefits of an abstracted view of the resources.
###   
Error Handling
It’s important that various aspects of provisioning a Ray cluster are handled appropriately to provide a well-abstracted and reliable experience for the end user. To this end, we perform several readiness checks to ensure that a Ray cluster is ready to perform further processing. An example of this is to query the worker status of a Ray cluster by connecting to the head node. This ensures that the requested number of workers have been provisioned successfully and connected to the head node of the cluster.
In cases when the cluster fails to be ready, we attempt to provide a simple and actionable reason to the end user. For example, we provide error messages when a job has invalid affinities that can’t be met or if the assigned resource pool didn’t have enough resources to be able to provision the entire cluster.
We also monitor the Kubernetes pods running the Ray workers for abnormal exits. This is done by assigning a special label to the pods running Ray head and workers and then watching the pods with that label. Using this watch, when we encounter a pod whose container exited with a non-zero code, we record the reason for pod termination and expose it to the user. This is useful for catching errors like out of memory that can typically be solved by the end user and helps them iterate faster. To record such pod errors, we add a field in the job status that holds an array of pod errors.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/poderrors-17436323138284-1024x335.png)Figure 3: Definition of the pod error field.
### Job Termination and Lifecycle Management
We model a Ray cluster as a fleeting resource that’s provisioned specifically for a given job. These Ray clusters use Kubernetes as the underlying cluster manager to obtain resources. The job controller provisions these resources for the job to run. This necessitates that we also track the job and release the resources after the job finishes. This is especially important because Ray clusters often occupy expensive and high-in-demand GPU resources.
There are several cases where a job can be terminated and therefore the underlying Ray cluster must be vacated and the resources released. The most common case is that the client that’s using the Ray cluster for processing finishes in a success or a failed state. In such cases, it’ll attempt to terminate the cluster. Another case is that the user that owns the resources decides to kill the job in an ad-hoc fashion. We provide a command line utility to enable this use case. This utility captures the user name along with a brief reason for termination. A third case is when the client behaves erroneously or crashes before terminating the cluster. To address this case, we run an idle detection mechanism that detects if there is no processing happening on the cluster for an extended period of time. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/jobtermination-17436324687529-1024x789.png)Figure 4: Job controller termination operations. 
To process termination, the job controller executes the state machine that runs via the reconcile mechanism described earlier. The intent to terminate is captured in the job spec. When the job controller detects the _TerminationSpec_ on the job CRD, it transitions the job into a “Killing” state to indicate the start of the resource cleanup. The cleanup is achieved by deleting the local job CRD that in turn deletes all the associated pods that have owner references to the CRD object. This sequence of operations is depicted in Figure 4.
###   
Ray Cluster Discovery
Within Uber’s infrastructure, we run several hundreds of Ray clusters at a time. The clients connecting to these Ray clusters are production batch jobs running on Uber infrastructure. Therefore, we need a reliable mechanism to discover the right Ray clusters that a given client service wishes to connect to. To support this requirement, we extended the Ray CRD by introducing a status field that exposes the Ray head node IP and the client port. This way the client services can query the Ray cluster from the global API server and determine the address that it needs to connect to.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/rayclusterdiscovery-17436325775974-1024x630.png)Figure 5: Discovery mechanism for clients. 
We use this head status to expose information on other endpoints that are useful for ‌clients to connect to. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/headnode-17436326413665-1024x428.png)Figure 6: Definition of the head node information field. 
* * *
## Local Control Plane
The Uber Compute team manages ‌local control plane clusters. We’ve established well-defined contracts on how to submit our jobs, how to monitor them, how to retrieve logs and metrics for past jobs, and how to share resources with non-machine learning jobs. As a part of this process, we installed the open-source Ray operator for every compute cluster that the job runs on.
###   
Ray Head Discovery
A commonly used feature in open-source Kubernetes is the concept of [services](https://kubernetes.io/docs/concepts/services-networking/service/). In several applications, this is used for service discovery between components. These services are typically backed by dynamic [cluster IP](https://kubernetes.io/docs/concepts/services-networking/cluster-ip-allocation/) allocation. However, Uber Compute infrastructure relies on host networking and dynamic port assignment. This limits our usage of applications that internally rely on services. The Ray operator is one such example where the Ray workers discover the head using a service. To work around this, we invented a discovery mechanism by adding an init container to the worker pods. This init container queries the API server for the head node by name and then writes the address of the head node into a shared mount. The Ray worker container entrypoint reads the head node information from this shared mount and passes it as an argument to the Ray worker process. This way the workers can connect to the head of the Ray cluster and form a fully functioning Ray cluster.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/ray-head-discovery-17436328527853-1024x743.png)Figure 7: Head discovery by workers. 
### Idle Detection
We strive to maintain high utilization in our Ray clusters. This is especially important in the case of clusters that occupy GPU resources. This is because GPUs are expensive and limited in supply. Therefore, it’s essential that we use them efficiently and derive high utilization from them. For this purpose, we employed an idle detection technique to find clusters that don’t have any utilization for a period of time and terminate them. This releases ‌resources for other jobs. Such a mechanism also helps with cases where the client doesn’t terminate the cluster after usage, either due to bugs or the lack of a termination process in the client code. 
To perform ‌idle detection monitoring, we added a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/) container to the head pod of the Ray cluster. This sidecar container runs a process for detecting if this cluster is idling. It does so by querying our metrics database to retrieve the utilization metrics for the Ray cluster. If it finds no utilization, then it sends a termination request to the Global API server to terminate the Ray cluster. Another criteria we use to determine idling is when no client is connected to the Ray cluster for an extended period of time. This can happen if the client crashes after spinning up the Ray cluster.
* * *
# Conclusion
To move all the machine learning projects running on GPUs to this new stack, we planned a year-long program in 2023 with workstreams to migrate projects based on their tier, resource requirements, technical dependencies, and data dependencies. At the beginning of 2024, we migrated all ML projects to the new ML Ray on Kubernetes and deprecated the legacy technical stacks on Peloton.  
  
With the improved architecture, we observed a 1.5- to 4-times improvement in ‌training speed. With the flexibility of our job placement and container management system, we can better utilize GPU resources across zones and clusters, resulting in additional GPU capacity for training.
In the next part of this blog series, we’ll zoom into the resource management aspect of running these Ray-based jobs.
Cover Photo Attribution: “[AI technology brain background digital transformation concept](https://www.freepik.com/free-photo/ai-technology-brain-background-digital-transformation-concept_17122619.htm#fromView=keyword&page=1&position=1&uuid=371522a4-5756-4e83-ab3e-b213b8d8dc28)” by [rawpixel.com](https://www.freepik.com/free-photo/ai-technology-brain-background-digital-transformation-concept_17122619.htm#fromView=keyword&page=1&position=1&uuid=371522a4-5756-4e83-ab3e-b213b8d8dc28) on freepik.
Apache®, Apache Spark™, Apache Hive™, Apache Mesos, Apache Helix, and the star logo are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries. No endorsement by The Apache Software Foundation is implied by the use of these marks.
The Grafana Labs® Marks are trademarks of Grafana Labs, and are used with Grafana Labs’ permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.
Kubernetes® and its logo are registered trademarks of The Linux Foundation® in the United States and other countries. No endorsement by The Linux Foundation is implied by the use of these marks.  
  
NVIDIA®, the NVIDIA logo, CUDA, DGX, HGX, HGX H100, NVLink, NVSwitch, OpenACC, TensorRT, and Volta are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries.
* * *
![Bharat Joshi](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/bharatpicture-17436333096538-1024x932.jpg)
Bharat Joshi
Bharat Joshi is a Staff Engineer on the ML platform at Uber. He’s based out of Seattle, WA. His current interests are in building scalable ML platforms. He has prior experience in large-scale distributed storage systems and holds a patent in the area of data restoration.
![Anant Vyas](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/03/anantpic-17436334916283.png)
Anant Vyas
Anant Vyas is a Senior Staff Engineer and the Tech Lead of AI Infrastructure at Uber. His focus is on maximizing the performance and reliability of their extensive computing resources for training and serving.
![Ben Wang](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/benpicture-17436336623053-942x1024.jpg)
Ben Wang
Ben Wang is a Staff Technical Program Manager at Uber. He’s based out of Seattle, WA. He has prior experience in ML infra and is now working on Uber’s ML infrastructure.
![Min Cai](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2022/08/image1-1-8-e1743634764523.jpg)
Min Cai
Min Cai is a Distinguished Engineer at Uber working on the AI/ML platform (Michelangelo). He also led many infra projects such as cluster management (Mesos and Peloton), microservice platform (uDeploy), all-active datacenters, etc. He received his Ph.D. degree in Computer Science from Univ. of Southern California. He has published over 20 journal and conference papers, and holds 6 US patents.
![Axansh Sheth](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/axansh-17436348453296-613x1024.jpeg)
Axansh Sheth
Axansh Sheth is an Engineering Manager at Uber, based in Bangalore, India. With prior experience as an IC in ML Infra, he manages the Batch Compute Platform team and is focused on modernizing the batch compute stack.
![Abhinav Dixit](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/ad-pic-17436342351958.png)
Abhinav Dixit
Abhinav Dixit is a Software Engineer II at Uber, based in Bangalore, India. As a key member of the Compute Batch team, he specializes in resource management and the deployment of batch jobs within the organization. With a strong background in Kubernetes and the Peloton stack, he is dedicated to optimizing performance and enhancing efficiency in Uber’s computational infrastructure.
* * *
Posted by Bharat Joshi, Anant Vyas, Ben Wang, Min Cai, Axansh Sheth, Abhinav Dixit 
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
[English](/en-CA/blog/ubers-journey-to-ray-on-kubernetes-ray-setup/)
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
[English](/en-CA/blog/ubers-journey-to-ray-on-kubernetes-ray-setup/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
