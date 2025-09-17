---
title: "5 DevEx and platform"
author: "Unknown"
url: "https://www.hashicorp.com/blog/5-devex-and-platform-mindset-lessons-from-bt-group-s-hybrid-cloud-journey"
date: "2025-09-15"
---

[](/en/blog/products/terraform)[](/en/blog/products/vault)[](/en/blog/products/boundary)Customer stories & success

* Twitter share
* LinkedIn share
* Facebook share
* Copy URL

# 5 DevEx and platform-mindset lessons from BT Group's hybrid cloud journey

Learn how highly-regulated BT Group transformed its security and operations approach using HashiCorp's platform.

Sep 08 2025[Mitch Pronschinske](/blog/authors/mitch-pronschinske)

When a company with nearly two centuries of history needs to modernize its infrastructure to defend against nation-state actors while meeting new regulatory requirements, the approach matters as much as the technology. BT Group's Security Director for Networking, Christian Schwartz, recently shared their transformation story, offering five key lessons for technical decision-makers navigating similar challenges.

## »**1\. Start with a gateway product**

The most successful [platform](https://www.hashicorp.com/en/resources/what-is-a-platform-team-and-why-do-we-need-them) adoptions don't try to solve everything at once. BT Group began its HashiCorp journey strategically, focusing on infrastructure automation before expanding to the broader platform.

> "We started off with [Terraform](https://www.hashicorp.com/en/products/terraform) because it is just this tool that allows us to create those templates, abstract infrastructure away, make this reusable stuff and create this shared responsibility model within BT between who's taking care of the platform engineering and who's building the apps on top." — Christian Schwartz, Security Director for Networking, BT Group

HashiCorp Terraform served as what he calls "the gateway product" — providing immediate value through [infrastructure as code](https://www.hashicorp.com/en/resources/what-is-infrastructure-as-code) while establishing the foundation for broader platform adoption. This approach allowed teams to experience the benefits of automation and standardization before committing to a complete platform overhaul.

**Key takeaway**: Choose an initial tool that delivers clear, measurable value while building the organizational muscle for platform thinking.

## »**2\. Focus on developer experience**

Security transformations fail when they create friction for development teams. BT Group's approach centers on the core principle of sustainable adoption.

> "I'm a big believer — as I said from the beginning, we want to make the secure way the easy way. You want to raise the security bar but also remove friction and put it to a minimum. Tools like [Vault](https://www.hashicorp.com/en/products/vault) (I spoke about [Boundary](https://www.hashicorp.com/en/products/boundary) and [EntraID](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id) at the leadership track last year, for example) create a frictionless experience for teams who want to either service, configure something, or build an app and deploy an app." — Christian Schwartz, Security Director for Networking, BT Group

The impact extends beyond convenience to actual security outcomes. By implementing HashiCorp Vault for secrets management with automatic rotation, they fundamentally changed their security posture. Making secrets [short-lived](https://www.hashicorp.com/en/blog/why-we-need-short-lived-credentials-and-how-to-adopt-them) and using workflows that remove the need for credentials altogether make it very hard for attackers to steal credentials or use them long enough to cause harm.

But it all starts with making security-by-default feel invisible and effortless to the developer when they use platform workflows.

**Key takeaway**: Security improvements that reduce developer friction will be adopted faster and maintained longer than those that create additional complexity.

## »**3\. Embrace platform thinking**

BT Group operates one of the most complex infrastructure environments imaginable — managing VM-first environments, Kubernetes clusters, [Nomad](https://www.hashicorp.com/en/products/nomad) deployments, and more across a hybrid cloud with multiple providers. Their solution was abstraction with a platform mindset.

The platform team built abstracted workflows in order to just be able to say, ‘Just develop your service, and based on your configurations, the platform will decide which environment is best for it.’ Developers don’t have to worry whether it runs on a Kubernetes cluster or whether it should run in a private cloud or public cloud. The templates and modules will help developers use the best security configurations and the most efficient infrastructure for their application.

This platform approach reduces cognitive load so teams can focus on business value rather than infrastructure specifics. The result is a model where security and compliance become built-in characteristics rather than afterthoughts.

**Key takeaway**: Platform thinking means abstracting complexity away from users, letting platform engineers and other stakeholders manage the complexity with well-planned automation and templates.

## »**4\. Standardize across environments**

Rather than attempting to standardize their diverse infrastructure environments, BT Group standardized its interaction model across all environments using HashiCorp's integrated platform.

> "If you use the whole chain of HashiCorp tooling, you can actually abstract away all of the underlying platforms. It's about simplification, it's about abstracting away what you have underneath, it's about focusing on building your ‘hello world’ and deploying it in the most efficient way with best practices built in." — Christian Schwartz, Security Director for Networking, BT Group

This approach enabled what Christian describes as an “API-first and not necessarily an opinionated view of where you should deploy.” Teams build for an abstracted environment rather than specific cloud providers, gaining portability and fine-grained control without vendor lock-in.

**Key takeaway**: Standardize developer interfaces so that you can work with non-standard, diverse infrastructure. Provide flexibility for configuration entry fields while including built-in security and compliance guardrails for all deployments.

## »**5\. Plan for the future**

While addressing immediate operational needs, BT Group simultaneously prepares for longer-term challenges that many organizations haven't yet considered. “We need to keep in mind that, certainly for big and complex companies such as ourselves, it takes about 10 years to switch crypto[graphy],” Christian said. He cites the emergence of quantum computing attacks as a major threat to every industry, and emphasizes the need to [start preparing now](https://www.hashicorp.com/en/blog/start-planning-for-quantum-computing-cyberattacks-now).

Their approach includes implementing Software Bill of Materials ([SBOM](https://www.hashicorp.com/en/blog/hcp-packer-provides-further-artifact-visibility-with-sbom-storage)) and Crypto Bill of Materials capabilities, along with supply chain security validation using standards like [Google SLSA](https://cloud.google.com/blog/products/application-development/google-introduces-slsa-framework). These investments in observability and validation create the foundation for future transitions while improving the current security posture.

**Key takeaway**: Architecture decisions made today should account for challenges that may emerge 5-10 years from now, especially in cryptography and supply chain security. Read about [HashiCorp’s plans](https://www.hashicorp.com/en/blog/nist-s-post-quantum-cryptography-standards-our-plans) for NIST’s quantum cryptography standards.

## »**The platform advantage**

BT Group's experience illustrates how navigating hybrid cloud in a highly regulated industry requires process and culture change, and it also requires technology stacks that can nudge your teams toward best practices.

By starting with a gateway product, focusing on developer experience, embracing platform thinking, standardizing interfaces rather than infrastructure, and planning for future challenges, they've positioned themselves to handle both current operational demands and emerging threats.

A platform approach:

* Reduces security toil
* Gives developers precise feedback
* Aligns environments with code

As Christian summarized: “It becomes all design patterns and reusability, best practices, secure-by-design, secure-by-default, simplification, reduction of cognitive load.”

To learn more about how HashiCorp can help you achieve the platform engineering outcomes that can drive your hybrid environments into the future, check out: [Deliver innovation at scale with The Infrastructure Cloud](https://www.hashicorp.com/en/on-demand/deliver-innovation-at-scale-with-the-infrastructure-cloud?utm_source=hashicorp.com&utm_medium=referral&utm_campaign=26Q3_WW_SPEED_5-lessons-BT_WHITEPAPER&utm_content=blog-learn-more-conclusion&utm_offer=whitepaper).

Watch Christian’s full interview session below:

* * *

[Speed & agility](/en/blog/tags/speed-agility)[Platform engineering](/en/blog/tags/platform)[Infrastructure automation](/en/blog/tags/infrastructure-automation)[Secrets & identity management](/en/blog/tags/secrets-identity-management)[Culture & collaboration](/en/blog/tags/culture-collaboration)

#### Sign up for the latest HashiCorp news

Email

Required

Send me news about HashiCorp products, releases, and events.

By submitting this form, you acknowledge and agree that HashiCorp will process your personal information in accordance with the [Privacy Policy](https://www.hashicorp.com/trust/privacy).

Sign Up

#### More blog posts like this one

[![4 security wins from Booking.com's hybrid cloud migration](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1749749749-cloud-maturity-road-bridge.png&w=3840&q=75)September 03 2025 | Customer stories & success4 security wins from Booking.com's hybrid cloud migrationLearn how Booking.com leveraged HashiCorp Vault to accelerate and secure their hybrid/multi-cloud transformation while maintaining operational efficiency.](/en/blog/4-security-wins-from-booking-com-s-hybrid-cloud-migration)[![5 lessons from Moneybox’s Terraform journey](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1755552449-moneybox-ed-fretwell.jpg&w=3840&q=75)August 19 2025 | Customer stories & success5 lessons from Moneybox’s Terraform journeyLearn about Moneybox’s infrastructure-scaling transformation, and how the transition to HCP Terraform supported it.](/en/blog/5-lessons-from-moneybox-s-terraform-journey)[![Helvetia’s journey building an enterprise serverless product with Terraform](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1742506469-16_9-social-image-helvetia.jpg&w=3840&q=75)July 02 2025 | Customer stories & successHelvetia’s journey building an enterprise serverless product with TerraformWhat started as a basic compliance challenge for one team at Helvetia Insurance evolved into a comprehensive enterprise solution for running self-managed installations like a cloud service, using Terraform to manage a serverless architecture.](/en/blog/helvetia-s-journey-building-an-enterprise-serverless-product-with-terraform)
