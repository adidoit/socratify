---
title: "Infrastructure As Code"
company: "render"
url: "https://docs.render.com/infrastructure-as-code"
focus_area: "deployment infrastructure, cloud platforms"
system_score: 44
content_length: 9047
type: "comprehensive_systems_collection"
date: "2025-09-15"
---

# Render Blueprints (IaC)

## Manage your Render infrastructure with a single YAML file.

**Blueprints** are Render's infrastructure-as-code (IaC) model for defining, deploying, and managing multiple resources with a single YAML file:

Web service

DB

Environment  
group

`render.yaml`

**\+ Show example Blueprint**

yamlCopy to clipboard
    
    
    # This is a basic example Blueprint for a Django web service and
    
    # the Render Postgres database it connects to.
    
    services:
    
      - type: web # A Python web service named django-app running on a free instance
    
        plan: free
    
        name: django-app
    
        runtime: python
    
        repo: https://github.com/render-examples/django.git
    
        buildCommand: './build.sh'
    
        startCommand: 'python -m gunicorn mysite.asgi:application -k uvicorn.workers.UvicornWorker'
    
        envVars:
    
          - key: DATABASE_URL # Sets DATABASE_URL to the connection string of the django-app-db database
    
            fromDatabase:
    
              name: django-app-db
    
              property: connectionString
    
    
    
    
    databases:
    
      - name: django-app-db # A Render Postgres database named django-app-db running on a free instance
    
        plan: free

A Blueprint acts as the single source of truth for configuring an interconnected set of services, databases, and [environment groups](/docs/configure-environment-variables#environment-groups). Whenever you update a Blueprint, Render automatically redeploys any affected services to apply the new configuration (you can disable this).

As your infrastructure grows over time, Blueprints become more and more helpful for managing changes and additions to it.

**Do not manage a particular service, database, or environment group with more than one Blueprint.**

If you do this, Render always attempts to apply the configuration from whichever Blueprint was synced most recently. If the Blueprints differ in their configuration, this can result in unpredictable behavior for your services.

To avoid this scenario, make sure that each of your resources is managed by at most one Blueprint.

## Setup

  1. From the root of a Git repo, create an empty file named `render.yaml`.

     * Every Blueprint file uses the name `render.yaml` and resides at the root of a Git repo.
  2. Populate `render.yaml` with the details of the resources you want to create and manage.

     * If you're testing out Blueprints, try pasting the example Blueprint at the [top of this page](/docs/infrastructure-as-code).
     * See also the complete [Blueprint specification reference](/docs/blueprint-spec).
  3. Commit and push your changes to GitHub or GitLab.

  4. Open the [Render Dashboard](https://dashboard.render.com) and click **New > Blueprint**:

![Creating a new Blueprint in the Render Dashboard](/docs-assets/a858645e26837a5428b4dc43d8d288dc386b09d30f959ecbf3df1aea33bfd1f7/new-blueprint.png)

  5. In the list that appears, click the **Connect** button for whichever repo contains your Blueprint.

     * You'll first need to connect your [GitHub](/docs/github)/[GitLab](/docs/gitlab) account if you haven't yet.
  6. In the form that appears, provide a name for your Blueprint and specify which branch of your repo to link.

     * Each push to this branch that modifies `render.yaml` triggers a deploy of any added or modified resources.
  7. Review the list of the changes that Render will apply based on the linked Blueprint:

![List of new resources from a Blueprint](/docs-assets/e11a90906bb931fc8a8b8287e84eb5a4cf1c9e4b5980095827806d2d65417f1c/yaml-sync.png)

If your Blueprint file contains errors, the page instead displays details about those errors.

  8. If everything looks correct, click **Apply**.




You're all set! Render begins provisioning the resources defined in your Blueprint:

![Blueprint provisioning progress in the Render Dashboard](/docs-assets/97b4ce4951c3ae1ffffcf2de3878c9fa97f4436f1013eb7907d65c83158260e7/blueprint-provisioning.png)

## Generating a Blueprint from existing services

You can generate a `render.yaml` file using any combination of your existing Render services. This is useful if you want to start managing those exact resources with a Blueprint, or if you want to replicate those resources.

In the [Render Dashboard](https://dashboard.render.com), select any number of your services, then click **Generate Blueprint** at the bottom of the page:

![UI for generating a Blueprint in the Render Dashboard](/docs-assets/15af8c7de656893617ff403e13df3d361bc4441b0cf02da78ae2f1823cb63041/generate-blueprint.png)

This opens a page where you can download or copy the generated `render.yaml` file. The page provides additional instructions for creating a Blueprint from that file.

**Important:** For security, the generated `render.yaml` file includes the _names_ of all defined environment variables for the selected services, _but not their values_. Instead, the file sets `sync: false` for each environment variable.

If you use your `render.yaml` file to create a Blueprint with _new_ services instead of your existing ones, you'll need to provide values for these environment variables. For details, see [Setting environment variables](/docs/blueprint-spec#setting-environment-variables).

## Replicating a Blueprint

You can create multiple Blueprints from a single `render.yaml` file. Each Blueprint creates and manages a completely independent set of resources.

The Blueprint creation flow displays a notice if your new Blueprint matches existing Render resources:

![Notification that Blueprint matches existing resources](/docs-assets/a83318f500c679203a0e4fcad1525662e8c0cef8a02db27656a3e8ec91b314c3/blueprint-existing-instance.png)

To replicate your Blueprint with a separate set of resources, click **Create New Resources**. Render appends a suffix to the name of each new resource to prevent collisions with your existing resources:

![render.yaml suffix](/docs-assets/7e81f2d012b1533520eb4aa80c9c61be5c79043abcbbc4329187bd35f9f88e5d/yaml-suffix.png)

Click **Apply** to create the new resources as usual.

## Managing Blueprint resources

### Adding an existing resource

**Do not add an existing resource to a Blueprint if it's already managed by _another_ Blueprint.**

Doing so can lead to unpredictable behavior for your services.

You can add an existing Render resource to your Blueprint. To do so, add the resource's details to your `render.yaml` file as you would for a new resource. See all supported fields and values for each service type in the [Blueprint specification reference](/docs/blueprint-spec).

**Make sure to include all configuration options that are currently set for the resource in the Render Dashboard.** For most services, this includes the service's `name`, `type`, `plan` (instance type), `buildCommand`, `startCommand`, and so on. If you omit some of these options, your Blueprint will use a default value that almost definitely differs from your service's existing configuration.

When you next sync your Blueprint, Render applies the new configuration to the existing resource. The resource retains any existing environment variable values that aren't overwritten by the Blueprint.

### Modifying a resource outside of its Blueprint

You _can_ still make changes to a Blueprint-managed resource in the [Render Dashboard](https://dashboard.render.com). However, if any of those changes conflict with configuration defined in the Blueprint, they're overwritten the next time you sync your Blueprint.

Even if you _delete_ a Blueprint-managed resource in the Render Dashboard, Render recreates it the next time you sync your Blueprint! See Deleting a resource.

### Deleting a resource

**Syncing a Blueprint never deletes an existing resource.** This is true even if you remove a resource definition from your Blueprint file, or if you disconnect your Blueprint from Render entirely. This is a safeguard against accidental deletions (for example, if you revert your Blueprint to a commit that predates the addition of a critical resource).

To delete a Blueprint-managed resource, _first_ remove it from your Blueprint, _then_ delete it in the [Render Dashboard](https://dashboard.render.com) as usual.

If you delete a resource in the Render Dashboard but _keep_ it in your Blueprint, Render _recreates_ that resource the next time you sync your Blueprint.

## Disabling automatic sync

By default, Render automatically updates affected resources every time you push Blueprint changes to your linked branch.

To instead control exactly when you sync a particular Blueprint, set **Auto Sync** to **No** on your Blueprint's Settings page:

![render.yaml settings screen](/docs-assets/f7fd2de35a6ec85b301332289b055bce344b885b077108448093b564a14b0b62/yaml-settings.png)

You can then manually trigger a sync by clicking **Manual Sync** on your Blueprint's page.

## Supported fields and values

See the complete [Blueprint specification reference](/docs/blueprint-spec).
