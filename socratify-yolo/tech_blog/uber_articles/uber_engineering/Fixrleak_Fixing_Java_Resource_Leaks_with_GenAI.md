---
title: "Fixrleak: Fixing Java Resource Leaks with GenAI"
author: "Unknown"
url: "https://www.uber.com/blog/fixrleak-fixing-java-resource-leaks-with-genai/"
published_date: "None"
downloaded_date: "2025-09-15T09:38:15.184869"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for Fixrleak: Fixing Java Resource Leaks with GenAI](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/newcover-17460410723873-1024x497.jpg)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Ffixrleak-fixing-java-resource-leaks-with-genai%2F&t=Fixrleak%3A+Fixing+Java+Resource+Leaks+with+GenAI)
  * [X social](https://twitter.com/share?text=Fixrleak%3A+Fixing+Java+Resource+Leaks+with+GenAI&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Ffixrleak-fixing-java-resource-leaks-with-genai%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Ffixrleak-fixing-java-resource-leaks-with-genai%2F)
  * [Envelope](mailto:?subject=Fixrleak%3A+Fixing+Java+Resource+Leaks+with+GenAI&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Ffixrleak-fixing-java-resource-leaks-with-genai%2F)
  * Link

# Introduction
Resource leaks, where resources like files, database connections, or streams aren’t properly released after use, are a persistent issue in Java applications. These leaks can lead to performance degradation, and system failures. While tools like SonarSource SonarQube™ effectively identify such leaks, the fixing process remains manual, time-consuming, and prone to errors. To address this, we developed FixrLeak, a generative AI-based framework that automates the detection and repair of resource leaks. FixrLeak combines Abstract Syntax Tree (AST) analysis with generative AI (GenAI) to produce accurate, idiomatic fixes while following Java best practices like try-with-resources. Deployed within Uber’s extensive Java codebase, FixrLeak significantly reduces manual effort, improves developer productivity, and improves code quality, showcasing the transformative potential of AI-driven solutions in large-scale software engineering.
* * *
## Background
### Understanding Resource Leaks in Java
Resource leaks occur when a program fails to properly release resources such as files, database connections, or streams after use. These leaks can lead to serious issues, including performance degradation, application failures, and an inability to handle additional operations due to resource exhaustion. For example, if a file descriptor isn’t released quickly, it could prevent an application from opening new files, ultimately causing system instability.
Consider the example below, where a BufferedReader object is used to read from a file. In the original code (Figure 1), the reader isn’t closed properly, resulting in a resource leak. Historically, developers relied on try/catch/finally blocks to handle such cases, but missing or incorrect finally blocks often led to leaks. Modern Java best practices recommend the try-with-resources statement, which significantly reduces boilerplate code and ensures resources are released safely, even if exceptions occur during execution.  

![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/fig1-17460413642644-1024x399.png)Figure 1: Original code with a resource leak. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/fig2-17460414046128-1024x372.png)Figure 2: Fixed Code using _try-with-resources_.
In the revised version (Figure 2) the _BufferedReader_ is declared within the try block using the _try-with-resources_ statement, ensuring that it’s automatically closed when no longer needed. This practice simplifies the code and eliminates the risk of resource leaks, making it an essential technique for modern Java programming.
###   
Tackling Resource Leaks: What Came Before FixrLeak
Before FixrLeak, resource leak fixes were either manual or handled by early automated tools. [RLFixer](https://dl.acm.org/doi/10.1145/3611643.3616267), a non-GenAI tool, relied on pre-designed templates and analysis frameworks like [WALA](https://github.com/wala/WALA). While effective for some leaks, these tools struggled to scale in massive codebases like Uber’s and required extensive manual setup for each new programming idiom.
GenAI-based solutions, like [InferFix](https://dl.acm.org/doi/10.1145/3611643.3613892), moved the needle by using large language models to automate fixes. However, InferFix had its limitations, including only 70% fix accuracy and challenges with complex leaks requiring advanced code analysis. Additionally, it relied on proprietary models that couldn’t easily adapt to evolving technologies.
FixrLeak builds on these lessons, using generative AI in a scalable, template-free approach that works seamlessly across Uber’s codebase. It focuses on easily fixable leaks to achieve higher accuracy, making it a game-changer for industrial-scale resource leak management.
* * *
## Architecture
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/fig3-17460414823287-1024x350.png)Figure 3: Resource leak-fixing workflow with Fixrleak.
The general flow of FixrLeak is shown in Figure 3. We currently focus on fixing leaks where the lifetime of the resource doesn’t exceed the function that allocated the resource.
###   
Input Gathering
FixrLeak starts by scanning resource leaks reported by SonarQube, gathering key details like file names and line numbers. To account for changes in the codebase, it uses a deterministic hash based on the file and function name, ensuring accurate tracking of leaks and their fixes. Once identified, FixrLeak uses the [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) library to parse the code and extract the relevant function for analysis.
###   
AST-Level Analysis 
Fixing resource leaks isn’t always straightforward—blindly applying fixes can lead to new issues, like use-after-close errors. For example, if a resource like a _BufferedReader_ is returned from a method, closing it prematurely could break the code at its caller site. To avoid such pitfalls, FixrLeak uses Tree-sitter to perform AST (Abstract Syntax Tree) analysis.
This analysis ensures that FixrLeak skips functions where resources are passed as parameters, returned, or stored in fields, as these resources often outlive the function’s scope. By focusing only on safe-to-fix scenarios, FixrLeak delivers precise, reliable fixes while leaving more complex cases for advanced analysis at the caller level.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/fig4-17460415865616-1024x234.png)Figure 4: An example that can’t be fixed using _try-with-resources_ within the function.
### Prompt Engineering
Once a resource leak passes initial checks, FixrLeak crafts a tailored prompt and sends it to a generative AI model like OpenAI® ChatGPT-4O. The AI responds with a suggested fix, which FixrLeak applies by replacing the original leaky function with the new, leak-free version. Finally, FixrLeak generates a pull request, streamlining the process for developers to review and approve the fix.
###   
Pull Request Verification
Before submitting a pull request, FixrLeak runs multiple validation checks to ensure the fix is rock-solid. It verifies that the target binary builds successfully, runs all existing tests to confirm nothing is broken, and can also recheck the code with SonarQube to confirm the resource leak has been resolved. This thorough testing ensures high-quality fixes that developers can confidently review and merge.
### Code Review
The final step is ‌code review from the developers to accept the pull request. Usually, all they need to do is one-click accept.
* * *
## Use Cases at Uber
To test FixrLeak, we applied it to 124 resource leaks identified by SonarQube in Uber’s Java codebase. After excluding 12 cases in deprecated code, FixrLeak’s AST-level analysis processed the remaining 112 leaks, ensuring that fixes were applied only where resources were confined to the scope of the function. This focus on intra-function leaks played to the strengths of generative AI, resulting in high success rates.
Out of the 102 eligible cases, FixrLeak successfully automated fixes for 93 leaks. 
By focusing on well-scoped issues and using advanced analysis, FixrLeak has proven to be a highly effective tool for improving code quality and reducing manual intervention. This approach accelerates development and ensures Uber’s systems remain robust and efficient at scale. Fixrleak continues to run periodically on the Java codebase and will quickly generate fixes for resource leaks introduced in the future.
* * *
## Next Steps 
Looking ahead, we aim to expand FixrLeak’s capabilities in several key areas:
  * **Support for inter-procedural fixes** : Enhancing the tool to handle resource leaks that span multiple functions or methods.
  * **GenAI-based leak detection** : Incorporating generative AI to identify resource leaks, complementing the existing detection process, and allowing it to work on Golang, which doesn’t currently have a resource leak detection tool.
  * **Advanced source code analysis** : Improving the accuracy of leak identification, particularly for user-defined resource classes.

These advancements will further increase FixrLeak’s effectiveness, enabling it to tackle more complex scenarios and deliver even greater value to large-scale codebases.
* * *
# Conclusion
Resource leaks remain a persistent challenge in large-scale software systems, but generative AI presents a powerful new approach to tackling this issue. FixrLeak combines GenAI and AST-level analysis to bridge the gap between detection and resolution, delivering accurate and efficient fixes while improving developer productivity. By addressing practical challenges like complex build systems, FixrLeak enhances code quality and reliability within Uber’s Java codebase, setting a precedent for AI-driven automation in software engineering.
For organizations dealing with similar challenges, FixrLeak offers key takeaways:
  * **Prioritize structured code analysis** : AST-based techniques help ensure fixes are safe and context-aware.
  * **Automate targeted fixes** : Focus on well-scoped, high-confidence fixes first to maximize success rates.
  * **Integrate AI responsibly** : Validate AI-generated code with rigorous testing and code review processes.

While FixrLeak is currently deployed at Uber, the principles behind it—combining static analysis with GenAI—can be adapted to other large-scale systems. Companies seeking to automate code quality improvements can explore similar techniques using AI-assisted code repair, AST analysis, and structured prompt engineering.
This blog kicks off a series from the Programming Systems group on leveraging GenAI for software engineering challenges. Stay tuned for the next post, where we explore how GenAI can automatically fix data races in Golang.
* * *
### Acknowledgments
We’d like to thank Jens Palsberg for several technical discussions around resource leaks.
Cover Photo Attribution: ​​”[BerwickDam01](https://openverse.org/image/383e5c76-6ffa-436e-be73-f7d254ec565b?q=pipe+leak&p=45)” by [Korona Lacasse](https://openverse.org/image/collection?source=flickr&creator=Korona+Lacasse)[.](https://www.flickr.com/photos/61132483@N00) is licensed under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/).
_OpenAI ® and its logos are registered trademarks of OpenAI®. _
Oracle, Java, MySQL, and NetSuite are registered trademarks of Oracle and/or its affiliates. Other names may be trademarks of their respective owners.
SONAR, SONARSOURCE, SONARQUBE, and CLEAN AS YOU CODE are trademarks of SonarSource SA.
* * *
![Chris Zhang](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2022/08/chrisheadshot-1-17418438469471.jpeg)
Chris Zhang
Chris Zhang is a Software Engineer on the Programming System team at Uber. His research interests include computer architecture, compilers, operating systems, and microservices.
![Akshay Utture](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/04/akshayphoto-17460432006943-983x1024.jpg)
Akshay Utture
Akshay Utture is a former software engineer on the Programming System team at Uber. He has been focused on building AI Code Review tools at Uber, but is more broadly interested in AI developer tools and program analysis.
![Manu Sridharan](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2022/08/manu-sridharan-pic-17460433851822.jpeg)
Manu Sridharan
Manu Sridharan, formerly a Staff Engineer at Uber, is a Professor of Computer Science and Engineering at the University of California, Riverside. His primary research areas are programming languages and software engineering.
* * *
Posted by Chris Zhang, Akshay Utture, Manu Sridharan 
Category:
[Engineering](/en-CA/blog/engineering/)
[Backend](/en-CA/blog/engineering/backend/)
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
[English](/en-CA/blog/fixrleak-fixing-java-resource-leaks-with-genai/)
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
[English](/en-CA/blog/fixrleak-fixing-java-resource-leaks-with-genai/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
