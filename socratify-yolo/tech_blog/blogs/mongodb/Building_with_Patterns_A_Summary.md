---
title: "Building with Patterns: A Summary"
company: "mongodb"
url: "https://www.mongodb.com/blog/post/building-with-patterns-a-summary"
type: "direct_systems_collection"
date: "2025-09-15"
---

# Building with Patterns: A Summary

[Learn More About MongoDB at MongoDB University](https://university.mongodb.com?jmp=blog)

Daniel Coupal and Ken W. Alger  
April 26, 2019 | Updated: April 24, 2025  


**This post is also available in:[Deutsch](https://www.mongodb.com/blog/post/building-with-patterns-a-summary-de), [Français](https://www.mongodb.com/blog/post/building-with-patterns-a-summary-fr), [Español](https://www.mongodb.com/blog/post/building-with-patterns-a-summary-es), [Português](https://www.mongodb.com/blog/post/building-with-patterns-a-summary-br), [日本人](https://www.mongodb.com/blog/post/building-with-patterns-a-summary-jp).**

As we wrap up the _Building with Patterns_ series, it’s a good opportunity to recap the problems the patterns that have been covered solve and highlight some of the benefits and trade-offs each pattern has. The most frequent question that is asked about schema design patterns, is “I’m designing an application to do X, how do I model the data?” As we hope you have discovered over the course of this blog series, there are a lot of things to take into consideration to answer that. However, we’ve included a _Sample Use Case_ chart that we’ve found helpful to at least provide some initial guidance on data modeling patterns for generic use cases.

## Sample Use Cases

The chart below is a guideline for what we’ve found after years of experience working with our customers of what schema design patterns are used in a variety of applications. This is not a “set in stone” set of rules about which design pattern can be used for a particular type of application. Ensure you look at the ones that are frequently used in your use case. However, don't discard the other ones, they may still apply. How you design your application’s data schema is very dependent on your data access patterns.

![Use Cases vs Patterns Matrix](https://webassets.mongodb.com/_com_assets/cms/patternsmatrix-xv1kqjlrpb.png)

## Design Pattern Summaries

### Approximation

The [Approximation Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-approximation-pattern) is useful when expensive calculations are frequently done and when the precision of those calculations is not the highest priority.

###### Pros

  * Fewer writes to the database.
  * Maintain statistically valid numbers.



###### Cons

  * Exact numbers aren’t being represented.
  * Implementation must be done in the application.



### Attribute

The [Attribute Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-attribute-pattern) is useful for problems that are based around having big documents with many similar fields but there is a subset of fields that share common characteristics and we want to sort or query on that subset of fields. When the fields we need to sort on are only found in a small subset of documents. Or when both of those conditions are met within the documents.

###### Pros

  * Fewer indexes are needed.
  * Queries become simpler to write and are generally faster.



### Computed

When there are very read intensive data access patterns and that data needs to be repeatedly computed by the application, the [Computed Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-computed-pattern) is a great option to explore.

###### Pros

  * Reduction in CPU workload for frequent computations.
  * Queries become simpler to write and are generally faster.



###### Cons

  * It may be difficult to identify the need for this pattern.
  * Applying or overusing the pattern should be avoided unless needed.



### Document Versioning

When you are faced with the need to maintain previous versions of documents in MongoDB, the [Document Versioning](https://www.mongodb.com/blog/post/building-with-patterns-the-document-versioning-pattern) pattern is a possible solution. 

###### Pros

  * Easy to implement, even on existing systems.
  * No performance impact on queries on the latest revision.



###### Cons

  * Doubles the number of writes.
  * Queries need to target the correct collection.



### Extended Reference

You will find the [Extended Reference](https://www.mongodb.com/blog/post/building-with-patterns-the-extended-reference-pattern) pattern most useful when your application is experiencing lots of JOIN operations to bring together frequently accessed data. 

###### Pros

  * Improves performance when there are a lot of JOIN operations.
  * Faster reads and a reduction in the overall number of JOINs.



###### Cons

  * Data duplication.



### Outlier

Do you find that there are a few queries or documents that don’t fit into the rest of your typical data patterns? Are these exceptions driving your application solution? If so, the [Outlier Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-outlier-pattern) is a wonderful solution to this situation. 

###### Pros

  * Prevents a few documents or queries from determining an application’s solution.
  * Queries are tailored for “typical” use cases, but outliers are still addressed.



###### Cons

  * Often tailored for specific queries, therefore ad hoc queries may not perform well.
  * Much of this pattern is done with application code.



### Pre-allocation

When you know your document structure and your application simply needs to fill it with data, the [Pre-Allocation Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-preallocation-pattern) is the right choice. 

###### Pros

  * Design simplification when the document structure is known in advance.



###### Cons

  * Simplicity versus performance.



### Polymorphic

The [Polymorphic Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-polymorphic-pattern) is the solution when there are a variety of documents that have more similarities than differences and the documents need to be kept in a single collection. 

###### Pros

  * Easy to implement.
  * Queries can run across a single collection.



### Schema Versioning

Just about every application can benefit from the [Schema Versioning Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-schema-versioning-pattern) as changes to the data schema frequently occur in an application’s lifetime. This pattern allows for previous and current versions of documents to exist side by side in a collection.

###### Pros

  * No downtime needed.
  * Control of schema migration.
  * Reduced future technical debt.



###### Cons

  * Might need two indexes for the same field during migration.



### Subset

The [ Subset Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-subset-pattern) solves the problem of having the working set exceed the capacity of RAM due to large documents that have much of the data in the document not being used by the application. 

###### Pros

  * Reduction in the overall size of the [working set](https://docs.mongodb.com/manual/reference/glossary/#term-working-set).
  * Shorter disk access time for the most frequently used data.



###### Cons

  * We must manage the subset.
  * Pulling in additional data requires additional trips to the database.



### Tree

When data is of a hierarchical structure and is frequently queried, the [Tree Pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-tree-pattern) is the design pattern to implement.

###### Pros

  * Increased performance by avoiding multiple JOIN operations.



###### Cons

  * Updates to the graph need to be managed in the application.



## Conclusion

As we hope you have seen in this series, the MongoDB document model provides a lot of flexibility in how you model data. That flexibility is incredibly powerful but that power needs to be harnessed in terms of your application’s data access patterns. Remember that schema design in MongoDB has a tremendous impact on the performance of your application. We’ve found that performance issues can frequently be traced to poor schema design.

Keep in mind that to further enhance the power of the document model, these schema design patterns can be used together, when and if it makes sense. For example, Schema Versioning can be used in conjunction with any of the other patterns as your application evolves. With the twelve schema design patterns that have been covered, you have the tools and knowledge needed to harness the power of the document model’s flexibility.

[](https://www.facebook.com/sharer.php?u=https://www.mongodb.com/company/blog/building-with-patterns-a-summary)[](https://www.linkedin.com/shareArticle?mini=true&url=https://www.mongodb.com/company/blog/building-with-patterns-a-summary&title=Building with Patterns: A Summary&summary=A summary of all the patterns we've looked at in this series&source=MongoDB)[](https://reddit.com/submit?url=https://www.mongodb.com/company/blog/building-with-patterns-a-summary&title=Building with Patterns: A Summary)[](https://twitter.com/intent/tweet?url=https://www.mongodb.com/company/blog/building-with-patterns-a-summary&text=Building with Patterns: A Summary)

[**← Previous**MongoDB’s Official Brew Tap Now Open And Flowing We know macOS users love using Homebrew, aka Brew, "the missing package manager for macOS". Its made life so much simpler installing both open source and freely available applications - it lets anyone create a tap to make their software available. That is why we are very happy to announce that we now have our own official MongoDB Tap which makes it simpler than ever to install the latest MongoDB. April 25, 2019](/blog/post/mongodbs-official-brew-tap-now-open-and-flowing)

[**Next →**Unlock AI With MongoDB and LTIMindtree’s BlueVerse Foundry  Many enterprises are eager to capitalize on gen AI to transform operations and stay competitive, but most remain stuck in proofs of concept that never scale. The problem isn’t ambition. It’s architecture. Rigid legacy systems, brittle pipelines, and fragmented data make it hard to move from idea to impact. That’s why LTIMindtree partnered with MongoDB to create BlueVerse Foundry : a no-code, full-stack AI platform powered by MongoDB Atlas , built to help enterprises quickly go from prototype to production without compromising governance, performance, or flexibility. The power of MongoDB: Data without limits At the heart of this platform is MongoDB Atlas, a multi-cloud database that redefines how enterprises manage and use data for AI. Unlike traditional relational databases, MongoDB’s document model adapts naturally to complex, evolving data, without the friction of rigid schemas or heavy extract, transform, and load pipelines. For AI workloads that rely on diverse formats like vector embeddings, images, or audio, MongoDB is purpose built. Its real-time data capabilities eliminate delays and enable continuous learning and querying. Search is another differentiator. With MongoDB Atlas Search and Atlas Vector Search , MongoDB enables enterprises to combine semantic and keyword queries for highly accurate, context-aware results. GraphRAG adds another layer, connecting relationships in data through retrieval-augmented generation (RAG) to reveal deeper insights. Features like semantic caching ensure performance remains high even under pressure, while built-in support for both public and private cloud deployments makes it easy to scale. Together, these capabilities turn MongoDB from a data store into an AI acceleration engine, supporting everything from retrieval to real-time interaction to full-stack observability. The challenge: Building with limitations Traditional systems were never designed for the kind of data modern AI requires. As enterprises embrace gen AI models that integrate structured and unstructured data, legacy infrastructure shows its cracks. Real-time processing becomes cumbersome, multiple environments create redundancy, and rising computing needs inflate costs. Building AI solutions often demands complex coding, meticulous model training, and extensive infrastructure planning, resulting in a delayed time to market. Add to that the imperative of producing responsible AI, and the challenge becomes even steeper. Models must not only perform but also be accurate, unbiased, and aligned with ethical standards. Enterprises are left juggling AI economics, data security, lineage tracking, and governance, all while trying to deliver tangible business value. This is precisely why a flexible, scalable, and AI-ready data foundation like MongoDB is critical. Its ability to handle diverse data types and provide real-time access directly addresses the limitations of traditional systems when it comes to gen AI. The solution: A smarter way to scale AI With BlueVerse Foundry and MongoDB Atlas, enterprises get the best of both worlds: LTIMindtree’s rapid no-code orchestration and MongoDB’s flexible, scalable data layer. This joint solution eliminates common AI bottlenecks and accelerates deployment, without the need for complex infrastructure or custom code. BlueVerse Foundry’s modular, no-code architecture enables enterprises to quickly build, deploy, and scale AI agents and apps without getting bogged down by technical complexity. This is significantly amplified by MongoDB’s inherent scalability, schema flexibility, and native RAG capabilities, which were key reasons for LTIMindtree choosing MongoDB as the foundational data layer. With features like the no-code agent builder, agent marketplace, and business-process-automation blueprints, enterprises can create tailored solutions that are ready for production, all powered by MongoDB Atlas. A synergistic partnership: Smarter together The collaboration between MongoDB and LTIMindtree’s BlueVerse Foundry brings together powerful AI capabilities with a future-ready database backbone. This partnership highlights how MongoDB’s AI narrative and broader partner strategy focus on enabling enterprises to build intelligent applications faster and more efficiently. Together, they simplify deployment, enable seamless integration with existing systems, and create a platform that can scale effortlessly as enterprise needs evolve. What makes this partnership stand out is the ability to turn ideas into impact faster. With no-code tools, prebuilt agents, and MongoDB’s flexible data model, enterprises don’t need to wait months to see results. They can use their existing infrastructure, plug in seamlessly, and start delivering real-time AI-driven insights almost immediately. Governance, performance, and scalability aren’t afterthoughts; they’re built into every layer of this ecosystem. “We’re seeing a shift from experimentation to execution—enterprises are ready to scale gen AI, but they need the right data foundation,” said Haim Ribbi, Vice President of Global CSI, VAR and Tech Partner at MongoDB. “That’s where MongoDB Atlas fits in, and where an agentic platform like LTIMindtree’s BlueVerse Foundry uses it to its full potential for innovation.” Real-world impact: From data to differentiated experiences This joint solution is already delivering real-world impact. A leading streaming platform used LTIMindtree’s solution, powered by MongoDB, to personalize content recommendations in real time. With MongoDB handling the heavy lifting of diverse data management and live queries, the company saw a 30% rise in user engagement and a 20% improvement in retention. Central to this transformation is the platform’s content hub, which acts as a unified data catalog, organizing enterprise information so it’s accessible, secure, and ready to power next-generation AI solutions with MongoDB’s robust data management. Whether dealing with text, images, or audio, the platform seamlessly manages multimodal data, eliminating the need for separate systems or processes. For businesses looking to accelerate development, BlueVerse Foundry and Marketplace offer a no-code builder, prebuilt agents, and templates, enabling teams to go from concept to deployment in a fraction of the time compared to traditional methods. BlueVerse Foundry’s RAG pipelines simplify building smart applications, using MongoDB Atlas Search and MongoDB Atlas Vector Search for highly effective RAG. Advanced orchestration connects directly with AI models, enabling rapid experimentation and deployment. A globally acclaimed media company has been using BlueVerse Foundry to automate content tagging and digital asset management, cutting its discovery time by 40% and reducing overheads by 15%—clear evidence of gen AI’s bottom-line impact when implemented right. BlueVerse Foundry’s strength lies in combining speed and control. By providing everything from ready-to-use user-experience kits, over 25 plug-and-play microservices, token-based economic models, 100+ safe listed large language models (LLMs), tools and agents, and full-stack observability, BlueVerse Foundry and Marketplace enables enterprises to move faster without losing sight of governance. Its support for voice interfaces, regional languages, Teams, mobile, and wearables like Meta AI Glasses ensures an omnichannel experience out of the box. Responsible AI: A built-in capability LTIMindtree doesn’t just build AI faster; it builds it responsibly. With built-in measures like LLM output evaluation, moderation, and audit trails, the platform ensures enterprises can trust the results their models generate. This is further supported by MongoDB’s robust security features and data governance capabilities, ensuring a secure and ethical AI ecosystem. It’s not just about preventing hallucinations or bias; it’s about creating an ecosystem where quality, transparency, and ethics are fundamental, not optional. Scaling: Streamlined for the long term The platform’s libraries, app galleries, and FinOps tooling enable businesses to test, deploy, and expand with confidence. Powered by MongoDB Atlas’s inherent scalability and multi-cloud flexibility, BlueVerse Foundry is built for long-term AI success, not just early experimentation. Enterprise AI: From possibility to production The BlueVerse Foundry and Marketplace, powered by MongoDB, is more than a technological partnership; it’s a new standard for enterprise AI. It combines deep AI expertise with an agile data foundation, helping organizations escape the trap of endless proofs of concept and unlock meaningful value. For enterprises still unsure about gen AI’s return on investment, this solution offers a proven path forward, grounded in real-world success, scalability, and impact. The future of AI isn’t something to wait for. With LTIMindtree and MongoDB, it’s already here. Explore how LTIMindtree and MongoDB are transforming gen AI from a concept into an enterprise-ready reality. Learn more about building AI applications with MongoDB through the AI Learning Hub . September 15, 2025](/company/blog/innovation/unlock-ai-with-mongodb-ltimindtrees-blueverse-foundry)
