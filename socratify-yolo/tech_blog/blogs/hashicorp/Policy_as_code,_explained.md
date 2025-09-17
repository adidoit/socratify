---
title: "Policy as code, explained"
author: "Unknown"
url: "https://www.hashicorp.com/blog/policy-as-code-explained"
date: "2025-09-15"
---

[](/en/blog/products/terraform)Strategy & insights

* Twitter share
* LinkedIn share
* Facebook share
* Copy URL

# Policy as code, explained

Policy as code gives you an automated way to check, in minutes or seconds, if your IT and business stakeholders’ requirements are being followed in your infrastructure deployments.

Aug 28 2025[Kashaf Salaheen](/blog/authors/kashaf-salaheen), [Mitch Pronschinske](/blog/authors/mitch-pronschinske)

[Infrastructure as code](https://www.hashicorp.com/en/resources/what-is-infrastructure-as-code) is steadily [becoming mainstream](https://www.snsinsider.com/reports/infrastructure-as-code-market-4659). Why? Because without it, operations teams typically end up relying on pages and pages of documentation or unwritten tribal knowledge to explain how they’re supposed to build, upgrade, and triage infrastructure.

[Codification](https://www.hashicorp.com/en/tao-of-hashicorp#versioning-through-codification) of infrastructure, by contrast, allows all of that knowledge to be automated by machines. Some configuration languages like HCL are built to maintain operator readability so that infrastructure code can do two things: Drive automation and serve as documentation.

Another codification within IT operations that’s gaining traction is _**policy as code**_. As it turns out, the same coding practices that are applied to infrastructure can be very effective at managing and automating the enforcement of IT operations policies.

This post will define policy as code, explain how it can be used, outline its benefits, and illustrate what it looks like in practice with real use case quotes from organizations including Fannie Mae, ADB, Wayfair, Booking.com, MediaMarkt, and Petco.

## »What is policy?

Policies are essentially requirements.

In this post, we’re not talking about the policies your company might have around whether you can bring your dog to work. We’re talking about the policies that must be followed by engineers, IT systems, and software products.

IT policies often start out in shared documents (PDFs, Word, GDocs, etc.). Once authors distribute them or add them to a document storage system, then it's up to operations, security, compliance reviewers, and/or developers to memorize the policy documents or reread them when reviewing every code review ticket.

This workflow is slow, error prone, and makes it difficult to scale up the number of policies and the number of tickets being reviewed.

## »What is policy as code?

Policy as code gives you an automated way to check, in seconds, if your IT and business stakeholders’ requirements are being followed — in every deployment. A policy as code framework includes a policy coding language that can be tested, peer reviewed, versioned, automated, and re-used much like application or infrastructure code.

Some software tools and IT systems have their own built-in policy systems. For example, [HashiCorp Vault](https://www.hashicorp.com/en/products/vault) — a secrets management system — has configurable (codable) [policies](https://developer.hashicorp.com/vault/docs/concepts/policies) that describe which stored credentials a user or machine can access. But this isn’t necessarily policy as code.

Policy as code is more _flexible_. You can write your own custom policy checks through a policy language.

It’s similar to things like [linting](https://owasp.org/www-project-devsecops-guideline/latest/01b-Linting-Code) code, static code analysis, and validation checks — it’s run by a framework and either blocks a submission or notifies the submitter when a requirement is not met. A codified policy knows what to look for and how to react based on how it was built, and policies can be customized in a multitude of ways.

The term “policy as code” applies specifically to policies being used for _infrastructure operations_ , especially infrastructure provisioning and workload orchestration.

Because a policy as code framework is so flexible, it can cover a wide range of operational concerns:

* Security
* Compliance
* Observability
* Architecture
* Resilience
* FinOps

A policy framework is most effective when it works as a preventative step, running within your infrastructure provisioning or orchestration tools instead of detecting policy violations after deployment is finished, which requires a more expensive remediation process.

![Example policy as code workflow. The policy as code automated check labelled "POLICY CHECK" occurs between the plan and apply phases of Terraform provisioning. The policies are written by the compliance team here.](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1756403967-terraform-sentinel-workflow-and-private-module-registry.png&w=3840&q=75)Open image in lightbox

The policy as code automated check labelled "Sentinel Policy" occurs between the plan and apply phases of Terraform provisioning. The policies are written by stakeholders such as the operations, security, finance, and compliance team.

## »Policy as code example

What does a policy in the form of code actually look like? It could use a few different domain-specific languages.

Because [HashiCorp Terraform](https://www.hashicorp.com/en/products/terraform) is the [most popular](https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-2025-survey-part-2) product for infrastructure as code, the policy as code framework that is built into HashiCorp Cloud Platform services and HashiCorp Enterprise products — [Sentinel](https://www.hashicorp.com/en/sentinel) — is a common language for policy as code. (Other high-level policy languages like Rego for Open Policy Agent (OPA) are options as well) So this example will be written in Sentinel.

This example policy enforces requirements for AWS EC2 provisioning. The comments describe what each section does, with more description after the code block:

    # Get all AWS instances from all modules
     
    ec2_instances = filter tfplan.resource_changes as _, rc {
       rc.type is "aws_instance" 
    }
     
    # Mandatory Instance Tags
     
    mandatory_tags = [
       "Name",
    ]
     
    # Allowed Types
     
    allowed_types = [
       "t2.micro",
       "t2.small",
       "t2.medium",
     
    ]
     
    # Rule to enforce "Name" tag on all instances
     
    mandatory_instance_tags = rule {
       all ec2_instances as _, instance {
           all mandatory_tags as mt {
               instance.change.after.tags contains mt
           }
       }
    }
     
    # Rule to restrict instance types
     
    instance_type_allowed = rule {
       all ec2_instances as _, instance {
           instance.change.after.instance_type in allowed_types
       }
    }
     
    # Main rule that requires other rules to be true
     
    main = rule {
       (instance_type_allowed and mandatory_instance_tags) else true
    }

In the policy above, all EC2 instances:

* Must have a Name tag
* Must be of type t2.micro, t2.small or t2.medium (no instances larger than medium)

If you create an EC2 instance that does not meet all of these criteria, Sentinel will flag it with a FAIL. In Sentinel, you can have one of three things happen when a run doesn’t pass a policy check:

* Stop the run and show the user a warning, but allow them to manually push through provisioning
* Only allow the run to continue if an admin manually accepts the run
* Stop the run until the user modifies their configuration and passes policy checks

Some policy as code interfaces will give you full visibility of what occured during a policy check, with the ability to drill down into the details. Here is a different policy check example from within the HCP Terraform UI.

![Policy as code check results in the HCP Terraform UI. 2 Advisory \(non-blocking\) errors logged.](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1756404155-sentinel-in-terraform.png&w=3840&q=75)Open image in lightbox

Policy as code check results in the HCP Terraform UI. 2 Advisory (non-blocking) errors logged.

### »Policy as code should be readable by non-experts

Policies can be built and reviewed in collaboration with stakeholders from compliance, finance, cybersecurity, and other departments, but in order to do that, the policy language must be simple to read and write by individuals with a limited background in programming.

Sentinel is a good example of a policy language that’s clear enough to parse even by a non-expert. This is a key benefit of policy as code.

## »What are the benefits of policy as code?

As you automate more systems, your teams will get faster and more efficient, but the speed and scale at which you introduce security holes, compliance breaches, and outages increases as well.

How do you keep security, compliance, and reliability intact?

**This is why policy as code exists**: To maintain a set of _guardrails_ , or even hard _gates_ , that automatically warn or block deployment when operational requirements aren’t being followed.

The potential benefits of policy as code can be broken down into three categories: Increased productivity, lower risk, and reduced costs.

### »Productivity benefits

* Eliminates many manual ticketing and approval bottlenecks
* Enables fast feedback loops and reduces deployment times from weeks to hours and minutes
* Shifts compliance [left](https://www.hashicorp.com/en/blog/fix-the-developers-vs-security-conflict-by-shifting-further-left) to developers and “down” into the deployment platform, so both developers and compliance offload work to automation
* Reduces onboarding time and improves developer experience
* Enables [developer self-service](https://www.hashicorp.com/en/blog/scalable-secure-infrastructure-code-the-right-way-use-a-private-module-registry) by automating the last mile of software deployment
* Makes end-to-end automation possible in large enterprises with strict requirements

### »Security/risk reduction benefits

* Reduces human error through automated policy enforcement
* Catches violations before production by enforcing secure-by-design infrastructure
* Provides version-controlled policies with full visibility, accountability, traceability, and testability
* Enables faster incident response with quick policy updates across systems
* Provides a codebase that stakeholders from compliance, security, finance, etc. can collaborate on for better compliance outcomes.

### »Cost reduction benefits

* Enables leaner teams by automating manual review processes
* Enforces resource limits, tag tracking, and usage policies to avoid unnecessary cloud costs
* Frees security, compliance, and ops staff for strategic work

## »Policy as code in real use cases

These benefits aren’t just theoretical. Dozens of companies have spoken about their successes with policy as code:

> “All our departments, like governance and security and our central platform team, can now write policies as code that define what is allowed and what isn’t. All users immediately see if their code is compliant or not. Also included is**cost estimation**.”— [MediaMarkt's journey to compliance with Terraform](https://www.hashicorp.com/resources/mediamarkt-journey-to-compliance-with-terraform)

> “We wrote Sentinel policies … to be like, ‘Did you set your metadata correctly?’”— [Using Terraform Enterprise to support 3000 users at Booking.com](https://www.hashicorp.com/resources/using-terraform-enterprise-to-support-3000-users-at-booking-com)

> We've written a bunch of Sentinel policies — a combination of advisory, soft mandatory, hard mandatory — mostly to guide folks away from dangerous configurations we've discovered over the years.— [Transforming access to cloud infrastructure at Wayfair with Terraform Enterprise](https://www.hashicorp.com/resources/transforming-access-to-cloud-infrastructure-at-wayfair-with-terraform-enterprise)

> Sentinel is going to be that bouncer in a club that allows you to go in or out. For us, that gives us 100% confidence that anything provisioned by Terraform is following our security postures.— [Scaling innovation: ADB's cloud journey with Terraform](https://www.hashicorp.com/resources/scaling-innovation-adb-s-cloud-journey-with-terraform)

> You need resource guardrails in the cloud because you don't want your CFO coming down to your office saying, "Why did you deploy 50 R5.16XLs? We just missed our quarterly objectives because of your deployment." And this is a job for Sentinel.— [Terraform for the rest of us: A Petco ops case study](https://www.hashicorp.com/resources/terraform-for-the-rest-of-us-a-petco-ops-case-study)

And Fannie Mae [has a great presentation](https://www.hashicorp.com/en/blog/fannie-mae-process-for-developing-policy-as-code-with-terraform-enterprise-sentinel) about how they build policy as code.

## »You don’t have to write policy as code from scratch

The great thing about a common policy language is that users can share their policies with the community, and teams can benefit from the work that other organizations have already done building solid, reusable policies.

The Terraform Registry includes plenty of publicly available Sentinel policy sets, including two highly tested, turnkey policy sets developed by HashiCorp and AWS engineers:

* [Pre-written Sentinel policies for AWS CIS foundations benchmarking](https://www.hashicorp.com/en/blog/simplify-policy-adoption-in-terraform-with-pre-written-sentinel-policies-for-aws)
* [Pre-written Sentinel policies for AWS FSBP foundations benchmarking](https://www.hashicorp.com/en/blog/terraform-adds-new-pre-written-sentinel-policies-aws-foundational-security-best-practices)

Need your own ideas for how policy as code could help your organization? Take a look at some concrete examples for each policy category:

**Category**|**Example**
---|---
Security | Ensure DynamoDB server-side encryption and CMK are enabled
Compliance | Ensure [CIS Benchmark policies](https://registry.terraform.io/policies/hashicorp/CIS-Policy-Set-for-AWS-Terraform/1.0.1#policies-included) are followed
Logging / Observability | Ensure Amazon ECS task logging to CloudWatch is enabled
Architecture | Ensure Azure Application Gateway uses approved subnets and security groups
Resilience | Ensure multi-availability-zone for Amazon RDS is enabled in production
FinOps | Ensure only approved instance types and sizings are used

## »Policy as code brings safe self-service

Overall, policy as code is a tool for automating requirements to create guardrails that keep infrastructure provisioning:

* Compliant
* Secure
* Resilient
* Cost-effective

**Developers like policy as code**because, although it may block them, they get instant feedback and can immediately try to start fixing their deployment, rather than having to manually create a ticket and then wait days or weeks for a review.

**Operations and other stakeholders**who need to ensure compliance**like policy as code**because they no longer have to spend most of their time managing and reviewing tickets, and can instead focus on more strategic work and on the most critical reviews.

We believe policy as code is a key requirement for many enterprises that want to modernize their software delivery processes. The implementation of policy as code in an organization helps to reduce human error, removes the need for a slow and error prone ticketing workflow, and minimizes dependencies on other teams as well. To enable a faster team that focuses on what matters, policy as code is a great next step in your infrastructure modernization journey.

Learn more about how HashiCorp can partner with you on your infrastructure modernization journey, read [Do cloud right with The Infrastructure Cloud](https://www.hashicorp.com/en/on-demand/infrastructure-cloud-whitepaper?utm_source=hashicorp.com&utm_medium=referral&utm_campaign=26Q3_WW_TDM_COST_policy-as-code-explained-blog&utm_content=ic-blog-end-cta&utm_offer=whitepaper).

* * *

[Risk & compliance](/en/blog/tags/risk-compliance)[Speed & agility](/en/blog/tags/speed-agility)[Optimize operations](/en/blog/tags/optimize-operations)[Platform engineering](/en/blog/tags/platform)[Infrastructure automation](/en/blog/tags/infrastructure-automation)[Sentinel](/en/blog/tags/sentinel)[Solution Engineering](/en/blog/tags/solution-engineering)

#### Sign up for the latest HashiCorp news

Email

Required

Send me news about HashiCorp products, releases, and events.

By submitting this form, you acknowledge and agree that HashiCorp will process your personal information in accordance with the [Privacy Policy](https://www.hashicorp.com/trust/privacy).

Sign Up

#### More blog posts like this one

[![10 strategies to mitigate hybrid cloud risk](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1756840076-unlock-hero-graphic-secrets-infrastructure-imagery-icon.png&w=3840&q=75)September 11 2025 | Strategy & insights10 strategies to mitigate hybrid cloud riskMitigate hybrid cloud risk management through proven security strategies that eliminate blind spots, prevent misconfigurations, and automate policy enforcement across your entire infrastructure estate.](/en/blog/10-strategies-to-mitigate-hybrid-cloud-risk)[![How do you overcome cloud complexity? Find out in our 2025 Cloud Complexity Report](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1757349646-ccr-thumbnail-16-9.png&w=3840&q=75)September 10 2025 | Strategy & insightsHow do you overcome cloud complexity? Find out in our 2025 Cloud Complexity ReportHashiCorp’s 2025 Cloud Complexity Report shares insight from 1,100 organizations around the world on the top cloud management challenges they are facing, and what you can do to overcome them.](/en/blog/how-do-you-overcome-cloud-complexity-find-out-in-our-2025-cloud-complexity-report)[![Why secrets management is incomplete without secret scanning](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1695238878-vault-keys-pki-imagery.png&w=3840&q=75)September 04 2025 | Strategy & insightsWhy secrets management is incomplete without secret scanningLearn how secret scanning gives your teams the visibility, detection, and guardrails to minimize secret exposure.](/en/blog/why-secrets-management-is-incomplete-without-secret-scanning)
