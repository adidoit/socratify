---
title: "Architecture"
company: "apache"
url: "https://cassandra.apache.org/doc/4.1/cassandra/architecture/"
content_length: 10465
type: "manual_premium_harvest"
premium: true
curated: true
date: "2025-09-15"
---

[![bluesky icon](../../../../assets/img/bluesky.png)](https://bsky.app/profile/cassandra.apache.org) [![linked-in icon](../../../../assets/img/LI-In-Bug.png)](https://www.linkedin.com/company/apache-cassandra/) [![youtube icon](../../../../assets/img/youtube-icon.png)](https://www.youtube.com/c/PlanetCassandra)

[![Cassandra Logo](../../../../assets/img/logo-white-r.png)](/)

![](../../../../assets/img/hamburger-nav.svg)

  * Get Started
    * [ ![cassandra basics icon](../../../../assets/img/sub-menu-basics.png) Cassandra Basics  ](/_/cassandra-basics.html)
    * [ ![cassandra basics icon](../../../../assets/img/sub-menu-rocket.png) Quickstart  ](/_/quickstart.html)
    * [ ![cassandra basics icon](../../../../assets/img/sub-menu-ecosystem.png) Ecosystem  ](/_/ecosystem.html)
  * [Documentation](/doc/latest/)
  * [Community](/_/community.html)
    * [ ![welcome icon](../../../../assets/img/sub-menu-welcome.png) Welcome  ](/_/community.html#code-of-conduct)
    * [ ![discussions icon](../../../../assets/img/sub-menu-discussions.png) Discussions  ](/_/community.html#discussions)
    * [ ![Governance icon](../../../../assets/img/sub-menu-governance.png) Governance  ](/_/community.html#project-governance)
    * [ ![Contribute icon](../../../../assets/img/sub-menu-contribute.png) Contribute  ](/_/community.html#how-to-contribute)
    * [ ![Meet the Community icon](../../../../assets/img/sub-menu-community.png) Meet the Community  ](/_/community.html#meet-the-community)
    * [ ![Catalyst icon](../../../../assets/img/sub-menu-catalyst.png) Catalyst Program  ](/_/cassandra-catalyst-program.html)
    * [ ![Events icon](../../../../assets/img/sub-menu-events.png) Events  ](/_/events.html)
  * Learn
    * [ ![Basics icon](../../../../assets/img/sub-menu-basics.png) Cassandra 5.0  ](/_/Apache-Cassandra-5.0-Moving-Toward-an-AI-Driven-Future.html)
    * [ ![Case Studies icon](../../../../assets/img/sub-menu-case-study.png) Case Studies  ](/_/case-studies.html)
    * [ ![Resources icon](../../../../assets/img/sub-menu-resources.png) Resources  ](/_/resources.html)
    * [ ![Blog icon](../../../../assets/img/sub-menu-blog.png) Blog  ](/_/blog.html)
  * [Download Now](/_/download.html)



## Cassandra Documentation

#### Version:

4.1

  *     * [website](../../../../_/index.html)
  *     * [trunk](../../../trunk/index.html)
    * [5.0](../../../5.0/index.html)
    * [4.1](../../index.html)
    * [4.0](../../../4.0/index.html)
    * [3.11](../../../3.11/index.html)



  *     * [Main](../../index.html)
      * [Glossary](../../../../_/glossary.html)
      * How to report bugs
      * Contact us
  *     * Cassandra
      * [Getting Started](../getting_started/index.html)
        * [Installing Cassandra](../getting_started/installing.html)
        * [Configuring Cassandra](../getting_started/configuring.html)
        * [Inserting and querying](../getting_started/querying.html)
        * [Client drivers](../getting_started/drivers.html)
        * [Support for Java 11](../getting_started/java11.html)
        * [Production recommendations](../getting_started/production.html)
      * [What’s new](../new/index.html)
      * [Architecture](index.html)
        * [Overview](overview.html)
        * [Dynamo](dynamo.html)
        * [Storage engine](storage_engine.html)
        * [Guarantees](guarantees.html)
        * [Improved internode messaging](messaging.html)
        * [Improved streaming](streaming.html)
      * [Data modeling](../data_modeling/index.html)
        * [Introduction](../data_modeling/intro.html)
        * [Conceptual data modeling](../data_modeling/data_modeling_conceptual.html)
        * [RDBMS design](../data_modeling/data_modeling_rdbms.html)
        * [Defining application queries](../data_modeling/data_modeling_queries.html)
        * [Logical data modeling](../data_modeling/data_modeling_logical.html)
        * [Physical data modeling](../data_modeling/data_modeling_physical.html)
        * [Evaluating and refining data models](../data_modeling/data_modeling_refining.html)
        * [Defining database schema](../data_modeling/data_modeling_schema.html)
        * [Cassandra data modeling tools](../data_modeling/data_modeling_tools.html)
      * [Cassandra Query Language (CQL)](../cql/index.html)
        * [Definitions](../cql/definitions.html)
        * [Data types](../cql/types.html)
        * [Data definition (DDL)](../cql/ddl.html)
        * [Data manipulation (DML)](../cql/dml.html)
        * [Operators](../cql/operators.html)
        * [Secondary indexes](../cql/indexes.html)
        * [Materialized views](../cql/mvs.html)
        * [Functions](../cql/functions.html)
        * [JSON](../cql/json.html)
        * [Security](../cql/security.html)
        * [Triggers](../cql/triggers.html)
        * [Appendices](../cql/appendices.html)
        * [Changes](../cql/changes.html)
        * [SASI](../cql/SASI.html)
        * [Single file of CQL information](../cql/cql_singlefile.html)
      * [Configuration](../configuration/index.html)
        * [cassandra.yaml](../configuration/cass_yaml_file.html)
        * [cassandra-rackdc.properties](../configuration/cass_rackdc_file.html)
        * [cassandra-env.sh](../configuration/cass_env_sh_file.html)
        * [cassandra-topologies.properties](../configuration/cass_topo_file.html)
        * [commitlog-archiving.properties](../configuration/cass_cl_archive_file.html)
        * [logback.xml](../configuration/cass_logback_xml_file.html)
        * [jvm-* files](../configuration/cass_jvm_options_file.html)
        * [Liberating cassandra.yaml Parameters' Names from Their Units](../configuration/configuration.html)
      * [Operating](../operating/index.html)
        * Snitches
        * [Topology changes](../operating/topo_changes.html)
        * [Repair](../operating/repair.html)
        * [Read repair](../operating/read_repair.html)
        * [Hints](../operating/hints.html)
        * [Bloom filters](../operating/bloom_filters.html)
        * [Compression](../operating/compression.html)
        * [Change Data Capture (CDC)](../operating/cdc.html)
        * [Backups](../operating/backups.html)
        * [Bulk loading](../operating/bulk_loading.html)
        * [Metrics](../operating/metrics.html)
        * [Security](../operating/security.html)
        * [Hardware](../operating/hardware.html)
        * [Compaction](../operating/compaction/index.html)
        * [Virtual tables](../operating/virtualtables.html)
        * [Audit logging](../operating/auditlogging.html)
        * [Audit logging 2](../operating/audit_logging.html)
        * [Full query logging](../operating/fqllogging.html)
        * [Transient replication](../operating/transientreplication.html)
      * [Tools](../tools/index.html)
        * [cqlsh: the CQL shell](../tools/cqlsh.html)
        * [nodetool](../tools/nodetool/nodetool.html)
        * [SSTable tools](../tools/sstable/index.html)
        * [cassandra-stress](../tools/cassandra_stress.html)
      * [Troubleshooting](../troubleshooting/index.html)
        * [Finding misbehaving nodes](../troubleshooting/finding_nodes.html)
        * [Reading Cassandra logs](../troubleshooting/reading_logs.html)
        * [Using nodetool](../troubleshooting/use_nodetool.html)
        * [Using external tools to deep-dive](../troubleshooting/use_tools.html)
      * [Development](../../../../_/development/index.html)
        * [Getting started](../../../../_/development/gettingstarted.html)
        * [Building and IDE integration](../../../../_/development/ide.html)
        * [Testing](../../../../_/development/testing.html)
        * [Contributing code changes](../../../../_/development/patches.html)
        * [Code style](../../../../_/development/code_style.html)
        * [Review checklist](../../../../_/development/how_to_review.html)
        * [How to commit](../../../../_/development/how_to_commit.html)
        * [Working on documentation](../../../../_/development/documentation.html)
        * [Jenkins CI environment](../../../../_/development/ci.html)
        * [Dependency management](../../../../_/development/dependencies.html)
        * [Release process](../../../../_/development/release_process.html)
      * [FAQ](../faq/index.html)
      * [Plug-ins](../plugins/index.html)



A newer version of this documentation is available.

[View Latest](../../../5.0/cassandra/architecture/index.html)

  * Cassandra
  * [Architecture](index.html)



  * [Edit](https://github.com/apache/cassandra/edit/cassandra-4.1/doc/modules/cassandra/pages/architecture/index.adoc "Edit Page")



# Architecture

This section describes the general architecture of Apache Cassandra.

  * [Overview](overview.html)

  * [Dynamo](dynamo.html)

  * [Storage Engine](storage_engine.html)

  * [Guarantees](guarantees.html)

  * [Snitches](snitch.html)




## Get started with Cassandra, fast.

[Quickstart Guide](/_/quickstart.html)

![Cassandra Logo](../../../../assets/img/logo-white-r.png)

Apache Cassandra![®](../../../../assets/img/registered.svg) powers mission-critical deployments with improved performance and unparalleled levels of scale in the cloud.

[![bluesky icon](../../../../assets/img/bluesky.png)](https://bsky.app/profile/cassandra.apache.org) [![linked-in icon](../../../../assets/img/LI-In-Bug.png)](https://www.linkedin.com/company/apache-cassandra/) [![youtube icon](../../../../assets/img/youtube-icon.png)](https://www.youtube.com/c/PlanetCassandra)

  * [Home](/)
  * [Cassandra Basics](/_/cassandra-basics.html)
  * [Quickstart](/_/quickstart.html)
  * [Ecosystem](/_/ecosystem.html)
  * [Documentation](/doc/latest/)
  * [Community](/_/community.html)
  * [Case Studies](/_/case-studies.html)
  * [Resources](/_/resources.html)
  * [Blog](/_/blog.html)



![ASF](../../../../assets/img//feather-small.png)

[Foundation](http://www.apache.org/)

[Events](https://www.apache.org/events/current-event.html)

[License](https://www.apache.org/licenses/)

[Thanks](https://www.apache.org/foundation/thanks)

[Security](https://www.apache.org/security)

[Privacy](https://privacy.apache.org/policies/privacy-policy-public.html)

[Sponsorship](https://www.apache.org/foundation/sponsorship)

© 2009- [The Apache Software Foundation](https://apache.org) under the terms of the Apache License 2.0. Apache, the Apache feather logo, Apache Cassandra, Cassandra, and the Cassandra logo, are either registered trademarks or trademarks of The Apache Software Foundation.
