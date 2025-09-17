---
title: "Advancing Invoice Document Processing at Uber using GenAI"
author: "Unknown"
url: "https://www.uber.com/blog/advancing-invoice-document-processing-using-genai/"
published_date: "None"
downloaded_date: "2025-09-15T09:38:21.124983"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for Advancing Invoice Document Processing at Uber using GenAI](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/01-cover-image-17448387506486.png)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fadvancing-invoice-document-processing-using-genai%2F&t=Advancing+Invoice+Document+Processing+at+Uber+using+GenAI)
  * [X social](https://twitter.com/share?text=Advancing+Invoice+Document+Processing+at+Uber+using+GenAI&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fadvancing-invoice-document-processing-using-genai%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fadvancing-invoice-document-processing-using-genai%2F)
  * [Envelope](mailto:?subject=Advancing+Invoice+Document+Processing+at+Uber+using+GenAI&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fadvancing-invoice-document-processing-using-genai%2F)
  * Link

# Introduction
In today’s fast-paced business environment, efficiently managing operational tasks is vital for maintaining workflows. Uber, with its large network of suppliers worldwide, faces considerable challenges in processing a high volume of invoices daily. Invoice processing is a critical function for Uber’s financial operations, directly impacting the efficiency and accuracy of our accounts payable processes.
This blog explores how we used GenAI to solve this problem, setting a new standard in financial operations management.
* * *
## Background
The traditional invoice processing approach relies on manual data entry or automation like RPA (Robotic Process Automation), Excel uploads, and rule-based systems. While Uber has automation solutions like RPA and self-serve supplier platforms, a significant portion of invoices still require manual handling. We believed that we could improve the existing process as the old process has proven inadequate in speed, accuracy, and cost-effectiveness.
To address ‌inefficiencies in ‌existing invoicing mechanisms, we implemented a GenAI-powered invoice automation system. This innovation uses advanced ML and NLP (Natural Language Processing) to automate and improve the invoice processing workflow, significantly reducing manual intervention and operational costs. The result is a robust and scalable system that accelerates invoicing processes, minimizes errors and improves the user experience. 
###   
Overall Procurement Process
Uber relies on external suppliers for goods and services. A supplier first onboards to Uber based on requirements. Uber employees then raise a PO (Purchase Order) against the suppliers representing the goods or services to procure. Suppliers submit invoices for services rendered or goods procured against the approved PO. Once submitted, the invoice goes through approvals before payment is issued to the supplier. Uber mandates that a copy of the invoice be provided in PDF format for processing payments. 
Figure 1 shows a high-level overview of the procurement process. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/02-overall-procurement-process-17448442294841-1024x96.png)Figure 1: Procurement process workflow at Uber.
###   
Invoice Submission Process
Figure 2 shows how suppliers submit invoices to Uber. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/03-invoice-submission-process-17448442599745-1024x474.png)Figure 2: Invoice process workflow at Uber.
There are two methods for suppliers to submit invoices:
  * **Self-Service Supplier Platform:** Uber has an in-house self-service platform for ‌suppliers. Suppliers use the platform to search for their POs and submit an invoice to any PO. 
  * **Email-based invoice submission** : Suppliers can send an email to an address, and those invoices are processed manually or via the RPA process. Emails are ingested into the ticketing system and a ticket is generated for each invoice based on predefined rules. Invoices are processed via RPA bots with an eyeball check or completely manually and ingested into the ERP application.

* * *
## Challenges
Uber handles a vast number of global supplier invoices. This presents business and technical challenges. 
### Business Challenges
Despite electronic submissions, a substantial portion of invoices require manual data extraction, leading to inefficiencies and delays. Another business challenge is increased operational costs. Manual processing is time-consuming and costly. Further, the AHT (Average Handling Time) taken by operators to process an invoice document is high, causing significant delays. Finally, human interventions heighten the risk of errors, leading to financial discrepancies and reconciliation challenges.
###   
Technical Challenges
Uber works with thousands of suppliers, each using varying invoice templates and formats. Beyond diverse formats, invoices arrive in over 25 languages, complicating data extraction. The presence of handwritten text and scanned copies further increases complexity. There’s also a high attribute volume within each invoice. Each invoice contains 15-20 attributes along with line information that needs to be captured accurately. Dealing with invoices spanning multiple pages adds another layer of intricacy.
###   
Problems with Existing Tools
Existing tools, including RBS (Rule-Based Systems) and RPA, need more adaptability and intelligence to handle the diverse and dynamic nature of invoice formats and processing needs. While RPA automation sufficed when we had a limited set of formats, as Uber grows and onboards new document formats, the RPA solution doesn’t scale well and needs training on the new formats via manual rule-setting. 
They also need more flexibility and maintenance. They require continual updates and manual intervention for error correction. They’re unable to process a high volume of invoices without degrading performance.
* * *
## Design
The design of Uber’s GenAI-powered invoice automation system emphasizes accuracy, scalability, and flexibility. 
### Principles
Several principles guide Uber’s design for the new invoice automation system:
  * **Accuracy:** Leveraging advanced trained ML models or GenAI models for precision, the system ensures high accuracy in data extraction from diverse invoice formats. This significantly reduces errors and improves the reliability of financial data.
  * **Scalability:** The system is designed to efficiently handle large volumes of invoices, accommodating Uber’s global operations. By using robust architectures and scalable technologies, it supports continuous growth without compromising on performance.
  * **Flexibility:** The invoice automation system is equipped to adapt to new and diverse invoice formats without requiring manual rule-setting. This adaptability ensures that the system remains relevant and efficient, even as suppliers and invoice structures evolve.
  * **User experience:** The design places high importance on creating a user-friendly interface that simplifies the review and correction process. By offering intuitive and accessible features, the system makes it easier for staff to manage and process invoices efficiently.

###   
Document Processing Platform
Our approach aimed to provide a robust and flexible document processing solution adaptable to various business requirements and document types without significant code changes.
We designed a modular and pluggable architecture, enabling the platform to scale for diverse use cases like entity extraction, summarization, and classification. For a configuration-driven integration, we emphasized minimal coding and extensive configurations to onboard new country-specific templates, significantly reducing rollout times. To manage nonlinear and verbose document processing workflows efficiently, we used Uber’s [Cadence](https://www.uber.com/en-IN/blog/announcing-cadence/) workflow platform. We also developed common and reusable components for future integrations and launches.
###   
Data Profiling and Labeling
Data profiling is a crucial part of the invoice data extraction process for training any LLM model to improve extraction accuracy through precise labeling of data elements. By creating accurate and consistent labels, the LLM model can better understand invoice structures. 
Analyzing our supplier base, we found that many invoices come from a small subset of suppliers. High-volume suppliers with significant yearly invoice volumes are prioritized for profiling, particularly when their field-level accuracy falls below a set threshold. This insight informed our prioritization strategy for ML model development and deployment.
Suppliers whose field-level accuracy falls below the threshold are targeted for labeling, allowing the model to learn and improve extraction precision. We label key invoice fields like invoice number, date, and amount. Accurate and consistent labels optimize the in-house-trained model’s understanding of invoice structures, leading to more reliable data extraction.
###   
UI Design
We designed a UI to enable users performing the HITL (Human in the Loop) review to do a side-by-side comparison of the PDF data versus the data extracted from the models. We also enabled multiple alerts and soft warning messages, ensuring all the information is in one place for user review. 
This enables the user to review all the details with simple eye movements compared to hand movements, fast-tracking the review process. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/04-ui-design-17448444959396-1024x666.png)Figure 3: Invoice processing platform UI design.
* * *
## Architecture
This section describes the architectural details of building the document processing platform and the invoice processing workflow. 
### **TextSense** : Scalable Document Processing Platform
Figure 4 shows the full document processing pipeline. For processing any document, pre-processing is usually common before calling any LLM models. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/05-document-processing-pipeline-17448446879370-1024x360.png)Figure 4: Document processing pipeline.
Uber built TextSense, a common document processing platform. TextSense abstracts all the above processes and serves as a versatile utility for extracting text from various document types, not just invoices. It provides a modular and reusable interface over OCR and LLM technologies, making it easy to onboard new document processing use cases through simple configuration changes.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/06-textsense-architecture-document-processing-platform-17448449911255-edited.png)Figure 5: TextSense architecture for the document processing platform.
This table explains the steps in the document processing workflow. 
**Step**| **Description**  
---|---  
1\. Document ingestion| Integrates documents from sources like emails, PDFs, and ‌ticketing systems, and saves files in an object storage platform. Supports structured and unstructured data formats.  
2\. Pre-processing| Includes image augmentation to handle low-resolution scans and handwritten texts.Converts document formats (PDFs, Word documents, images) into a standard format suitable for processing.Converts multi-page documents into standardized formats.  
3\. Computer vision (CV) and OCR integration  | Uses Uber’s Vision Gateway CV platform for optical character recognition to extract text from document images.  
4\. AI and ML models | Leverages trained or pre-trained LLM models for extracting specific data elements like invoice numbers, dates, and amounts.Continuously improves through periodic re-training and feedback loops to address accuracy issues and adapt to new document formats.  
5\. Post-processing and integration| Applies business rules and user-defined post-processing steps to refine extracted data before final use.Integrates with client systems for further processing and payment actions, enabling end-to-end automation.  
6\. Data validation and extraction accuracy | Ensures data quality by cross-referencing with existing databases or predefined rules.Includes HITL validation for critical reviews and corrections.  
7\. Metrics and performance monitoring | Captures key performance indicators like processing speed, accuracy rates, and cost efficiency.Uses these metrics to drive continuous improvements.  
###   
Invoicing Workflow Using TextSense 
The invoicing workflow is built into our in-house application. The flow integrates with TextSense for processing supplier invoice PDFs. There are two ways documents come in: invoice PDF manual uploads and invoice tickets ingested from our ticketing system.
During manual PDF uploads, the front-end web app service accepts the user-submitted file and sends a request to a common back-end endpoint. This back-end endpoint sends the document to TextSense for processing.
For ‌document ingestion from the ticketing system, an ingestion service reads the open tickets and extracts supplier emails and any associated PDFs. The email text is passed on to TextSense for parsing key information, which helps in further processing. The PDFs are sent (along with the details from the email text) to the common back-end endpoint for further processing. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/07-invoicing-workflow-leveraging-textsense-17448452614933-edited.png)Figure 6: Invoicing workflow using TextSense.
Once the response is extracted by TextSense, the post-processing layer kicks in. It validates the information, enriches the extracted data, and makes it ready for human review. Upon review and approval, the documents are processed as invoices and sent to the ERP system for approval and vendor payments.
###   
Model Evaluation and Selection
The process starts with data preparation and considers the past invoice data and associated attachments as the ground truth. There are two datasets: 
  * **Structured labelled data** : The invoice data (fields we want to extract) that are entered into systems.
  * **Unstructured PDF data** : Extracted text from the associated invoice PDF documents. 

We considered the last year of invoice data for training and took 90% for training data and 10% for test data.
These data sets become the input for fine-tuning and training an open-source LLM model. We fine-tuned and rigorously evaluated multiple LLM models, such as seq2seq, Meta® Llama 2®, and Google® Flan T5 to determine the optimal solution for our invoice processing use case. T5 showed promise with great accuracy of over 90% for the invoice header fields, but it didn’t do well predicting the line’s information. First-line accuracy was good, but we saw a considerable drop in accuracy while predicting the second line onwards. While fine-tuning helped in understanding the data patterns and multiple business rules of the existing invoices and predicted accordingly, this also led to hallucinations, especially for the line information. 
  
We evaluated OpenAI® GPT-4 models, which demonstrated better performance in accuracy and adaptability. OpenAI® GPT-4 ability to handle complex, unstructured data and its potential for future ensemble approaches made it the preferred choice. Even though GenAI wasn’t adept at detecting our existing invoice data patterns, it was very good at predicting what was available in the documents. So, for our data pipeline, we predicted all the details required from an invoice and built a post-processing layer to apply any business logic before showing it to the user for HITL review. 
This table shares what we found comparing a fine-tuned open-source model with an out-of-the-box LLM model under a proprietary license.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/image-4-18-25-at-10.26am-17449971754520-1024x663.jpeg)
So, based on the cost-benefit analysis, GenAI was a clear winner in terms of overall accuracy. Even though the LLM model had slightly higher header accuracy, GenAI was the winner for line prediction. 
In the future, we plan to follow an ensemble approach and implement the chaining of more sophisticated models further to enhance accuracy and adaptability for broader use cases.
###   
Accuracy Calculation
Calculating the performance of a GenAI model can be challenging. We calculate accuracy at the header level (overall invoice information) and the line level (individual line items within the invoice) for the invoice processing use case. We determine the accuracy for each field based on the specific type of match required. ‌For example, some fields require an exact match (like invoice number), while others allow for fuzzy string matching (like invoice description).
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/10-accuracy-calculation-pipeline-17448457846579-908x1024.png)Figure 7: Accuracy metric workflow. 
Our accuracy metrics are designed to provide granular insights into model performance, enabling us to identify areas for improvement and guide model retraining efforts. ‌‌We also track accuracy trends over time to ensure that models continue to perform effectively as our invoice processing workload evolves.
* * *
## Results
The implementation of the GenAI-powered invoice automation system at Uber has yielded remarkable results. 
Our GenAI-based solution achieved: 
  * **A significant reduction in manual processing:** We’ve seen a**** 2x reduction in manual invoicing. 
  * **High accuracy:** It has an impressive overall accuracy rate of 90%. 35% of submitted invoices achieved a near-perfect accuracy of 99.5%, and 65% achieved more than 80% accuracy.
  * **Reduced handling time:** The solution reduced the average handling time of invoice processing by 70%.
  * **Improved user experience:** Smarter data extraction from PDFs, post-processing rules, intuitive UI design, and robust integration with the ERP systems enable seamless invoice creation and vendor payment. 

These results have significantly reduced manual intervention and set a new benchmark for operational excellence within Uber’s financial operations management. They have also resulted in a 25-30% cost saving compared to the manual process.
* * *
## Next Steps
Looking ahead, we’ll further improve ‌accuracy, expand capabilities, and build a document classification layer. We also plan to enable ‌fully automated end-to-end processing for cases where 100% accuracy is met historically, reducing manual interventions and speeding up workflows.
Through regular feedback loops and performance monitoring, TextSense will continue to evolve, incorporating new developments in AI technology. Future updates aim to expand the platform’s ability to process additional document types and further integrate with other enterprise systems, making TextSense a versatile tool for comprehensive document management. The document classification layer we build will classify documents according to a particular type.
* * *
# Conclusion
Developing and deploying Uber’s GenAI-powered invoice automation revolutionizes Uber’s financial operations. ‌By overcoming the challenges of manual processing, we’ve achieved significant efficiency gains and cost reductions. 
Our commitment to innovation extends beyond invoices, with TextSense poised to streamline other document processing across the organization. The integration of NLP and AI models enables precise data extraction and validation, while the use of HITL processes allows for necessary human oversight, ensuring the highest levels of accuracy and compliance.
By harnessing the power of GenAI, TextSense sets a new standard for document processing automation, paving the way for further innovations at Uber.
Cover photo attribution: Image created with the enterprise version of ChatGPT 4.
_Google ® is a trademark of Google LLC and this blog post is not endorsed by or affiliated with Google in any way._
_Llama 2 ®, Llama 3® and their logos are registered trademarks of Meta® in the United States and other countries. No endorsement by Meta is implied by the use of these marks._
_OpenAI ® and its logos are registered trademarks of OpenAI®. No endorsement by Meta is implied by the use of these marks._
* * *
![Rohit Subudhi](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/rohit-pic-17448462076705.jpg)
Rohit Subudhi
Rohit Subudhi is a Software Engineering Manager on the Fintech Team at Uber, based in Hyderabad.
![Rakesh Vagvala](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/profile-photo-rakesh-vagvala-17448464135596-1024x850.png)
Rakesh Vagvala
Rakesh Vagvala is a Software Engineering Manager on the Fintech Team at Uber, based in Hyderabad.
![Sushil Kumar Jain Devichand](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/profile-photo-sushil-jain-17448467737379-1024x955.jpeg)
Sushil Kumar Jain Devichand
Sushil is a Sr. Applications Engineer on the Fintech Team at Uber, based in Hyderabad.
![Indrani Bose](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/indrani-pic-17448469014048.png)
Indrani Bose
Indrani Bose is a Sr. Manager on the Fintech Team at Uber, based in Hyderabad.
![Balaram Baral](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/profile-photo-balaram-baral-17448470278614-886x1024.png)
Balaram Baral
Balaram Baral is a Director on the Fintech Team at Uber, based in Hyderabad.
* * *
Posted by Rohit Subudhi, Rakesh Vagvala, Sushil Kumar Jain Devichand, Indrani Bose, Balaram Baral 
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
[English](/en-CA/blog/advancing-invoice-document-processing-using-genai/)
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
[English](/en-CA/blog/advancing-invoice-document-processing-using-genai/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
