---
title: "Building with Patterns: The Bucket Pattern"
company: "mongodb"
url: "https://www.mongodb.com/blog/post/building-with-patterns-the-bucket-pattern"
content_length: 15304
type: "manual_premium_harvest"
premium: true
curated: true
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

[**Next →**3 “Lightbulb Moments” for Better Data Modeling We all know that feeling: the one where you have been wrestling with a complex problem for hours, maybe even days, and suddenly, it just clicks. It is a rush of clarity, a "lightbulb moment" that washes away the frustration and replaces it with pure, unadulterated excitement. It's the moment you realize a solution is not just possible, it is elegant. This blog post is dedicated to that feeling—the burst of insight when you discover a more intuitive, performant, and powerful way to work. We have spoken with hundreds of developers new to MongoDB to understand where they get stuck, and we have distilled their most common "Lightbulb Moments" to help you get there faster. We found that the key to getting the best performance from MongoDB is to adjust the way you think about data. Once developers recognize that the flexible document model gives them more control, not less, they become unstoppable. In this inaugural post of our new “Lightbulb Moments” blog series, we will walk you through three essential data modeling tips on schema validation and versioning, the aggregation pipeline framework, and the the Single Collection Pattern. These concepts will help you structure your data for optimal performance in MongoDB and lead to your own "Lightbulb Moments," showing you how to build fast, efficient, and scalable applications. 1\. Schema validation and versioning: Flexibility with control A common misconception about MongoDB is that its underlying document model is “schemaless.” With MongoDB, your schema is flexible and dependent on the needs of your application. If your workload demands a more structured schema, you can create validation rules for your fields with schema validation. If your schema requires more flexibility to adapt to changes over time, you can apply the schema versioning pattern. db.createCollection("students", { validator: { $jsonSchema: { bsonType: "object", title: "Student Object Validation", required: [ "address", "major", "name", "year" ], properties: { name: { bsonType: "string", description: "'name' must be a string and is required" }, year: { bsonType: "int", minimum: 2017, maximum: 3017, description: "'year' must be an integer in [ 2017, 3017 ] and is required" }, gpa: { bsonType: [ "double" ], description: "'gpa' must be a double if the field exists" } } } } } ) MongoDB has offered schema validation since 2017, providing as much structure and enforcement as a traditional relational database. This feature allows developers to define validation rules for their collections using the industry-standard JSON Schema. Schema validation gives you the power to: Ensure every new document written to a collection conforms to a defined structure. Specify required fields and their data types, including for nested documents. Choose the level of strictness, from off to strict , and whether to issue a warning or an error when a document fails validation. The most powerful feature, however, is schema versioning . This pattern allows you to: Gradually evolve your data schema over time without downtime or the need for migration scripts. Support both older and newer document versions simultaneously by defining multiple schemas as valid within a single collection using the oneOf operator. db.contacts.insertOne( { _id: 2, schemaVersion: 2, name: "Cameron", contactInfo: { cell: "903-555-1122", work: "670-555-7878", instagram: "@camcam9090", linkedIn: "CameronSmith123" } } ) Performance problems can stem from poor schema design—not the database. One example from a financial services company showed that proper schema design improved query speed from 40 seconds to 377 milliseconds. The ability to enforce a predictable structure while maintaining the flexibility of the document model gives developers the best of both worlds. For a deeper dive: See an example of schema optimization in MongoDB Design Reviews: how applying schema design best practices resulted in a 60x performance improvement by Staff Developer Advocate, Graeme Robinson. Learn how to use MongoDB Compass to analyze, export, and generate schema validation rules. 2\. Aggregation pipeline framework: Simplifying complex data queries In SQL, developers often use JOINs to aggregate data across multiple tables. As joins stack up, queries can become slow and operationally expensive. Some may attempt a band-aid solution by querying each table separately and manually aggregating the data in their programming language, but this can introduce additional latency. MongoDB's Aggregation Framework provides a much simpler alternative. Instead of a single, complex query, you can break down your logic into an Aggregation Pipeline , or a series of independent pipeline stages. This approach offers several advantages: Easier to debug: Each pipeline stage can be developed and tested independently. Visual query building: MongoDB's stage-based Aggregation Pipeline simplifies query visualization compared to SQL. Tools like the Pipeline Builder in Atlas and Compass make it easy to build complex queries with stages like $match , $group , and $sort , while analyzing performance in real-time. Fewer joins: The framework's design encourages a schema that reduces the need for joins in the first place, as data that is accessed together should be stored together. When you do need to pull data from another collection, the $lookup operator handles it easily. Figure 1. MongoDB Compass aggregation pipeline builder. The ability to decompose complex queries into independent stages is a powerful new experience that long-time SQL users will find far smoother. For more information and case studies, see: MongoDB official resources on Aggregation and Aggregation Operations . Take a free, one-hour MongoDB Skills course on Fundamentals of Data Transformation to learn how to build aggregation pipelines to process, transform, and analyze data efficiently in MongoDB. Aggregation Optimization in MongoDB: A Case Study From the Field (Part 1) by Staff Developer Advocate, Graeme Robinson. 3\. The Single Collection Pattern: Storing data together for faster queries Many developers new to MongoDB create a separate collection for each entity. If someone were building a new book review app, they might have collections for books , reviews , and users . While this seems logical at first, it can lead to slow queries that require expensive $lookup operations or multiple queries to gather all the data for a single view, which can slow down your overall app and increase your database costs. A more efficient approach is to use the Single Collection Pattern. This pattern helps model many-to-many relationships when embedding is not an option. It lets you store all related data in a single collection, avoiding the need for data duplication when the costs outweigh the benefits. This approach adheres to three defining characteristics: All related documents that are frequently accessed together are stored in the same collection. Relationships between the documents are stored as pointers or other structures within the document. An index is built on a field or array that maps the relationships between documents. Such an index supports retrieving all related documents in a single query without database join operations. When using this pattern, you can add a docType field (e.g., book, review, user) and use a relatedTo array to link all associated documents to a single ID. This approach offers significant advantages: Faster queries: A single query can retrieve a book, all of its reviews, and user data. No joins: This eliminates the need for expensive joins or multiple database trips. Improved performance: Queries are fast because all the necessary data lives in the same collection. For developers struggling with slow MongoDB queries, understanding this pattern is a crucial step towards better performance. For more details and examples, see: Building with Patterns: The Single Collection Pattern by Staff Senior Developer Advocate, Daniel Coupal. Take a free, one-hour MongoDB Skills course on Schema Design Optimization . Get started with MongoDB Atlas for free today. Start building your MongoDB skills through the MongoDB Atlas Learning Hub . September 15, 2025](/company/blog/technical/3-lightbulb-moments-for-better-data-modeling)
