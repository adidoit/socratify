---
title: "Building Dash: How RAG and AI agents help us meet the needs of businesses"
author: "Unknown"
url: "https://dropbox.tech/machine-learning/building-dash-rag-multi-step-ai-agents-business-users"
date: "2025-09-15"
---

Knowledge workers today face myriad challenges in managing their digital workflows. Information is often scattered across multiple applications and formats, and finding the right document, message, or piece of information can be both tedious and time-consuming. This fragmentation creates two major problems for businesses: it hinders collaboration and productivity, and it can lead to costly security issues.
To address these challenges, we launched [Dropbox Dash](https://www.dash.dropbox.com/), a universal search and knowledge management product that combines AI-powered features with in-depth content access control. Designed to help knowledge workers organize their digital lives, Dash allows users to find, organize, share, and secure content across their apps so they can focus on the work that matters most.
At its core, Dash is a universal search product powered by many machine learning technologies and supercharged by generative AI. It offers a powerful AI-driven search experience with advanced filtering capabilities that allow users to quickly locate the information they need, regardless of where it’s stored. With granular access controls, Dash also makes sure employees and external partners see only the right content so that sensitive company information isn’t surfaced unintentionally. And with advanced AI features, Dash can summarize, answer questions, surface insights, and generate drafts.
Throughout our development process, we experimented extensively and explored numerous solutions to build an AI product for businesses. In order to meet the challenges of modern work in data-intensive environments, we ultimately turned to retrieval-augmented generation (RAG) and AI agents. Additionally, we engineered a minimal Python interpreter focused exclusively on essential features required by our AI agents and supported by extensive testing and security reviews to ensure safe code execution.
In the following sections, we’ll dive into the specific challenges we faced while building Dash, the innovative solutions we developed to address them, and important lessons that’ll inform our work moving forward.
## Challenges in making an AI product that’s ready for businesses
Building an AI product like Dash presents a unique set of challenges that differ from those that developers typically encounter with consumer-facing applications. These challenges stem from the inherent complexities of business data environments, which are characterized by diversity, fragmentation, and multiple data modalities.
Understanding and addressing these challenges is crucial for delivering effective AI solutions that meet the sophisticated needs of business users. Before we dive into how we solved ‌these challenges, let’s first take a look at what each of these data environments entails.
### Data diversity
Data diversity refers to the wide range of data types that a business handles, including emails, documents, meeting notes, task management data, and more. Each type of data has its own structure and context, and that can complicate AI processing.
![](/cms/content/dam/dropbox/tech-blog/en-us/2025/april/building-dash-for-business/diagrams/updated/BuildingDfB-01.png/_jcr_content/renditions/BuildingDfB-01.webp)
Example of identifying the right data source, which requires domain knowledge and contextual information
Effectively managing diverse data types is critical because each type of data has its own structure and context. For Dash to perform well in a business setting, it must seamlessly process and understand all these different data types.
### Data fragmentation
Data fragmentation occurs when an organization’s data is spread across multiple applications. This means that relevant information isn’t stored in a single location, but is instead scattered across different tools and services.
Data fragmentation complicates the process of retrieving and synthesizing information. For users, this means context switching between multiple apps to manually search for the information they need, which is time-consuming, tedious, and inefficient. An AI system that can aggregate and make sense of fragmented data would greatly enhance the user experience by providing a unified and accessible information repository.
![](/cms/content/dam/dropbox/tech-blog/en-us/2025/april/building-dash-for-business/diagrams/updated/BuildingDfB-02.png/_jcr_content/renditions/BuildingDfB-02.webp)
Example of information spread across multiple apps, which requires combining fragmented information to construct a complete answer
### Data modalities
Data modalities refer to the different forms or modes in which data exists. Common modalities include text, images, audio, and video. Handling multiple data modalities is essential for providing a comprehensive AI solution.
Business users often deal with a mix of text documents, images, presentations, and videos, among other formats. An AI system that can process and integrate all these modalities can provide a more complete and accurate response to user queries.
![](/cms/content/dam/dropbox/tech-blog/en-us/2025/april/building-dash-for-business/diagrams/updated/BuildingDfB-03.png/_jcr_content/renditions/BuildingDfB-03.webp)
Example of information spread across multiple modalities
In summary, these challenges—data diversity, data fragmentation, and data modalities—present unique complexities when building these types of AI products. Addressing these challenges is essential to creating a robust and effective AI solution that meets the various needs of knowledge workers in dynamic and data-intensive environments. To pull this off, we implemented and experimented with multiple solutions. That’s where [r](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)[etrieval-](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)[a](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)[ugmented ](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)[g](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)[eneration](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) (RAG) and AI agents come in.
## Leveraging retrieval-augmented generation
When building Dash, we knew that delivering accurate and relevant responses to user queries was paramount. That’s why we turned to RAG, an industry-standard approach for tasks like query responses and summarization. RAG's ability to combine external information retrieval with state-of-the-art generative models makes it the perfect fit for our product, especially in the complex landscape of enterprise data.
RAG works by first retrieving the most relevant pieces of content from a dataset or knowledge base and then using a large language model (LLM) to generate a response based on that content. This approach ensures that the answers that the AI system provides aren’t only contextually relevant but also up to date, which is crucial in business environments where data is constantly evolving.
![](/cms/content/dam/dropbox/tech-blog/en-us/2025/april/building-dash-for-business/diagrams/BuildingDfB-04.png/_jcr_content/renditions/BuildingDfB-04.webp)
Retrieval-augmented generation (RAG)
### Choosing the right retrieval system
The retrieval system is the backbone of any RAG pipeline. It determines not just speed but also whether the LLM has the right context to generate meaningful answers—and a misstep here can compromise the entire user experience. Put another way, the retrieval system sets the bounds of what your LLM can “know” at inference time. It also greatly affects latency, which in turn impacts user satisfaction. And, it shapes the perceived quality of the final answer, since retrieval coverage can make or break correctness and completeness.
There are many options when it comes to designing a retrieval system. For question-answering systems, the most common one is to have a vector index where chunked data is indexed on their embeddings. Embeddings are simply a low-dimensional semantic representation of the chunk of data. To retrieve from such an index, [semantic search](https://dropbox.tech/machine-learning/selecting-model-semantic-search-dropbox-ai) is often used.
Another choice is to go with a more traditional approach to a search index, where documents are indexed by their lexical features (e.g., words that appear in the title or body). This approach, however, adds extra latency due to the need for on-the-fly chunking and re-ranking of the chunks during serving time.
There are many other options that prioritize data freshness, such as by directly interacting with the API for the platform where your data is stored, for example. But there are a few trade-offs to consider for each of these approaches:
***Latency vs. quality:**There’s a pervasive assumption that you can’t have both extremely low latency and high-quality results. Why? Because advanced or larger embedding-based semantic searches may take longer due to their complexity—whether that’s a heavier model or additional reranking steps. For example, if you want more than 95% of your requests to reliably complete in under 1–2 seconds, you might have to use smaller embedding models, which can reduce retrieval accuracy.
***Data freshness vs. scalability:**Many projects need to keep their data fresh—for instance, re-indexing a news site every few minutes. Frequent re-indexing processes can hinder system throughput or spike latency when they’re underway. Alternatively, on-the-fly API calls to third-party data can push latency well above a few seconds. If near-real-time information is crucial (e.g., updating stock quotes), your system might spend more resources on frequent indexing or caching, throttling your ability to scale.
***Budget vs. user experience:**High-quality solutions—advanced embeddings, re-ranking steps, and large-chunked indexes—often require additional compute, and more compute means more cost. If the user experience demands near-instant results with best-in-class recall, the resource burn can be significant. And if budgets are constrained, you might be forced to choose a simpler retrieval pipeline that could degrade the overall quality.
For Dash use cases, we prioritized reasonable latency but also high-quality and reasonable data freshness, with both periodic data syncs and the implementation of webhooks whenever appropriate. Specifically, we stayed under 1–2 seconds for over 95% of our queries, which allows us some latency budget for the rest of the pipeline so that our users don’t click away because the response time is too long.
Ultimately, we landed on a traditional information retrieval (IR) approach combined with on-the-fly chunking and reranking:
***Traditional IR:**We use a lexical-based system, along with smarter rerankers that use embedding features.
***On-the-fly chunking:**Documents are chunked at query time to ensure we’re pulling only the relevant sections.
***Reranking:**A larger, but still efficient, embedding model then re-sorts those results to place the most relevant chunks at the top.
In practice, this yields high-quality results in under 2 seconds for over 95% of our queries, balancing speed and relevance. The combination allows us to keep costs in check while avoiding the pitfalls of purely semantic or purely lexical retrieval.
Quality is best when measured end-to-end because all the parts of the RAG system need to work together effectively. Once we chose the retrieval system that best fit our needs, it was time to pick the best LLM for the job.
### Choosing the right model
To ensure this approach met our requirements, we conducted a rigorous evaluation. We tested multiple retrieval methods and model variations on several public datasets, including Google’s Natural Questions (featuring real user queries with large documents); MuSiQue (with multi-hop questions requiring information linking across different passages); and Microsoft’s Machine Reading Comprehension (containing often short passages and multi-document queries from Bing logs).
We also designed hand-tuned metrics to help evaluate the quality of generated answers. These included an LLM judge for answer correctness (passing retrieved evidence through an LLM to score final answer accuracy), an LLM judge for completeness (measuring the extent to which all relevant question aspects are addressed), as well as source precision, recall, and F1 metrics to evaluate how accurately we retrieved key passages needed for correct answers.
By cross-referencing these metrics, we could directly compare multiple open-source and closed-source LLMs in a consistent environment. This led us to narrow down a few model families that best suited Dash’s use cases.
Our RAG system remains model agnostic: We want to provide the flexibility of choosing the models and providers our customers are most comfortable with. Being model agnostic also allows us to be prepared to adapt to rapid developments in the field of LLMs.
Although RAG provides a solution for the most common types of questions—kinds that require fetching information from one or more documents—it’s incapable of performing complex, multi-step tasks. This is where AI agents come in.
## The role of AI agents
Imagine you’ve asked a colleague to help you with a complex task, such as, “What’s the progress on projects in my team’s Q1 OKRs?” This person would likely find the answer to this question by first breaking it down into individual steps before tackling those steps one at a time.
To handle the business challenges outlined above, we need an AI system that can approach complex tasks like humans do. These tasks may require domain knowledge, contextual information, and planning and executing multiple steps—and AI agents are exceptional at doing just that.
The term "AI agent" is often used loosely across the tech industry, and with various interpretations. However, there’s a common theme among all of them: an AI agent is a system that can autonomously perform tasks with very little to no human interaction.
At Dropbox, our interpretation of AI agents is more specific and aligned with the needs of business applications. We view AI agents as multi-step orchestration systems that can dynamically break down user queries into individual steps, execute those steps using available resources and information from the current user, and generate a final response—all while requiring minimal human oversight.
![](/cms/content/dam/dropbox/tech-blog/en-us/2025/april/building-dash-for-business/diagrams/BuildingDfB-1200x628_05.png/_jcr_content/renditions/BuildingDfB-1200x628_05.webp)
Agents as multi-step orchestration
The multi-step orchestration in our AI agents includes two stages: planning and execution.
### Stage 1: Planning
The planning stage involves breaking down a user's query into a sequence of high-level steps. This is done by an LLM, which interprets the query and generates simple code statements to express the logic of responding to the user’s query. The LLM-generated code is written in our domain-specific language (DSL), which is similar to the Python programming language. The initial plan of responding to the user’s query is restricted to high-level or simple code statements, which ensures clarity and precision in defining each step.
For example, let’s explore the request, "Show me the notes for tomorrow’s all-hands meeting." These steps contain the logic necessary to respond to the query:
1.**Resolve concrete dates and times for the phrase “tomorrow.”**There needs to be an established time window to identify what “tomorrow” is referring to. This must be done relative to the current date and time.
2.**Identify the meeting.**There needs to be a search conducted for a meeting with a title matching "all-hands" (and within the determined time window).
3.**Retrieve notes.**Documents attached to or linked from the identified meeting must be fetched.
The AI agent, however, expresses this logic as statements of code in our Python-like DSL. Below is a simplified version of what that’d look like:
Copy
time_window: TimeWindow = time_helper.get_time_window_for_tomorrow()
meeting: Meeting = meetings_helper.find_meeting(title="all-hands",
time_window=time_window)
notes: list[Document] = meetings_helper.get_attached_documents(meeting=meeting)
Each XXXX_helper object in the generated code contains functionality that acts as a building block for the LLM to use when expressing the logic of responding to the user’s query.
### Stage 2: Execution
The next step is to validate and execute the logic that was expressed as code. The code is validated through static analysis to ensure correctness, safety, and to detect missing functionality. We intentionally allow the LLM to assume that missing functionality exists. If missing functionality is identified, we use the LLM a second time to implement the missing code.
This two-stage approach to generating code allows the agents to be clear and focused with an overall plan, while also being adaptable to new types and variations of user queries. Below is a simplified version of what the result of each of the steps might look like:
1\.**Time window retrieval:**Resolve the relative phrase “tomorrow” to concrete values.
Copy
time_window: TimeWindow = time_helper.get_time_window_for_tomorrow()
# TimeWindow(start="2025-03-19", end="2025-03-20")
2\.**Meeting identification:**Search for the "all-hands" meeting within the resolved time window.
Copy
meeting: Meeting = meetings_helper.find_meeting(title="all-hands",
time_window=time_window)
# Meeting(title="Company All-Hands", start_time=..., attendees=...)
3\.**Document retrieval:**Finally, fetch the notes attached to the identified meeting.
Copy
notes: list[Document] = meetings_helper.get_attached_documents(meeting=meeting)
# [Document(title="All-Hands-Notes", content="...")]
The final response to the user’s query is the result of the last step. In this example, the list of documents will be returned to the user.
### Validation and testing
The interpreter we use to execute the LLM-generated code was developed from scratch here at Dropbox. This gave us full control over everything inside the interpreter, including integrating static analysis passes and “dry runs,” in addition to having run-time type enforcement.
Static analysis allows our interpreter to examine the code without executing it, helping us automatically identify potential security risks, missing functionality, or code correctness errors. Having run-time type enforcement helps ensure that the data and objects being operated on are the types of values that we expect. In our example, the list of documents returned to the user will _always_ be a list of documents.
Normally, testing LLM integrations can be an ever-moving target. As new model versions are released, slight changes in how things are phrased or reacted to can be expected. Knowing exactly why a test failed or why the final response differed from expectations is often challenging.
However, as a result of the LLM using code to express its logic in responding to the user, we’re able to make the LLM “show the work.” This helps with understanding at which step the logic failed, having more deterministic testing, and evaluating the response to a query. For example:
***Logic failure:**“Can’t answer this question” vs. “Error on step 3 when fetching attached documents to meeting…”
***More deterministic testing**: Does resolving “tomorrow” always return the correct time window?
***Evaluating responses**: “Does the response text have the approximate same meaning as what we expected?” vs. “Does the response value match the expected type list[Document]?”
### Security and efficiency
To address security concerns, we implemented security controls in our interpreter and its development process. Only the minimal required functionality is implemented in its runtime—feature parity with CPython isn’t the goal. This turns major security risks that exist in other full-featured interpreters into non-issues.
As we’ve explored, AI agents play a pivotal role in addressing the complexities of business tasks through their ability to plan and execute multi-step workflows autonomously. By leveraging LLMs and DSLs, these agents break down intricate queries into actionable steps, ensuring precision and efficiency. The structured approach, combined with strong typing and built-in security controls, enhances reliability and [mitigates security risks](https://assets.dropbox.com/www/en-us/business/solutions/solutions/dfb_security_whitepaper.pdf).
The future of AI agents in business environments is promising. And as we continue to refine and expand their capabilities, they’ll become indispensable in streamlining operations, enhancing productivity, and driving innovation.
## Lessons learned and future direction
Throughout our journey in developing business-ready AI solutions, we’ve learned several valuable lessons that have shaped our approach and informed our decisions. While AI agents excel at handling complex tasks through multi-step orchestration, RAG remains indispensable for simpler information retrieval tasks. The key is determining the appropriate tool for each scenario.
Our development of business AI solutions has forced us to adapt our approach to address data diversity, fragmentation, and modalities. We’ve had to innovate to make our solutions robust and scalable. We‘ve also observed that not all LLMs are equal: the same prompts can’t be used for different LLMs. This variability necessitates careful selection and optimization of prompts for LLMs to complete specific tasks.
Moreover, the trade-offs between model size, latency, and accuracy are real. While larger models may provide more precise results, they can introduce delays that may not align with user expectations. Understanding these trade-offs is crucial for delivering a good user experience.
Looking ahead, we’re excited to explore several promising directions that’ll further enhance our AI capabilities and drive innovation in knowledge management. Enabling AI agents to engage in multi-turn conversations will allow for more natural and intuitive interactions, mimicking human-like dialogue and improving the overall user experience. And developing self-reflective agents that can evaluate their own performance and adapt to new information will increase their autonomy and effectiveness, reducing the need for human intervention.
In addition, continuous fine-tuning of LLMs to align with specific business needs will enhance their relevance and accuracy, ensuring they meet the high standards of business environments. And lastly, expanding AI capabilities to support multiple languages will make our products more accessible and valuable to a global user base, fostering collaboration and productivity across diverse teams.
The integration of RAG and AI agents has significantly enhanced Dropbox Dash with AI capabilities to bring useful answers to users’ questions, and we’re focused on addressing challenges and exploring opportunities based on what we’ve learned. We’re also committed to our [AI principles](https://www.dropbox.com/ai-principles) and [being worthy of trust](https://trust.dropbox.com/?product=dash). By consistently innovating and refining our approach, we aim to develop products that meet the current needs of businesses and help move the future of knowledge work forward.
The landscape of business AI is evolving rapidly, and we’re excited about advancing AI capabilities to empower users to focus on truly meaningful, human work.
~ ~ ~
_If building innovative products, experiences, and infrastructure excites you, come build the future with us! Visit_[ _jobs.dropbox.com_](https://jobs.dropbox.com/) _to see our open roles, and follow @LifeInsideDropbox on_[ _Instagram_](https://www.instagram.com/lifeinsidedropbox/?hl=en) _and_[ _Facebook_](https://www.facebook.com/lifeinsidedropbox/) _to see what it's like to create a more enlightened way of working._
* * *
// Tags
* [ Machine Learning ](https://dropbox.tech/machine-learning)
* [LLM](https://dropbox.tech/tag-results.llm)
* [models](https://dropbox.tech/tag-results.models)
* [AI](https://dropbox.tech/tag-results.ai)
* [Dash](https://dropbox.tech/tag-results.dash)
* [Business](https://dropbox.tech/tag-results.business)
// Copy link
![Copy link](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/copy.svg)
