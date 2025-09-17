---
title: "Next Gen Data Processing at Massive Scale At Pinterest With Moka (Part 2 of 2) | by Pinterest Engineering | Pinterest Engineering Blog | Sep, 2025"
author: "Unknown"
url: "https://medium.com/pinterest-engineering/next-gen-data-processing-at-massive-scale-at-pinterest-with-moka-part-2-of-2-d0210ded34e0?source=rss----4c5a5f6279b6---4"
date: "2025-09-15"
---

# Next Gen Data Processing at Massive Scale At Pinterest With Moka (Part 2 of 2)

[![Pinterest Engineering](https://miro.medium.com/v2/resize:fill:64:64/1*iAV-apeVpCJ1h6Znt1AzCg.jpeg)](/@Pinterest_Engineering?source=post_page---byline--d0210ded34e0---------------------------------------)

[Pinterest Engineering](/@Pinterest_Engineering?source=post_page---byline--d0210ded34e0---------------------------------------)

14 min read

·

4 days ago

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fpinterest-engineering%2Fd0210ded34e0&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fnext-gen-data-processing-at-massive-scale-at-pinterest-with-moka-part-2-of-2-d0210ded34e0&user=Pinterest+Engineering&userId=ef81ef829bcb&source=---header_actions--d0210ded34e0---------------------clap_footer------------------)

\--

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fd0210ded34e0&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fnext-gen-data-processing-at-massive-scale-at-pinterest-with-moka-part-2-of-2-d0210ded34e0&source=---header_actions--d0210ded34e0---------------------bookmark_footer------------------)

Listen

Share

_Soam Acharya: Principal Engineer · Rainie Li: Manager, Data Processing Infrastructure · William Tom: Senior Staff Software Engineer · Ang Zhang: Sr. Director, Big Data Platform_

As Pinterest’s data processing needs grow and as our current [Hadoop](https://hadoop.apache.org/docs/r2.10.0/)-based platform (Monarch) ages, the Big Data Platform (BDP) team within Pinterest Data Engineering started considering alternatives for our next generation massive scale data processing platform. In [part one](/pinterest-engineering/next-gen-data-processing-at-massive-scale-at-pinterest-with-moka-part-1-of-2-39a36d5e82c4) we shared the overall design of Moka, our new next gen data processing platform, and detailed its application focused components. In part two of our series, we spotlight the infrastructure focused aspects of our platform: how we deploy Moka using AWS Elastic Kubernetes Service (EKS), our approach to logging and observability, image management, and how we built a UI for Moka. We conclude with our learnings and future direction.

## Deploying EKS at Pinterest

We have standardized on four cluster environments at Pinterest — test, dev, staging, and production:

* test: intended for cluster or other infrastructure level development, e.g. [Spark Operator](https://github.com/kubeflow/spark-operator) experimentation
* dev: higher platform level development, e.g. Archer additions
* staging: integration testing and [Spark](http://spark.apache.org/) job validation
* production: user workload execution

Each environment has different levels of access and isolation. For example, it is not possible to write production data from a dev environment. We deploy our EKS clusters within each environment using [Terraform](https://developer.hashicorp.com/terraform) augmented by a collection of AWS originated modules and [Helm](https://helm.sh/) charts. All of our Terraform root modules live in a single internal git repository, _terraform-aws-eks-live_. They use the following reusable modules:

1. _terraform-aws-common-eks_ : contains resources common across all Pinterest EKS projects. In addition to Spark, this includes [TiDB](/pinterest-engineering/tidb-adoption-at-pinterest-1130ab787a10), [Ray](/pinterest-engineering/last-mile-data-processing-with-ray-629affbf34ff) (in development), and others. This module also incorporates [_terraform-aws-eks_](https://github.com/pinterest/terraform-aws-eks/tree/pinterest-main), our Pinterest public fork from open source, which creates an EKS cluster & EKS managed addons.
2. _terraform-aws-doeks_ : this is a project specific module forked from open source for Moka/Spark on EKS specific resources.
3. Other kubernetes resource modules forked from [AWS EKS Blueprints v5](https://aws-ia.github.io/terraform-aws-eks-blueprints/v4-to-v5/motivation/):
\- _terraform-aws-eks-blueprints-addons_ : Forked from open source, contains a select set of addons supported by EKS Blueprints
\- _terraform-aws-eks-pinterest-addons_ : Forked from eks-blueprints-addons, contains a select set of addons supported by Pinterest
\- _eks-blueprints-addon_ : Forked from open source, creates a Terraform-based “addon” by installing a Helm chart. Used by eks-blueprints-addons and eks-pinterest-addons.

_terraform-aws-eks-data-addons_ : Forked from open source, contains addons for data on EKS. Used by doeks for Spark Operator.

Figure 1 illustrates how these modules are interlinked.

Press enter or click to view image in full size

Figure 1: Terraform Module Dependency Tree

Our deployment process remains an area of active development. For example, we expect to move the items from #3 above away from Terraform to a separate deploy-focused pipeline in the future.

## Logging Infrastructure

Effective management of logs output by cluster components and Spark applications is critical to determining how well they are running, identifying issues, and performing post mortem analysis. Our users expect this as a matter of course when running jobs, thus it was important for us to find an effective alternative to the functionality provided by Hadoop. Broadly categorizing, a logging solution for Moka would have to consider: 1) Amazon EKS control plane logs, 2) Spark Application logs, and 3) System pod logs. The following figure illustrates the various log categories.

Press enter or click to view image in full size

Figure 2: Amazon EKS log categories

Control plane logs are those generated by the components that constitute the Amazon EKS control plane. These include the K8s API server, audit system, scheduler, and authenticator. The latter is unique to AWS and represents the control plane component that EKS uses for K8s Role-Based Access Control (RBAC) authentication using [AWS Identity and Access Management (IAM)](https://aws.amazon.com/iam/) credentials.

Because the control plane is managed by Amazon EKS, logs for these components are not available directly. Instead, Amazon EKS exports logs for each of the components to [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/). Each log listed previously can be enabled/disabled independently. Once the logs are ingested into CloudWatch, they can be analyzed in-place using [CloudWatch Log Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html). Because a solution for collecting these logs already exists, we instead focus in the remainder of this section on how best to collect system pod and spark application logs.

Spark applications generate a variety of logs depending on the application component:

***Driver**: These logs are generated by the Spark driver and contain information about the driver’s activities, such as task submission, task scheduling, and data shuffling.
***Executor**: These logs are generated by the Spark executors and contain information about the tasks executed by the executors, such as task start, completion, and failures.
***Event Logs**: These logs are also generated by the Spark driver during execution and contain information about the internal operations of Spark, such as the allocation of resources, the scheduling of tasks, and the execution of stages. The event logs provide a comprehensive view of the operations performed by Spark and are useful for performance tuning, debugging, and profiling.

We also felt it would be crucial to persist logs from non Spark system-critical pods in order to diagnose failures that may occur under heavy load. In particular, this is due to the transient nature of pods in K8s and the logs they produce as well as our initial lack of familiarity with operating Amazon EKS at scale.

Taken together, a logging solution for Moka would need to meet the following requirements:

* Spark application logs for a single job have to be grouped together in one location in Amazon S3 such that individual logs for drivers/executors for that job can be retrieved.
* Upload Spark event logs to Amazon S3 in a way that can be consumed by Spark History Server. Spark is able to upload event logs to Amazon S3 but, by default, the driver buffers the logs on the local disk and only uploads once the main job completes. In the event of job errors or driver crashes, the event log is not uploaded. Spark 3.x [introduced a feature (rolling event logs)](https://spark.apache.org/docs/latest/monitoring.html#applying-compaction-on-rolling-event-log-files) that uploads Amazon S3 event logs in increments. However, the minimum increment is 10 MB, which means we would effectively suffer the same problem for small applications.
* System pod logs have to be uploaded to individual locations in Amazon S3.
* YuniKorn pod logs, in addition to being uploaded to Amazon S3, also need to be filtered to collect Spark application resource usage summaries that would be placed in another Amazon S3 location so that it could be processed by our cluster usage analysis workflows.

We explored a number of possible solutions and ultimately settled on [Fluent Bit](https://fluentbit.io/), a Cloud Native Computing Foundation (CNCF) graduated project, and a well-known solution for handling K8s logs. Fluent Bit is able to filter, forward, and augment logs, and it can be extended through plugins. In particular, [an Amazon S3 plugin](https://docs.fluentbit.io/manual/pipeline/outputs/s3) allows a Fluent Bit agent to directly upload files to Amazon S3.

We collaborated with members of the AWS Solution Architects team to deploy Fluent Bit on our EKS clusters as a DaemonSet, making sure each node has a Fluent Bit pod running. We configured Fluent Bit to perform the following tasks:

* System pods running in their own namespaces are uploaded to unique locations in Amazon S3.
* When submitting to Amazon EKS, Archer makes sure the driver and executor pods of a Spark job have the same unique prefix (Archer unique ID). Fluent Bit is configured to make sure logs from Spark pods are uploaded under this unique ID in Amazon S3. This makes sure logs from the same Spark application are grouped together in one location.
* The driver of a Spark application outputs events to a single uniquely named log file to a central location on a host. Fluent Bit uploads this file in chunks to Amazon S3 in a layout that mimics the rolling event log format. It uses filtering to create additional files necessary for Spark History Server to recognize event logs files in Amazon S3.
* Filtering is also used to extract specific strings corresponding to resource summaries from YuniKorn logs and to upload to a separate location.

The following figure illustrates the various log flows performed by Fluent Bit on a single node.

Press enter or click to view image in full size

Figure 3: Fluent Bit log upload flow

Once Spark application logs are uploaded to S3, Archer is able to retrieve and piece sections of the logs together on demand (recall that Fluent Bit uploads all logs to S3 in chunks). For more details on our logging setup, please refer to our joint blog post series with AWS: [Inside Pinterest’s Custom Spark Job logging and monitoring on Amazon EKS: Using AWS for Fluent Bit, Amazon S3, and ADOT Part I](https://aws.amazon.com/blogs/containers/inside-pinterests-custom-spark-job-logging-and-monitoring-on-amazon-eks-using-aws-for-fluent-bit-amazon-s3-and-adot/).

## Metrics and Observability

In order to operate a K8s platform efficiently, storing metrics in a queryable, displayable format is critical to overall platform stability, performance/efficiency, and, ultimately, operating costs. Prometheus formatted metrics are the standard for K8s ecosystem tools. Observability frameworks such as [Prometheus](https://prometheus.io/) (the project, not the format), OTEL, and other CNCF projects continue to see increases in activity year over year.

At Pinterest, the current observability framework, [Statsboard](/pinterest-engineering/analyzing-time-series-for-pinterest-observability-95f8cc0c5885), is TSDB-based and ingests metrics via a sidecar metrics-agent that runs on every host. Systems typically use TSDB libraries to write to their local metrics-agent, which passes the metrics on to Kafka clusters, after which they are ingested into [Goku](/pinterest-engineering/goku-building-a-scalable-and-high-performant-time-series-database-system-a8ff5758a181), Pinterest’s custom TSDB implementation, and made available in Statsboard dashboards. In contrast, the Prometheus-styled frameworks involve systems exposing their metrics for scraping by agents. Unfortunately, support for TSDB as a metrics destination within the open source Cloud Native Computing Foundation (CNCF)/K8s ecosystem is inactive. To address this gap, the Cloud Runtime team at Pinterest has developed _kubemetricsexporter_ , a K8s sidecar container that can periodically scrape Prometheus endpoints in a pod and write the scraped metrics to the local metrics-agent. Because Amazon EKS pods can be in a different network than the host, the batch processing platform team at Pinterest worked with the Cloud Runtime team to extend _kubemetricexporter_ so that it could be configured to use the host IP address instead of localhost. The following figure shows the deployment pattern.

Press enter or click to view image in full size

Figure 4: Using kubemetricexporter with Prometheus Metrics Source

After exploring a variety of options and configurations, we ultimately decided to use a combination of OTEL for extracting detailed insights from our EKS clusters and [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics), an open source K8s tool, for providing a broader overview of the Amazon EKS control plane. In contrast with Prometheus, the OTEL framework only focuses on metrics collection and pre-processing, leaving metrics storage to other solutions. A key portion of the framework is the [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector/tree/main), which is an executable binary that can extract telemetry data, optionally process it, and export it further. The Collector supports several popular open source protocols for receiving and sending telemetry data, as well as offering a pluggable architecture for adding more protocols.

Data receiving, processing, and exporting in OTEL is done using [Pipelines](https://github.com/open-telemetry/opentelemetry-collector/blob/main/docs/internal-architecture.md). The Collector can be configured to have one or more pipelines. Each pipeline includes:

* A set of [Receivers](https://github.com/open-telemetry/opentelemetry-collector/blob/main/docs/scraping-receivers.md) that receive the data
* A series of optional [Processors](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor) that get the data from receivers and process it
* A set of [Exporters](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter) that get the data from processors and send it further outside the Collector

After extensive experimentation, we ended up with a pipeline consisting of a [Prometheus receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/prometheusreceiver), [Attributes processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor), and a [Prometheus exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/prometheusexporter#prometheus-exporter). Our OTEL metrics pipeline looks like the following:

Press enter or click to view image in full size

Figure 5: OTEL pipeline for Moka observability

For more information on our observability infrastructure for EKS, please visit the [second part](https://aws.amazon.com/blogs/containers/inside-pinterests-custom-spark-job-logging-and-monitoring-on-amazon-eks-using-aws-for-fluent-bit-amazon-s3-and-adot-2/) of our joint blog with AWS: [Inside Pinterest’s Custom Spark Job logging and monitoring on Amazon EKS: Using AWS for Fluent Bit, Amazon S3, and ADOT Part II](https://aws.amazon.com/blogs/containers/inside-pinterests-custom-spark-job-logging-and-monitoring-on-amazon-eks-using-aws-for-fluent-bit-amazon-s3-and-adot-2/).

## Image Management

Containerization is a key difference between how Pinterest runs Spark applications on Monarch compared to how they run on Moka. On Monarch, Spark drivers and executors were containerized only from the resource perspective but still shared a common environment including things like Hadoop, Spark, and Java versions. Furthermore, containers running on non-Kerberized Monarch clusters had full access to any other container running on that host. In Moka, we get the full isolation benefits of containerization (cgroups and namespaces) by default with Kubernetes. Given our previous operating model, we did not have a structured system in place for defining, building, deploying, and maintaining container images, nor did we have any support for ARM builds. We wanted applications running on Moka to be architecture agnostic, so not only did we have to build our image generation pipelines from scratch, but we had to ensure that they supported both Intel and ARM from the beginning.

Our images needed to mirror the base environment that each Spark application was accustomed to when running on Monarch, with the main requirements being Java, Hadoop libraries, Spark, and in the case of PySpark, both Python and Python modules.

We built three main pipelines:

* Hadoop Debian Package: Generates a multi-architecture debian package of Hadoop 2.10 to be used by both Monarch and Moka
* Spark Debian Package: Generates a multi-architecture debian package of Spark 3.2 to be used by both Monarch and Moka
* Spark image builder: Using Corretto Java 11 as a base image, installs the two previous multi-architecture packages, standard libraries, compression libraries, and commonly used static jars from S3

Press enter or click to view image in full size

Figure 6: Moka Image Management

## Accessing Spark Components In Moka

### Spark Live UI Access

Each driver for a running Spark application serves a dedicated UI showing the status of various aspects of the job. Because driver pods can run anywhere on a K8s cluster, setting up a dynamic ingress solution per live application can be tricky. Our ingress solution is built using an ingress-nginx controller, AWS LoadBalancer controller, and an AWS Network Load Balancer (NLB) with IP-based routing for each cluster. The AWS LoadBalancer manages the NLB, which configures the user facing NLB for the ingress controller. The Spark on K8s Operator has a _uiService_ component that provisions a Service resource and Ingress Resource for a Spark application. The Service resource is of type ClusterIP, which points to the UI port (4045) on the driver pod. The Ingress resource has the following mappings:

* host: NLB address
* path: AppID
* backend: Service object.

In the example below, the ingress resource for App-A would be configured with host: Moka-NLB.elb.us-east1.amazonaws.com, path: /App-A, and backend: App-A-ui-svc. Users access the actual link to each running application from the [Moka UI](https://docs.google.com/document/d/1FICDrO9-iVKuY-olohL23Tn1euBcsPwnaZ5LSgtc344/edit#heading=h.o9s6dya7w9cz). Figure 7 visualizes the resulting workflow.

Press enter or click to view image in full size

Figure 8: Spark Live UI Architecture

### Spark History Server

In Moka, there is one Spark History Server (SHS) cluster (consisting of one or more nodes) _per environment_. This is a shift from the layout in Monarch, our Hadoop setup, which had one more Spark History Servers _per cluster._ The rationale behind this change from per cluster to per environment is to simplify the overhead in managing many Moka clusters.

Users access SHS through dedicated moka-<environment>-spark-historyserver ingress endpoints, which routes the traffic to the corresponding cluster and performs load-balancing across the history servers in the cluster. We’ve made modifications to SHS for faster parsing and management of event logs, as they are now uploaded to S3 by our logging infrastructure.

## Moka UI

One of the main components that we had to build from scratch was an interface to provide both a comprehensive overview of the platform and detailed information about a Spark application. Coming from Hadoop YARN, many users were accustomed to the native interface that the Hadoop project provided. The YARN interface had existing proxy support for Spark applications, which was seamless to the user. However, one downside to the YARN UI was that it is per-cluster, meaning that users had to have knowledge about the different Hadoop clusters underlying the data platform.

When designing Moka, one of our goals was to abstract away individual clusters from the user and have them interact with it as a monolithic platform. To build the interface, we chose to use Internal Tools Platform (ITP), which is a Typescript React-based internal framework for building internal tooling. The first interface we built is our Application Explorer, which aggregates applications running on different clusters and exposes basic information to the user.

Press enter or click to view image in full size

Figure 9: Application Explorer part of the Moka UI

The second UI we built was the Moka Application UI, which gives users information about their Spark application. It surfaces commonly used pieces of information such as identity of the client that submitted the job,the identity of the job itself, job run location, and current job state. The UI also surfaces dynamic links such as those to the driver log or Spark UI. These dynamic links redirect based on the state of the underlying Spark application. For example, while the application is running, the log links will return logs fetched from the Kubernetes control plane, which allows users to debug and track their application in real time. After the application completes or if the user requests logs that have already been rotated from the control plane, Archer will coalesce the chunked logs located in S3 and serve them back to the user.

Press enter or click to view image in full size

Figure 10: Moka Application UI

## Current Status and Learnings

Pinterest’s transition from Monarch to Moka has marked a significant advancement for infrastructure at Pinterest beyond just batch data processing. Spark on EKS is resource intensive beyond just CPUs — it has bursty AWS API requirements and requires a significant number of IP addresses. Consequently, supporting the Spark on EKS use case has catalyzed infrastructure modernization efforts at Pinterest including:

* Moving to AWS multi-account
* Rethinking our networking topology (see our joint publications with AWS on Spark on EKS networking, parts [1](https://aws.amazon.com/blogs/containers/spark-on-amazon-eks-networking-part-2/) and [2](https://aws.amazon.com/blogs/containers/spark-on-amazon-eks-networking-part-2/), for more details on this topic).
* Support for pod level identities, credentials, and access control.
* Extending our internal logging system, [Singer](http://interference), so that it can take over more of the logging duties from Fluent Bit.

Finally, Moka has opened the doors for EKS adoption by other use cases at Pinterest Data Engineering, particularly those that require access to the Kubernetes API. These include both TiDB on EKS for online systems use cases and Flink for our Stream processing platform. We’re currently working on adopting Ray and PyTorch on EKS and are particularly excited about the possibility of commingling CPU and GPU focused workloads.

## Acknowledgements

Moka was a massive project that necessitated and continues to require extensive cross functional collaboration between teams at multiple organizations at Pinterest and elsewhere. Here’s an incomplete list of folks and teams that helped us build our first set of production Moka clusters:

Data Processing Infra: Aria Wang, Bhavin Pathak, Hengzhe Guo, Royce Poon, Bogdan Pisica

Big Data Query Platform: Zaheen Aziz, Sophia Hetts, Ashish Singh

Batch Processing Platform: Nan Zhu, Yongjun Zhang, Zirui Li, Frida Pulido, Chen Qin

SRE: Ashim Shrestha, Samuel Bahr, Ihor Chaban, Byron Benitez, Juan Pablo Daniel Borgna

TPM: Ping-Huai Jen, Svetlana Vaz Menezes Pereira, Hannah Chen

Cloud Architecture: James Fogel, Sekou Doumbouya

Traffic: James Fish, Scott Beardsley

Security: Henry Luo, Jeremy Krach, Ali Yousefi, Victor Savu, Vedant Radhakrishnan, Cedric Staub

Continuous Integration Platform: Anh Nguyen

Infra Provisioning: Su Song, Matthew Tejo

Cloud Runtime: David Westbrook, Quentin Miao, Yi Li, Ming Zong

Workflow Platform: Dinghang Yu, Yulei Li, Jin Hyuk Chang

ML platform: Se Won Jang, Anderson Lam

AWS Team: Doug Youd, Alan Tyson, Vara Bonthu, Aaron Miller, Sahas Maheswari, Vipul Viswanath, Raj Gajjar, Nirmal Mehta

Leadership: Chunyan Wang, Dave Burgess, David Chaiken, Madhuri Racherla, Jooseong Kim, Anthony Suarez, Amine Kamel, Rizwan Tanoli, Alvaro Lopez Ortega
