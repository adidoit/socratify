---
title: "Building Pinterest’s A/B testing platform"
company: "pinterest"
url: "https://medium.com/pinterest-engineering/building-pinterests-a-b-testing-platform-ab4934ace9f4"
type: "system_architecture"
date: "2025-09-15"
---

# Building Pinterest’s A/B testing platform

[![Pinterest Engineering](https://miro.medium.com/v2/resize:fill:64:64/1*iAV-apeVpCJ1h6Znt1AzCg.jpeg)](/@Pinterest_Engineering?source=post_page---byline--ab4934ace9f4---------------------------------------)

[Pinterest Engineering](/@Pinterest_Engineering?source=post_page---byline--ab4934ace9f4---------------------------------------)

6 min read

·

Apr 8, 2016

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fpinterest-engineering%2Fab4934ace9f4&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fbuilding-pinterests-a-b-testing-platform-ab4934ace9f4&user=Pinterest+Engineering&userId=ef81ef829bcb&source=---header_actions--ab4934ace9f4---------------------clap_footer------------------)

\--

2

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fab4934ace9f4&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fbuilding-pinterests-a-b-testing-platform-ab4934ace9f4&source=---header_actions--ab4934ace9f4---------------------bookmark_footer------------------)

Listen

Share

Shuo Xiang | Pinterest engineer, Data

As a data-driven company, we rely heavily on experiments to guide products and features. At any given time, we have around 1,000 experiments running, and we’re adding more every day. Because we’re constantly increasing the number of experiments and logging corresponding data, we need a reliable, simple to use platform engineers can use without error. To eliminate common errors made by experimenters, we introduced a lightweight config UI, QA workflow and simplified APIs supporting A/B testing across multiple platforms. (For more information about our dashboards and data pipeline, check out our [previous experiments post](https://engineering.pinterest.com/blog/scalable-ab-experiments-pinterest).)

We prioritized the following requirements when building the experiments platform:

  1. Realtime config change: We need to be able to quickly shut down or ramp up experiments in real time without code deploy for each config change, in particular when fixing site incidents.
  2. Lightweight process: Setting up the experiment shouldn’t be more complicated than a normal feature launch, yet should prevent the user from making predictable errors.
  3. Client-agnostic: The user shouldn’t have to learn a new experiment method for each platform.
  4. Analytics: To make better experiment decisions, we built a new analytics dashboard that was easier to use.
  5. Scalability: We needed the entire system to scale in both online service and offline experiment data processing.



### Simplified process

Experiments at Pinterest follow a common pattern:

  1. Create the experiment with an initial configuration, create a hypothesis and document approach to test that hypothesis.
  2. Expose the experiment to Pinners, add new groups, disable groups and modify the audience via filters.
  3. Finish the experiment by shipping the code to all Pinners or rolling it back and documenting results.



In our prior framework, these changes were handled via code, however we wanted to structure these changes in a UI to provide interactive feedback and validation, and in a configuration-based framework to push changes independent of code release.

Press enter or click to view image in full size

Common experiment mistakes like syntax errors, imbalanced group allocation, overlapping groups or violation of experiment procedures are verified interactively. We also proactively provide typeahead search suggestions to reduce the amount of human input, as shown in Figure 2. Now making an experiment change is usually a couple of clicks away.

In order to make the configuration accessible by an arbitrary client in real-time, we take advantage of our internal system to store all experiment settings in a serialized format and synchronize them to every host of our experiment system within seconds. A typical config file has the following content after deserialization:
    
    
    {"holiday_special":   
        {  
              "group_ranges": {  
                  "enabled": {"percent": 5.0, "ranges": [0, 49]},   
                  "hold_out": {"percent": 5.0, "ranges": [50, 99]}  
               },   
              "key": "holiday_special",   
               “global filter”: user_country(‘US’),  
               “overwrite_filter”: {“enabled”: is_employee()},  
               "unauth_exp": 0,   
               "version": 1  
          }  
      }

The benefit of the separation of config and code is the instant update of experiment settings, meaning configuration changes such as increasing the traffic of a treatment group doesn’t require code deployment. This frees up the experiment from the production deployment schedule and greatly speeds up the iteration, particularly when urgent changes are needed.

### Quality assurance

A single experiment could affect millions of Pinners, so we have high standards for experiment operations and critical quality assurance tools. The experiment web app is also equipped with a review tool, which creates a review process for each experiment change. Figure 3 shows a pending change that modifies group ranges and filters. Reviewers are specified through the UI and will be notified by email.

For most experiments we have a cross-team helper group made up of platform developers, users and data scientists. Almost every change is required to be reviewed by a helper who closely examines planning, hypothesis, key results, triggering logic, filter set up, group validation and documentation. Such a process is enforced on our web app so that each change is required to fill in an helper. We also have a regular experiment helper training program to ensure each team has at least one person who’s certified.

An experiment is often associated with code changes that embed the control/treatment group information into the decision logic. We require experiment users to add a Pull Request (PR) link in the experiment platform via the Pull Requests button, so it’s easier for helpers and analysts to trace the experiment behavior and potentially debug if needed. In addition, we also send every change as a comment to the corresponding PR in Phabricator (our repository management tool), as shown in Figure 4.

Users can create a test-only copy of the ongoing experiment in the UI (as shown in Figure 1). They’ll then be ported to a test panel shown in Figure 5. Any changes made in the test panel will not affect the experiment in production and will only be visible to the testing engineer, who can use the one-click Copy To Prod button to enable it in production.

### API

The experiment API is the interface users will call to link their application code to the experiment settings they made via the UI. Two key methods provided are:
    
    
    def get_group(self, experiment_name)  
      
      def activate_experiment(self, experiment_name)

Specifically, the _get_group_ method returns the name of the group to which the caller will be directed. Internally, the group is computed by computing a hash value based on experiment information, and the method has no side effect. On the other hand, calling _activate_experiment_ sends a message to the logging system and contributes to the analytics result. These two methods sufficiently cover the majority of user cases and are commonly used in the following way:
    
    
    # Get the experiment group given experiment name and gatekeeper object, without actually triggering the experiment.  
    group = gk.get_group("example_experiment_name")  
       
    # Activate/trigger experiment. It will return experiment group if any.  
    group = gk.activate_experiment("example_experiment_name")  
       
    # Application code showing treatment based on group.  
    if group in ['enabled', 'employees']:  
      # behavior for enabled group  
      pass  
    else:  
      # behavior for control group  
      pass

The gatekeeper object _gk_ in the code above is a wrapper of user/session/meta information needed for an experiment. In addition to the Python library shown above, we have a separate JVM (Scala and Java) library implemented. Support for Javascript and mobile apps (Android & iOS) are also available.

### Design and architecture

The experiment platform is logically partitioned into three components: a configuration system, a set of APIs and the analytics pipeline. They’re connected by the following one directional data flow:

  1. Configuration system persists user changes made on the web UI to our experiment database, whose information is regularly published at sub-minute granularity in a serialized format to each service.
  2. Experiment clients pick up the experiment configuration and make API calls to determine the experiment logic, such as experiment type and group allocation.
  3. The experiment activation logs generated by various clients are sent to Kafka through our internal [Singer service](http://www.slideshare.net/DiscoverPinterest/singer-pinterests-logging-infrastructure), from which the analytics pipeline will create experiment reports with user defined metrics and deliver them on the dashboard.



### Summary

This system rolled out last summer and supports the majority of experiments inside Pinterest. Team specific functionalities such as real-time metrics dashboard, experiments email notification, interactive documentation and collaboration tool and SEO API/UI are also being added to the system. If you’re interested in experiment framework and analytics platforms, [join us](https://careers.pinterest.com/careers/engineering/san-francisco)!

_Acknowledgements: Multiple teams across Pinterest provide insightful feedbacks and suggestions shaping the experiment framework. Major contributors include Shuo Xiang, Bryant Xiao, Justin Mejorada Pier, Jooseong Kim, Chunyan Wang and the rest of Data Engineering team._
