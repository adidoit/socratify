---
title: "Listening, Learning, and Helping at Scale: How Machine Learning Transforms Airbnb’s Voice Support Experience | by Yuanpei Cao | The Airbnb Tech Blog"
author: "Unknown"
url: "https://medium.com/airbnb-engineering/listening-learning-and-helping-at-scale-how-machine-learning-transforms-airbnbs-voice-support-b71f912d4760?source=rss----53c7c27702d5---4"
date: "2025-09-15"
---

#**Listening, Learning, and Helping at Scale: How Machine Learning Transforms Airbnb’s Voice Support Experience**

[![Yuanpei Cao](https://miro.medium.com/v2/resize:fill:64:64/1*wZhTYXwJYILN7S_XlD52-w.jpeg)](/@caoyuanpei?source=post_page---byline--b71f912d4760---------------------------------------)

[Yuanpei Cao](/@caoyuanpei?source=post_page---byline--b71f912d4760---------------------------------------)

7 min read

·

May 29, 2025

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2Fb71f912d4760&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Flistening-learning-and-helping-at-scale-how-machine-learning-transforms-airbnbs-voice-support-b71f912d4760&user=Yuanpei+Cao&userId=dd368cae1247&source=---header_actions--b71f912d4760---------------------clap_footer------------------)

\--

1

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fb71f912d4760&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Flistening-learning-and-helping-at-scale-how-machine-learning-transforms-airbnbs-voice-support-b71f912d4760&source=---header_actions--b71f912d4760---------------------bookmark_footer------------------)

Listen

Share

A look into how Airbnb uses speech recognition, intent detection, and language models to understand users and assist agents more effectively.

_By_[ _Yuanpei Cao_](https://www.linkedin.com/in/yuanpei-cao-792b103b/) _,_[_H_ eng Ji](https://www.linkedin.com/in/heng-j-1a44a711/) _,_[_Elaine Liu_](https://www.linkedin.com/in/elaineliu5/) _,_[_Peng Wang_](https://www.linkedin.com/in/peng-wang-13117371/) _, and_[ _Tiantian Zhang_](https://www.linkedin.com/in/tiantian-zhang-a4208726/)

Press enter or click to view image in full size

At Airbnb, we aim to provide a smooth, intuitive, and helpful community support experience, whether it’s helping a guest navigate a booking change or helping a host with a listing issue. While our Help Center and customer support chatbot helps resolve many inquiries efficiently, some users prefer the immediacy of a voice conversation with a support representative. To make these interactions faster and more effective, we’ve significantly improved our Interactive Voice Response (IVR) system via machine learning.

Over the years, Airbnb has invested in conversational AI to enhance customer support. In our previous blog posts [_Task-Oriented Conversational AI in Airbnb Customer Support_](/airbnb-engineering/task-oriented-conversational-ai-in-airbnb-customer-support-5ebf49169eaa) and[ _Using Chatbots to Provide Faster COVID-19 Community Support_](/airbnb-engineering/using-chatbots-to-provide-faster-covid-19-community-support-567c97c5c1c9), we explored how AI-driven chatbots streamline guest and host interactions through automated messaging. This post explains how we extend that work to voice-based support, leveraging machine learning to improve real-time phone interactions with our intelligent IVR system.

We’ll take you through the end-to-end IVR journey, the key machine learning components that power it, and how we designed a system that delivers faster, more human-like, and more intuitive voice support for our community.

## Reimagining the voice support journey

Traditional IVR systems often rely on rigid menu trees, requiring callers to press buttons and navigate pre-set paths. Instead, we designed an adaptive, conversational IVR that listens, understands, and responds in real time. Here’s normally what happens when a caller reaches out to Airbnb support:

1.**Call and greeting:**IVR picks up and prompts, _“In a few sentences, please tell us why you’re calling today.”_
2.**Automated speech recognition (ASR):**The caller’s response is transcribed with Airbnb-specific ASR. For example, if a caller says, _“I need to request a refund for my reservation,”_ ASR accurately converts this speech into text, preserving key domain-specific terms.
3.**Understanding intent:**A Contact Reason Detection model classifies the issue into a category like cancellations, refunds, account issues, etc.
4.**Decision-making:**If self-service is possible, the system retrieves and sends a relevant help article or an intelligent workflow via SMS or app notification. If the caller explicitly requests agent support or the issue requires human intervention, the call is routed to a customer support agent with relevant details attached.
5.**Clarifying response:**A Paraphrasing model generates a summary of the user intent, which IVR shares with the user before delivering the solution. This ensures that users understand the context of the resource they receive. Continuing our example, the system would respond, “ _I understand your issue is regarding a refund request._ _We have sent you a link to resources about this topic. Follow the instructions to find answers. If you need to speak with an agent, press 0 to be connected to our customer service representative._ ” The underscored Paraphrasing component enhances engagement by bridging the gap between system-generated responses and user comprehension, making the self-service experience more intuitive.
6.**Resolution or escalation:**The caller receives an SMS or app notification with a direct link to a relevant [Airbnb Help Center](https://www.airbnb.com/help) article. If further assistance is needed, they can press 0 to connect with a customer service representative.

By moving away from rigid menus to natural language understanding, we allow guests and hosts to express their issues in their own words, helping to increase satisfaction and resolution efficiency.

Press enter or click to view image in full size

Figure 1: High-level architecture of how Airbnb IVR Core Service interacts with core machine learning components to resolve user issues over the phone.

## Breaking down our ML-powered IVR system

### 1\. Automated speech recognition (ASR): transcribing with precision

In a voice-driven support system, achieving high transcription accuracy is essential, particularly in noisy phone environments where speech can be unclear. General speech recognition models often struggle with Airbnb-specific terminology, leading to errors like misinterpreting “listing” as “lifting” or “help with my stay” as “happy Christmas Day.” These inaccuracies create challenges in understanding user intent and impact downstream processes.

To enhance ASR accuracy, we transitioned from a generic high-quality pretrained model to one specifically adapted for noisy phone audio. Additionally, we introduced a domain-specific phrase list optimization that ensures Airbnb terms are properly recognized. Based on a sample of hundreds of clips, this significantly**reduced the word error rate (WER) from 33% to approximately 10%**. The reduced WER significantly enhanced the accuracy of downstream help article recommendations, increasing user engagement, improving customer NPS among users who interacted with the ASR menu, while reducing reliance on human agents and lowering customer service handling time.

### 2\. Contact Reason prediction: understanding the why

After transcribing the caller’s statements, the next step involves identifying their intent. We accomplished this by creating a detailed Contact Reason taxonomy that categorizes all potential Airbnb inquiries, as elaborated in “[T-LEAF: Taxonomy Learning and EvaluAtion Framework](/airbnb-engineering/t-leaf-taxonomy-learning-and-evaluation-framework-30ae19ce8c52).” We then use an intent detection model to classify calls into a Contact Reason category, ensuring each inquiry is handled appropriately. For example, if a caller mentions “I haven’t received my refund yet,” the model predicts the Contact Reason as Missing Refund and forwards it to the relevant downstream components.

In production, we deploy the Issue Detection Service to host the intent detection models, running them in parallel to achieve optimal scalability, flexibility, and efficiency. Parallel computing ensures that intent detection**latency remains under 50ms on average**, making the process imperceptible to IVR users and ensuring a seamless real-time experience. The detected intent is then analyzed within the IVR workflow to determine the next action, whether it’s guiding the user through a self-service resolution or escalating directly to a human agent.

Occasionally, callers prefer to speak directly with a human agent instead of describing their issues, using terms like “agent” or “escalation.” For such scenarios, we use a different intent detection model to recognize when a caller wants to escalate to a human agent. If this intent is detected, the IVR system honors the caller’s request and routes the call to the suitable support team.

Press enter or click to view image in full size

Figure 2. Intent detection architecture and Issue Detection Service.

### 3\. Help article retrieval: delivering the right information

Many common Airbnb issues can be quickly resolved by providing clear and relevant educational information. To help provide useful information to users and minimize the need for human customer support, we use the Help Article Retrieval and Ranking system. This advanced system automatically identifies the issue in a user’s inquiry and delivers the most relevant help article link via SMS text message and Airbnb app notification. Our process incorporates two machine learning stages.

**Semantic retrieval and ranking:**We index Airbnb Help Article embeddings into a vector database, enabling efficient retrieval of up to 30 relevant articles per user query using cosine similarity, typically within 60ms. An LLM-based ranking model then re-ranks these retrieved articles, with the top-ranked article directly presented to users via IVR channels. This dual-stage system not only powers IVR interactions but also supports our customer support chatbot and Help Center search. Across these platforms, its effectiveness is continuously evaluated using metrics like Precision@N, facilitating ongoing improvements and refinements.

Press enter or click to view image in full size

Figure 3. Architecture diagram for the Help Article Retrieval and Ranking system.

### 4\. Paraphrasing model: enhancing user understanding

A key challenge in IVR-based customer support is ensuring users clearly understand the resolution before receiving help article links, as they typically lack visibility into the article’s contents or title. To address this, we implemented a lightweight paraphrasing approach leveraging a curated set of standardized summaries.

UX writers created concise and clear paraphrases for common Airbnb scenarios. During online serving, user inquiries are mapped to these curated summaries via nearest-neighbor matching based on text embedding similarity. We calibrated a similarity threshold to ensure high-quality matches. Manual evaluation of end-to-end model outputs confirmed precision exceeding 90%.

The outcome was a finite-state solution delivering the most appropriate paraphrased IVR prompt before presenting a help article link. For example, if a caller states, “I need to cancel my reservation and request a refund,” the model generates a response like “I understand your issue is about a refund request” before sending the retrieved help article link.

Integrating this model ensures users receive clear, contextually relevant summaries prior to accessing help articles. In an experiment targeting English hosts who contacted customer support, we found that presenting a paraphrased summary before sending the article link increases user engagement with article content, resulting in improvement in self-resolution rates, helping to reduce the need for direct customer support assistance.

## Conclusion

By combining Automated Speech Recognition and Contact Reason Detection systems with a help article retrieval system, and a paraphrasing model, we have created an IVR system that streamlines support interactions and improves user satisfaction. Our solution enables callers to describe issues naturally, reduces dependency on human agents for common inquiries, and provides instant, relevant support through self-service. When human assistance is necessary, the system ensures a smooth transition by routing users to the right agent with essential context.

Interested in working at Airbnb? Check out our [open roles](https://careers.airbnb.com/).

##**Acknowledgements**

Thanks to Zhenyu Zhao, Mia Zhao, Wayne Zhang, Lucca Siaudzionis, Lulu Chen, Sukey Xu, Floria Wan, Michael Zhou, Can Yang, Yaolin Chen, Shuaihu Wang, Huifan Qu, Ming Shang,Yu Jiang, Wanting Chen, Elena Zhao, Shanna Su, Cassie Cao, Hao Wang, Haoran Zhu, Xirui Liu, Ying Tan, Xiaohan Zeng, Xiaoyu Meng, Gavin Li, Gaurav Rai, Hemanth Kolla, Ihor Hordiienko, Matheus Scharf, and Stepan Sydoruk who helped bring this vision to life. Also thanks to Paige Schwartz, Stephanie Chu, Neal Cohen, Becky Ajuonuma, Iman Saleh, Dani Normanm, Javier Salido, and Lauren Mackevich for the review and editing.

Thanks to Jeremy Werner, Joy Zhang, Claire Cheng, Yashar Mehdad, Shuohao Zhang, Shawn Yan, Kelvin Xiong, Michael Lubavin, Teng Wang, Wei Ji, and Chenhao Yang’s leadership support on building conversational AI products at Airbnb.
