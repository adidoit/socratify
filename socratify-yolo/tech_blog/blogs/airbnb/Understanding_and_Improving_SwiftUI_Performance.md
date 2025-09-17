---
title: "Understanding and Improving SwiftUI Performance"
author: "https://medium.com/@calstephens98"
url: "https://medium.com/airbnb-engineering/understanding-and-improving-swiftui-performance-37b77ac61896?source=rss----53c7c27702d5---4"
date: "2025-09-15"
---

#**Understanding and Improving SwiftUI Performance**
[![Cal Stephens](https://miro.medium.com/v2/resize:fill:64:64/1*_mdLFeRldMIbg6MCFe-DJQ.jpeg)](/@calstephens98?source=post_page---byline--37b77ac61896---------------------------------------)
[Cal Stephens](/@calstephens98?source=post_page---byline--37b77ac61896---------------------------------------)
9 min read
·
Jun 24, 2025
[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2F37b77ac61896&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Funderstanding-and-improving-swiftui-performance-37b77ac61896&user=Cal+Stephens&userId=9f2d9950f30f&source=---header_actions--37b77ac61896---------------------clap_footer------------------)
\--
14
[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F37b77ac61896&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Funderstanding-and-improving-swiftui-performance-37b77ac61896&source=---header_actions--37b77ac61896---------------------bookmark_footer------------------)
Listen
Share
New techniques we’re using at Airbnb to improve and maintain performance of SwiftUI features at scale
By [Cal Stephens](https://www.linkedin.com/in/calstephens/), [Miguel Jimenez](https://www.linkedin.com/in/miguel-jimenez-b98216112)
Press enter or click to view image in full size
Airbnb [first adopted SwiftUI in 2022](/airbnb-engineering/unlocking-swiftui-at-airbnb-ea58f50cde49), starting with individual components and later expanding to entire screens and features. We’ve seen major improvements to engineers’ productivity thanks to its declarative, flexible, and composable architecture. However, adopting SwiftUI has brought new challenges related to performance. For example, there are many common code patterns in SwiftUI that can be inefficient, and many small papercuts can add up to a large cumulative performance hit. To begin addressing some of these issues at scale, we’ve created new tooling for proactively identifying these cases and statically validating correctness.
## SwiftUI feature architecture at Airbnb
We’ve been leveraging declarative UI patterns at Airbnb for many years, using our UIKit-based [Epoxy library](/airbnb-engineering/introducing-epoxy-for-ios-6bf062be1670) and [unidirectional data flow](/airbnb-engineering/introducing-epoxy-for-ios-6bf062be1670#fbe0) systems. When adopting SwiftUI in our screen layer, we decided to continue using our existing unidirectional data flow library. This simplified the process of incrementally adopting SwiftUI within our large codebase, and we find it improves the quality and maintainability of features.
However, we noticed that SwiftUI features using our unidirectional data flow library didn’t perform as well as we expected, and it wasn’t immediately obvious to us what the problem was. Understanding SwiftUI’s performance characteristics is an important requirement for building performant features, especially when venturing outside of the “standard” SwiftUI toolbox.
## Understanding SwiftUI view diffing
When working with declarative UI systems like SwiftUI, it’s important to ensure the framework knows which views need to be re-evaluated and re-rendered when the state of the screen changes. Changes are detected by diffing the view’s stored properties any time its parent is updated. Ideally the view’s body will only be re-evaluated when its properties actually change:
Press enter or click to view image in full size
However, this behavior is not always the reality (more on why in a moment). Unnecessary view body evaluations hurt performance by performing unnecessary work.
How do you know how often a view’s body is re-evaluated in a real app? An easy way to visualize this is with a modifier that applies a random color to the view every time it’s rendered. When testing this on various views in our app’s most performance-sensitive screens, we quickly found that many views were re-evaluated and re-rendered more often than necessary:
Press enter or click to view image in full size
### The SwiftUI view diffing algorithm
SwiftUI’s built-in diffing algorithm is often overlooked and not officially documented, but it has a huge impact on performance. To determine if a view’s body needs to be re-evaluated, SwiftUI uses a reflection-based diffing algorithm to compare each of the view’s stored properties:
1. If a type is _Equatable_ , SwiftUI compares the old and new values using the type’s _Equatable_ conformance. Otherwise:
2. SwiftUI compares value types (e.g., structs) by recursively comparing each instance property.
3. SwiftUI compares reference types (e.g., classes) using reference identity.
4. SwiftUI attempts to compare closures by identity. However, most closures cannot be compared reliably.
If all of the view’s properties compare as equal to the previous value, then the body isn’t re-evalulated and the content isn’t re-rendered. Values using SwiftUI property wrappers like _@State_ and _@Environment_ don’t participate in this diffing algorithm, and instead trigger view updates through different mechanisms.
When reviewing different views in our codebase, we found several common patterns that confounded SwiftUI’s diffing algorithm:
1. Some types are inherently not supported, like closures.
2. Simple data types stored on the view may be unexpectedly compared by reference instead of by value.
Here’s an example SwiftUI view with properties that interact poorly with the diffing algorithm:
struct MyView: View {
/// A generated data model that is a struct with value semantics,
/// but is copy-on-write and wraps an internal reference type.
/// Compared by reference, not by value, which could cause unwanted body evaluations.
let dataModel: CopyOnWriteDataModel
/// Other miscellaneous properties used by the view. Typically structs, but sometimes a class.
/// Unexpected comparisons by reference could cause unwanted body evaluations.
let requestState: MyFeatureRequestState
/// An action handler for this view, part of our unidirectional data flow library.
/// Wraps a closure that routes the action to the screen's action handler.
/// Closures almost always compare as not-equal, and typically cause unwanted body evaluations.
let handler: Handler<MyViewAction>
var body: some View { ... }
}
If a view contains any value that isn’t diffable, the entire view becomes non-diffable. Preventing this in a scalable way is almost impossible with existing tools. This finding also reveals the performance issue caused by our unidirectional data flow library: action handling is closure-based, but SwiftUI can’t diff closures!
In some cases, like with the action handlers from our unidirectional data flow library, making the value diffable would require large, invasive, and potentially undesirable architecture changes. Even in simpler cases, this process is still time consuming, and there’s no easy way to prevent a regression from creeping in later on. This is a big obstacle when trying to improve and maintain performance at scale in large codebases with many different contributors.
## Controlling SwiftUI view diffing
Fortunately, we have another option: If a view conforms to Equatable, SwiftUI will diff it using its Equatable conformance _instead_ of using the default reflection-based diffing algorithm.
The advantage of this approach is that it lets us selectively decide which properties should be compared when diffing our view. In our case, we know that the handler object doesn’t affect the content or identity of our view. We only want our view to be re-evalulated and re-rendered when the _dataModel_ and _requestState_ values are updated. We can express that with a custom _Equatable_ implementation:
// An Equatable conformance that makes the above SwiftUI view diffable.
extension MyView: Equatable {
static func ==(lhs: MyView, rhs: MyView) -> Bool {
lhs.dataModel == rhs.dataModel
&& lhs.requestState == rhs.requestState
// Intentionally not comparing handler, which isn't Equatable.
}
}
However:
1. This is a lot of additional boilerplate for engineers to write, especially for views with lots of properties.
2. Writing and maintaining a custom conformance is error-prone. You can easily forget to update the _Equatable_ conformance when adding new properties later, which would cause bugs.
So, instead of manually writing and maintaining _Equatable_ conformances, we created a new _@Equatable_ macro that generates conformances for us.
// A sample SwiftUI view that has adopted @Equatable
// and is now guaranteed to be diffable.
@Equatable
struct MyView: View {
// Simple data types must be Equatable, or the build will fail.
let dataModel: CopyOnWriteDataModel
let requestState: MyFeatureRequestState
// Types that aren't Equatable can be excluded from the
// generated Equatable conformance using @SkipEquatable,
// as long as they don’t affect the output of the view body.
@SkipEquatable let handler: Handler<MyViewAction>
var body: some View { ... }
}
The _@Equatable_ macro generates an _Equatable_ implementation that compares all of the view’s stored instance properties, excluding properties with SwiftUI property wrappers like _@State_ and _@Environment_ that trigger view updates through other mechanisms. Properties that aren’t _Equatable_ and don’t affect the output of the view body can be marked with _@SkipEquatable_ to exclude them from the generated implementation. This allows us to continue using the closure-based action handlers from our unidirectional data flow library without impacting the SwiftUI diffing process!
After adopting the _@Equatable_ macro on a view, that view is guaranteed to be diffable. If an engineer adds a non-_Equatable_ property later, the build will fail, highlighting a potential regression in the diffing behavior. This effectively makes the _@Equatable_ macro a sophisticated linter — which is really valuable for scaling these performance improvements in a codebase with many components and many contributors, since it makes it less likely for regressions to slip in later.
## Managing the size of view bodies
Another essential aspect of SwiftUI diffing is understanding that SwiftUI can only diff proper View structs. Any other code, such as computed properties or helper functions that generate a SwiftUI view, cannot be diffed.
Consider the following example:
// Complex SwiftUI views are often simplified by
// splitting the view body into separate computed properties.
struct MyScreen: View {
/// The unidirectional data flow state store for this feature.
@ObservedObject var store: StateStore<MyState, MyAction>
var body: some View {
VStack {
headerSection
actionCardSection
}
}
private var headerSection: some View {
Text(store.state.titleString)
.textStyle(.title)
}
private var actionCardSection: some View {
VStack {
Image(store.state.cardSelected ? "enabled" : "disabled")
Text("This is a selectable card")
}
.strokedCard(.roundedRect_mediumCornerRadius_12)
.scaleEffectButton(action: {
store.handle(.cardTapped)
})
}
}
This is a common way to organize complex view bodies, since it makes the code easier to read and maintain. However, at runtime, SwiftUI effectively inlines the views returned from the properties into the main view body, as if we instead wrote:
// At runtime, computed properties are no different
// from just having a single, large view body!
struct MyScreen: View {
@ObservedObject var store: StateStore<MyState, MyAction>
// Re-evaluated every time the state of the screen is updated.
var body: some View {
VStack {
Text(store.state.titleString)
.textStyle(.title)
VStack {
Image(store.state.cardSelected ? "enabled" : "disabled")
Text("This is a selectable card")
}
.strokedCard(.roundedRect_mediumCornerRadius_12)
.scaleEffectButton(action: {
store.handle(.cardTapped)
})
}
}
}
Since all of this code is part of the same view body, all of it will be re-evaluated when any part of the screen’s state changes. While this specific example is simple, as the view grows larger and more complicated, re-evaluating it will become more expensive. Eventually there would be a large amount of unnecessary work happening on every screen update, hurting performance.
To improve performance, we can implement the layout code in separate SwiftUI views. This allows SwiftUI to properly diff each child view, only re-evaluating their bodies when necessary:
struct MyScreen: View {
@ObservedObject var store: StateStore<MyState, MyAction>
var body: some View {
VStack {
HeaderSection(title: store.state.titleString)
CardSection(
isCardSelected: store.state.isCardSelected,
handler: store.handler,
)
}
}
}
/// Only re-evaluated and re-rendered when the title property changes.
@Equatable
struct HeaderSection: View {
let title: String
var body: some View {
Text(title)
.textStyle(.title)
}
}
/// Only re-evaluated and re-rendered when the isCardSelected property changes.
@Equatable
struct CardSection: View {
let isCardSelected: Bool
@SkipEquatable let handler: Handler<MyAction>
var body: some View {
VStack {
Image(store.state.isCardSelected ? "enabled" : "disabled")
Text("This is a selectable card")
}
.strokedCard(.roundedRect_mediumCornerRadius_12)
.scaleEffectButton(action: {
handler.handle(.cardTapped)
})
}
}
By breaking the view into smaller, diffable pieces, SwiftUI can efficiently update only the parts of the view that actually changed. This approach helps maintain performance as a feature grows more complex.
### View body complexity lint rule
Large, complex views aren’t always obvious during development. Easily available metrics like total line count aren’t a good proxy for complexity. To help engineers know when it’s time to refactor a view into smaller, diffable pieces, we created a custom [SwiftLint](https://github.com/realm/SwiftLint) rule that parses the view body using [SwiftSyntax](https://github.com/swiftlang/swift-syntax) and measures its complexity. We defined the view complexity metric as a value that increases every time you compose views using computed properties, functions, or closures. With this rule we automatically trigger an alert in Xcode when a view is getting too complex. (The complexity limit is configurable, and we currently allow a maximum complexity level of 10.)
Press enter or click to view image in full size
The rule shows as a warning during local Xcode builds alerting engineers as early as possible. In this screenshot, the complexity limit is set to 3, and this specific view has a complexity of 5.
## Conclusion
With an understanding of how SwiftUI view diffing works, we can use an _@Equatable_ macro to ensure view bodies are only re-evaluated when the values inside views actually change, break views into smaller parts for faster re-evaluation, and encourage developers to refactor views before they get too large and complex.
Applying these three techniques to SwiftUI views in our app has led to a large reduction in unnecessary view re-evaluation and re-renders. Revisiting the examples from earlier, you see far fewer re-renders in the search bar and filter panel:
Press enter or click to view image in full size
Using results from our [page performance score](/airbnb-engineering/airbnbs-page-performance-score-on-ios-36d5f200bc73) system, we’ve found that adopting these techniques in our most complicated SwiftUI screens really does improve performance for our users. For example, we reduced [scroll hitches](/airbnb-engineering/airbnbs-page-performance-score-on-ios-36d5f200bc73#4c63) by****15% on our main Search screen by adopting _@Equatable_ on its most important views, and breaking apart large view bodies into smaller diffable pieces. These techniques also give us the flexibility to use a feature architecture that best suits our needs without compromising performance or imposing burdensome limitations (e.g., completely avoiding closures in SwiftUI views).
Of course, these techniques aren’t a silver bullet. It’s not necessary for all SwiftUI features to use them, and these techniques by themselves aren’t enough to guarantee great performance. However, understanding how and why they work serves as a valuable foundation for building performant SwiftUI features, and makes it easier to spot and avoid problematic patterns in your own code.
If you’re interested in joining us on our quest to make the best iOS app in the App Store, please see our [careers](https://careers.airbnb.com/) page for open iOS roles.
