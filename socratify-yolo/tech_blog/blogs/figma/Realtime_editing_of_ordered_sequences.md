---
title: "Realtime editing of ordered sequences"
company: "figma"
url: "https://www.figma.com/blog/realtime-editing-of-ordered-sequences/"
content_length: 14618
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

March 6, 2017

# Realtime editing of ordered sequences

![](data:image/jpeg;base64,/9j/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAUABQDASIAAhEBAxEB/8QAHAABAAEEAwAAAAAAAAAAAAAAAAUBAgMEBgcI/8QAJRAAAgIDAAAFBQEAAAAAAAAAAQIDBAAFEQYTITFhBxIVIiMy/8QAFwEAAwEAAAAAAAAAAAAAAAAAAQUGBP/EAB0RAAICAgMBAAAAAAAAAAAAAAECAAMEERIhUTH/2gAMAwEAAhEDEQA/AOwPHniCeltIKMYdYSnmSMo9SO+wzeTd1KmrNmJJQUQSElT6g5D/AFXuwVPx7CeNLDOUC+7EEZYm2i1up08d2ZI69mUIXlHQRzvMn0oLOeo8WxBT2Zz+nYW1VinQH7ZFDDvzjMcFqu8StBLG0fP1KsOYw8SJk2J4xbebC5u45rdh55C3+pD3JjxBv7+0uQ1bcoNesP5oBwD5xjK6hQcqvY9iO1iMazRlK+0vQR+XDbnRAfQBzzGMZRFF38iEM3s//9k=)![](https://cdn.sanity.io/images/599r6htc/regionalized/193b6e56f51b0c0ac8ae1fdeaab81f9f14b48531-416x416.jpg?w=416&h=416&q=75&fit=max&auto=format)

Evan WallaceCo-founder, Figma

  * [Inside Figma](https://www.figma.com/blog/inside-figma/)
  * [Behind the scenes](https://www.figma.com/blog/behind-the-scenes/)
  * [Quality & performance](https://www.figma.com/blog/quality-and-performance/)
  * [Engineering](https://www.figma.com/blog/engineering/)
  * [Product updates](https://www.figma.com/blog/product-updates/)
  * 


![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAJCAYAAAAywQxIAAAACXBIWXMAABYlAAAWJQFJUiTwAAABmElEQVQoz1WSyW7jQAxEZS29iq3W5kSyosDAOBcfJgHm/3+tpqh4JsmBILrVfCyyVBRFAY2maeDaAJMDXIro+x5dzvDewxgDaxxiFKTrGfJnh127495Ze9SeTic8WAUqHgI/hkFgtww7RMQ2QtoWMbCB8WjNjBwWyDggLBlN69BYAqM/8g9gV1W4OodJWDwKYp+QUsJZBHsMGBzhdkZyZzYQBN6pOpM8/JqZw0/gWNd4I3CmfB31drvhZdvwQuCdClcfEAj1LnDsT+W6Ctcz7wNMH3Eqyy+gpUIh1DGmecL9fsfrvmNm8eI8OjZzzDG0VN5B2EgbP19W5PN4jF2z9j+wLCuUdYVGHOSpRz+PGFi4UMlMhZ7KvRVkt6CLE0IWLNcNvz/esV02BL6xfPMYm6ZQYd3UsDP3wxEaoQkc6ZlKVGWgwtZn9O4CCRP8U8bwtmL/dcUwcGSa8s3pT6CGoXO6l8bRPYUQpi5rSJsITdxdhMvxMM9LPMz5V//12/BQcqnaRaUfinWnujsq9Y/Qs32o0VCY5u/Av+3TyeCaxKSdAAAAAElFTkSuQmCC)![](https://cdn.sanity.io/images/599r6htc/regionalized/eb174f1882c5e0b196054814f529ab9c29db709a-2120x1000.png?rect=1,0,2119,1000&w=1632&h=770&q=75&fit=max&auto=format)

One of the problems we had to solve when we added multiplayer editing to Figma was supporting simultaneous editing of ordered sequences of objects. 

One of the problems we had to solve when we added [multiplayer editing](https://blog.figma.com/multiplayer-editing-in-figma-8f8076c6c3a6) to Figma was supporting simultaneous editing of ordered sequences of objects. We have many compound object types in Figma (the document, groups, components, etc.) and each compound object has an ordered list of children. Users can insert new children, remove children, or drag them around to reorder them and everything updates in realtime:

Realtime collaborative editing of an ordered sequence in Figma

The core problem is maintaining eventual-consistency. Each client instantaneously applies its edits locally and then sends them off to the server, which then sends the edits to other connected clients. This means edits may be applied in a different order on each client. When designing the algorithm, we have to make sure the document ends up looking identical regardless of the order in which edits are applied.

## Operational transformation

We initially considered using a technique called Operational Transformation to solve this. It’s an old algorithm that was originally developed for text and was popularized by early collaborative text editors such as Google Wave. While we didn’t end up using OT, it’s perhaps the most common approach to this type of problem and it’s useful to contrast OT with our approach. In OT, new operations are carefully transformed past other concurrent operations such that the resulting operation has the same effect:

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAARCAYAAADdRIy+AAAACXBIWXMAAAsSAAALEgHS3X78AAABaklEQVQ4y41U7baDIAzb+7/p5jcg4h+4Cd4oOtzmOTlAoSEtrY91XVMIIc3znJZlSVwT3vvknMvj1aZz8rPW7raHNmggOK+BZHQkRKo9zUUYsYgwZpRzkEQoiCCIIIrTNEVjTAbtPEt/geuqQioYxzH1fZ8BohwaVRKcKx2lutuQGRaJ2rZNXdclKDrlVykgqXKv8KuEHOWgnHF95HQ9RaII6Hf7KKVdIV7VGGNT07SI5Ijip1emnQ7DMGQ11jpcwFf3UGixd0TwlZD7tJOIal6vBmMPIiqm3/nsF0I+Qvh/qBkPNKXncwDpmAm9fxfwk8KN0EOZAdkEYpPzV+b0Y9nUcujcDFUGods8V8sxt2VNVjtFHSC7uoVj2U3sHNRqRK3mOfdvFZYdUdahQttUb3VI6AexK2Tf6nbehBLJN+PwqW8VgXCNjISBH4wZ/EAQQBjQfgE5Crgs1D76XkHCFntvAPmO0n53XvgDfzYk8z6kVn0AAAAASUVORK5CYII=)![](https://cdn.sanity.io/images/599r6htc/regionalized/42f7de559f14a97ea68d9bb5fb4aae238318cda2-1400x1212.png?w=804&h=696&q=75&fit=max&auto=format)

An example of concurrent text editing using OT

In the picture above, transforming the operation _Delete(at: 1, n: 2)_ past the operation _Insert(at: 0, text: “x”)_ on the server and on client A results in a new operation _Delete(at: 2, n: 2)_. This is because the insert must affect the index of the delete to ensure that the text “bc” is still deleted. Transforming the operation _Insert(at: 0, text: “x”)_ past the operation _Delete(at: 1, n: 2)_ on client B is a no-op because the delete doesn’t affect the index of the insert.

That’s the basic idea at least. The actual implementation details are a lot more complex. They’re actually so complex that the [first paper on OT](https://scholar.google.com/scholar?q=Concurrency+control+in+groupware+systems) had some [subtle problems](https://scholar.google.com/scholar?q=A+Survey+on+Operational+Transformation+Algorithms%3A+Challenges%2C+Issues+and+Achievements) that went undiscovered for several years. The problems have since been fixed and OT is a very viable algorithm, but the high implementation cost is only worth it you need the specific benefits it offers for editing text sequences.

**Benefits:**

  * Good performance and low memory overhead for very large sequences
  * Concurrent insertions are linearized instead of interleaved (i.e. inserting “abc” and “xyz” in the same place won’t make something like “axbycz”)



Drawbacks:

  * OT is hard to understand and hard to implement correctly
  * Reordering is usually done using a delete and insert instead of a move



OT was overkill for us because we didn’t need to work with enormous sequences and we didn’t need to avoid interleaving. Reordering is also a very common operation in a layer-based design tool like ours and we wanted to make that efficient without additional complexity. With an OT system, adding more operations increases implementation complexity quadratically since every operation must transform correctly past every other operation.

## Fractional indexing

Instead of OT, Figma uses a trick that’s often used to implement reordering on top of a database. Every object has a real number as an index and the order of the children for an element of the tree is determined by sorting all children by their index. To insert between two objects, just set the index for the new object to the average index of the two objects on either side. We use arbitrary-precision fractions instead of 64-bit doubles so that we can’t run out of precision after lots of edits.

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAQCAIAAACZeshMAAAACXBIWXMAAAsSAAALEgHS3X78AAABWklEQVQoz3WT25aDIAxF+///2DWieGEqSuuN8Wk2ibaO7ZxlKSQ5yiZ6+RGt6xpj9N5/ibIsu16vmUgnGqeAMorVdTma+74vy9KK8jwvCsvFxO6i4INZNc/z4/G43+99H7zv2rZj5Gl4CJKapulYfzYPw0AR1W3r5eput44lQVIUfDbrtquqKkX7bmtjGkYipEIIlL2bN2bKC0CtNQZmVBlTMWrwMzMR7giSMvME/1LH8l/mZVnA4SI3ihS7E/HPUuNUnsyRs6hrX5bfdd2AXIvYpPIn7l08/8QcCVnrhA1UI6jFc8IbwihtL9iImA/MNEA4E2oIffqlVr3EUlIBLrwc0Msc4zL9FS3VW6iN5Z6Zx3EW9riZyTnnmqZhBKwRAaycYEsgpaTs5pwfhnEzc29lA0xHBLNO+B50ovDGcIQOzM3Mbp6NeVdq9C4pS11n/+fX86j3yDGl+gUGSYIV80JZFAAAAABJRU5ErkJggg==)![](https://cdn.sanity.io/images/599r6htc/regionalized/dc3ac373a86b1d25629d651e2b75100dc3d9fbb9-1400x1144.png?w=804&h=657&q=75&fit=max&auto=format)

An example sequence of objects being edited

In our implementation, every index is a fraction between 0 and 1 exclusive. Being exclusive is important; it ensures we can always generate an index before or after an existing index by averaging with 0 or 1, respectively. Each index is stored as a string and averaging is done using string manipulation to retain precision. For compactness, we omit the leading “0.” from the fraction and we use the entire ASCII range instead of just the numbers 0–9 (base 95 instead of base 10).

**Benefits:**

  * Easy to understand and implement
  * Reordering an object only involves editing a single value



**Drawbacks:**

  * Index length can grow over time
  * Merging new elements from multiple clients may interleave them
  * Averaging between two identical indices doesn’t work



The first drawback (index length) isn’t a concern for us since we don’t need to order huge numbers of elements. The number of reordering operations is bounded by user activity in practice, and normal usage patterns never generate prohibitively-large index lengths.

The second drawback (interleaving) would be a concern for a text editor but isn’t really a concern for us given the nature of design documents. Interleaving concurrently inserted elements in a design is usually fine because the new objects likely don’t overlap. And if interleaving looks weird, users can just manually fix the ordering afterwards.

The third drawback (averaging identical indices) has a simple workaround that avoids this problem entirely. This case arises when two clients try to simultaneously insert a new object between the same two objects. The server can avoid ever having two objects with an identical position by just generating and assigning a unique position to the second insert operation.

We’ve been using fractional indexing for multiplayer editing in Figma from the beginning and it’s worked out really well for us. Even though OT provides some additional benefits around performance and interleaving, it’s much more beneficial for the Figma platform to use simple algorithms that are easy to understand and implement than to use the most advanced algorithms out there. It means more people can work on Figma, the implementation is more stable, and we can develop and ship features faster.

_Like thinking about realtime collaboration? Figma is building a browser-based collaborative design tool, and[we’re hiring!](https://www.figma.com/careers/)_

![](data:image/jpeg;base64,/9j/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAUABQDASIAAhEBAxEB/8QAHAABAAEEAwAAAAAAAAAAAAAAAAUBAgMEBgcI/8QAJRAAAgIDAAAFBQEAAAAAAAAAAQIDBAAFEQYTITFhBxIVIiMy/8QAFwEAAwEAAAAAAAAAAAAAAAAAAQUGBP/EAB0RAAICAgMBAAAAAAAAAAAAAAECAAMEERIhUTH/2gAMAwEAAhEDEQA/AOwPHniCeltIKMYdYSnmSMo9SO+wzeTd1KmrNmJJQUQSElT6g5D/AFXuwVPx7CeNLDOUC+7EEZYm2i1up08d2ZI69mUIXlHQRzvMn0oLOeo8WxBT2Zz+nYW1VinQH7ZFDDvzjMcFqu8StBLG0fP1KsOYw8SJk2J4xbebC5u45rdh55C3+pD3JjxBv7+0uQ1bcoNesP5oBwD5xjK6hQcqvY9iO1iMazRlK+0vQR+XDbnRAfQBzzGMZRFF38iEM3s//9k=)![](https://cdn.sanity.io/images/599r6htc/regionalized/193b6e56f51b0c0ac8ae1fdeaab81f9f14b48531-416x416.jpg?w=416&h=416&q=75&fit=max&auto=format)

Evan Wallace is the co-founder and former Chief Technology Officer at Figma.

[Twitter](https://twitter.com/evanwallace)

## Subscribe to Figma’s editorial newsletter

Enter email*

I agree to opt-in to Figma's mailing list.*

By clicking “Submit” you agree to our [TOS](https://www.figma.com/tos/) and [Privacy Policy](https://www.figma.com/privacy/).

## Related articles

  * [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAJCAYAAAAywQxIAAAACXBIWXMAABYlAAAWJQFJUiTwAAABiElEQVQoz62SN4oqUBSGjWBAEQwYEHNEzIgKIjY2xkrEQlCxsLEVA7oEC0GwEcFtWFi5ADf0Pe6FKd6M001x4HCL7/zhKhQKBWK0Wi2JRIJut0utViMQCBCNRgkGg8RiMXK5HNVqlfV6zfF4pN/vk06ncbvdqNVqvjiKr0Wj0RCJRGg2m5TLZUKhEIVCgWKxSCqVol6v0+v1mM/nzGYzuU8mExqNBnq9/idQpVLhcrkolUokk0mpajqdstvtGAwGLJdLTqeThIhjQvFisaDVamE0Gn8CxdhsNqkqHo+Tz+c5n8+8Xi/2+z3b7Zbn88nlcpEwh8NBJpORkYi4PgLNZrPM0e/3k81muV6vvN9vNpsNnU6H2+3G4/FgPB5jt9sxmUwYDAaUSuVnoMfjod1uy/CFytVqxf1+ZzQayUPD4ZDD4SBtWq1WaVWn030GikfRqshIQL1eL5VKRbYpShFxiEbD4TBOp1MWIWDC7q9Ai8UioT6fT1oREQiQUCK+hiju+3yD/W/5L+Yf6TYFTxjlbEMAAAAASUVORK5CYII=)![](https://cdn.sanity.io/images/599r6htc/regionalized/f5e0b63326f08745f246b676731c5ad01bc92b59-2120x1000.png?w=528&h=249&q=75&fit=max&auto=format)18 designers predict UI/UX trends for 2018December 15, 2017By Valerie VetetoA designer’s obsession always circles back to one simple question: How can we improve the user’s experience?](https://www.figma.com/blog/eighteen-designers-predict-ui-ux-trends-for-2018/)

    * [Insights](https://www.figma.com/blog/insights/)
    * [UI/UX](https://www.figma.com/blog/ui-ux/)
    * [Thought leadership](https://www.figma.com/blog/thought-leadership/)

  * ### [5 books that shaped the design approach of Airbnb’s Jem GoldApril 27, 2017By Carmel DeAmicisIf you surfed design Twitter this week, you probably saw chatter about Airbnb’s new open source library for rendering React code as Sketch designs. It’s a pioneering approach that brings design and engineering closer together, and it’s the brainchild of Airbnb designer Jem Gold.](https://www.figma.com/blog/five-books-that-shaped-the-design-approach-of-airbnbs-jon-gold/)

    * [Insights](https://www.figma.com/blog/insights/)
    * [UI/UX](https://www.figma.com/blog/ui-ux/)
    * [Design](https://www.figma.com/blog/design/)
    * [Tips & inspiration](https://www.figma.com/blog/tips-and-inspiration/)
    * [Thought leadership](https://www.figma.com/blog/thought-leadership/)
    *   * [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAJCAYAAAAywQxIAAAACXBIWXMAABYlAAAWJQFJUiTwAAAArElEQVQoz6WRSxLEIAhEvf9VVfC7ZoCIxWRMNrPoAgt4NhrGGDTnJIm1VgIAKqVo7iNK3jq13vVsfZ3PnhFOQFHOWYWIqgxIqXCdlbkeY9S+1tozUIp2e0pJQeqOI7AiXGDEsi96BYpDHV4O70411w1w98nMI1DcGMiD99rsOi1Zz6tDD/QydwKSt5NoFxnQ9LPy188uZz738r98BN4lzaZT3eTngx0k/iNjfACSdLCU/+bFYwAAAABJRU5ErkJggg==)![](https://cdn.sanity.io/images/599r6htc/regionalized/c2eda7441961dea4e3a11d9096777f10863d4238-2120x1000.png?w=528&h=249&q=75&fit=max&auto=format)5 essential ways to use design constraintsMay 25, 2017By Carmel DeAmicisRemember the good ‘ol era of tech design, when you had to create interfaces — at most — for a PC and a Mac? Me neither.](https://www.figma.com/blog/five-essential-ways-to-use-design-constraints/)

    * [Working Well](https://www.figma.com/blog/working-well/)
    * [Design](https://www.figma.com/blog/design/)
    * [Tips & inspiration](https://www.figma.com/blog/tips-and-inspiration/)
    * [Figma Design](https://www.figma.com/blog/figma-design/)
    * 


## Create and collaborate with Figma

[Get started for free](https://www.figma.com/signup)
