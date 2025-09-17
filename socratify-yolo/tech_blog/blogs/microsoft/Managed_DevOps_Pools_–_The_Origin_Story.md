---
title: "Managed DevOps Pools – The Origin Story"
author: "Unknown"
url: "https://devblogs.microsoft.com/engineering-at-microsoft/managed-devops-pools-the-origin-story/"
date: "2025-09-15"
---

Microsoft has over 100,000 software engineers working on software projects of all sizes. Some projects have thousands of engineers working in the same source repository, while others have thousands of individual repositories. Microsoft can be viewed as an organization of organizations due to its range of businesses: Operating systems, Cloud services, Devices, Games, Search, Office Productivity applications, Hardware, Developer applications/services, etc. Because of the range of businesses Microsoft is in, it has a unique challenge in the diversity of programming languages, build engines, test frameworks, operating systems and hardware infrastructure used inside Microsoft. Keeping those diverse engineering teams highly productive while meeting the ever-increasing scale and security demands is a challenge, and why the [One Engineering System (1ES)](https://azure.microsoft.com/en-us/solutions/devops/devops-at-microsoft/one-engineering-system/) organization inside Microsoft exists.

## The opportunity

In 2021, 1ES inventoried Microsoft’s Azure DevOps agents infrastructure and estimated that engineers had created over 5,000 self-hosted Azure DevOps pools with hundreds of thousands of agents. In Azure DevOps, [Microsoft-hosted agents](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops&tabs=yaml) are readily available for teams to use, but teams were unable to use them for all their scenarios. Sometimes, teams wanted larger SKUs, agents connected to private networks, their own images, stateful agents and run-long running tests. Larger teams each created their own tooling to scale and maintain the pools and had support processes in place if the pools ran into any issues. Medium-sized teams had created their own tooling, but they were at different levels of maturity depending on how much resources they could spend on their Engineering systems infrastructure. Smaller teams included engineers installing an agent in a VM or on a self-managed physical device. This system had many inefficiencies and challenges:

***Duplicate effort**: Different teams spent a significant amount of their dev cycles on engineering systems tooling building similar redundant systems. This is time they could have been spending on their primary charter of delivering features for their customers.
***Support & reliability**: Due to different teams having varying amount of dev cycles, some pools were well supported and while others had no support systems in place. When their agents were down, it took a while before they were fixed and their CI/CD pipelines were restored to normal functioning.
***Inefficient**: Some of the infrastructure tooling was missing basic cost saving features such as automated scaling. When utilization was low, they were paying for resources they weren’t using.
***Security Risk**: Some of the pools did not follow the best practices or install the recommended security monitoring tools. Some of the pools were manually maintained and not patched on time.
***Compliance**: Because of many different CI/CD infrastructure tools, practices and maturities, it was hard to audit compliance of the CI/CD infrastructure. It took a long time to get a baseline on audits and additional time for individual teams to implement identified compliance gaps.

## The solution

In addressing the complexities of teams managing their own infrastructure, 1ES developed an internal service known as 1ES Hosted Pools. This service accommodates the scenarios that teams required for Continuous Integration/Continuous Deployment (CI/CD) and tooling while unifying it all within a single solution. We worked with various teams in Microsoft to adopt 1ES Hosted Pools, the standard for custom CI/CD infrastructure using Azure DevOps inside of Microsoft. Key attributes of 1ES Hosted Pools that stand out include:

***Private Networking**: Teams can create pools that connect to resources on their private network, such as package registries, secret managers, and other on-premises services.
***Bring your own Image**: Teams can create pools with images that the team has created with pre-requisites that are unique to their scenario. They can use centrally maintained images as their base image.
***Business Continuity**: Teams can set up multiple backup pools and configure agents to be spun up in backup Azure regions when Azure might be having a rare outage in a single region.
***Stateful Agents**: By default, 1ES Hosted Pools are stateless and a new agent is created for every pipeline job. However, teams can choose to reuse the same agent in multiple jobs to improve performance of their pipelines because of not needing to re-download files or not needing to re-compute operations due to local cache hits. 1ES Hosted Pools implements best practices for stateful agents by auto-recycling agents based on time or the agent running out of disk space.
***Pick any SKU**: Azure offers a variety of compute families that are tailored for various workload characteristics. Teams can pick an Azure SKU family and a size that matches their workload’s unique core/memory/disk usage profile to make them more performant or cost effective.
***Standby Agents**: Teams can choose to make their pipelines start more quickly by deciding how many agents they want pre-warmed during different hours of a week or choose the “automatic” option that uses historical data to warm machines up.

## The benefits

Through Microsoft’s adoption of this internal standard, we achieved numerous benefits:

***Lower DevOps Bill**: Teams were able to reduce their CI/CD infrastructure bill by over 60% due to using historical data to improve machine utilization, moving to the most optimal Azure SKU for their workload and strategic use of Azure SPOT VMs. Many teams ended up shifting their testing left due to the extra machine hours they now had with the same DevOps budget.
***Quick Compliance**: Since teams were using a standard infrastructure, it was straight forward to determine if different services complied with compliance requirements due to the consistent telemetry from 1ES Hosted Pools. When the US presidential executive order for software development was released, teams already using 1ES Hosted Pools didn’t have to do much except to not use certain features considered non-compliant. This also enabled new compliance requirements to be implemented centrally.
***Efficient Dev Cycles**: Many teams that switched to 1ES Hosted Pools were able to spend more of their developers’ time on writing code because they were no longer maintaining or supporting their own custom team-specific infrastructure.
***Team Mobility**: In 2024, the number of self-hosted pools left at Microsoft dropped from 5,000+ to a few dozen pools. When developers moved from one team to another, they didn’t have to learn a new way to create/maintain their CI/CD infrastructure.
***Continuous Security Improvements**: 1ES Hosted Pools was able to apply security features to all existing pools or add advanced security features that teams can optionally leverage to raise their security bar further. Some of the features that were implemented were: Azure Confidential VMs, Trusted Launch, SecureTPM, etc.

## The external offering

1ES created an internal solution to quickly iterate and to prove the solution hypothesis that a HOBO (Host On Behalf Of) service can drastically reduce self-hosting and improve developer productivity.

With the internal success of 1ES Hosted Pools at Microsoft and requests from external customers navigating the same problems that Microsoft solved with 1ES Hosted Pools, the team decided to release the service as a third-party offering we’re calling Managed DevOps Pools(MDP). Microsoft customers can now achieve the gains that teams inside Microsoft realized with 1ES Hosted Pools. If you currently maintain VM Scaleset agents or self-hosted agents, you can switch to Managed DevOps Pools to leverage all the benefits it offers. Not all features of 1ES Hosted pools will be available in Managed DevOps Pools yet, but may be added in future releases.

You can read more about Managed DevOps Pools [here](https://devblogs.microsoft.com/devops/managed-devops-pools/).

* * *

Updated August 2, 2024: This article was published prior to publication of Managed DevOps Pools’ public preview details. The last paragraph has been updated to reflect the public preview information now available.
