---
title: "Changes Are Coming to the Okta Developer Edition Organizations"
company: "okta"
url: "https://developer.okta.com/blog/2025/05/13/okta-developer-edition-changes"
focus_area: "identity systems, authentication, security architecture"
system_score: 85
content_length: 10799
type: "comprehensive_systems_collection"
date: "2025-09-15"
---

  * [advocacy](/blog/tags/advocacy)
  * [javascript](/blog/tags/javascript)
  * [okta](/blog/tags/okta)
  * [python](/blog/tags/python)



#  Changes Are Coming to the Okta Developer Edition Organizations

[![avatar-edunham.jpg](/assets-jekyll/avatar-edunham-6d4800017cae969b6e9e28afdf7de8a85c8bdaec7e6421dcd91cb4f586d8ede4.jpg)](/blog/authors/edunham/) [E. Dunham](/blog/authors/edunham/)

May 13, 2025

Last Updated: May 28, 2025

4 MIN READ 

[__](https://twitter.com/intent/tweet?text=Changes Are Coming to the Okta Developer Edition Organizations by @oktadev &url=https://developer.okta.com/blog/2025/05/13/okta-developer-edition-changes "Share on Twitter")[__](https://www.linkedin.com/shareArticle?mini=true&url=https://developer.okta.com/blog/2025/05/13/okta-developer-edition-changes "Share on Linkedin")

![Changes Are Coming to the Okta Developer Edition Organizations](/assets-jekyll/blog/developer-edition-changes/social-68ed7bd594dc8adbb71af53ff72d27fc5c0610564e3f2884fc3947874bb47c16.png)

As part of [Okta’s Secure Identity Commitment](https://www.okta.com/secure-identity-commitment/) (OSIC) to lead the industry in the fight against identity attacks, we are making changes to improve our architecture related to developer organizations.

On May 22, 2025, our new Integrator Free Plan will become the default organization type when you sign up on developer.okta.com. If you are actively using an Okta Developer Edition org, please create an Integrator organization and migrate to it. The Okta Developer Edition [terms of service](https://developer.okta.com/terms/) will also be updated to clarify: neither your old Developer Edition organization nor your new Integrator organization is meant for production use cases.

## New Okta developer organization types tailored for you

We’ve redesigned our developer orgs to better fit how you build. Whether you’re testing app integrations, validating identity flows, or preparing for OIN submission, the new Integrator Free Plan is purpose-built for iterative development—not production deployment.

This new structure reflects real-world developer needs:

  * A clean, focused environment optimized for building and validating integrations
  * Terms that match typical pre-production use cases
  * Streamlined signup and org management aligned with how developers work today



By moving to an Integrator organization, you’ll get an environment that’s aligned with modern dev workflows—simpler, more relevant, and built to support how you build.

## Integrator organization benefits

This new organization structure will come with a number of benefits, such as improving integrator access to Okta support resources and expanding developer access to Okta product offerings for testing purposes.

The features available in the Integrator Free Plan are listed in [our reference docs](/docs/reference/org-defaults/).

## Deprecating Okta Developer Edition organizations

In July 2025, existing Okta Developer Edition organization will be deactivated. At this time, you will lose access to your old Okta Developer Edition organization and all resources in it.

### How to tell whether your organization is affected

To check whether an organization is in Okta Developer Edition, navigate to **Applications** > **Applications** in the Okta Admin Console. If you’re on Developer Edition, large text will inform you that “Developer Edition provides a limited number of apps”. This message appears below the Applications heading and above the Create App Integration button.

![Screenshot of developer edition app limit banner](/assets-jekyll/blog/developer-edition-changes/dev-org-banner-a2c2789d6634e5136ca06e7a27560df1c3009e1ae528b28569cb54d7cd246db4.jpg)

Organizations in which this banner is absent from the Applications list are not part of Developer Edition, and are unaffected by the Developer Edition deprecation.

## How to migrate your resources from Okta Developer Edition to Integrator Free Plan

Creating an Integrator Free Plan organization will give you a clean slate to test and develop in. However, you might want to replicate setup steps that you’ve performed in your Okta Developer Edition organization to continue work in progress. Several options are available for migrating your configuration from your Okta Developer Edition organization to your Integrator Free Plan organization.

![flowchart for deciding if and how to migrate data](/assets-jekyll/blog/developer-edition-changes/flowchart-584b0cda5cb153df188fb86edb28ca888524f17d8ccabcae7334cbc75bcd8436.jpg)

### Migrating published integrations

When you submit an integration to [the Okta Integration Network (OIN)](https://www.okta.com/integrations/), Okta makes its own copy of the integration for distribution to users. The integration is displayed in your account so you can update it and submit the updates, but users who install the app from the OIN get a copy of the latest accepted submission.

If you have a published integration in the OIN, it’ll remain available to users without interruption. To update your published integration from your integrator account, email `oin@okta.com` with your integrator account ID and a link to your app in the OIN catalog. The OIN team will verify that you can move the integration and then link it to the integrator account you specified.

You can make this request at any time, even after Developer Edition orgs are no longer available. Getting your integration linked to your Integrator account may take several days.

### Migrating data is optional

If you want to discard the configuration and data from your Okta Developer Edition organization and start fresh in a new Integrator Free Plan organization, create a new Integrator Free Plan organization and begin using it. Your Developer Edition resources and configuration will be deleted when old organization are deactivated in July..

### Re-create resources by re-running automation

If you automated the creation of resources in your Okta Developer Edition organization that you’d like to continue using in your Integrator Free Plan organization, your environment setup will be simple. Create an Integrator Free Plan organization, provide credentials to your setup tooling, and re-run that tooling.

### Add automation for long-term management

If you created resources in your Okta Developer Edition organization by hand and you want to automate management of those resources going forward, this is a great time to build the tooling you want using [Terraform](https://registry.terraform.io/providers/okta/okta/latest/docs) or [PowerShell](https://github.com/okta/okta-powershell-cli). [Terraformer](https://github.com/GoogleCloudPlatform/terraformer/blob/master/docs/okta.md) can help you generate Terraform configurations based on existing resources in your old organization.

### Use our migration tool for one-off organization backup

If you’d like to capture a snapshot of your current Okta Developer Edition configuration, try [our EnvSync migration tool](https://github.com/oktadev/okta-dev-account-migration-tool). It wraps the [Okta CLI Client](https://github.com/okta/okta-cli-client) to create files representing all supported objects in your Developer Edition organization, and can use these backup files to automatically re-create many of the objects in your new Integrator Free Plan organization.

## Migrate your public OIN Integration

If you have an integration in the [Okta Integration Network](https://www.okta.com/integrations/) associated with your Okta Developer Edition organization, sign up for a new Integrator Free Plan organization and contact Developer Support to request that your integration be migrated to your new organization. Developer Support will link your new organization to your integration so that you can easily update it as needed.

If you have been working on an integration for the Okta Integration Network but it has not yet been accepted, you are responsible for migrating your work in progress from your Developer Edition organization to an Integrator Free plan organization.

### Cutoff dates for OIN submissions

As of May 22, 2025, no new OIN integration submissions will be accepted from developer orgs. After May 22, you must use an Integrator Free Plan organization to submit OIN integrations.

If you have submitted an OIN integration from an Okta Developer Edition organization, it must be approved by June 9. Any submissions coming from Okta Developer Edition organizations that are still in Draft or In Review status on June 9 will be automatically rejected, and you will need to re-submit the same integration from an Integrator Free Plan organization.

## Key dates

Date | What happens  
---|---  
May 22, 2025 | Okta Developer Edition organizations can no longer be created. Following the sign-up flow now creates an Integrator Free Plan organizations instead. New OIN submissions from Developer Edition organizations are no longer accepted.  
June 9, 2025 | Draft and In Review OIN submissions from Okta Developer Edition organizations are automatically declined. Affected integrations must be re-submitted from an Integrator Free Plan organization.  
July 18, 2025 | Okta Developer Edition organizations deactivation begins, and all Okta Developer Edition organizations are deactivated in batches over the following days  
  
## Plan your migration now!

If you’ve used Okta Developer Edition organizations in the past, check now to see if any contain configurations that you’d like to keep. You can check whether you have an organization by checking your password manager for credentials saved on [the login page](https://developer.okta.com/login/), or searching your email for a welcome message from `<noreply@test-account.dev>`.

If you have any questions, don’t hesitate to contact us in the comments below.

**Changelog** :

  * May 28, 2025: Added info on determining org type 
  * Jul 9, 2025: Added "Migrating published integrations" section 



[![avatar-edunham.jpg](/assets-jekyll/avatar-edunham-6d4800017cae969b6e9e28afdf7de8a85c8bdaec7e6421dcd91cb4f586d8ede4.jpg)](/blog/authors/edunham/) [E. Dunham](/blog/authors/edunham/)

[__](https://github.com/edunham "GitHub Profile")[__](https://twitter.com/qedunham "Twitter Profile")

[ __Previous post](/blog/2025/04/21/akanksha-bhasin-intro "Astronomy Geek to Oktanaut: Landing as a Dev Advocate at Okta") [Next post __](/blog/2025/06/16/sohail-pathan-intro "Superheroes, Startups, and Security: Sohail's Path to Developer Advocacy at Okta")

[](/blog/2025/05/13/okta-developer-edition-changes)

Okta Developer Blog Comment Policy

We welcome relevant and respectful comments. Off-topic comments may be removed.

Please enable JavaScript to view the comments inline. [Visit the forum to comment](https://devforum.okta.com/c/okta-dev-blog/17). 
