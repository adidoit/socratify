---
title: "Developer Experience at Pinterest: The Journey to PinConsole"
author: "https://medium.com/@Pinterest_Engineering"
url: "https://medium.com/pinterest-engineering/developer-experience-at-pinterest-the-journey-to-pinconsole-b34ac9e3bdd9?source=rss----4c5a5f6279b6---4"
date: "2025-09-15"
---

#**Developer Experience at Pinterest: The Journey to PinConsole**
[![Pinterest Engineering](https://miro.medium.com/v2/resize:fill:64:64/1*iAV-apeVpCJ1h6Znt1AzCg.jpeg)](/@Pinterest_Engineering?source=post_page---byline--b34ac9e3bdd9---------------------------------------)
[Pinterest Engineering](/@Pinterest_Engineering?source=post_page---byline--b34ac9e3bdd9---------------------------------------)
13 min read
·
Aug 22, 2025
[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fpinterest-engineering%2Fb34ac9e3bdd9&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fdeveloper-experience-at-pinterest-the-journey-to-pinconsole-b34ac9e3bdd9&user=Pinterest+Engineering&userId=ef81ef829bcb&source=---header_actions--b34ac9e3bdd9---------------------clap_footer------------------)
\--
2
[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fb34ac9e3bdd9&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fdeveloper-experience-at-pinterest-the-journey-to-pinconsole-b34ac9e3bdd9&source=---header_actions--b34ac9e3bdd9---------------------bookmark_footer------------------)
Listen
Share
Authors: Ashlin Jones, Engineering Manager; Haniel Martino, Software Engineer; Su Rong, Software Engineer; Viktoria Czaran, Software Engineer
At Pinterest, our mission is to bring everyone the inspiration to create a life they love. This ambitious goal is powered by a complex technological ecosystem managed by thousands of engineers who develop and maintain services to support over 550 million monthly active users¹.
As Pinterest evolved to a platform serving hundreds of millions of users, we faced a critical question: How do we maintain engineering velocity while managing increasing technological complexity? The answer led us to reimagine our developer experience through an Internal Developer Platform — PinConsole, our unified developer portal built on [Backstage](https://github.com/backstage/backstage).
## The Strategic Case for Internal Developer Platforms
Internal Developer Platforms represent a fundamental shift in how engineering organizations scale beyond organic tool growth. At Pinterest’s scale, we reached a critical inflection point where our historically successful approach of decentralized tool adoption began creating organizational bottlenecks rather than eliminating friction.
When Pinterest was a younger company, each team solved immediate problems by adopting or building tools that worked for their specific context. This organic approach enabled rapid innovation and helped us scale from startup to platform. However, at a certain organizational threshold, this same approach creates exponential complexity where new engineers face an overwhelming landscape of tools, tribal knowledge becomes critical for productivity, and cognitive overhead begins consuming more engineering time than actual development work.
An Internal Developer Platform (IDP) addresses this challenge by creating a consistent abstraction layer that allows engineers to focus on business logic rather than infrastructure complexity. Unlike tool consolidation, which simply reduces the number of interfaces, a platform approach enables self-service capabilities and multiplies the effectiveness of engineering investments.
##**The Developer Experience Challenge: Understanding the Problem**
Our engineering velocity survey revealed patterns that indicated we had crossed the complexity threshold, where organic tool growth was hindering rather than helping productivity.
**Inconsistent Workflows and Tool Fragmentation:**We identified over 20 different internal tools that engineers needed to navigate daily, with multiple tools serving similar purposes but with different interfaces and workflows. Engineers consistently reported confusion about recommended approaches, with one engineer noting, “There are various, inconsistent ways to do the same thing, and the recommended or right way is hard to uncover.”
**Tool Discovery and Context Switching:**Survey responses highlighted that engineers were spending substantial portions of their time navigating between different tools and searching for information. Multiple engineers mentioned that context switching between disparate interfaces was a major productivity drain that interrupted their development flow.
**Fragmented Information and Knowledge Sharing:**Documentation was scattered across multiple systems including Google Docs, Wiki, and GitHub READMEs, making it difficult to find authoritative sources of information. Engineers consistently reported spending significant time searching for answers to questions that had already been solved elsewhere in the organization.
The pattern emerging from our research was clear: Pinterest had reached the scale where organic tool growth was creating cognitive overhead that outweighed the benefits of specialized tooling. This represented a strategic inflection point requiring platform thinking rather than continued tool proliferation.
## Evaluating Solutions: The Platform vs. Tools Decision
When tasked with solving this problem, we conducted a comprehensive evaluation that focused not just on immediate pain relief but on long-term platform strategy.
**Option 1: Continue with existing fragmented ecosystem**
* No upfront investment required
* Continued productivity degradation as organization scales
* Growing technical debt and onboarding complexity
**Option 2: Build a completely custom Internal Developer Platform**
* Full control over features and integration
* Estimated 24–36 month development timeline
* Significant engineering resources required with ongoing maintenance burden
**Option 3: Leverage existing open-source platforms for IDP foundation**
* Faster time to value with 6–8 months to initial deployment
* Community support and ability to leverage established platform patterns
* Ability to customize for Pinterest-specific needs while maintaining upgrade path
**Option 4: Purchase an Internal Developer Platform from a vendor**
* As a SaaS solution, there is no infrastructure overhead
* Fast time to use, just implement the integrations to provide our data and the service would be running
* Limited customization capabilities may lead to gaps with Pinterest-specific needs
* Higher costs, especially as usage scales or customization requests grow
* Risk of increased friction if the platform does not adapt well to evolving requirements
The strategic decision centered on whether to invest in platform infrastructure or continue managing tool complexity. We chose to build an Internal Developer Platform using open-source foundations because it aligned with our need to create consistent abstractions while maintaining development velocity.
## Why Backstage for Our IDP Foundation
After evaluating multiple open-source platform solutions, we chose Backstage for several reasons that aligned with our platform strategy:
**Community Adoption and Patterns:**Over 100 publicly listed companies were using Backstage. We consulted with peer companies to learn from their platform implementations. This provided confidence in the architectural patterns and long-term viability.
**Plugin Architecture for Platform Extension:**Backstage’s extensible plugin model aligned perfectly with our need to integrate existing Pinterest tools while providing a consistent developer experience. This architecture enables the platform thinking we need rather than simple tool aggregation.
**Active Development and Long-term Support:**The project had strong backing from Spotify and the CNCF, ensuring long-term support and continued platform evolution.
## PinConsole Architecture: Building Beyond Basic Backstage
PinConsole represents our customized implementation of Backstage that extends the platform to meet Pinterest’s unique requirements. Our architecture demonstrates how to build an IDP that provides consistent abstractions while integrating with existing organizational systems.
Press enter or click to view image in full size
**Authentication Layer:**We integrated PinConsole with Pinterest’s internal OAuth system and LDAP for authentication. This required developing custom authentication resolvers to map Pinterest’s identity model to Backstage’s user entities. The integration flow maintains security while providing seamless access:
* Incoming unauthenticated users are redirected to Pinterest’s internal oauth provider
* After successful authentication, user details are passed via HTTP headers
* Custom resolvers match these details against user entities loaded in PinConsole
* The resolved identity enables personalization and access control
**Entity Data Model:**We developed a comprehensive entity model that integrates with our existing LDAP directory through Backstage’s ldapOrg provider. This automatic synchronization ensures that user and group information remains current, enabling platform features like accurate ownership tracking, team-based views of components and services, and fine-grained access control based on group membership.
The entity model synchronizes every 60 minutes, pulling approximately 9,000 user entities and 2,200 group entities from our LDAP directory, providing the foundation for the unified data model that makes IDPs effective.
**Database and Storage Architecture:**PinConsole uses PostgreSQL databases for both production and staging environments, hosted on AWS RDS instances. We implemented logical database separation to maintain plugin isolation while enabling cross-plugin data relationships:
* backstage_plugin_auth: Stores authentication-related data
* backstage_plugin_catalog: Stores entity data synchronized from LDAP and from our existing software catalog system
* Plugin-specific databases: Each plugin maintains its own logical database for isolation
**UI Customization and Design System Integration:**Rather than using Backstage’s default Material UI components, we themed the interface using Pinterest’s [Gestalt](https://gestalt.pinterest.systems/home) design system. This ensures consistency with our other internal tools and reinforces the platform experience rather than introducing yet another interface paradigm. This required developing a custom theme provider and component overrides while maintaining compatibility with Backstage’s plugin architecture.
## The PinCompute Plugin: A Case Study in Platform Integration
One of our first and most impactful plugins is the PinCompute plugin, which provides a unified interface for managing PinCompute (Kubernetes) workloads. This plugin demonstrates how IDPs can integrate complex infrastructure functionality while simplifying the developer experience through consistent abstractions.
**Why a Custom Kubernetes Plugin?**While Backstage offers a built-in Kubernetes plugin, we built a custom PinCompute plugin for several platform-specific reasons:
**Custom Resource Definitions Integration:**Pinterest’s PinCompute environment extensively uses custom resources (CRDs) like PinApps and PinScalers that represent our platform abstractions with varying functionality and behaviors. These aren’t supported by the standard plugin and are essential to our developer experience.
**Multi-tenancy and Access Control:**Our multi-tenant platform requires fine-grained access controls that integrate with our existing security systems — something that couldn’t be easily implemented with the standard plugin architecture.
**Integration with Pinterest Infrastructure:**We needed seamless integration with our security systems, service registry, and artifact repositories to provide the unified experience that defines effective IDPs(see the illustrations below for a general layout). We expose project owner’s cost, provide debugging terminals (Terminal), and emit platform audit logs (Insights) to enrich service owners development and deployment experience.
**Managed Platform:**PinCompute is a platform-as-a-service with a facade layer that abstracts away the complexity of managing Kubernetes clusters. By providing this lightweight facade layer, PinCompute seamlessly manages user services across multiple clusters and accounts, reducing operational complexity and ensuring scalable, reliable, and efficient infrastructure for service owners.
Press enter or click to view image in full size
Press enter or click to view image in full size
Press enter or click to view image in full size
Press enter or click to view image in full size
**Technical Implementation:**The PinCompute plugin interacts with our Kubernetes clusters through a dedicated API service (PinCompute API) rather than direct cluster access. This architecture pattern ensures proper authentication and authorization through our FGAC policy system, provides a caching layer to reduce load on the Kubernetes API server, and enables cross-cluster aggregation for a unified view of a service owner’s project resources.
The plugin is implemented as a React application that communicates with PinCompute APIs to retrieve information and perform actions on resources, demonstrating the consistent interface patterns that make IDPs effective.
Press enter or click to view image in full size
## Homepage Widgets: Personalizing the Platform Experience
To make PinConsole immediately valuable to engineers, we developed personalized homepage widgets that integrate with tools they use daily. These widgets originated from a hackathon project and demonstrate how IDPs can reduce context switching while providing personalized experiences.
Press enter or click to view image in full size
**GitHub Integration:**The GitHub widget provides real-time visibility into pull requests that need attention, including open PRs created by the engineer, PRs where the engineer is requested as a reviewer, and status information including build/check status and review status. This integration uses GitHub’s GraphQL API to retrieve and display PR data, with customized caching to minimize API calls while keeping information current.
**Find Any Commit**: This feature set is an extension on the GitHub widget that allows developers to track their PRs post merge. Since Pinterest has many services that deploy at their own cadences, this tool is extremely useful for engineers when determining where their code is in the deployment lifecycle. This feature supports both of Pinterest’s primary service deployment platforms, and it was recently extended to support tracking mobile releases.
**Jira Integration:**The Jira widget shows the engineer’s open issues, allowing them to view and filter their assigned tasks, track progress on work items, and see due dates and priority information. This integration reduces the need to context switch between PinConsole and Jira, contributing to the unified developer experience that IDPs aims to create.
**Observability Integration:**The Statsboard widget shows recently viewed monitoring dashboards, enabling engineers to quickly access metrics for services they’re responsible for. This enhances observability of their systems within the unified platform interface. To further reduce friction, this widget pops up a drawer with those dashboards within the same UI.
**PagerDuty Integration:**The PagerDuty widget provides engineers immediate access to incident information directly in PinConsole. Engineers can quickly view recent and ongoing incidents, monitor their current on-call status, and see upcoming on-call schedules at a glance.
## Performance and Scalability: Platform Engineering Considerations
To ensure PinConsole provides a responsive experience that scales with Pinterest’s engineering organization, we implemented several performance optimizations that are essential for adoption.
**Data Prefetching and Caching:**We use Apollo Client’s cache policies to prefetch commonly accessed data, significantly reducing perceived latency for common workflows. This is critical for platform adoption since slow performance can undermine the productivity benefits that justify IDP investments.
**Code Splitting and Optimization:**[React.lazy](https://github.com/Merri/react-lazy) and [Suspense](https://github.com/kentcdodds/react-suspense) are used to split the application into smaller chunks, resulting in substantial improvements to initial bundle size and time-to-interactive metrics. These optimizations are essential for a platform that engineers use throughout their workday.
**Server-Side Rendering:**Critical pages are server-side rendered, improving time-to-first-meaningful-paint. This ensures that the platform feels responsive even as it grows in functionality and user base.
**Multi-level Caching Strategy:**We implemented caching at multiple levels including CDN caching for static assets, API gateway caching for frequently requested data, and database query caching for common queries. These optimizations maintain consistent sub-500ms response times for dashboard components, even as user adoption has grown significantly.
## Adoption and Results: Measuring Platform Success
PinConsole launched as a beta and has seen substantial adoption across the engineering organization, demonstrating the value that IDPs can provide when implemented thoughtfully.
Press enter or click to view image in full size
**User Adoption Patterns:**Daily Active Users have grown substantially from initial pilot users to over 700 engineers. Approximately 30% of Pinterest engineers are now Monthly Active Users. Average session duration has increased significantly as engineers find more value in the unified platform experience.
**User Satisfaction and Feedback:**Net Promoter Score of >70 places PinConsole in the top tier of internal tools. Engineers consider PinConsole important to their daily workflow.
One staff engineer commented: “PinConsole has changed how I work. I used to have a dozen bookmarks for different tools and dashboards. Now everything I need is in one place, with a consistent interface. It’s cut significant overhead from my day.”
**Platform Impact Indicators:**The adoption patterns and user feedback indicate that PinConsole is successfully addressing the core problems that Internal Developer Platforms are designed to solve: reducing cognitive load, improving discoverability, and enabling self-service capabilities.
## Lessons Learned: Building Effective IDPs
Building and rolling out PinConsole taught us several valuable lessons that may benefit other organizations undertaking similar platform initiatives.
**Start With High-Value Integrations:**We initially focused on integrating the tools that engineers use most frequently including GitHub, Jira, Statsboard, PagerDuty, and PinCompute. This approach delivered immediate value and drove adoption, creating momentum for further development. Platform success depends on demonstrating value quickly rather than building comprehensive functionality before launch.
**Invest in Integration APIs and Standards:**We developed a standardized approach for tool integration, making it easier to add new tools over time. This investment in platform infrastructure has enabled us to add new integrations with substantially less development time compared to our initial integrations.
**Customize Thoughtfully While Maintaining Upgrade Path:**While we customized Backstage significantly, we were careful to maintain compatibility with upstream changes. This approach allows us to benefit from community development while still meeting our specific needs, which is essential for long-term platform sustainability.
**Focus on Performance Before Wide Rollout:**Early feedback highlighted that slow performance would hinder adoption regardless of functionality. By investing in performance optimization before wide rollout, we ensured a positive first impression and higher retention, which is critical for platform success.
**Address Common Platform Objections Proactively:**We encountered predictable resistance including “Why not just use existing tools?” and “How do you prevent the platform from becoming another silo?” Addressing these concerns through demonstration and clear communication about platform benefits was essential for organizational buy-in.
## Looking Ahead: The PinConsole Platform Roadmap
While we’ve made significant progress with PinConsole, our platform journey continues to evolve. Looking ahead, we’re focused on several key initiatives that demonstrate the ongoing value of Platform thinking.
**Unified Data Model:**We’re developing a comprehensive data model that will provide a complete view of all software components at Pinterest, including their relationships and dependencies. This will enable platform features like impact analysis for changes, dependency visualization, and comprehensive ownership tracking that would be impossible with fragmented tooling.
**Software Catalog:**Our Software Catalog will be expanded to include more types of software components with enriched metadata, improving discoverability and understanding of our complex technical ecosystem. This represents the evolution from tool integration to true platform capabilities.
**End-to-End Capacity Management:**We’re building capabilities for engineers to easily predict, request, and manage infrastructure capacity throughout the application lifecycle, streamlining resource allocation and optimizing utilization through self-service platform capabilities.
**Advanced Observability Integration:**We’re developing deeper integrations with our observability stack, enabling engineers to quickly identify and resolve issues from a single interface while maintaining the unified experience that defines effective IDPs.
## Conclusion: The Strategic Value of IDPs
PinConsole represents a significant step forward in our mission to create a world-class developer experience at Pinterest. By providing a unified, personalized platform for our engineers, we’re reducing cognitive load, improving productivity, and enabling faster innovation through consistent abstractions rather than tool proliferation.
The journey has reinforced our belief that investing in Internal Developer Platform capabilities is critical for scaling engineering organizations effectively. Even modest improvements in developer productivity across large engineering organizations translate to substantial organizational capacity gains, representing significant return on platform investment.
As we continue to evolve PinConsole, we’re committed to listening to our engineers and adapting to their needs. The platform will grow alongside Pinterest, enabling us to deliver on our mission to bring everyone the inspiration to create a life they love while maintaining engineering velocity at scale.
The transition from organic tool growth to platform thinking represents a fundamental shift in how we approach developer experience. PinConsole demonstrates that IDPs can successfully bridge the gap between organizational complexity and individual productivity, providing a foundation for continued innovation as Pinterest continues to scale.
## Acknowledgements
We would like to thank the following individuals who contributed to the development and success of PinConsole:
Alvaro Mauricio Ortiz Rodriguez, Anika Mukherji, Anthony Suarez, Brian Overstreet, Daniel Sera, David Westbrook, Eric Kalkanger, George Yiu, Haniel Martino, Howard Nguyen, James Fish, Jiajun Wang, Karthik Anantha Padmanabhan, Lise Statelman, Marcus Oliveira, Mitch Goodman, Molly Junck, Qi Shu, Robson Braga, Sahil Puri, Sanson Hu, Sara Abdelmottaleb, Sekou Doumbouya, Svetlana Vaz Menezes Pereira, Yaonan Huang, Zhihuang Chen
¹ <https://business.pinterest.com/en-gb/audience/>
