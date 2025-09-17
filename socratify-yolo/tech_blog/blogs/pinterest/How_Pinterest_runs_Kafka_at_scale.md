---
title: "How Pinterest runs Kafka at scale"
company: "pinterest"
url: "https://medium.com/pinterest-engineering/how-pinterest-runs-kafka-at-scale-ff9c6f735be"
type: "system_architecture"
date: "2025-09-15"
---

# How Pinterest runs Kafka at scale

[![Pinterest Engineering](https://miro.medium.com/v2/resize:fill:64:64/1*iAV-apeVpCJ1h6Znt1AzCg.jpeg)](/@Pinterest_Engineering?source=post_page---byline--ff9c6f735be---------------------------------------)

[Pinterest Engineering](/@Pinterest_Engineering?source=post_page---byline--ff9c6f735be---------------------------------------)

6 min read

·

Nov 27, 2018

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fpinterest-engineering%2Fff9c6f735be&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fhow-pinterest-runs-kafka-at-scale-ff9c6f735be&user=Pinterest+Engineering&userId=ef81ef829bcb&source=---header_actions--ff9c6f735be---------------------clap_footer------------------)

\--

11

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fff9c6f735be&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fhow-pinterest-runs-kafka-at-scale-ff9c6f735be&source=---header_actions--ff9c6f735be---------------------bookmark_footer------------------)

Listen

Share

Yu Yang | Pinterest engineer, Data Engineering

Pinterest runs one of the largest Kafka deployments in the cloud. We use [Apache Kafka](https://kafka.apache.org/) extensively as a message bus to transport data and to power real-time streaming services, ultimately helping more than 250 million Pinners around the world discover and do what they love.

As mentioned in [an earlier post](/@Pinterest_Engineering/scalable-and-reliable-data-ingestion-at-pinterest-b921c2ee8754), we use Kafka to transport data to our data warehouse, including critical events like impressions, clicks, close-ups, and repins. We also use Kafka to transport visibility metrics for our internal services. If the metrics-related Kafka clusters have any glitches, we can’t accurately monitor our services or generate alerts that signal issues. On the real-time streaming side, Kafka is used to power many streaming applications, such as fresh content indexing and recommendation, spam detection and filtering, real-time advertiser budget computation, and so on.

We’ve shared out experiences at the [Kafka Summit 2018](https://kafka-summit.org/kafka-summit-san-francisco-2018/schedule/) on [incremental db ingestion using Kafka](https://www.confluent.io/kafka-summit-sf18/pinterests-story-of-streaming-hundreds-of-terabytes), and [building real-time ads platforms using kafka streams](https://www.confluent.io/kafka-summit-sf18/building-pinterest-real-time-ads-platform-using-kafka-streams). With >2,000 brokers running on Amazon Web Services, transporting >800 billion messages and >1.2 petabytes per day, and handling >15 million messages per second during the peak hours, we’re often asked about our Kafka setup and how to operate Kafka reliably in the cloud. We’re taking this opportunity to share our learnings.

**Pinterest Kafka setup**

Figure 1 shows the Pinterest Kafka service setup. Currently we have Kafka in three regions of AWS. Most of the Kafka brokers are in the us-east-1 region. We have a smaller footprints in us-east-2 and eu-west-1. We use MirrorMaker to transport data among these three regions. In each region, we spread the brokers among multiple clusters for topic level isolation. With that, one cluster failure only affects a limited number of topics. We limit the maximum size of each cluster to 200 brokers.

We currently use d2.2xlarge as the default broker instances.The d2.2xlarge instance type works well for most Pinterest workloads. We also have a few small clusters that use d2.8xlarge instances for highly fanout reads. Before settling on d2 instances with local storage, we experimented with using Elastic Block Store st1 (throughput optimized hard drives) for our Kafka workloads. We found that the d2 instances with local storage performed better than EBS st1 storage.

Press enter or click to view image in full size

 _Figure 1. Pinterest Kafka setup_

We have _default.replication.factor_ set to 3 to protect us against up to two broker failures in one cluster. As of November 2018, AWS [Spread Placement Groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html#placement-groups-spread) limit running instances per availability zone per group to seven. Because of this limit, we cannot leverage spread placement groups to guarantee that replicas are allocated to different physical hosts in the same availability zone. Instead, we spread the brokers in each Kafka cluster among three availability zones, and ensure that replicas of each topic partition are spread among the availability zones to withstand up to two broker failures per cluster.

**Kafka Cluster auto-healing**

With thousands of brokers running in the cloud, we have broker failures almost every day. Manual work was required to handle broker failures. That added significant operational overhead to the team. In 2017, we built and open-sourced [DoctorKafka](https://github.com/pinterest/doctorkafka), a Kafka operations automation service to perform partition reassignment during broker failure for operation automation.

It turned out that partition reassignment alone is not sufficient. In January 2018, we encountered broker failures that partition reassignment alone could not heal due to degraded hardware. When the underlying physical machines were degraded, the brokers ran into unexpected bad states. Although DoctorKafka can assign topic partitions on the failed brokers to other brokers, producers and consumers from dependent services may still try to talk to the failed or degraded broker, resulting in issues in the dependent services. Replacing failed brokers quickly is important for guaranteeing Kafka service quality.

In Q1 2018, we improved DoctorKafka with a broker replacement feature that allows it to replace failed brokers automatically using user-provided scripts, which has helped us protect the Kafka clusters against unforeseeable issues. Replacing too many brokers in a short period of time can cause data loss, as our clusters only store three replicas of data. To address this issue, we built a rate limiting feature in DoctorKafka that allows it to replace only one broker for a cluster in a period of time.

It’s also worth noting that the [AWS ec2 api](https://docs.aws.amazon.com/cli/latest/reference/ec2/assign-private-ip-addresses.html) allows users to replace instances while keeping hostnames and IP addresses unchanged, which enables us to minimize the impact of broker replacement on dependent services. We’ve since been able to reduce Kafka-related alerts by >95% and keep >2000 brokers running in the cloud with minimum human intervention. See [here](https://github.com/pinterest/doctorkafka/blob/master/drkafka/config/doctorkafka.properties#L51) for our broker replacement configuration in DoctorKafka.

**Working with the Kafka open source community**

The Kafka open source community has been active in developing new features and fixing known issues. We set up an internal build to continuously pull the latest Kafka changes in release branches and push them into production in a monthly cadence.

We’ve also improved Kafka ourselves and contributed the changes back to the community. Recently, Pinterest engineers have made the following contributions to Kafka:

  * [KIP-91](https://cwiki.apache.org/confluence/display/KAFKA/KIP-91+Provide+Intuitive+User+Timeouts+in+The+Producer) Adding delivery.timeout.ms to Kafka producer
  * [KIP-245](https://cwiki.apache.org/confluence/display/KAFKA/KIP-245%3A+Use+Properties+instead+of+StreamsConfig+in+KafkaStreams+constructor) Use Properties instead of StreamsConfig in KafkaStreams constructor
  * [KAFKA-6896](https://issues.apache.org/jira/browse/KAFKA-6896) Export producer and consumer metrics in Kafka Streams
  * [KAFKA-7023](https://issues.apache.org/jira/browse/KAFKA-7023) Move prepareForBulkLoad() call after customized RocksDBConfigSettters
  * [KAFKA-7103](https://issues.apache.org/jira/browse/KAFKA-7103) Use bulk loading for RocksDBSegmentedBytesStore during init



We’ve also proposed several Kafka Improvement Proposals that are under discussion:

  * [KIP-276](https://cwiki.apache.org/confluence/display/KAFKA/KIP-276+Add+StreamsConfig+prefix+for+different+consumers) Add config prefix for different consumers
  * [KIP-300](https://cwiki.apache.org/confluence/display/KAFKA/KIP-300%3A+Add+Windowed+KTable+API+in+StreamsBuilder) Add windowed KTable API
  * [KIP-345](https://cwiki.apache.org/confluence/display/KAFKA/KIP-345%3A+Introduce+static+membership+protocol+to+reduce+consumer+rebalances) Reduce consumer rebalances through static membership



**Next Steps**

Although we’ve made improvements to scale the Kafka service at Pinterest, many interesting problems need to be solved to bring the service to the next level. For instance, we’ll be exploring Kubernetes as an abstraction layer for Kafka at Pinterest.

We’re currently investigating using two availability zones for Kafka clusters to reduce interzone data transfer costs, since the chance of two simultaneous availability zone failures is low. AWS latest generation instance types are EBS optimized, and have dedicated EBS bandwidth and better network performance than previous generations. As such, we’ll evaluate these latest instance types leveraging EBS for faster Kafka broker recovery.

Pinterest engineering has many interesting problems to solve, from building scalable, reliable, and efficient infrastructure to applying cutting edge machine learning technologies to help Pinners discover and do what they love. Check out [our open engineering roles and join us](https://careers.pinterest.com/careers)!

**_Acknowledgements_** _: Huge thanks to Henry Cai, Shawn Nguyen, Yi Yin, Liquan Pei, Boyang Chen, Eric Lopez, Robert Claire, Jayme Cox, Vahid Hashemian, and Ambud Sharma who improved Kafka service at Pinterest._

**Appendix:**

1.**** The Kafka broker setting that we use with d2.2xlarge instances. Here we only list the settings that are different from Kafka default values.

Press enter or click to view image in full size

2\. The following is Pinterest Kafka java parameters.

Press enter or click to view image in full size

We enable TLS access for Kafka at Pinterest. As of Kafka 2.0.0, each KafkaChannel with a ssl connection costs ~122K memory, and Kafka may accumulate a large number of unclosed KafkaChannels due to frequent re-connection (see [KAFKA-7304](https://issues.apache.org/jira/browse/KAFKA-7304) for details). We use a 8GB heap size to minimize the risk of having Kafka run into long-pause GC. We used a 4GB heap size for Kafka process before enabling TLS.

Press enter or click to view image in full size

 _Figure 2. The size of a KafkaChannel object with an SSL connection._
