---
title: "Unlocking Financial Insights with Finch: Uber’s Conversational AI Data Agent"
author: "Unknown"
url: "https://www.uber.com/blog/unlocking-financial-insights-with-finch/"
published_date: "None"
downloaded_date: "2025-09-15T09:37:59.181953"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for Unlocking Financial Insights with Finch: Uber’s Conversational AI Data Agent](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/29486852321114e7a132o-17527100487267-scaled.jpg)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Funlocking-financial-insights-with-finch%2F&t=Unlocking+Financial+Insights+with+Finch%3A+Uber%E2%80%99s+Conversational+AI+Data+Agent)
  * [X social](https://twitter.com/share?text=Unlocking+Financial+Insights+with+Finch%3A+Uber%E2%80%99s+Conversational+AI+Data+Agent&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Funlocking-financial-insights-with-finch%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Funlocking-financial-insights-with-finch%2F)
  * [Envelope](mailto:?subject=Unlocking+Financial+Insights+with+Finch%3A+Uber%E2%80%99s+Conversational+AI+Data+Agent&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Funlocking-financial-insights-with-finch%2F)
  * Link

# Introduction
At Uber, financial analysts and accountants sift through vast data sets to support real-time decision-making. Traditional data access—often involving complex SQL queries across multiple platforms—creates delays that can impact critical financial insights. 
To address this, our team built Finch, an AI agent integrated directly into Slack®**.** Finch transforms natural language queries into structured data retrieval, delivering secure, real-time financial intelligence. This solution accelerates analysis and empowers finance teams to focus on strategy rather than troubleshooting data pipelines. This need to eliminate friction in data retrieval was the driving force behind Finch’s development.
* * *
## Motivation
We developed Finch to**** simplify and optimize the process of data retrieval for financial teams at Uber. During the development of Finch, the Uber FinTech team evaluated various technologies, and ultimately, we selected a combination of generative AI, RAG, and self-querying agents. Key factors that influenced this decision included ensuring data security, achieving seamless integration with existing systems, and maintaining scalability for future growth. By using these technologies, Finch empowers finance teams to access real-time, secure, and accurate financial insights directly within their Slack environment.
* * *
## The Problem: Traditional Data Access Is a Bottleneck
At Uber, financial analysts rely on data to make critical decisions. Yet, retrieving that data has historically been slow and inefficient. Financial Analysts like Taya often face multiple challenges when preparing reports.
  * **Manually searching for the right dataset**. Taya must log into multiple platforms like Presto®, IBM® Planning Analytics, Oracle® Enterprise Performance Management, and Google Docs™, unsure which system holds the most up-to-date figures. This back-and-forth creates delays and introduces room for error.
  * **Writing complex SQL queries**. If Taya is SQL-savvy and knows the table structure, she can attempt to write the query herself. But this often requires cross-referencing documentation, troubleshooting syntax errors, and ensuring all the necessary columns are included. Even for experienced analysts, this is time-consuming and prone to mistakes.
  * **Submitting a data request**. If the query is too complex or if Taya lacks the right permissions, she must submit a request to the Data Science team. This can mean waiting hours—or even days—for a response.

By the time her report is complete, valuable time has been lost, impacting decision-making and potentially delaying key business insights. This friction in traditional data access made it clear that a better solution was needed—one that could simplify data retrieval without compromising security or accuracy.
* * *
## The Solution: Finch as an Intelligent Financial Assistant
We developed Finch, an AI agent that streamlines financial data retrieval to address these challenges. Integrated directly into Slack, Finch allows finance teams to query data using natural language, removing the need for manual SQL queries or data requests. 
Finch is designed with several key capabilities that address common pain points:
  * **Conversational AI interface in Slack**. Users can ask, _“What was GB value in US &C in Q4 2024?”_ and Finch dynamically retrieves the correct data. 
  * **Uber-specific language understanding**. Finch maps internal finance terminology (like “US&C” → US and Canada region, “GBs” → gross bookings) to structured data sources. 
  * **Self-querying agents**. Finch searches through metadata about all accessible tables, considers the most relevant source to a user’s requests, and executes the correct SQL queries. 
  * **Security and access controls**. Built-in role-based permissions (RBAC) ensure that only authorized users can query sensitive financial data. 
  * **Automated data export to Google Sheets ™**. Finch can automatically export results into Google Sheets when retrieving large datasets, enabling users to analyze them seamlessly within their preferred workflow.

By combining natural language understanding, metadata-driven query generation, and secure data access, Finch reduces the complexity of financial data retrieval—giving analysts faster access to the information they need.
* * *
## Architecture
Finch’s architecture is built on a robust, modular framework designed to deliver financial insights with high accuracy. The solution uses a mix of internal and third-party technologies that integrate into Uber’s tech ecosystem.
What sets Finch apart is our approach to data retrieval: curated domain-specific data marts and a semantic layer on metadata. Finch relies on a curated set of single-table data marts that consolidate frequently accessed financial and operational metrics to maximize efficiency and accuracy. These datasets are optimized for simplicity. They’re structured to minimize query complexity and retrieval time, making it easier for the LLM to write a query and quickly get feedback, like error messages, so it can take action and correct its mistakes. The datasets are also structured and governed. Controlled access ensures only authorized users can query specific financial dimensions.
Finch dramatically improves the accuracy of WHERE clause filters by storing natural language aliases for both SQL table columns and their values in our OpenSearch™ index. This is a significant enhancement over traditional methods used by LLM-powered SQL agents that rely solely on table schemas and a few sample rows.
###   
Key Components and Technologies
Finch accesses a wide array of self-hosted and third-party large language models via Uber’s Generative AI Gateway. This approach allows us to swap out models easily as the underlying AI technology advances.
We use LangChain Langgraph™ to construct and orchestrate our agents. It coordinates the flow of queries between specialized agents (like the SQL Writer Agent and Supervisor Agent) and ensures that each task is executed in the proper sequence.
Finch uses an OpenSearch index to store dataset metadata, including SQL table columns, values, and natural language aliases. This novel approach allows for fuzzy matching of terms extracted by the LLM. Consequently, Finch achieves significantly improved reliability in generating accurate WHERE clause filters compared to conventional methods.
Using the Slack SDK, Finch connects directly to Slack via API. A dedicated callback handler in our Langgraph application updates Slack status messages in real-time so users can track what the agent is doing at every stage of the query process. We also leverage the recently released Slack AI Assistant APIs, which enable suggested questions at the start of a new conversation, the ability to pin Finch within the Slack application, and an always-open split pane to talk with Finch. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/figure-1-illustration-of-system-integrations-17527071535702-892x1024.png)_Figure 1: System integrations._
### Finch Data Agent Flow
Here’s the flow of the Finch data agent. 
  1. **User query input.** A finance team member asks Finch a question in Slack.
  2. **Agent orchestration.** The Supervisor Agent receives the query and sends it to an appropriate sub-agent, such as the SQL Writer Agent. The appropriate agents are selected based on the nature of the query.
  3. **Metadata retrieval.** The appropriate agents can query the OpenSearch index to fetch relevant metadata, including natural language aliases for both column names and values. This enhances the LLM’s ability to construct precise SQL queries.
  4. **SQL query construction and execution.** The SQL Writer Agent dynamically builds the query using the retrieved metadata and executes it against the appropriate data source.
  5. **Real-time feedback via Slack.** Throughout the process, a Slack callback handler updates the user’s Slack status with real-time messages describing each operation step, such as when the agent makes tool calls.
  6. **Result delivery.** Once the query is executed, the results are formatted and delivered back to Slack in a clear, actionable format, with details on the executed query and a link to a Google Sheet with the query results.

* * *
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/figure-2-illustration-of-finch-data-agent-context-building-flow-17527074161268-1024x580.png)_Figure 2: Finch data agent context-building flow._
### Integration with Uber’s Tech Stack
Finch is designed to work in harmony with Uber’s broader tech stack. It integrates with internal data platforms (such as Presto, IBM Planning Analytics, and Oracle EPM) and leverages internal services like the Generative AI Gateway. This integration ensures that Finch meets stringent data security and scalability requirements as well as delivers consistent, real-time insights to finance teams across the organization.
* * *
## How Finch Works: A User Journey
Finch is designed to integrate seamlessly into Slack, where Uber’s finance teams already collaborate. Instead of logging into multiple systems, users can ask questions in plain English, just like messaging a colleague.
For example, while preparing a report, Taya types in Slack, _“Show me the Q4 2024 GBs value.”_
As shown in ‌Figure 3, Finch performs a number of steps, which can vary from question to question.  

  1. **Supervisor agent intent routing**. The Supervisor Agent determines that this is a data retrieval request and routes it to the SQL Writer Agent.
  2. **Data retrieval**. The SQL Writer Agent: 
     * Identifies the correct table by looking up words or phrases it thinks could refer to a column or WHERE clause filter value.
     * Follows look-up table-specific instructions with details on caveats or nuances. 
     * Constructs the necessary SQL query to retrieve the values.
     * Validates Taya’s security permissions before executing the query.
     * If an error occurs, the agent rewrites the query considering the error message.
  3. **Slack response**. Within seconds, Finch posts a structured response with a summary and breakdown table. For example, _“The Gross Bookings (GBs) value for Q4 2024 is approximately $44,197.28M USD.”_  

* * *
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/figure-3-illustration-of-how-a-user-interacts-with-finch-in-the-slack-environment-17527074983092.png)_Figure 3: How a user interacts with Finch in the Slack environment._
  4. **Follow-up and refinement**. Taya needs to see how it compares to the previous year and replies,_“Compare to Q4 2023”._

As shown in Figure 4, Finch updates the query, fetching the data from Q4 2023 and summarizing the trend (increase), presents it in Slack, and offers an option to export to Google Sheets.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/figure-4-illustration-of-how-finch-updates-the-query-based-on-a-follow-up-prompt-from-a-user-17527075514532.png)_Figure 4: How Finch updates the query based on a follow-up prompt from a user._
Finch revolutionizes how Uber’s finance teams access data through conversational retrieval, leading to less friction, fewer delays, and faster data-driven decisions.
* * *
## Performance and Accuracy: Ensuring Reliable Insights
Finch is built to deliver fast, accurate, and reliable financial insights at scale. To achieve this, it undergoes rigorous performance testing and continuous optimization.
### **Continuous Evaluation & Benchmarking**
To maintain high accuracy and efficiency, Finch employs:
  * **Agent accuracy evaluation.** Each sub-agent (SQL Writer, Document Reader) is independently evaluated against a set of expected responses. Specifically for data retrieval agents, like the SQL Writer Agent, the results of the generated query are compared to those of the “golden” query, since there are many ways to write a query. Still, we want to ensure the final output is correct.
  * **Supervisor agent routing accuracy.** This identifies issues with intent collisions, where the supervisor makes the wrong choice when the question is ambiguous or tools have similar capabilities (for example, data retrieval tools for Presto and Oracle EPM pull data for different use cases).
  * **End-to-end validation.** Simulated real-world queries ensure system-wide reliability.
  * **Regression testing.** Historical queries are re-run to detect accuracy drifts before updates are deployed for system prompts or model changes.

This iterative approach ensures that Finch delivers correct financial insights and maintains consistency as new improvements are introduced.
###   
**Optimizing for Speed and Scalability**
Finch is designed to handle high-demand queries efficiently. Finch minimizes database load by optimizing SQL queries. Sub-agents execute tasks simultaneously, reducing response time. Lastly, Finch pre-fetching frequently accessed metrics enhances performance.
Finch continuously improves its accuracy and speed, ensuring that finance teams receive real-time insights with minimal latency and maximum reliability.
* * *
## How Finch Stands Out from Other AI Finance Tools
Finch is specifically designed to meet the needs of Uber’s finance teams, offering real-time, AI-powered financial insights with built-in security, automation, and scalability. As shown in Figure 5, unlike generic AI chatbots or traditional BI tools, Finch combines structured data retrieval, intelligent self-querying, and enterprise-grade access controls.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/figure-5-table-depicting-how-finch-compares-to-other-tools-17527076318297-1024x502.png)_Figure 5: How Finch compares to other tools._
Finch’s key differentiators are: 
  * **Live financial data queries**. Finch dynamically retrieves up-to-date financial data, whereas traditional AI chatbots rely on pre-trained knowledge.
  * **AI-powered self-querying**. Unlike BI tools that require manual SQL input or predefined reports, Finch automatically determines the best query strategy.
  * **Embedded in daily workflows**. Finch integrates with Slack on a desktop or ‌mobile device. This allows finance teams to access data where they work rather than switching between tools, making it perfect for even non-SQL-savvy executives.
  * **Advanced security and compliance**. Unlike standard AI solutions, Finch enforces enterprise authentication, granular permissions, and query validation to ensure data security.

* * *
## Future Roadmap
Finch continuously evolves to provide deeper insights and improved efficiency for Uber’s finance teams. 
One area of planned improvement is to expand integrations with Uber FinTech systems. This will offer a more unified and interactive finance ecosystem for automated financial analysis, reporting, forecasting, and budgeting.
Another area of improvement is to support the executive leadership user experience. Executive leaders like Dara (Uber CEO) and Prashanth (Uber CFO) need fast and accurate data for decision-making. While Finch is good enough for day-to-day operations for most Finance teams at Uber, like all generative AI technologies at this point, it’s not 100% reliable and is prone to hallucination. Beyond our ongoing focus on improving accuracy, we also want to integrate human-in-the-loop validation upon request for our leaders. For example, Finch will have a button next to its response for “Request validation,” which will send the context and Finch-generated response to one of our subject matter experts to verify or correct the response. Once that expert ensures the answer is correct, Finch will inform the leader. This “on-demand” human-in-the-loop will allow leaders to use Finch freely without including a human for less critical questions. Still, having a human verify accuracy will allow them to use Finch confidently for critical questions.
We also want to update Finch to handle more user intents with more agents and toolkits. Our goal is to make Finch a one-stop-shop for Finance users at Uber, so we’re continuing to build more agents and agent toolkits to address those needs. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/figure-6-illustration-of-finchs-intent-flow-future-state-17527077548179-1024x969.png)_Figure 6: Finch’s intent flow future state._
* * *
# Conclusion
Finch is transforming how Uber’s finance teams interact with data, making financial insights more accessible, secure, and real-time. By combining generative AI, self-querying agents, and enterprise-grade security, Finch eliminates the inefficiencies of traditional data retrieval, empowering teams to focus on strategy rather than SQL.
As Finch continues to evolve, its capabilities will expand to deliver even more personalized financial insights. The future of financial intelligence at Uber is here, and Finch is at the forefront.
With Finch, we aren’t just answering questions, we’re reshaping financial decision-making one query at a time.
_Cover Photo Attribution: “_[ _-‘You crunch the numbers, I’ll crunch the birdseed’_](https://www.flickr.com/photos/17333088@N00/2948685232) _” by_[ _JunCTionS_](https://www.flickr.com/photos/17333088@N00) _is licensed under_[ _CC BY 2.0_](https://creativecommons.org/licenses/by/2.0/?ref=openverse) _._
_IBM ®, IBM Planning Analytics, the IBM logo, and ibm.com® are trademarks or registered trademarks of International Business Machines Corporation, in the United States and/or other countries._
_Oracle ®, Oracle EPM, Java, MySQL, and NetSuite are registered trademarks of Oracle and/or its affiliates. Other names may be trademarks of their respective owners._
_OpenSearch ™ is a trademark of LF Projects, LLC. _
_Google Docs ™ and Google Sheets™ are trademarks of Google LLC and this blog post is not endorsed by or affiliated with Google in any way._
_LangGraph ™ is a trademark of LangChain Inc.._
_Presto ® is a registered trademark of LF Projects, LLC._
_Slack ® is a registered trademark and service mark of Slack Technologies, Inc._
Stay up to date with the latest from Uber Engineering—follow us on [LinkedIn](https://p.uber.com/eng-linkedin) for our newest blog posts and insights.
* * *
![Austin Harrison](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/austin-harrison-headshot-17527078974077.png)
Austin Harrison
Austin Harrison is the Director of Finance Data Analytics &amp; AI in Uber’s FinTech division, where he drives the application of advanced data analysis, machine learning, and generative AI. His work enables the Finance team to conduct in-depth, trip-level analyses, transforming how data is leveraged for decision-making.
![Eddie Huang](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/eddie-huang-headshot-17527081025614.png)
Eddie Huang
Eddie Huang is a Business System Manager at Uber FinTech, managing data pipelines for Finance and Accounting while leveraging Generative AI to simplify data access for teams.
![Spencer Garth](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/spencer-garth-headshot-17527082004101-e1752708245296.png)
Spencer Garth
Spencer Garth is a FinTech Software Engineer at Uber, focusing on AI-driven financial data solutions and integrating LLMs into finance and data engineering workflows.
![Tim Ross](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/tim-ross-headshot-17527083809716.png)
Tim Ross
Tim Ross is a Lead Product Manager at Uber, dedicated to helping teams harness AI to work more efficiently with data. He builds and manages financial data systems and is excited to create AI-powered products like Finch on top of them.
![Taya Yusuf](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/taya-yusuf-headshot-17527085337512.png)
Taya Yusuf
Taya Yusuf is a Senior Product Manager at Uber FinTech, building tools that simplify and streamline financial processes and improve efficiency through automation.
* * *
Posted by Austin Harrison, Eddie Huang, Spencer Garth, Tim Ross, Taya Yusuf 
Category:
[Engineering](/en-CA/blog/engineering/)
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
[English](/en-CA/blog/unlocking-financial-insights-with-finch/)
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
[English](/en-CA/blog/unlocking-financial-insights-with-finch/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
