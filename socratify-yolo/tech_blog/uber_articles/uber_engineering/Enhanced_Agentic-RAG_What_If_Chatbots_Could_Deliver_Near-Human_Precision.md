---
title: "Enhanced Agentic-RAG: What If Chatbots Could Deliver Near-Human Precision?"
author: "Unknown"
url: "https://www.uber.com/blog/enhanced-agentic-rag/"
published_date: "None"
downloaded_date: "2025-09-15T09:38:10.756327"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for Enhanced Agentic-RAG: What If Chatbots Could Deliver Near-Human Precision?](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/cover-17484716129443-1024x683.jpg)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fenhanced-agentic-rag%2F&t=Enhanced+Agentic-RAG%3A+What+If+Chatbots+Could+Deliver+Near-Human+Precision%3F)
  * [X social](https://twitter.com/share?text=Enhanced+Agentic-RAG%3A+What+If+Chatbots+Could+Deliver+Near-Human+Precision%3F&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fenhanced-agentic-rag%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fenhanced-agentic-rag%2F)
  * [Envelope](mailto:?subject=Enhanced+Agentic-RAG%3A+What+If+Chatbots+Could+Deliver+Near-Human+Precision%3F&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fenhanced-agentic-rag%2F)
  * Link

# Introduction
[Genie](https://www.uber.com/en-NL/blog/genie-ubers-gen-ai-on-call-copilot/) is Uber’s internal on-call copilot, designed to provide real-time support for thousands of queries across multiple help channels in Slack®. It enables users to receive prompt responses with proper citations from Uber’s internal documentation. It also improves the productivity of on-call engineers and subject matter experts (SMEs) by reducing the effort required to address common, ad-hoc queries.
While Genie streamlines the development of an LLM-powered on-call Slack bot, ensuring the accuracy and relevance of its responses remains a significant challenge. This blog details our efforts to improve Genie’s answer quality to near-human precision, allowing SMEs to rely on it for most queries without concern over potential misinformation in the engineering security and privacy domain.
* * *
## Motivation
Genie has revolutionized on-call assistance within Uber by enabling domain teams to deploy an LLM-powered Slack bot overnight using a configurable framework. This framework seamlessly integrates with nearly all internal knowledge sources, including the engineering wiki, Terrablob PDFs, Google Docs™, and custom documents. Additionally, it supports the full RAG (Retrieval-Augmented Generation) pipeline, covering document loading, processing, vector storage, retrieval, and answer generation.
While this system is advanced from a machine learning infrastructure perspective, delivering highly precise and relevant responses to domain-specific queries remains an area for improvement. To assess whether the Genie-powered on-call bot was ready for deployment across all Slack channels related to engineering security and privacy, SMEs curated a golden set of 100+ test queries based on their extensive experience handling domain engineers’ inquiries.
When Genie was integrated with Uber’s repository of 40+ engineering security and privacy policy documents—stored as PDFs—and tested against the golden test set, the results revealed significant gaps in accuracy. SMEs determined that ‌response quality didn’t meet the standards required for a broader deployment. Many answers were either incomplete, inaccurate, or failed to retrieve relevant information in correct detail from the knowledge base. Before rolling out the on-call copilot across critical security and privacy Slack channels, it was clear that significant improvements were needed to ensure response accuracy and reliability.
In this blog, we share our journey of improving the quality of responses by increasing the percentage of acceptable answers by a relative 27% and reducing incorrect advice by a relative 60% through our transition from a traditional RAG architecture to an enhanced agentic RAG approach.
* * *
## Architecture
RAG, introduced by Lewis et al. in 2020, transformed LLMs’ effectiveness in domain-specific NLP tasks. However, recent studies highlight retrieval challenges, particularly in Q&A setups where ambiguous or context-lacking queries hinder accurate document retrieval. When irrelevant content is retrieved, LLMs struggle to generate correct answers, often leading to errors or hallucinations.
To tackle the above issue, we used the agentic RAG approach. We introduce LLM-powered agents to perform several pre-and post-requisite steps to make the retrieval and answer generation more accurate and relevant. Figure 1 showcases the agentic RAG workflow, including the enriched document processing. We refer to this workflow as _EAg-Rag_ (Enhanced Agentic RAG).
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/figure-1-17484736625654-1024x769.png)Figure 1: End-to-end workflow of EAg-RAG architecture for Uber’s on-call Q&A copilot.
Like any RAG architecture, EAg-RAG consists of two key components: offline document processing and near-real-time answer generation. We’ve introduced several improvements in both, as discussed in the following sections.
###   
Enriched Document Processing
_“The quality of a model depends on the quality of its assumptions and the quality of its data.”_
_–_ Judea Pearl 
In today’s rapidly evolving and growing landscape of LLM-powered applications, this fundamental principle is often overlooked. As generative AI continues to advance at an unprecedented pace, ensuring robust assumptions and high-quality data remains essential for building reliable and effective AI systems.
As part of our efforts to improve the performance of the Genie chatbot, we evaluated the quality of processed documents before converting them into embedding vectors and storing them in the vector database as part of the RAG pipeline. During this assessment, we discovered that existing PDF loaders often fail to correctly capture structured text and formatting (such as bullet points and tables). This issue negatively impacts downstream processes like chunking, embedding, and retrieval. For example, many of our policy documents contain complex tables spanning more than five pages, including nested table cells. When processed using traditional PDF loaders (such as SimpleDirectoryLoader from LlamaIndex™ and PyPDFLoader from LangChain™), the extracted text loses its original formatting. As a result, many table cells become isolated, stand-alone text, disconnecting them from their respective row and column contexts. This fragmentation poses challenges for chunking, as the model may split a table into multiple chunks incorrectly. Additionally, during retrieval, the lack of contextual information often prevents semantic search from fetching the correct cell values. We experimented with several state-of-the-art PDF loaders, including PdfPlumber, PyMuPDF®, and LlamaIndex LlamaParse. While some of these tools provided better-formatted extractions, we were unable to find a universal solution that worked across all of our policy documents.
To address this challenge, we transitioned from PDFs to Google Docs, using HTML formatting for more accurate text extraction. Additionally, Google Docs offer built-in access control, crucial for security-sensitive applications. Access control metadata can be indexed and used during answer generation to prevent unauthorized access to restricted information. But even with HTML formatting, when we implemented traditional document loaders such as html2text or even state-of-the-art Markdownify from LangChain to extract the content of Google documents as markdown text, we found plenty of room for improvements, especially with formatting tables correctly.
To provide an example, we’ve generated a mock table with a nested structure, as shown in Figure 2. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/figure-2-17484736997542.png)Figure 2: A mock table used for demonstrating the content enrichment.
After this Google document is parsed as markdown-formatted text using html2text, we used MarkDownTextSplitter to chunk‌ it. When we did this, the row and column context of the table cells were often missing, as shown in Figure 3.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/split1-17484738582338.png)
* * *
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/split2-17484738712091.png)Figure 3: Chunked texts extracted through html2text and chunked using MarkdownTextSplitter.
To address this issue, we built a custom Google document loader using the Google® __ Python API, extracting paragraphs, tables, and the table of contents recursively. For tables and structured text like bullet points, we integrated an LLM-powered enrichment process, prompting the LLM to convert extracted table contents into markdown-formatted tables. Additionally, we enriched the metadata with identifiers to distinguish table-containing text chunks, ensuring they remain intact during chunking. Figure 4 shows the improvements achieved through these enhancements. We also added a two-line summary and a few keywords from the table so that the corresponding chunk would improve the relevancy of the semantic search.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/figure-4png-17484739317231-1024x395.png)Figure 4: Chunked texts extracted through a custom loader with LLM-powered formatting and split using table-aware chunking based on metadata identifiers.
The same approach can also be applied to text, which requires more formatting and structures before conversion to embeddings.
To further enhance chatbot accuracy, we focused on improving text extraction and formatting as well as enriching the metadata. In addition to standard metadata attributes such as title, URL, and IDs, we’ve introduced several custom attributes. Leveraging the remarkable capabilities of LLMs to summarize large documents, we incorporated document summaries, a set of FAQs, and relevant keywords into the metadata. The FAQs and keywords were added after the chunking step, ensuring they dynamically align with specific chunks, whereas the document summary remains consistent across all chunks originating from the same document.
These enriched metadata serve two purposes. First, certain metadata attributes are used in the precursor or post-processing steps of the semantic retrieval process to refine the extracted context, making it more relevant and clear for the answer-generating LLM. Second, attributes such as FAQs and keywords are directly employed in the retrieval process itself to enhance the accuracy of the retrieval engine. 
After enriching and chunking the extracted documents, we index them and generate embeddings for each chunk, storing them in a vector store using the pipeline configurations detailed in [this blog](https://www.uber.com/en-NL/blog/genie-ubers-gen-ai-on-call-copilot/). Additionally, we save artifacts like document lists (titles and summaries) and FAQs from the enrichment process in an offline feature store for later use in answer generation.
###   
Agentic RAG Answer Generation
Traditionally, answer generation involves two steps: retrieving semantically relevant document chunks via vector search and passing them along with the user’s query and instructions, to an LLM. However, in domain-specific cases like Uber’s internal security and privacy channels, document chunks often have subtle distinctions—not only within the same policy document but also across multiple documents. These distinctions can include variations in data retention policies, data classification, and sharing protocols across different personas and geographies. Simple semantic similarity can lead to retrieving irrelevant context, reducing the accuracy of the final answer.
To address this, we introduced LLM-powered agents in the pre-retrieval and post-processing steps to improve context relevance and enhance extracted content before answer generation. This agentic RAG approach has significantly improved answer quality and opened avenues for further targeted enhancements.
In the pre-processing step, we use two agents: _Query Optimizer_ and _Source Identifier_. Query Optimizer refines the query when it lacks context or is ambiguous. It also breaks down complex queries into multiple simpler queries for better retrieval. Source Identifier then processes the optimized query to narrow down the subset of policy documents most likely to contain relevant answers.
To achieve this, both agents use the _document list artifact_ (titles, summaries, and FAQs) fetched from the offline store as context. Additionally, we provide a few-shot examples to improve in-context learning for the Source Identifier. The output of the pre-processing step is an optimized query and a subset of document titles, which are then used to restrict the retrieval search within the identified document set.
To further refine retrieval, we introduced an additional BM25-based retriever alongside traditional vector search. This retriever fetches the most relevant document chunks using enriched metadata, which includes summaries, FAQs, and keywords for each chunk. The final retrieval output is the union of results from the vector search and the BM25 retriever, which is then passed to the post-processing step.
The Post-Processor Agent performs two key tasks: de-duplication of retrieved document chunks and structuring the context based on the positional order of chunks within the original documents.
Finally, the original user query, optimized auxiliary queries, and post-processed retrieved context are passed to the answer-generating LLM, along with specific instructions for answer construction. The generated answer is then shared with the user through the Slack® interface.
* * *
## Challenges
Improving accuracy in a RAG-powered system typically involves refining prompt instructions, adjusting retrieval configurations, and using advanced PDF parsers like LlamaParse instead of basic loaders. However, our use case presented two key challenges that led us to adopt the enhanced agentic RAG architecture:
  * **High SME involvement and slow evaluation**. While Genie’s modular framework allowed easy experimentation, assessing improvements required significant SME bandwidth, often taking weeks.
  * **Marginal gains and plateauing accuracy**. Many experiments yielded only slight accuracy improvements before plateauing, with no clear path for further enhancement.

At the start of development, overcoming these challenges was critical to ensuring Genie could reliably support security and privacy teams without risking inaccurate guidance. To address them, we introduced: Automated evaluation with generative AI and the agentic RAG framework. The automated evaluation reduced experiment evaluation time from weeks to minutes, enabling faster iterations and more effective directional experimentation. Unlike traditional RAG, the agentic RAG approach allows seamless integration of different agents, making it easier to test and assess incremental improvements quickly.
###   
LLM-as-Judge for Automation of Batch Evaluation
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/figure-5-17484739834624-1024x373.png)Figure 5: LLM-as-a-Judge, taken from [Gu et. al. 2024](https://arxiv.org/abs/2411.15594).
In recent years, the [LLM-as-a-Judge framework](https://arxiv.org/abs/2411.15594) has been widely adopted to automate evaluation, identify improvement areas, and enhance performance. As shown in Figure 5 and detailed in the referenced paper, we use an LLM to assess chatbot responses (x) within a given context (C), producing structured scores, correctness labels, and AI-generated reasoning and feedback.
We apply this approach to automate bot response evaluation, ensuring alignment with SME quality standards (Figure 6). The process consists of three stages:
  1. **One-time manual SME review**. SMEs provide high-quality responses or feedback on chatbot-generated answers (SME responses).
  2. **Batch execution**. The chatbot generates responses based on its current version.
  3. **LLM evaluation**. The LLM-as-Judge module evaluates chatbot responses using the user query, SME response, and evaluation instructions as context (C), along with additional content retrieved from source documents via the latest RAG pipeline.

Integrating these additional documents enhances the LLM’s domain awareness, improving evaluation reliability—particularly for domain-specific complex topics like engineering security and privacy policies at Uber.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/figure-6-17484740192508-1024x346.png)Figure 6: LLM-as-Judge-based automatic batch evaluation flow.
In our use case, the LLM-as-Judge module scores responses on a 0-5 scale, with 5 being the highest quality. It also provides reasoning for its evaluations, enabling us to incorporate feedback into future experiments.
###   
Developing Agentic RAG Using LangChain and LangGraph
We built most components of the agentic RAG framework using Langfx, Uber’s internal LangChain-based service within [Michelangelo](https://www.uber.com/en-NL/blog/michelangelo-machine-learning-platform/). For agent development and workflow orchestration, we used LangChain [LangGraph](https://langchain-ai.github.io/langgraph/)™, a scalable yet developer-friendly framework for agentic AI workflows. While our current implementation follows a sequential flow (Figure 2), integrating with LangGraph allows for future expansion into more complex agentic frameworks.
* * *
## Use Cases at Uber
The EAg-RAG framework was tested for the on-call copilot Genie within the engineering security and privacy domain. In these domains, it showed a significant improvement in the accuracy and relevancy of the golden test-set answers. With these improvements, the copilot bot can now scale across multiple security and privacy help channels to provide real-time responses to common user queries. This has led to a measurable reduction in the support load for on-call engineers and SMEs, allowing them to focus on more complex and high-value tasks—ultimately increasing overall productivity for Uber Engineering. Additionally, by showing that better-quality source documentation enables improved bot performance, this development encourages teams to maintain more accurate and useful internal docs. These enhancements aren’t limited to the security and privacy domain. They’ve been designed as configurable components within the Michelangelo Genie framework, making them easily adoptable by other domain teams across Uber.
* * *
## Next Steps 
This blog represents an early step in Uber’s agentic AI evolution. As requirements evolve, more complex architectures may be needed. For example, currently our custom Google Docs plugin and document enrichment supports textual content. The same can be extended to extract and enrich multi-modal content, including images. In the answer generation step, instead of a single-step query optimization, an iterative [Chain-of-RAG](https://arxiv.org/abs/2501.14342) approach could enhance performance, especially for multi-hop reasoning queries. Additionally, a [self-critique](https://proceedings.neurips.cc/paper/2019/hash/6018df1842f7130f1b85a6f8e911b96b-Abstract.html) agent could be introduced after answer generation to dynamically refine responses and further reduce hallucinations. Further, to ensure flexibility with complex and simple type queries, we’d like to introduce many of these features as tools. Then, we can allow LLM-powered agents to choose the tools as required based on the type and complexity of the queries. With the development described in this blog, we aim to establish a foundation for building agentic RAG systems for Q&A automation at Uber, paving the way for future advancements.
* * *
# Conclusion
By leveraging enriched document processing and the Agentic RAG framework, we’ve shown how the EAg-RAG architecture significantly improves answer quality. As we roll out these improvements across multiple help channels within Uber’s internal Slack, we aim to observe how better answers help users get accurate guidance faster and provide peace of mind to SMEs and on-call engineers by resolving common queries through the on-call copilot.
Cover photo attribution: Clicked by Arnab Chakraborty.
_Google ® and Google Docs™ are trademarks of Google LLC and this blog post is not endorsed by or affiliated with Google in any way._
_LangChain ™ and LangGraph™ are trademarks of Langchain, Inc._
_LlamaIndex ™ is a trademark of LlamaIndex, Inc._
PyMuPDF®, Artifex, the Artifex logo, MuPDF, and the MuPDF logo are registered trademarks of Artifex Software Inc.  
_Slack ® is a registered trademark and service mark of Slack Technologies, Inc._
* * *
![Arnab Chakraborty](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/arnab-pic-17484751108023-620x1024.png)
Arnab Chakraborty
Arnab Chakraborty is a Senior Applied Scientist on Uber’s Engineering Security team in Amsterdam, where he focuses on AI/ML initiatives to enhance security and privacy at Uber. Previously, he worked on building large-scale AI systems in the FinTech domain.
![Paarth Chothani](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/01/paarth-pic-17484754567250-e1748475528904.jpg)
Paarth Chothani
Paarth Chothani is a Staff Software Engineer on the Uber AI Gen AI/CoreML team in the San Francisco Bay area. He specializes in building distributed systems/Gen AI solutions at scale.
![Christopher Settles](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2023/09/Christopher-Settles-1024x1024.png)
Christopher Settles
Christopher Settles is a former Machine Learning Engineer on Uber’s AI Platform - Feature Store team, where he leads both Uber’s Data for Realtime ML initiatives and Uber’s GenAI on complex documents initiatives.
![Adi Raghavendra](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/05/adi-pic-17484759038471.jpg)
Adi Raghavendra
Adi Raghavendra is a Senior Engineering Manager leading the AI/ML team for Engineering Security and Privacy. He is leading efforts in leveraging agentic workflows to solve complex challenges in security and privacy. His work focuses on the intersection of security, privacy, traditional machine learning, and generative AI to develop intelligent, automated solutions that enhance protection, compliance, and threat detection.
* * *
Posted by Arnab Chakraborty, Paarth Chothani, Christopher Settles, Adi Raghavendra 
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
[English](/en-CA/blog/enhanced-agentic-rag/)
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
[English](/en-CA/blog/enhanced-agentic-rag/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
