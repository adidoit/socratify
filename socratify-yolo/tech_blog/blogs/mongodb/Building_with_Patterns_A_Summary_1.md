---
title: "Building with Patterns: A Summary"
company: "mongodb"
url: "https://www.mongodb.com/blog/post/building-with-patterns-a-summary"
content_length: 17925
type: "manual_premium_harvest"
premium: true
curated: true
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

[**Next →**3 “Lightbulb Moments” for Better Data Modeling We all know that feeling: the one where you have been wrestling with a complex problem for hours, maybe even days, and suddenly, it just clicks. It is a rush of clarity, a "lightbulb moment" that washes away the frustration and replaces it with pure, unadulterated excitement. It's the moment you realize a solution is not just possible, it is elegant. This blog post is dedicated to that feeling—the burst of insight when you discover a more intuitive, performant, and powerful way to work. We have spoken with hundreds of developers new to MongoDB to understand where they get stuck, and we have distilled their most common "Lightbulb Moments" to help you get there faster. We found that the key to getting the best performance from MongoDB is to adjust the way you think about data. Once developers recognize that the flexible document model gives them more control, not less, they become unstoppable. In this inaugural post of our new “Lightbulb Moments” blog series, we will walk you through three essential data modeling tips on schema validation and versioning, the aggregation pipeline framework, and the the Single Collection Pattern. These concepts will help you structure your data for optimal performance in MongoDB and lead to your own "Lightbulb Moments," showing you how to build fast, efficient, and scalable applications. 1\. Schema validation and versioning: Flexibility with control A common misconception about MongoDB is that its underlying document model is “schemaless.” With MongoDB, your schema is flexible and dependent on the needs of your application. If your workload demands a more structured schema, you can create validation rules for your fields with schema validation. If your schema requires more flexibility to adapt to changes over time, you can apply the schema versioning pattern. db.createCollection("students", { validator: { $jsonSchema: { bsonType: "object", title: "Student Object Validation", required: [ "address", "major", "name", "year" ], properties: { name: { bsonType: "string", description: "'name' must be a string and is required" }, year: { bsonType: "int", minimum: 2017, maximum: 3017, description: "'year' must be an integer in [ 2017, 3017 ] and is required" }, gpa: { bsonType: [ "double" ], description: "'gpa' must be a double if the field exists" } } } } } ) MongoDB has offered schema validation since 2017, providing as much structure and enforcement as a traditional relational database. This feature allows developers to define validation rules for their collections using the industry-standard JSON Schema. Schema validation gives you the power to: Ensure every new document written to a collection conforms to a defined structure. Specify required fields and their data types, including for nested documents. Choose the level of strictness, from off to strict , and whether to issue a warning or an error when a document fails validation. The most powerful feature, however, is schema versioning . This pattern allows you to: Gradually evolve your data schema over time without downtime or the need for migration scripts. Support both older and newer document versions simultaneously by defining multiple schemas as valid within a single collection using the oneOf operator. db.contacts.insertOne( { _id: 2, schemaVersion: 2, name: "Cameron", contactInfo: { cell: "903-555-1122", work: "670-555-7878", instagram: "@camcam9090", linkedIn: "CameronSmith123" } } ) Performance problems can stem from poor schema design—not the database. One example from a financial services company showed that proper schema design improved query speed from 40 seconds to 377 milliseconds. The ability to enforce a predictable structure while maintaining the flexibility of the document model gives developers the best of both worlds. For a deeper dive: See an example of schema optimization in MongoDB Design Reviews: how applying schema design best practices resulted in a 60x performance improvement by Staff Developer Advocate, Graeme Robinson. Learn how to use MongoDB Compass to analyze, export, and generate schema validation rules. 2\. Aggregation pipeline framework: Simplifying complex data queries In SQL, developers often use JOINs to aggregate data across multiple tables. As joins stack up, queries can become slow and operationally expensive. Some may attempt a band-aid solution by querying each table separately and manually aggregating the data in their programming language, but this can introduce additional latency. MongoDB's Aggregation Framework provides a much simpler alternative. Instead of a single, complex query, you can break down your logic into an Aggregation Pipeline , or a series of independent pipeline stages. This approach offers several advantages: Easier to debug: Each pipeline stage can be developed and tested independently. Visual query building: MongoDB's stage-based Aggregation Pipeline simplifies query visualization compared to SQL. Tools like the Pipeline Builder in Atlas and Compass make it easy to build complex queries with stages like $match , $group , and $sort , while analyzing performance in real-time. Fewer joins: The framework's design encourages a schema that reduces the need for joins in the first place, as data that is accessed together should be stored together. When you do need to pull data from another collection, the $lookup operator handles it easily. Figure 1. MongoDB Compass aggregation pipeline builder. The ability to decompose complex queries into independent stages is a powerful new experience that long-time SQL users will find far smoother. For more information and case studies, see: MongoDB official resources on Aggregation and Aggregation Operations . Take a free, one-hour MongoDB Skills course on Fundamentals of Data Transformation to learn how to build aggregation pipelines to process, transform, and analyze data efficiently in MongoDB. Aggregation Optimization in MongoDB: A Case Study From the Field (Part 1) by Staff Developer Advocate, Graeme Robinson. 3\. The Single Collection Pattern: Storing data together for faster queries Many developers new to MongoDB create a separate collection for each entity. If someone were building a new book review app, they might have collections for books , reviews , and users . While this seems logical at first, it can lead to slow queries that require expensive $lookup operations or multiple queries to gather all the data for a single view, which can slow down your overall app and increase your database costs. A more efficient approach is to use the Single Collection Pattern. This pattern helps model many-to-many relationships when embedding is not an option. It lets you store all related data in a single collection, avoiding the need for data duplication when the costs outweigh the benefits. This approach adheres to three defining characteristics: All related documents that are frequently accessed together are stored in the same collection. Relationships between the documents are stored as pointers or other structures within the document. An index is built on a field or array that maps the relationships between documents. Such an index supports retrieving all related documents in a single query without database join operations. When using this pattern, you can add a docType field (e.g., book, review, user) and use a relatedTo array to link all associated documents to a single ID. This approach offers significant advantages: Faster queries: A single query can retrieve a book, all of its reviews, and user data. No joins: This eliminates the need for expensive joins or multiple database trips. Improved performance: Queries are fast because all the necessary data lives in the same collection. For developers struggling with slow MongoDB queries, understanding this pattern is a crucial step towards better performance. For more details and examples, see: Building with Patterns: The Single Collection Pattern by Staff Senior Developer Advocate, Daniel Coupal. Take a free, one-hour MongoDB Skills course on Schema Design Optimization . Get started with MongoDB Atlas for free today. Start building your MongoDB skills through the MongoDB Atlas Learning Hub . September 15, 2025](/company/blog/technical/3-lightbulb-moments-for-better-data-modeling)
