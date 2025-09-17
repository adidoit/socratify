---
title: "Simplify multi-tenant encryption with a cost-conscious AWS KMS key strategy"
author: "Unknown"
url: "https://aws.amazon.com/blogs/architecture/simplify-multi-tenant-encryption-with-a-cost-conscious-aws-kms-key-strategy/"
date: "2025-09-15"
---

# Simplify multi-tenant encryption with a cost-conscious AWS KMS key strategy

Organizations face [diverse challenges when it comes to managing encryption keys](https://aws.amazon.com/blogs/security/aws-kms-how-many-keys-do-i-need/). While some scenarios demand strict separation, there are compelling use cases where a centralized approach can streamline operations and reduce complexity. In this post, our focus is on a software-as-a-service (SaaS) provider scenario, but the principles we discuss can be adopted by large organization facing similar key management challenges.

Managing encryption across a multi-tenant, multi-service architecture presents a significant challenge. Many organizations find themselves struggling with the complexity and costs associated with provisioning separate [AWS Key Management Service (AWS KMS) customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk) for each tenant and service. This approach, while secure, often leads to growing operational overhead and increased AWS KMS usage costs over time.

But what if there was a more efficient way?

In this post, we unveil a strategy that uses a single customer managed key (symmetric) per tenant across services. By the end of this post, you’ll learn:

* How to implement a scalable, secure, and cost-effective encryption model
* Techniques for using one customer managed key per tenant across multiple services and environments
* Methods for encrypting tenant data in [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) and other storage types while maintaining tenant isolation

##**Multi-tenant encryption requirements for SaaS providers**

Data isolation is fundamental to multi-tenant SaaS architectures, serving both compliance requirements and customer confidence. Many SaaS providers need to encrypt sensitive information—from API keys and credentials to personal data—across storage solutions such as DynamoDB and [Amazon Simple Storage Service (Amazon S3)](https://aws.amazon.com/s3/).

While these storage services provide default encryption at rest, they typically use a single shared key across data items. Consider [DynamoDB in a shared pool model](https://aws.amazon.com/blogs/apn/partitioning-pooled-multi-tenant-saas-data-with-amazon-dynamodb/), where one table contains data from multiple tenants. In this setup, the tenant data is encrypted using the same [AWS KMS Key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html), regardless of ownership.

KMS key represents a container for top-level key material and is uniquely defined within the KMS, for more information on the different keys involved when encrypting or decrypting data using KMS, see [AWS KMS key hierarchy](https://docs.aws.amazon.com/kms/latest/cryptographic-details/key-hierarchy.html).

This shared-key approach often proves insufficient for SaaS providers operating under strict security and compliance frameworks. Some customers require:

* Bring your own key (BYOK) capabilities
* Logical isolation of their data through dedicated encryption keys

To meet these requirements, providers can implement customer-specific AWS KMS managed keys, helping to ensure that each customer’s sensitive data remains isolated and inaccessible to other tenants.

Alternatively, providers might consider a silo model with separate tables for each customer. However, this approach introduces its own challenges—as the tenant base grows, managing numerous individual tables becomes increasingly complex and [service quota](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) limits might become a constraint.

##**Managing growth: KMS key management at scale**

When scaling a SaaS platform, empowering teams to develop services independently is crucial. A quick way to scale is to have [each team develop independently using a dedicated account](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-workload-oriented-ous.html). This often leads to a decentralized approach where each service manages its own KMS keys per customer. However, this autonomy comes with hidden costs as your customer base and service portfolio expand.

### The challenge of key proliferation

As the company grows, the number of keys multiplies with each new customer and service addition. This proliferation creates several organizational challenges:

***Cost impact**: A single AWS KMS key costs $1 monthly, increasing to a maximum of $3 per month with two or more key rotations.
***Operational complexity**: Managing many KMS keys across environments and accounts is error-prone and hard to scale.
***Organizational waste**: Duplicate efforts across teams because each develops and maintains their own code for managing customer key lifecycles.
***Governance overhead**: It becomes difficult to enforce consistent policies or track KMS key usage across multiple AWS accounts.

### A streamlined approach

The solution lies in implementing a [centralized key management strategy](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-kms-best-practices/key-management.html). One KMS key per tenant, maintained in a central AWS account. This approach effectively addresses the cost, operational, and governance challenges while maintaining security.

In the following sections, we explore how to implement this centralized approach and securely share KMS keys across various services and AWS accounts.

##**Solution overview: Centralizing tenant key management**

At the heart of our solution lies a centralized tenant key management service (shown as Service A in the following figure). This service handles every aspect of customer KMS key lifecycle—from creation during tenant onboarding to managing aliases, access policies and deletion.

The service achieves secure, scalable key usage across the organization through cross-account AWS Identity and Access Management (IAM) access. It grants other services (for example, the customer-facing service in Account B in the following figure) a permission to perform specific encryption operations using tenant-specific KMS keys through role delegation. This implementation follows AWS best practices for cross-account access, utilizing IAM and [AWS Security Token Service (AWS STS)](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html) role assumption as described in[ the AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies-cross-account-resource-access.html) and this [blog post](https://aws.amazon.com/blogs/apn/isolating-saas-tenants-with-dynamically-generated-iam-policies/).

![Architecture diagram showing centralizing tenant key management flow with JWT authentication, role assumption ,data encryption and saving in DynamoDB](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/07/ARCHBLOG-1093.png)

### Centralized key management in practice: Encrypting customer data

Let’s examine how this works in practice with a common scenario:

* Service A: Our centralized tenant key management service in Account A
* Service B: A customer-facing workload running in Account B

When a customer interacts with Service B, it needs to store sensitive information securely, whether that’s secrets, API keys, or license information in a DynamoDB table. Instead of relying on shared KMS keys or default encryption, Service B encrypts data using the customer’s dedicated KMS key managed by Service A. The process works through [AWS Identity and Access Management (IAM)](https://aws.amazon.com/iam) role delegation. Service B temporarily assumes a role (`ServiceARole`) in Account A, receiving fine-grained, scoped down permissions for the specific tenant’s KMS key. With these temporary credentials, Service B can perform client-side encryption operations on sensitive information using the AWS SDK or the [AWS Encryption SDK](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/introduction.html).

In this blog post, we used Boto3. For more advanced use-cases requiring [data key caching](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/data-key-caching.html) or [keyrings](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/choose-keyring.html), use the AWS Encryption SDK.

##**Solution walkthrough**

Let’s expand the technical aspects of the solution depicted above. Assumptions and definitions:

* Incoming requests include an authentication header with a [JSON Web Token](https://jwt.io/) (JWT) that includes data identifying the current tenant’s ID. These tokens are signed by an identity provider, making sure that the JWT cannot be modified, and the tenant identity can be trusted.
* Account A: Centralized key management service.
* Account B: Business service that serves customer requests.
*`alias/customer-<tenant-id>`is the format of the aliases in account A. Each alias points to the KMS key of the corresponding customer identified by value of`<tenant-id>`. Service A creates these aliases during tenant onboarding and deletes them during tenant offboarding.
*`ServiceARole`: A role in Account A that can encrypt and decrypt a KMS key that has an alias prefixed with`alias/customer-*`. The permissions are scoped down further using [session policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) when`ServiceBRole`assumes`ServiceARole`.
*`ServiceBRole`: A role in Account B that can assume`ServiceARole`in Account A to gain access to the customer’s KMS key. This will be the [AWS Lambda](https://aws.amazon.com/lambda/) function’s execution role.

Note that Service B’s compute layer in this case is a Lambda function, but the solution works for other compute architectures. Let’s go over the flow in more detail:

### Use service with JWT

A customer who belongs to a tenant signs in to the SaaS solution and is given a JWT that identifies its tenants with a tenant ID (`<tenant-id>`). The customer makes an action in ServiceB and sends sensitive information.

ServiceB handles the request (in a Lambda function), verifies the JWT token and wants to:

* 1. Encrypt the customer’s sensitive data
    2. Save the encrypted data along with other data in the DynamoDB table

### Assume role

In this example, the Lambda function uses its [execution role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html) credentials to assume the ServiceA role in the ServiceA account. Another way to grant cross-account access to KMS keys is by using KMS [grants](https://docs.aws.amazon.com/kms/latest/developerguide/grants.html), to learn more, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).

Let’s review the ServiceRoleA IAM policy:

Grants encrypt and decrypt access to a KMS key using the`alias/customer-*`pattern.

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowKMSByAlias",
          "Effect": "Allow",
          "Action": [
            "kms:Encrypt",
            "kms:Decrypt",
            "kms:GenerateDataKey*"
          ],
          "Resource": "*",
          "Condition": {
            "StringLike": {
              "kms:RequestAlias": "alias/customer-*"
            }
          }
        }
      ]
    }

To encrypt tenant secrets securely and at scale, we grant application roles cross-account access to KMS keys—but only through their alias, which maps to a tenant identifier present in their JWT authentication token, enforcing strong isolation.

You can control access to KMS keys based on the aliases that are associated with each KMS key. To do so, use the [kms:RequestAlias](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-request-alias) and [kms:ResourceAliases](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-resource-aliases) condition keys as specified in the [Use aliases to control access to KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/alias-authorization.html).

In addition, the trust relationship policy of the ServiceARole allows the ServiceBRole in account B to assume it:

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::<ACCOUNT_B_ID>:role/ServiceBRole"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }

Depending on your environment, you can add additional conditions to this trust policy to further reduce the scope of who can assume this role. For more information, see [IAM and AWS STS condition context keys.](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html)

Then, each KMS customer managed key will have the following policy. For example, a KMS key for a customer with`<tenant-id>: 123`will have a policy that restricts access to the key using the specific customer alias and only through ServiceRoleA.

    {
      "Version": "2012-10-17",
      "Id": "TenantKeyPolicy",
      "Statement": [
        {
          "Sid": "AllowServiceARoleViaAlias",
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::<ACCOUNT_A_ID>:role/ServiceARole"
          },
          "Action": [
            "kms:Encrypt",
            "kms:Decrypt",
            "kms:GenerateDataKey*"
          ],
          "Resource": "*",
          "Condition": {
            "StringLike": {
              "kms:RequestAlias": "alias/customer-123"
            }
          }
        }
      ]
    }

The following is a Python code example demonstrating how Service B dynamically assumes a role in Account A to encrypt data for a specific tenant using a session-scoped IAM policy that allows access only to that tenant’s KMS key alias.

This pattern follows the same principles outlined in[ Isolating SaaS Tenants with Dynamically Generated IAM Policies](https://aws.amazon.com/blogs/apn/isolating-saas-tenants-with-dynamically-generated-iam-policies/). The idea is to generate and attach a tenant-specific IAM policy at runtime, granting the minimum required permissions to operate on tenant-owned resources—in this case, a KMS key alias. The credentials will allow the Lambda function to use only the KMS key that belongs to a customer (identified by`tenant_id`).

We will call the`assume_role_for_tenant`for every tenant.

The condition of`"StringEquals" - "kms:RequestAlias": alias`is the magical AWS STS sauce, it restricts ServiceB to use the current tenant’s alias in its encryption SDK calls and relies on [alias authorization](https://docs.aws.amazon.com/kms/latest/developerguide/alias-authorization.html)

    import boto3
    def assume_role_for_tenant(tenant_id: str):
        alias = f"alias/customer-{tenant_id}"
        # Session policy scoped to only the specific alias
        session_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "kms:Encrypt",
                        "kms:Decrypt",
                        "kms:GenerateDataKey*"
                    ],
                    "Resource": "*",
                    "Condition": {
                        "StringEquals": {
                            "kms:RequestAlias": alias
                        }
                    }
                }
            ]
        }
        # Assume ServiceARole in Account A with inline session policy
        sts = boto3.client("sts")
        assumed = sts.assume_role(
            RoleArn="arn:aws:iam::<ACCOUNT_A_ID>:role/ServiceARole",
            RoleSessionName=f"Tenant{tenant_id}Session",
            Policy=json.dumps(session_policy)
        )
        return assumed["Credentials"]

### Encrypt data and save in DynamoDB

Now, what remains to do is use the assumed role credentials and use AWS SDK to encrypt the sensitive customer data and store it in the DynamoDB table.

    # Use temporary credentials to create a KMS client
        creds = assume_role_for_tenant(tenant_id, plaintext)
        kms = boto3.client(
            "kms",
            region_name="us-east-1",
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"]
        )
        # Encrypt using the alias
        response = kms.encrypt(
            KeyId= f"alias/customer-{tenant_id}"
            Plaintext=plaintext
        )
        # store response["CiphertextBlob"] in DynamoDB table

This post doesn’t address isolation between different services, only between tenants. If such service isolation is required, you can use [encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html), an optional set of non-secret key/value pairs that can contain additional contextual information about the data, for example the service identifier. This helps ensure that services can only encrypt or decrypt data using the relevant service encryption context.

##**Benefits of centralized key management**

Let’s examine how this solution addresses our earlier challenges.

### Tenant isolation by design

Despite reducing the total number of KMS keys, we maintain strict tenant isolation. Each customer’s sensitive data remains encrypted with their dedicated key, identified by a unique alias (`alias/customer-<tenant-id>`). Access control to the tenant key is tightly managed through IAM role delegation, following least privilege principles:

* Service A exclusively controls the management of the tenants’ KMS keys.
* Service B can only assume a role that grants restricted encrypt, decrypt, and GenerateDataKey access for the customer managed key designated by the alias:`alias/customer-<tenant-id>`.

### Optimized cost management

Our approach significantly reduces costs by moving from multiple service-specific KMS keys per tenant to a single KMS key per tenant that is shared securely across services and environments. This behavior introduces a new centralized account (Account A) that provides access to encryption keys under the right circumstances. It is important to understand [AWS STS limits](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html), specifically for`AssumeRole`calls and consider temporary IAM credentials caching mechanisms if those limits become a bottleneck. Additionally, if [KMS limits](https://docs.aws.amazon.com/kms/latest/developerguide/requests-per-second.html) are a bottleneck, consider using [data key caching](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/data-key-caching.html) by using the AWS Encryption SDK.

### Streamlined operations and governance

By centralizing key management in Service A, you can achieve:

* Consistent KMS key lifecycle management across the organization
* Improved audit capabilities using [AWS CloudTrail](https://aws.amazon.com/cloudtrail) to better understand key access patterns by service
* Reduced operational overhead
* Simplified compliance monitoring

The only additional complexity is the initial cross-account role delegation setup between Service A and other services. After being established, this framework can be scaled to accommodate new tenants and services.

It’s best to encapsulate the assume-role logic, policy generation, and AWS SDK client initialization within a shared organization-wide SDK. This abstraction reduces cognitive load for developers and minimizes the risk of misconfigurations. You can take it a step further by exposing high-level utility functions such as`encrypt_tenant_data()`and`decrypt_tenant_data()`, hiding the underlying complexity while promoting secure and consistent usage patterns across teams.

##**Conclusion**

In this post, we explored an efficient approach to managing encryption keys in a multi-tenant SaaS environment through centralization. We examined common challenges faced by growing SaaS providers, including key proliferation, rising costs, and operational complexity across multiple AWS accounts and services. The solution, centralizing key management, uses AWS best practices for IAM role delegation and cross-account access, enabling organizations to maintain security and compliance while reducing operational overhead. By implementing this approach, SaaS providers or large organizations facing similar challenges can effectively manage their encryption infrastructure as they scale, without compromising on security or increasing complexity.

* * *

### About the authors

Loading comments…
