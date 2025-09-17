---
title: "Building with Patterns: The Bucket Pattern"
company: "mongodb"
url: "https://www.mongodb.com/blog/post/building-with-patterns-the-bucket-pattern"
type: "direct_systems_collection"
date: "2025-09-15"
---

# Building with Patterns: The Bucket Pattern

[Learn More About MongoDB at MongoDB University](https://university.mongodb.com)

Daniel Coupal and Ken W. Alger  
January 31, 2019 | Updated: July 14, 2021  


**For information about our new time series features launched with MongoDB 5.0, please check out[this blog](https://developer.mongodb.com/how-to/new-time-series-collections/).**

In this edition of the _Building with Patterns_ series, we're going to cover the Bucket Pattern. This pattern is particularly effective when working with Internet of Things (IoT), Real-Time Analytics, or Time-Series data in general. By _bucketing_ data together we make it easier to organize specific groups of data, increasing the ability to discover historical trends or provide future forecasting and optimize our use of storage.

#### The Bucket Pattern

With data coming in as a stream over a period of time (time series data) we may be inclined to store each measurement in its own document. However, this inclination is a very relational approach to handling the data. If we have a sensor taking the temperature and saving it to the database every minute, our data stream might look something like:
    
    
    {
       sensor_id: 12345,
       timestamp: ISODate("2019-01-31T10:00:00.000Z"),
       temperature: 40
    }
    
    {
       sensor_id: 12345,
       timestamp: ISODate("2019-01-31T10:01:00.000Z"),
       temperature: 40
    }
    
    {
       sensor_id: 12345,
       timestamp: ISODate("2019-01-31T10:02:00.000Z"),
       temperature: 41
    }
    

This can pose some issues as our application scales in terms of data and index size. For example, we could end up having to index `sensor_id` and `timestamp` for every single measurement to enable rapid access at the cost of RAM. By leveraging the document data model though, we can "bucket" this data, by time, into documents that hold the measurements from a particular time span. We can also programmatically add additional information to each of these "buckets".

By applying the Bucket Pattern to our data model, we get some benefits in terms of index size savings, potential query simplification, and the ability to use that pre-aggregated data in our documents. Taking the data stream from above and applying the Bucket Pattern to it, we would wind up with:
    
    
    {
        sensor_id: 12345,
        start_date: ISODate("2019-01-31T10:00:00.000Z"),
        end_date: ISODate("2019-01-31T10:59:59.000Z"),
        measurements: [
           {
           timestamp: ISODate("2019-01-31T10:00:00.000Z"),
           temperature: 40
           },
           {
           timestamp: ISODate("2019-01-31T10:01:00.000Z"),
           temperature: 40
           },
           … 
           {
           timestamp: ISODate("2019-01-31T10:42:00.000Z"),
           temperature: 42
           }
        ],
       transaction_count: 42,
       sum_temperature: 2413
    } 
    

By using the Bucket Pattern, we have "bucketed" our data to, in this case, a one hour bucket. This particular data stream would still be growing as it currently only has 42 measurements; there's still more measurements for that hour to be added to the "bucket". When they are added to the `measurements` array, the `transaction_count` will be incremented and `sum_temperature` will also be updated.

With the pre-aggregated `sum_temperature` value, it then becomes possible to easily pull up a particular bucket and determine the average temperature (`sum_temperature / transaction_count`) for that bucket. When working with time-series data it is frequently more interesting and important to know what the average temperature was from 2:00 to 3:00 pm in Corning, California on 13 July 2018 than knowing what the temperature was at 2:03 pm. By bucketing and doing pre-aggregation we're more able to easily provide that information.

Additionally, as we gather more and more information we may determine that keeping all of the source data in an archive is more effective. How frequently do we need to access the temperature for Corning from 1948, for example? Being able to move those buckets of data to a data archive can be a large benefit.

#### Sample Use Case

One example of making time-series data valuable in the real world comes from an [IoT implementation by Bosch](https://www.mongodb.com/customers/bosch). They are using MongoDB and time-series data in an automotive field data app. The app captures data from a variety of sensors throughout the vehicle allowing for improved diagnostics of the vehicle itself and component performance.

Other examples include major banks that have incorporated this pattern in financial applications to group transactions together.

#### Conclusion

When working with time-series data, using the Bucket Pattern in MongoDB is a great option. It reduces the overall number of documents in a collection, improves index performance, and by leveraging pre-aggregation, it can simplify data access.

The Bucket Design pattern works great for many cases. But what if there are outliers in our data? That's where the next pattern we'll discuss, the _[Outlier Design Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-outlier-pattern)_ , comes into play.

If you have questions, please leave comments below.

[](https://www.facebook.com/sharer.php?u=https://www.mongodb.com/company/blog/building-with-patterns-the-bucket-pattern)[](https://www.linkedin.com/shareArticle?mini=true&url=https://www.mongodb.com/company/blog/building-with-patterns-the-bucket-pattern&title=Building with Patterns: The Bucket Pattern&summary=Learn about the Bucket Schema Design pattern in MongoDB. This pattern is used to group similar documents together for easier aggregation.&source=MongoDB)[](https://reddit.com/submit?url=https://www.mongodb.com/company/blog/building-with-patterns-the-bucket-pattern&title=Building with Patterns: The Bucket Pattern)[](https://twitter.com/intent/tweet?url=https://www.mongodb.com/company/blog/building-with-patterns-the-bucket-pattern&text=Building with Patterns: The Bucket Pattern)

[**← Previous**Five Minute MongoDB: Why Documents? The document is the natural representation of data . We only broke data up into rows and columns back in the 70s as a way to optimize data access. Back then, storage and compute power was expensive and so it made sense to use developer time to reduce the data set into a schema of rows and column, interlinked by relationships and then normalized between tables to reduce duplication. This process was cost-effective then and so it came to dominate database thinking. That domination means that many people accept the burden of defining rows and columns as an essential part of using databases. In many ways though, relational databases are still expecting the designer and developer to pre-chew the data for easier processing by the database. The Document Alternative January 29, 2019](/blog/post/five-minute-mongodb-why-documents)

[**Next →**Unlock AI With MongoDB and LTIMindtree’s BlueVerse Foundry  Many enterprises are eager to capitalize on gen AI to transform operations and stay competitive, but most remain stuck in proofs of concept that never scale. The problem isn’t ambition. It’s architecture. Rigid legacy systems, brittle pipelines, and fragmented data make it hard to move from idea to impact. That’s why LTIMindtree partnered with MongoDB to create BlueVerse Foundry : a no-code, full-stack AI platform powered by MongoDB Atlas , built to help enterprises quickly go from prototype to production without compromising governance, performance, or flexibility. The power of MongoDB: Data without limits At the heart of this platform is MongoDB Atlas, a multi-cloud database that redefines how enterprises manage and use data for AI. Unlike traditional relational databases, MongoDB’s document model adapts naturally to complex, evolving data, without the friction of rigid schemas or heavy extract, transform, and load pipelines. For AI workloads that rely on diverse formats like vector embeddings, images, or audio, MongoDB is purpose built. Its real-time data capabilities eliminate delays and enable continuous learning and querying. Search is another differentiator. With MongoDB Atlas Search and Atlas Vector Search , MongoDB enables enterprises to combine semantic and keyword queries for highly accurate, context-aware results. GraphRAG adds another layer, connecting relationships in data through retrieval-augmented generation (RAG) to reveal deeper insights. Features like semantic caching ensure performance remains high even under pressure, while built-in support for both public and private cloud deployments makes it easy to scale. Together, these capabilities turn MongoDB from a data store into an AI acceleration engine, supporting everything from retrieval to real-time interaction to full-stack observability. The challenge: Building with limitations Traditional systems were never designed for the kind of data modern AI requires. As enterprises embrace gen AI models that integrate structured and unstructured data, legacy infrastructure shows its cracks. Real-time processing becomes cumbersome, multiple environments create redundancy, and rising computing needs inflate costs. Building AI solutions often demands complex coding, meticulous model training, and extensive infrastructure planning, resulting in a delayed time to market. Add to that the imperative of producing responsible AI, and the challenge becomes even steeper. Models must not only perform but also be accurate, unbiased, and aligned with ethical standards. Enterprises are left juggling AI economics, data security, lineage tracking, and governance, all while trying to deliver tangible business value. This is precisely why a flexible, scalable, and AI-ready data foundation like MongoDB is critical. Its ability to handle diverse data types and provide real-time access directly addresses the limitations of traditional systems when it comes to gen AI. The solution: A smarter way to scale AI With BlueVerse Foundry and MongoDB Atlas, enterprises get the best of both worlds: LTIMindtree’s rapid no-code orchestration and MongoDB’s flexible, scalable data layer. This joint solution eliminates common AI bottlenecks and accelerates deployment, without the need for complex infrastructure or custom code. BlueVerse Foundry’s modular, no-code architecture enables enterprises to quickly build, deploy, and scale AI agents and apps without getting bogged down by technical complexity. This is significantly amplified by MongoDB’s inherent scalability, schema flexibility, and native RAG capabilities, which were key reasons for LTIMindtree choosing MongoDB as the foundational data layer. With features like the no-code agent builder, agent marketplace, and business-process-automation blueprints, enterprises can create tailored solutions that are ready for production, all powered by MongoDB Atlas. A synergistic partnership: Smarter together The collaboration between MongoDB and LTIMindtree’s BlueVerse Foundry brings together powerful AI capabilities with a future-ready database backbone. This partnership highlights how MongoDB’s AI narrative and broader partner strategy focus on enabling enterprises to build intelligent applications faster and more efficiently. Together, they simplify deployment, enable seamless integration with existing systems, and create a platform that can scale effortlessly as enterprise needs evolve. What makes this partnership stand out is the ability to turn ideas into impact faster. With no-code tools, prebuilt agents, and MongoDB’s flexible data model, enterprises don’t need to wait months to see results. They can use their existing infrastructure, plug in seamlessly, and start delivering real-time AI-driven insights almost immediately. Governance, performance, and scalability aren’t afterthoughts; they’re built into every layer of this ecosystem. “We’re seeing a shift from experimentation to execution—enterprises are ready to scale gen AI, but they need the right data foundation,” said Haim Ribbi, Vice President of Global CSI, VAR and Tech Partner at MongoDB. “That’s where MongoDB Atlas fits in, and where an agentic platform like LTIMindtree’s BlueVerse Foundry uses it to its full potential for innovation.” Real-world impact: From data to differentiated experiences This joint solution is already delivering real-world impact. A leading streaming platform used LTIMindtree’s solution, powered by MongoDB, to personalize content recommendations in real time. With MongoDB handling the heavy lifting of diverse data management and live queries, the company saw a 30% rise in user engagement and a 20% improvement in retention. Central to this transformation is the platform’s content hub, which acts as a unified data catalog, organizing enterprise information so it’s accessible, secure, and ready to power next-generation AI solutions with MongoDB’s robust data management. Whether dealing with text, images, or audio, the platform seamlessly manages multimodal data, eliminating the need for separate systems or processes. For businesses looking to accelerate development, BlueVerse Foundry and Marketplace offer a no-code builder, prebuilt agents, and templates, enabling teams to go from concept to deployment in a fraction of the time compared to traditional methods. BlueVerse Foundry’s RAG pipelines simplify building smart applications, using MongoDB Atlas Search and MongoDB Atlas Vector Search for highly effective RAG. Advanced orchestration connects directly with AI models, enabling rapid experimentation and deployment. A globally acclaimed media company has been using BlueVerse Foundry to automate content tagging and digital asset management, cutting its discovery time by 40% and reducing overheads by 15%—clear evidence of gen AI’s bottom-line impact when implemented right. BlueVerse Foundry’s strength lies in combining speed and control. By providing everything from ready-to-use user-experience kits, over 25 plug-and-play microservices, token-based economic models, 100+ safe listed large language models (LLMs), tools and agents, and full-stack observability, BlueVerse Foundry and Marketplace enables enterprises to move faster without losing sight of governance. Its support for voice interfaces, regional languages, Teams, mobile, and wearables like Meta AI Glasses ensures an omnichannel experience out of the box. Responsible AI: A built-in capability LTIMindtree doesn’t just build AI faster; it builds it responsibly. With built-in measures like LLM output evaluation, moderation, and audit trails, the platform ensures enterprises can trust the results their models generate. This is further supported by MongoDB’s robust security features and data governance capabilities, ensuring a secure and ethical AI ecosystem. It’s not just about preventing hallucinations or bias; it’s about creating an ecosystem where quality, transparency, and ethics are fundamental, not optional. Scaling: Streamlined for the long term The platform’s libraries, app galleries, and FinOps tooling enable businesses to test, deploy, and expand with confidence. Powered by MongoDB Atlas’s inherent scalability and multi-cloud flexibility, BlueVerse Foundry is built for long-term AI success, not just early experimentation. Enterprise AI: From possibility to production The BlueVerse Foundry and Marketplace, powered by MongoDB, is more than a technological partnership; it’s a new standard for enterprise AI. It combines deep AI expertise with an agile data foundation, helping organizations escape the trap of endless proofs of concept and unlock meaningful value. For enterprises still unsure about gen AI’s return on investment, this solution offers a proven path forward, grounded in real-world success, scalability, and impact. The future of AI isn’t something to wait for. With LTIMindtree and MongoDB, it’s already here. Explore how LTIMindtree and MongoDB are transforming gen AI from a concept into an enterprise-ready reality. Learn more about building AI applications with MongoDB through the AI Learning Hub . September 15, 2025](/company/blog/innovation/unlock-ai-with-mongodb-ltimindtrees-blueverse-foundry)
