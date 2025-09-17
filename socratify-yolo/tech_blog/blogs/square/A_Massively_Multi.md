---
title: "A Massively Multi"
author: "Unknown"
url: "https://developer.squareup.com/blog/a-massively-multi-user-datastore-synced-with-mobile-clients"
date: "2025-09-15"
---

April 12, 2018 | 6 minute read

# A Massively Multi-user Datastore, Synced with Mobile Clients

### At Square, we manage large amounts of information for our merchants. This includes the data surrounding what a merchant sells — their…

![Twitter](/blog/images/twitter-icon.svg)![Facebook](/blog/images/facebook-icon.svg)![Reddit](/blog/images/reddit-icon.svg)![LinkedIn](/blog/images/linkedin-icon.svg)

At Square, we manage large amounts of information for our merchants. This includes the data surrounding what a merchant sells — their products, prices, taxes, and the configurations associated with those entities. We refer to this dataset as a merchant’s _catalog_.

Managing this data can be challenging. Merchants’ catalogs can be quite large. They must be synced with mobile devices which may be offline for extended periods of time, allowing the two versions of the catalog to diverge. Catalogs need a sophisticated query interface to support a responsive web UI, but they also need to support large bulk operations via API, including re-writing the entire data set. Additionally, the data needs structure to allow it to display and function properly across a variety of services and mobile clients, but it also needs enough flexibility to allow rapid development of new features, and to enable merchants and third parties to create custom data specific to their business or integration.

We recently re-architected the system that we use for storing catalog data, and are writing this article to share some of our learnings. We needed a number of the features offered by traditional databases. For example, we needed to write data without impacting reads until the entire operation is complete (even across multiple API calls). We wanted to be able to page through data consistently even if other clients are writing to the catalog. These features needed to be per-user, so that activity by one user would not impact another. At the same time, we needed much more structure than a traditional database would provide, while still allowing new elements to be added without the need for a schema change, re-deploy or migration.

We accomplished this by using an _entity-attribute-value_ data model, where entities have types which may be system defined and attributes that follow specific attribute definitions, which may be system or user defined. By using an append-only data model, we were able to achieve the transactionality properties that we needed without relying on transactions in the underlying sharded MySql database, which we chose as a storage infrastructure due to strong institutional support.

## Merchant datastore design

## Structured, but Flexible

We needed an object model that was structured enough to allow clients to handle data in predictable formats, but which had enough flexibility to allow clients, integrators, and even end-users to extend the data model for their own use cases. We settled on an entity-attribute-value store with a few characteristic features. The model could be represented as follows:

![](//images.ctfassets.net/1wryd5vd9xez/bKDY3oyaQ9ZUEHC3R7na0/c56859049760896b87bf6ab850020c5e/https___cdn-images-1.medium.com_max_2000_1_VwrAJm_Td8EW8yX1o2MUSg.png)

Each object has a unique token and a predefined type. It has a set of attributes, which must use a predefined definition. An attribute definition specifies the type of the attribute and is used by clients to validate and interpret the attribute data. It is namespaced in a way that identifies its owner. Definitions and (eventually) types can be created via API. The same definition can appear in multiple attributes, allowing for sets of values to be represented. Attributes can reference other objects by their tokens, allowing for more complex data to be represented through related objects. We will discuss location overrides below.

## Features

One of the key values of this model is that it allows clients to operate with structured data which they understand, while allowing indefinite extensibility. New object types can be added with ease, including allowing clients to create new object types via API. Likewise, new attribute definitions can be added via API. Having attributes definitions namespaced (according to the Java package convention) makes it easy to distinguish the owner of the attribute definition, and can be used to prevent non-owners from overwriting definitions. For efficiency and consistency, standard types and definitions are shared across all users, while user created types are only visible to the individual user.

One domain-specific behavior that we wanted to support in a first-class fashion is the concept of the location. Within our user model, a merchant may have multiple physical or virtual locations where they conduct business. Some clients are location-aware, which means that they only need to have the data particular to a specific location, while others are merchant-aware, meaning that they need visibility into all locations. Values on the same object can also vary by location, for example, the same product might have different prices in different locations. We support this by giving each attribute a location value, which is global by default. When a location-aware client requests data, we send only the global attributes and attributes for the client’s location, allowing the client to operate on a smaller and simpler data set. Merchant aware clients must handle the complexity of values which may have different values at different locations. Objects can also be entirely removed from individual locations through a special “enabled” attribute, which can toggle availability.

## Synchronizable Constraints

One of the more interesting features of our datastore is its use of synchronizable constraints. Having data with a constant structure is key to building clients that can understand and use it properly. Constraints ensure that clients can expect data to have a given format, and protects them from other clients creating or modifying data in an unexpected way.

Instead of relying on database level constraints which require schema changes to alter, we wanted constraints to be easy to introduce while maintaining consistent behavior across the core datastore and mobile clients. For this reason, we modeled constraints as catalog objects themselves, which allows them to be created via API and synced with mobile clients. In this way, a client creating a new object type or attribute definition could create new constraints ensuring that it has the specified structure.

Constraints are built on special global attributes that trigger software validations that must be built on mobile clients as well as the core service. They provide for validations ranging from requiring attributes, to specifying valid integer ranges, to regular expression matches, to requiring that references not be broken, to cascading deletions if a referenced object is deleted. Put together, they create a large palette of options that enables object structure to be tightly constrained.

Allowing these constraints to be synced to clients enables clients to enforce constraints as soon as a violation takes place, rather than waiting for the invalid object to be sent to the server to receive an error message. This speeds debugging, and, in the unfortunate case where code that creates invalid objects is released, limits the potential impact of that bug on customers.

## Rollback and History

At the core of the merchant catalog is an append-only data model. When a request is received to delete or modify an object, entities are marked as having been deleted by the request in question, and are not returned in future requests. This is made relatively efficient by handling modifications by creating deletions at the attribute level. Thus, a request that modifies a single attribute only creates one new attribute entry, rather than an entire new object.

This data model allows a number of useful features. For example, a response to a query to page through the merchants data includes a paging token that encodes the current catalog version. Requests for additional pages with the same token will ignore deletions and creations that took place after that version, allowing for consistent paging.

This tooling is easily extended to allow a historic lookback of a catalog as of a specific request. Supplying a specific catalog version (which is incremented with each write request) makes it possible to view the entire catalog as it existed at that point in time. It also makes it possible to query the set of changes after that point in time, which makes it trivial to revert those changes, and restore a catalog to a previous version. Because rollbacks are themselves append-only changes to the datastore, they can be reverted in turn.

This same functionality makes it possible to expose user level transactions. As an optional parameter, a put request can request to open a transaction. If a transaction is opened, the merchant’s catalog is locked with a token that is returned to the client. Other attempts to write the catalog are blocked while the catalog is locked, and requests to read receive that catalog as of the lock version without any incremental changes. Additional writes with the token update the lock version, allowing changes to continue inside the transaction for as long as necessary without impacting other users. When the transaction is completed, the lock is removed, and all operations access the catalog with the modifications from the transaction.

If a request is received to roll back the transaction, all changes made after the lock version are deleted, and there are no side effects from the aborted transaction. Likewise, if a client that opens a transaction does not make any write calls within a timeout, the transaction is automatically rolled back. This allows long running operations, such as the import of new catalog data, to execute atomically, and allows clients to always read the catalog as of a clean version.

Finally, this model provides auditability. Because every write is tagged with information about the caller, it becomes possible not only to view the catalog as of a certain period, but to attribute specific changes to specific callers. This is a great help in debugging clients that make unexpected changes to a catalog, and also makes it possible for users to know the individual responsible for specific modifications.

## Conclusion

While the merchant catalog datastore was designed for our specific needs, it has a number of behaviors which may be of use for other applications. Specifically, using an append-only datastore enables a number of useful behaviors which greatly increase the flexibility of the platform. APIs for creating attribute definitions and syncable constraints allow data to be structured and validated while enabling multiple parties to independently iterate on their own parts of the model. We hope that our learnings may be useful to others facing similar problems.

#### Authored By

![Picture of Tad Book](https://images.ctfassets.net/1wryd5vd9xez/7pNFB6oaDfyIupL95wk7Zl/1d4e64b0ab19420fa3e7c3a63cf6749d/Tad_Book.jpeg?w=50&h=50&fl=progressive&q=100&fm=jpg)

**Tad Book**

#### Tags

[Software Architecture](/blog/archive/tags/software-architecture/)[Engineering](/blog/archive/tags/engineering/)[APIs](/blog/archive/tags/api/)[Developer](/blog/archive/tags/developer/)

[![Twitter](/blog/images/twitter-icon.svg)Discuss on Twitter](https://twitter.com/search?q=developer.squareup.com%2Fblog%2Fa-massively-multi-user-datastore-synced-with-mobile-clients)[![Discord](/blog/images/discord-gray.svg)Join our Discord](https://discord.gg/squaredev)

Table Of Contents

* Merchant datastore design
* Structured, but Flexible
* Features
* Synchronizable Constraints
* Rollback and History
* Conclusion
