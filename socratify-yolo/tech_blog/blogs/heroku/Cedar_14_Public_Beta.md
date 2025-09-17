---
title: "Cedar-14 Public Beta"
company: "heroku"
url: "https://blog.heroku.com/archives/2013/7/10/cedar-14-public-beta"
type: "final_harvest"
date: "2025-09-15"
---

[Blog](https://www.heroku.com/blog/) / [News](https://www.heroku.com/blog/category/news/) / **Cedar-14 Public Beta**

# Cedar-14 Public Beta

[![Michael Friis](https://secure.gravatar.com/avatar/b32ac91bd970eb65707862970ec67a443bac4189031c6837ebd9a6f4b276226a?s=50&d=mm&r=g)](https://www.heroku.com/blog/author/michael-friis/)

Posted By [Michael Friis](https://www.heroku.com/blog/author/michael-friis/)

  * Last Updated: April 30, 2024 



At Heroku, we want to give our users access to the latest and greatest software stacks to base their apps on. That’s why we continuously update buildpacks to support new language and framework versions and let users [experiment further using third-party buildpacks](https://devcenter.heroku.com/articles/buildpacks#using-a-third-party-buildpack).

Sitting underneath slugs and buildpacks are [stacks](https://devcenter.heroku.com/articles/stack). Stacks are the operating system and system libraries required to make apps run. Today we’re releasing into public beta a new version of the Celedon Cedar stack: `cedar-14`.

`cedar-14` is built on the latest LTS version of Ubuntu Linux and has recent versions of libraries and system dependencies that will receive maintenance and security updates for a long time to come.

Before making `cedar-14` the default stack, Heroku is looking for feedback from our users. To help weed out bugs and problems, please try out the stack with existing apps and new source code.

##  Creating a cedar-14 app  


Here’s how to create a new app running on `cedar-14`:
    
    
    $ heroku create --stack cedar-14
    ...
    

Pushing and deploying to `cedar-14` apps works exactly the same as deploying apps on the classic Cedar stack.

##  Updating an app to cedar-14  


Before migrating an existing app to cedar-14, we recommend either first upgrading an existing staging app or testing your app source in a new cedar-14 staging app.

To migrate an existing app to `cedar-14`, use the `stack` command:
    
    
    $ heroku stack:set cedar-14 -a example-app
    ...
    $ git commit -m "update to cedar-14" --allow-empty
    ...
    $ git push heroku master
    ...
    

Note that running `stack:set` only tells Heroku that you want the next push to be built and deployed on a different stack. You have to push and force a rebuild for the change to take effect. See the full [Migrating to Cedar-14](https://devcenter.heroku.com/articles/cedar-14-stack) Dev Center article for additional details.

If, despite of testing, your app doesn’t work correctly on `cedar-14`, you can always use rollback to revert the stack change:
    
    
    $ heroku rollback
    

Note that this will cause the apps stack to be reset to `cedar` and you need to re-run `stack:set cedar-14` to deploy to cedar-14.

##  Compatibility  


Stack compatibility is important to us, but we are also trying to take advantage of this opportunity to remove some less-used parts of the current stack surface area. We have [documented the differences between the classic Cedar stack and `cedar-14` beta stack](https://devcenter.heroku.com/articles/stack-packages) on Dev Center. In addition to missing packages, apps may also encounter incompatibilities simply because most libraries on `cedar-14` have been updated to their most recent versions. Please get in touch on [stack-feedback@heroku.com](mailto:stack-feedback@heroku.com) or open a support ticket if your app fails to build or run on `cedar-14` for any reason.

##  Buildpacks  


We have updated all of the [default buildpacks](https://devcenter.heroku.com/articles/buildpacks) that we maintain to work with `cedar-14` and are keen to get user feedback. We have also updated certain much used non-default buildpacks such as [nginx-buildpack](https://github.com/ryandotsmith/nginx-buildpack) and [buildpack-pgbouncer](https://github.com/heroku/heroku-buildpack-pgbouncer).

If you maintain a 3rd buildpack, please refer to the [Buildpack API article](https://devcenter.heroku.com/articles/buildpack-api) for details on how to support multiple stacks. We want to help buildpack maintainers with this update process, so please don’t hesitate to reach out to [stack-feedback@heroku.com](mailto:stack-feedback@heroku.com) with questions or concerns.

We’re looking forward to helping our users move to `cedar-14`, the latest and greatest Heroku stack. Apps running on `cedar-14` will stay updated, fast and secure for a long time to come. Get in touch on [stack-feedback@heroku.com](mailto:stack-feedback@heroku.com) if you encounter problems or have suggestions.

  * Originally Published:  August 19, 2014



__

Tweet 

__

Share 

__

Share 

### Related Posts

[ Securing Salesforce Integrations with Heroku AppLink ](https://www.heroku.com/blog/securing-salesforce-integrations-with-heroku-applink/)

[ Triage and Fix with Confidence: `heroku run` and OTel on Heroku Fir ](https://www.heroku.com/blog/heroku-run-and-otel-on-heroku-fir/)

[ Corrective Action Update for the Heroku June 10th Outage ](https://www.heroku.com/blog/corrective-action-update-june-10-outage/)

[ Discover How Heroku’s AI PaaS Delivers Real-World Results at Dreamforce ](https://www.heroku.com/blog/heroku-ai-paas-dreamforce-2025/)

[ Amazon Nova Models: Now Available on Heroku ](https://www.heroku.com/blog/amazon-nova-models-now-available/)

###### More from the Author

[![](https://secure.gravatar.com/avatar/b32ac91bd970eb65707862970ec67a443bac4189031c6837ebd9a6f4b276226a?s=70&d=mm&r=g)](https://www.heroku.com/blog/author/michael-friis/)

[Michael Friis](https://www.heroku.com/blog/author/michael-friis/)

Product Manager

Heroku Staff

* * *

  * [Heroku is Now Available to Purchase in AWS Marketplace](https://www.heroku.com/blog/heroku-in-aws-marketplace/)
  * [More Predictable Shared Dyno Performance](https://www.heroku.com/blog/more-predictable-shared-dyno-performance/)
  * [Container and Runtime Performance Improvements](https://www.heroku.com/blog/runtime-performance-improvements/)



Browse the archives for [News](https://www.heroku.com/blog/category/news/) or [all blogs](/blog/). Subscribe to the RSS feed for [News](https://www.heroku.com/blog/category/news/feed/) or [all blogs](https://www.heroku.com/blog/feed).
