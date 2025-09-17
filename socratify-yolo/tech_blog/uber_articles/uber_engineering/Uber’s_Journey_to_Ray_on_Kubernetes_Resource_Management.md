---
title: "Uber’s Journey to Ray on Kubernetes: Resource Management"
author: "Unknown"
url: "https://www.uber.com/blog/ubers-journey-to-ray-on-kubernetes-resource-management/"
published_date: "None"
downloaded_date: "2025-09-15T09:38:23.743998"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for Uber’s Journey to Ray on Kubernetes: Resource Management](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/part2-17442386436676-1024x683.jpg)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fubers-journey-to-ray-on-kubernetes-resource-management%2F&t=Uber%E2%80%99s+Journey+to+Ray+on+Kubernetes%3A+Resource+Management)
  * [X social](https://twitter.com/share?text=Uber%E2%80%99s+Journey+to+Ray+on+Kubernetes%3A+Resource+Management&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fubers-journey-to-ray-on-kubernetes-resource-management%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fubers-journey-to-ray-on-kubernetes-resource-management%2F)
  * [Envelope](mailto:?subject=Uber%E2%80%99s+Journey+to+Ray+on+Kubernetes%3A+Resource+Management&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fubers-journey-to-ray-on-kubernetes-resource-management%2F)
  * Link

# Introduction
This is the second blog in a two-part series that describes Uber’s journey to Ray® on Kubernetes®. In the [first part](https://www.uber.com/blog/ubers-journey-to-ray-on-kubernetes-ray-setup/), we introduced our motivation to the problem and the approach we took to set up a Ray-based job management system. In this blog, we zoom into how we run this job management platform on top of Kubernetes. In particular, we talk about the enhancements we made to Kubernetes to be able to run these Ray-based jobs.
* * *
## Motivation 
In the world of containerized applications, Kubernetes has emerged as the de-facto standard for orchestration. However, as we push the boundaries of large-scale, multi-tenant environments, we discovered that Kubernetes’ native resource management capabilities, while robust, leave room for optimization.
In addition, the upstream components described in the first blog post make use of some of the custom abstractions that we built on top of Peloton. We adapted them to work on Kubernetes.
* * *
## Elastic Resource Management in Kubernetes
A resource pool is a logical abstraction for a subset of resources in a cluster. All resources in a cluster can be divided into hierarchical resource pools based on organizations and teams. A resource pool can contain hierarchical child resource pools to further divide the resources within an organization. Resource sharing among pools is elastic in nature—resource pools with high demand can borrow resources from other pools if they aren’t using those resources.
Every resource pool has different resource dimensions, such as those for CPUs, memory, disk size, and GPUs. We expect the number of resource dimensions to increase in the future as cluster management systems begin to support more types of resource isolation, such as Disk IO.
###   
Resource Entitlement
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/respool-17442325395008.png)Figure 1: Hierarchical entitlement calculation.
[Max-min fairness](https://en.wikipedia.org/wiki/Max-min_fairness) ensures that each resource pool (logical subsets of cluster resources allocated to teams) gets its fair share of resources. However, if a resource pool’s demand exceeds its reserved capacity, and other pools have unused resources, elastic sharing allows it to borrow resources. When these unused resources are required by the original owners, they can be preempted.
Advantages of elastic resource management include: 
  * **Higher resource utilization**. Elastic sharing maximizes resource usage, as no resources remain idle if other teams demand them. This helps clusters maintain high utilization rates, approaching 100% in peak demand periods.
  * **Cost savings on infrastructure.** By sharing resources dynamically, teams need to purchase significantly fewer resources. 
  * **Flexible workload management.** Teams can prioritize their critical production workloads while borrowing resources for less critical, experimental pipelines when production demands are low. This flexibility ensures optimal use of guaranteed and opportunistic capacity.

![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/compute-resource-pools-utilisation-17442327405886-1024x242.png)Figure 2:**** Cluster allocation (orange) and demand (pink) plotted with the total cluster capacity (green).
### Design to Extend Kubernetes
Since Kubernetes doesn’t natively offer this type of dynamic preemption and resource sharing, we came up with our own solution to support elastic resource sharing in Kubernetes.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/abhinav-resmgr-component-diagram-17442371684572-1024x885.png)Figure 3: Elastic resource sharing in Kubernetes.
[](https://lucid.app/lucidchart/f32e07f5-260f-4504-9d77-3defa3c7571c/edit?page=0&v=759&s=612)  
This architecture aims to extend Kubernetes with features of elastic resource sharing and preemption.
For resource pool management, the resource pools are defined as Kubernetes custom resources (CRDs), marking the resource pool configuration. Pods are assigned to resource pools by applying an annotation containing the pool name. This allows efficient grouping and management of resources within the cluster.
For resource accounting, the resource manager monitors all pod events to track demand and usage per resource pool. Demand is calculated as the sum of resource requests for pods waiting for admission. Usage is calculated from pods already admitted to the resource pool. Periodically, the resource manager sums the allocatable capacity of all cluster nodes (excluding nodes marked with maintenance taints) to determine the total cluster capacity. Entitlement is calculated periodically, based on current demand, usage, and total cluster capacity available.
We also introduced a custom scheduler called _kube-resource-manager-scheduler_ for admission control. When a pod is created, its scheduler name is set to this scheduler. It places the pod in a priority queue. Once the pod passes admission control, the scheduler name is changed to default scheduler. The default scheduler then schedules the pod on a node. Pods that pass admission control but aren’t placed by the scheduler are killed after 25 minutes to free up resources. Pods with the scheduler name _kube-resource-manager-scheduler_ are still pending admission, while all others are admitted.
If a resource pool exceeds its entitlement due to increased demand in other pools, pods are preempted to bring the pool’s usage in line with its new entitlement. The preemption algorithm is implemented in Kubernetes by using the eviction API. Preemptible pods are marked with the annotation _preemptible: true_. Non-preemptible pods can’t exceed their reservation. A pod condition is set before eviction to log the reason for preemption.
Pods are also labeled with gang metadata. A gang is a group of instances that’ll be scheduled together at once for a workload. During scheduling, the resource manager ensures that the entire gang’s demand can be satisfied by the assigned entitlement before admitting any of the Pods within the gang. In Kubernetes, gang scheduling relies on pod metadata. Pods part of the same gang are labeled with _gang-member: <gang-name>_. An annotation _number-gang-members_ is added to indicate the total number of pods in the gang. The resource manager waits until all pods in the gang are created before proceeding with admission control. Pods without these metadata aren’t considered part of a gang.
Pods are placed in a priority queue based on the priority field in their pod spec. This field directly determines their order in the queue for admission control.
* * *
## Heterogeneous Clusters
We run a few training jobs on mixed hardware clusters. The Ray cluster is set up to have both GPU-enabled nodes and non-GPU nodes. Such clusters are optimized for resource utilization. This is achieved by offloading ‌work that doesn’t require GPUs to CPU-only nodes. An example of such CPU-only work is data loading and shuffling in a machine learning training job. In a heterogeneous cluster, the loaded data is then fed to the GPU nodes to achieve high GPU utilization. Ray supports this out of the box by allowing the Ray nodes to be labeled as a data processing node or a GPU-enabled training node. It runs the [Ray data](https://docs.ray.io/en/latest/data/data.html) loader on the data processing nodes to load and shuffle the data required for the training. This data is then fed to the nodes that are labeled as GPU-enabled training nodes.
To support running such heterogeneous training jobs, the underlying Kubernetes cluster is equipped with both CPU and GPU hosts in the same cluster. We developed a GPU filter plugin to filter out non-GPU pods and allow only the GPU pods to run on the GPU hosts.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/gpufilterpluginworkflow-17442374081854-900x1024.jpg)Figure 4: Filter plugin for GPU pods. 
The Kube scheduler distributes the non-GPU pods on the CPU nodes using the load-aware strategy to choose the least occupied CPU nodes. In the case of GPU workloads, we use a bin-packing scheduling strategy to efficiently use the GPU nodes and minimize fragmentation of the GPU hosts.
* * *
## Scheduling Workloads on Specific GPUs
At Uber, we have a variety of Ray workloads. Some of these workloads require more powerful, newer-generation GPUs like the NVIDIA® H100. However, this new-generation hardware is expensive, so we only run a few specific workloads on it. 
To effectively manage scheduling for special hardware requests in Kubernetes, we proposed an enhanced architecture that incorporates an SKU-based filtering mechanism. This approach ensures that workloads requesting specific GPU models are scheduled on the corresponding nodes, while general requests avoid these special resources.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/specialskufilter-17442375365202-790x1024.png)Figure 5: SpecialResourceExclusionFilter plugin lifecycle.
[](https://lucid.app/lucidchart/0a7f2f04-1a15-4776-83d1-a59eb288f82a/edit?page=0&v=3371&s=560)
Each GPU node in the cluster gets labeled with its model name. When submitting workloads, the pod specification includes a _nodeSelector_ that matches the required GPU model from the list of supported special hardware (SKUs). For example, a pod requiring an NVIDIA H100 GPU will have a node selector _gpu-node-label-model: NVIDIA_H100_80GB_HBM3_ in its spec.
A list of supported special hardware is maintained at the cluster level, containing real model names, aliases, and configurations. This list is stored in etcd using a [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/), and the Kubernetes scheduler and workload requestors have access to it.
For special hardware requests, the default Kubernetes scheduler ensures that pods are placed on nodes matching the _nodeSelector_ specified in the pod spec. For general GPU requests, a new scheduling plugin, _SKUExclusionFilter_ , filters out nodes that have special hardware, ensuring that these nodes are reserved exclusively for workloads requiring specific GPU models.
In a typical pod spec, general workloads can request GPUs without specifying a model. However, special workloads need to include the appropriate _nodeSelector_ to ensure they’re scheduled on nodes with the requested GPU mod.
* * *
## Metrics
In Kubernetes, pods are launched through [Containerd](https://containerd.io/), a container runtime that manages the lifecycle of containers. Containerd emits various metrics related to the performance and resource usage of containers, which are crucial for monitoring and optimizing workloads.
For CPU metrics, Containerd tracks CPU usage per container, providing data like the total CPU time consumed and CPU throttling.
Memory usage metrics include total memory used, memory limits, and memory failures (like out-of-memory events). These metrics help monitor container memory consumption, ensuring workloads don’t exceed their memory allocations and trigger crashes or performance degradation.
For GPU-accelerated workloads, Ccontainerd can expose GPU usage metrics if supported by the underlying hardware and drivers. This includes GPU memory utilization, GPU processing time, and other relevant statistics, helping to optimize and track GPU-bound tasks.
The pod container metrics are aggregated over a workload level and reported on Grafana® dashboards. To gather ‌pod metrics, we use a daemon agent to collect resource utilization metrics of containers running on a machine. The daemon agent uses [cAdvisor](https://github.com/google/cadvisor) as a library to gather metrics and enhance them with Uber-specific labels, like the Ray job ID to all its head and worker containers to aggregate over the job level. A central collector service collects these metrics.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/ray-container-utilisation-metrics-17442381898637-1024x513.png)Figure 6: Container Utilization Metrics of a Pod. 
* * *
# Conclusion
Elastic resource management, heterogeneous clusters, and GPU-specific workload scheduling have been critical to Uber’s machine learning pipeline orchestration on Kubernetes. These enhancements help Uber run its machine learning workloads efficiently and reliably. As a next step, we’re considering open-sourcing the technologies described in this blog series.
Cover Photo Attribution: “[AI technology brain background digital transformation concept](https://www.freepik.com/free-vector/ai-technology-brain-background-vector-digital-transformation-concept_16396122.htm#fromView=keyword&page=1&position=48&uuid=6bc9792e-96b7-479d-8397-366c377626e9)” by [rawpixel.com](https://www.freepik.com/free-photo/ai-technology-brain-background-digital-transformation-concept_17122619.htm#fromView=keyword&page=1&position=1&uuid=371522a4-5756-4e83-ab3e-b213b8d8dc28) on freepik.
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
![Axansh Sheth](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/axansh-17436348453296-613x1024.jpeg)
Axansh Sheth
Axansh Sheth is an Engineering Manager at Uber, based in Bangalore, India. With prior experience as an IC in ML Infra, he manages the Batch Compute Platform team and is focused on modernizing the batch compute stack.
![Abhinav Dixit](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/ad-pic-17436342351958.png)
Abhinav Dixit
Abhinav Dixit is a Software Engineer II at Uber, based in Bangalore, India. As a key member of the Compute Batch team, he specializes in resource management and the deployment of batch jobs within the organization. With a strong background in Kubernetes and the Peloton stack, he is dedicated to optimizing performance and enhancing efficiency in Uber’s computational infrastructure.
* * *
Posted by Bharat Joshi, Anant Vyas, Ben Wang, Axansh Sheth, Abhinav Dixit 
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
[English](/en-CA/blog/ubers-journey-to-ray-on-kubernetes-resource-management/)
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
[English](/en-CA/blog/ubers-journey-to-ray-on-kubernetes-resource-management/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
