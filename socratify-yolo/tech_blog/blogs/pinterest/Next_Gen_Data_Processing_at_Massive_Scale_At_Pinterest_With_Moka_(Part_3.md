---
title: "Next Gen Data Processing at Massive Scale At Pinterest With Moka (Part 1 of 2)"
author: "https://medium.com/@Pinterest_Engineering"
url: "https://medium.com/pinterest-engineering/next-gen-data-processing-at-massive-scale-at-pinterest-with-moka-part-1-of-2-39a36d5e82c4?source=rss----4c5a5f6279b6---4"
date: "2025-09-15"
---

# Next Gen Data Processing at Massive Scale At Pinterest With Moka (Part 1 of 2)
[![Pinterest Engineering](https://miro.medium.com/v2/resize:fill:64:64/1*iAV-apeVpCJ1h6Znt1AzCg.jpeg)](/@Pinterest_Engineering?source=post_page---byline--39a36d5e82c4---------------------------------------)
[Pinterest Engineering](/@Pinterest_Engineering?source=post_page---byline--39a36d5e82c4---------------------------------------)
16 min read
·
Jul 11, 2025
[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fpinterest-engineering%2F39a36d5e82c4&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fnext-gen-data-processing-at-massive-scale-at-pinterest-with-moka-part-1-of-2-39a36d5e82c4&user=Pinterest+Engineering&userId=ef81ef829bcb&source=---header_actions--39a36d5e82c4---------------------clap_footer------------------)
\--
2
[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F39a36d5e82c4&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fnext-gen-data-processing-at-massive-scale-at-pinterest-with-moka-part-1-of-2-39a36d5e82c4&source=---header_actions--39a36d5e82c4---------------------bookmark_footer------------------)
Listen
Share
_Soam Acharya: Principal Engineer · Rainie Li: Manager, Data Processing Infrastructure · William Tom: Senior Staff Software Engineer · Ang Zhang: Director, Big Data Platform_
As Pinterest’s data processing needs grow and as our current [Hadoop](https://hadoop.apache.org/docs/r2.10.0/)-based platform (Monarch) ages, the Big Data Platform (BDP) team within Pinterest Data Engineering started considering alternatives for our next generation massive scale data processing platform. In this blog post series, we share details of our subsequent journey, the architecture of our next gen data processing platform, and some insights we gained along the way. In part one, we provide rationale for our new technical direction prior to outlining the overall design and detailing the application focused layer of our platform. We conclude with current status and some of our learnings. Part two of our series can be found [here](/pinterest-engineering/next-gen-data-processing-at-massive-scale-at-pinterest-with-moka-part-2-of-2-d0210ded34e0) where we spotlight the infrastructure focused aspects of our platform.
## Introduction
Encouraged by its growing popularity and increasing adoption in the Big Data community, we explored [Kubernetes](https://kubernetes.io/) (K8s)-based systems as the most likely replacement for Hadoop 2.x. Candidate platforms had to meet the following criteria:
* Extensive support for containers to enhance platform data privacy and security
* Execute Pinterest’s custom [Spark](http://spark.apache.org/) fork at comparable or better performance and scale
* Leverage key technical improvements such as GPU support, newer EC2 instance types such as ARM/Graviton, newer JDK versions, and autoscaling
* Lower operational and maintenance costs than the current platform
* Better developer velocity; jobs could be transparently migrated to the newer platform
Armed with these requirements, we performed a comprehensive evaluation of running Spark on various platforms during 2022. We leaned towards Kubernetes-focused frameworks for the following advantages they offered:
* Container-based isolation and security as first class platform citizens
* Ease of deployment (simplification, instance types)
* Built-in frameworks
* Performance tuning options
We consider each advantage in turn.
### Built-in Container Support
Unlike Hadoop, Kubernetes was built as a container orchestration system, first and foremost. Consequently, it provides more fine grained support for container management and deployment than other systems. Similarly, there’s extensive built-in support for Role-Based Access Control (RBAC) and account management at the container level, as well as networking within a Kubernetes cluster.
However, Kubernetes as a general purpose system does not have the built in support for data management, storage, and processing that Hadoop does. Nor does it have support for batch-based scheduling. As a result, we have to rely on Spark, S3, and third party schedulers like [YuniKorn](https://yunikorn.apache.org/), respectively, to fashion a Kubernetes-based data processing solution.
### Deployment
Our current deployment model in Hadoop is cumbersome, involving a mixture of [Terraform](https://developer.hashicorp.com/terraform), Puppet, and custom scripts. In Kubernetes, deployment is typically handled via a mixture of:
* Terraform for setting up the base cluster
* Container images for pod specific environments and customizations
* [Helm](https://helm.sh/) for composing and deploying services
This promised to be a more straightforward approach on the surface with the possibility of custom container images being an effective tool for deploying customer specific environments.
### Supporting Frameworks
A number of frameworks are available for Kubernetes, such as [Prometheus](https://prometheus.io/) and [FluentBit](https://fluentbit.io/) for logging and monitoring, [KubeCost](https://github.com/kubecost) for resource usage tracking, [Spark Operator](https://github.com/kubeflow/spark-operator) for Spark application deployment, and pluggable third party schedulers such as YuniKorn and [Volcano](https://volcano.sh/en/). While not all of these frameworks apply well to our use case, their availability made it easier for us to evaluate multiple approaches to find the best fit.
### Performance Tuning
The Kubernetes architecture and deployment model makes a number of levers available when optimizing for performance:
* JDK versions: the absence of Hadoop simplifies the deployment of Spark on a newer JDK on Kubernetes.
* GPU: while library dependencies must still be considered, the absence of Hadoop makes it easier to deploy a Spark only GPU-based Kubernetes cluster.
* Graviton: it is difficult to run Hadoop 2.x on ARM instances. Removing it made it more straightforward to deploy the rest of the stack.
* Autoscaling: Kubernetes has autoscaling and node labeling built in.
Our POC indicated we would be able to achieve acceptable performance with Spark on AWS Elastic Kubernetes Service (EKS) clusters running both x86 and ARM instances depending on the price / performance observed for the workload.
## Design
Building a new platform that leverages Kubernetes and EKS to replace Monarch at Pinterest introduced several challenges. These included integrating EKS into the existing Pinterest environment, finding replacements for Hadoop components, ensuring compatibility with the Pinterest ecosystem, building an operational framework to observe and support the new platform, and optimizing overall cost-effectiveness through the use of Graviton instances. This required thorough understanding of EKS as well as the ecosystem of supporting tools, together with careful planning and implementation. In particular:
* _Integrating with Pinterest_ : we must deploy EKS in a manner that is consistent with Pinterest guidelines and security practices. Additionally, we have to reduce our reliance on tools such as Puppet that are slowly being deprecated, yet find a way to leverage replacements that are commonly used for Kubernetes but not necessarily in wide use at Pinterest.
* _Instance Types_ : as mentioned previously, moving away from Hadoop into a Spark on Kubernetes framework allows us to leverage newer EC2 instance types such as Graviton. This entailed careful porting of our Spark/PySpark images as well as other supporting components.
* Over the years, Hadoop and Monarch have come to encompass a tremendous amount of functionality. Building an alternative implies developing replacements for the following:
* _User UI_ : The YARN UI in the Hadoop resource manager provides users with a view of the status of a cluster and of the jobs running on it.
* _Job Submission_ : Monarch uses Argonath, aka Job Submission Service, which incorporates a Hadop client that performs the actual job submission. We have to build an alternate job submission system that ensures compatibility with existing upstream data pipelines, applications, and workflows.
* _Resource Management and Job Scheduling:_ YARN provides a variety of schedulers and resource management tools such as weighted queues. These are used extensively in Monarch to ensure appropriate resource allocation between various workflows.
* _Log aggregation:_ Hadoop provides application log aggregation. At Pinterest, we’ve modified Hadoop further to upload application logs and resource summary logs to S3.
* _Security_ : Hadoop provides security features such as authentication, authorization, and role-based access control (RBAC). While the bulk of these features are employed in our Fine grained Access Control (FGAC) Hadoop clusters in conjunction with Kerberos integration, we have to ensure our EKS platform honors basic security expectations.
* _HDFS_ : While HDFS is not the storage system of record for data at Pinterest, it is used for some system use cases such as storing Spark application event logs. Consequently, we have to find ways of deprecating such as use cases in favor of S3.
* _Observability_ : Monarch supports an extensive set of monitoring tools targeted at various layers of the Hadoop stack.
Figure 1 illustrates the initial high level design of**Moka**, our new Spark on EKS platform. For phase one, we built a system able to process batch Spark workloads that only access non sensitive data. In this post, we will detail our design for phase one. We have also added other functionality to Moka such as interactive query submission and FGAC and will present those changes at a later date.
Press enter or click to view image in full size
Figure 1: Initial Moka High Level Design
In our first iteration, jobs are submitted and processed as follows:
* Scheduled workflows are decomposed into specific jobs by [**Spinner**](/pinterest-engineering/spinner-pinterests-workflow-platform-c5bbe190ba5), our [Airflow](https://airflow.apache.org/)-based workflow composition and management system, which transmits them to**Archer**, Pinterest’s EKS Job Submission Service.
***Archer**converts the incoming job specifications into a Kubernetes CRD. It then submits the CRD to a suitable**EKS cluster**.
* Pinterest EKS clusters intended for Spark are augmented by the addition of:
\-**Spark Operator,**which allows Spark applications to run natively on Kubernetes
\- [**YuniKorn**](https://yunikorn.apache.org/), which brings YARN style batch scheduling to Kubernetes
\-**Remote Shuffle Service,**which allows Spark applications to offload the shuffling to a dedicated service
* SparkSQL jobs running on EKS contact the [**Hive Metastore**](https://hive.apache.org/) to help convert SQL into Spark jobs
* The actual job uses container images stored in the**AWS ECR**service
* When the job is executing:
* Archer keeps track of its status for upstream status updates
\- Users will be able to connect to the live UI of the Spark drivers of the running jobs in EKS clusters through a**Proxy**network of AWS Network Load Balancers and K8s Ingress resources
\- Spark application and event logs together with system pod logs are uploaded to S3.
\- Various aspects of the platform are collected by a set of agents and transmitted to Statsboard, Pinterest’s internal metrics management and display platform, and other custom dashboards
* Post job execution, users use the**Spark History Server**to obtain job records and logs
* The**Moka UI**provides a centralized portal for users to view the (read only) status of their jobs and connect to either the live UI if the job is running or to the job’s Spark History Server page if it has completed execution
Next, we provide more details on the core application focused aspects of our platform. Infrastructure and other remaining components will be described in the second part of our blog series.
## Spark Operator
To manage the deployment and lifecycle of Spark applications at Pinterest, we decided to leverage the [Spark Operator](https://github.com/kubeflow/spark-operator/tree/master) instead of running`spark-submit`directly. Spark Operator exposes the`SparkApplication`Custom Resource Definition (CRD), which allows us to define Spark applications in a declarative manner and leave it to the Spark Operator to handle all of the underlying submission details. Internally, Spark Operator still utilizes the native`spark-submit`command. The Spark Operator will run`spark-submit`in cluster mode to start the driver pod, and the driver pod will internally run`spark-submit`in client mode to start the driver process.
Press enter or click to view image in full size
Figure 2: Spark Operator ([source](https://www.kubeflow.org/docs/components/spark-operator/overview/))
During our evaluation process and migration, we identified several bottlenecks or scalability issues caused by the Spark Operator. Here are some of the issues we found and how we addressed them:
### Premature Driver Pod Cleanup and Incorrect Final Status
When the number of pods in K8s reaches a certain threshold (in our case 12.5k) defined by PodGCControllerConfiguration, PodGC Controller will trigger cleanup of terminal pods. We observed cases where a driver pod completes and is cleaned up before the Spark Operator has a chance to retrieve the pod status and update the Spark Application. In this case, the Spark Operator will incorrectly interpret and mark the SparkApplication as FAILED. In order to prevent premature cleanup of the driver pod by PodGC controller, we utilize Pod Templates to add a [finalizer](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/) to all Spark Driver pods upon creation. If a finalizer exists on a pod, it will prevent the PodGC Controller from removing it. We added logic to the Spark Operator that will remove the finalizer on the driver pod only when the final status of the Driver has been retrieved and the SparkApplication transitions to a terminal state.
### Spark Operator Mutating Admission Webhook
In Moka, we utilize volume mounts to allow access to predefined host-level directories from within the pod as soon as the pod starts. For example, Normandie, an internal security process which manages certificates, exposes a FUSE endpoint on a fixed path in every Pinterest host and should be accessible as soon as the Spark process starts.
Originally, we relied on the Spark Operator’s mutating admission webhook to mutate the pod after it was created to add the volume mounts. However, as the platform scaled we found that the increased load caused increased latency against the K8s control plane. As a mitigation we deployed multiple spark operators to the platform. To fully resolve the webhook related latency issues we utilized [pod templates](https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates), which we passed to Spark via [Spark template configs](https://spark.apache.org/docs/latest/running-on-kubernetes.html#pod-template) to configure the volume mounts instead. This allowed us to remove our reliance on the Spark Operators webhook and return to a single Spark operator deployment which manages multiple namespaces.
## Archer
Our existing job submission service (Argonath aka JSS) for Hadoop only supports job deployment to YARN clusters. To support job submission to a large scale, more accurately track job status, and provide job uniqueness checks, we built Archer — a new job submission service for Spark on K8s, with focus on EKS. Archer provides the following features: job submission, job deletion, and job information tracking. It integrates with existing user interface frameworks such as
### External components
Figure 3 focuses on the components that interact with Archer.
Press enter or click to view image in full size
Figure 3: Archer Job Submission System
* Users trigger jobs through Spinner that will then forward the request to Archer through Envoy (Pinterest service mesh) and Pastis, our internal access configuration system. We use Envoy and Pastis between Spinner and Archer for authentication and authorization.
* Archer will insert the request to its DB and convert the incoming request to a Spark Operator CRD.
* Archer submits the request to EKS API-server.
* Spark Operator will enhance the request and submit to the K8s API control plane.
* Archer periodically polls for job logs from S3.
### Internal Design
Press enter or click to view image in full size
Figure 4: Archer Detailed Design
Archer comprises two layers:
1. Service layer
* Talks to the database to get job information including state and job details, then exposes this information to users.
* Enqueues new jobs to the DB when users submit or delete applications.
* Security checks including authorization and authentication will be handled in this layer.
2\. Worker layer
* Interacts with the K8s client to submit or delete an application to K8s clusters.
* Calls one or multiple Spark Operators (based on cluster load) to handle submission and deletion. Spark Operators are assigned to dedicated namespaces. Spark Operators will distribute jobs to different YuniKorn queues.
* Submitting and deleting jobs after dequeuing entries from the job queue. The job queue is implemented as a table stored in the DB.
It is possible for Archer to get job status directly from K8s api-server, which would make the state machine unnecessary. With this approach, the worker layer would only handle light-weight operations (dequeue from DB, call K8s api, balance load between multiple Spark Operators, etc.), and we could combine the worker layer and service layer into one layer to simplify the design. However keeping separate layers can provide the following benefits:
* The service layer focuses on interacting with users and querying the latest information from DB.
* The worker layer interacts with the K8s api-server and handles actual job submission, deletion, and updating job status asynchronously.
* To support more features (e.g. job routing and resource allocation) in the future, we only need to modify and deploy the worker layer, and the service layer will not be affected. These features might result in long response times, thus having a worker layer could avoid blocking API calls.
### Spinner Integration and Job Migration
Migrating Spark jobs from Hadoop to EKS is a non-trivial undertaking. We’re essentially building a new platform on top of EKS while ensuring everything remains performant and compatible. Here are a few key challenges we encountered:
* Graviton vs. x86: Our new Moka platform is built to support both ARM and x86 to allow us the freedom to select either depending on efficiency, while the existing Hadoop infrastructure relies on Intel processors. As a result, we had to recompile certain libraries to run on ARM64. We also noticed a slight uptick in memory usage, which we suspect stems from library changes for the ARM architecture.
* JDK Upgrade: We moved from Java 8 to Java 11 during the migration, which introduced deprecation issues for some JVM parameters. It required careful tuning and refactoring to accommodate the newer JDK.
* Containerization and Dependencies: Because everything is containerized in Kubernetes, we needed to build Spark images that closely matched our Hadoop/YARN environment. This process surfaced several missing libraries, configurations, and dependencies, and required thorough testing to ensure compatibility and stability.
To address these challenges and ensure job reliability in production, we designed and implemented a “dry run” process.
Press enter or click to view image in full size
Figure 5: Moka Validation Process
Whenever there is a production job submission to [JSS](/pinterest-engineering/efficient-resource-management-at-pinterests-batch-processing-platform-61512ad98a95), our Monarch/Hadoop job submissions service, we will submit the same request to Archer. Archer automatically replaces all the prod output buckets and tables and replaces them with test buckets. Archer submits the dryRun requests to Moka staging clusters. Once both Monarch production run and Moka staging runs complete, Archer will automatically trigger data validation. This includes:
* Comparing output bucket data sizes
* Creating tables for both output datasets
* Comparing line count and checksum of tables
With the dryRun pipeline, we were able to automatically detect unexpected failures for prod jobs in the staging environment to avoid job failures in production.
Once jobs pass dryRun validation, they are ready to be migrated to Moka prod. We designed and implemented migration flow by extending the Airflow/Spinner-based Spark Operator (not to be confused with the Kubernetes Spark Operator) and Spark SQL Operator to support both the existing JSS YARN operator and the new Archer Operator. The extended Airflow operators decide whether to route to Monarch or Moka during runtime based on corresponding info in the migration DB. Overall, our dryRun framework greatly eased the Spark workflow validation and migration process.
Press enter or click to view image in full size
Figure 6: Migration Framework
## Remote Shuffle Service
Data shuffling is a process where the data is redistributed across different partitions to enable parallel processing and better performance, which is important for big data. Figure 7 shows how this applies to MapReduce. On Hadoop YARN, we use the external shuffle service (ESS). By utilizing ESS, we achieve support for dynamic allocation since we have the ability to scale down executors that no longer have the responsibility of managing shuffle data. However, there are two challenges with ESS on YARN: shuffle timeouts, and noisy neighbor interference because of shared disks filling up.
Figure 7: Map reduce
To enable dynamic allocation on K8s, we adopted Apache Celeborn as Remote Shuffle Service (RSS) on Moka. Here are some of the key advantages of a Remote shuffle service:
* More IO efficient and less shuffle timeouts
* Partition auto split
* Decouple storage and compute clusters to unblock us to use more optimized instance types for compute
Figure 8: Apache Celeborn Remote Shuffle Service
We’ve found our usage of Celeborn for RSS has improved platform reliability and stability with overall Spark job performance improving 5% on average.
## Resource Management and Scheduling
We set up a data processing pipeline to collect historical workflow resource usage from our past Monarch and Moka jobs. This pipeline generates resource strategy based on historical data and workflow SLO. It sets up queue usage for each workflow and populates a resource DB with routing information. When a workflow is submitted, Archer queries this resource DB and routes the workflow to specific queues and specific clusters.
Press enter or click to view image in full size
Figure 9: Moka Resource Management
We adopted Apache YuniKorn as Scheduler on Moka since YuniKorn provides several advantages over the default K8s scheduler.
1\. YuniKorn provides queue-based scheduling & maxApplication Enforcement.
YuniKorn is very similar to YARN. This is useful as having queue structures is important for batch applications. It allows us to control resource allocation between different organizations, teams, and projects. YuniKorn also supports maxApplication enforcement, which is a critical feature we used on YARN. When there are a large number of concurrent jobs, they will all compete for resources and a certain amount of resources will be wasted, which could lead to job failure.
An example of org-based queue structure in Moka:
Press enter or click to view image in full size
Figure 10: Org-Based Queue Structure
2\. YuniKorn provides preemption.
Preemption feature allows higher-priority jobs to dynamically reallocate resources by preempting lower-priority ones, ensuring critical workloads get necessary resources. Our workload tiers are defined using K8s priorityClass:
* Tier 1 jobs: set higher priority and these jobs cannot be preempted
* Tier 2 or 3 jobs: set lower priority, and these jobs can be preempted by higher priority jobs
Press enter or click to view image in full size
Figure 11: YuniKorn Preemption
### Current Status and Learnings
We’ve currently migrated approximately 70% of our batch Spark workloads to Moka from Monarch while managing high growth on both platforms, with all new Spark and SparkSQL workloads running on Moka by default. We expect to have all Spark workloads running on Moka by the end of the year. In tandem, we’re also working on transitioning non Spark batch workloads to Spark, which will allow us to sunset all Hadoop clusters at Pinterest.
Regarding cost savings, we benefit from being able to leverage Moka clusters with ARM instance types. However, it’s been our experience that not all workloads perform well on ARM. In addition, since we’re sunsetting our Hadoop clusters and moving the same EC2 instances to Moka, many of our Moka clusters run the same CPUs as our Monarch clusters (i.e.**x86**-based instance types). However, other components in our architecture ensure we continue extracting meaningful cost efficiencies via Moka:
* Centralizing our shuffle processing into Celeborn led to faster identification and resolution of performance bottlenecks, allowing us to pack more applications onto EKS clusters.
* Greater isolation provided by a container-based system allowed removal of dedicated yet underutilized Hadoop environments in favor of running jobs with differing security requirements on the same Moka cluster.
* Moka provides a platform for implementing techniques such as opportunistic temporal autoscaling, whereby we scale up Moka clusters at night to take advantage of temporary idle capacity elsewhere at Pinterest (through scheduling) for further savings.
## Acknowledgements
Moka was a massive project that necessitated and continues to require extensive cross functional collaboration between teams at multiple organizations at Pinterest and elsewhere. Here’s an incomplete list of folks and teams that helped us build our first set of production Moka clusters:
Data Processing Infra: Aria Wang, Bhavin Pathak, Hengzhe Guo, Royce Poon, Bogdan Pisica
Big Data Query Platform: Zaheen Aziz, Sophia Hetts, Ashish Singh
Batch Processing Platform: Nan Zhu, Yongjun Zhang, Zirui Li, Frida Pulido, Chen
SRE/PE: Ashim Shrestha, Samuel Bahr, Ihor Chaban, Byron Benitez, Juan Pablo Daniel Borgna
TPM: Ping-Huai Jen, Svetlana Vaz Menezes Pereira, Hannah Chen
Cloud Architecture: James Fogel, Sekou Doumbouya
Traffic: James Fish, Scott Beardsley
Security: Henry Luo, Jeremy Krach, Ali Yousefi, Victor Savu, Vedant Radhakrishnan
Continuous Integration Platform: Anh Nguyen
Infra Provisioning: Su Song, Matthew Tejo
Cloud Runtime: David Westbrook, Quentin Miao, Yi Li, Ming Zong
Workflow Platform: Dinghang Yu, Yulei Li, Jin Hyuk Chang
ML platform: Se Won Jang, Anderson Lam
AWS Team: Doug Youd, Alan Tyson, Vara Bonthu, Aaron Miller, Sahas Maheswari, Vipul Viswanath, Raj Gajjar, Nirmal Mehta
Leadership: Chunyan Wang, Dave Burgess, David Chaiken, Madhuri Racherla, Jooseong Kim, Anthony Suarez, Amine Kamel, Rizwan Tanoli, Alvaro Lopez Ortega
