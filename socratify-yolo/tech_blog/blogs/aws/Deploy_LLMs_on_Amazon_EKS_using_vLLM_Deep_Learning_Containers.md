---
title: "Deploy LLMs on Amazon EKS using vLLM Deep Learning Containers"
author: "Unknown"
url: "https://aws.amazon.com/blogs/architecture/deploy-llms-on-amazon-eks-using-vllm-deep-learning-containers/"
date: "2025-09-15"
---

# Deploy LLMs on Amazon EKS using vLLM Deep Learning Containers
Organizations face significant challenges when deploying large language models (LLMs) efficiently at scale. Key challenges include optimizing GPU resource utilization, managing network infrastructure, and providing efficient access to model weights.When running distributed inference workloads, organizations often encounter complexity in orchestrating model operations across multiple nodes. Common challenges include effectively distributing model components across available GPUs, coordinating seamless communication between processing units, and maintaining consistent performance with low latency and high throughput.
[vLLM](https://docs.vllm.ai/en/latest/) is an open source library for fast LLM inference and serving. The [vLLM AWS Deep Learning Containers (DLCs)](https://docs.aws.amazon.com/deep-learning-containers/latest/devguide/dlc-vllm-0-8-x86-ec2.html) are optimized for customers deploying vLLMs on [Amazon Elastic Compute Cloud](http://aws.amazon.com/ec2) (Amazon EC2), [Amazon Elastic Container Service](http://aws.amazon.com/ecs) (Amazon ECS), and [Amazon Elastic Kubernetes Service](https://aws.amazon.com/eks/) (Amazon EKS), and are provided at no additional charge. These containers package a preconfigured, pre-tested environment that functions seamlessly out of the box, includes the necessary dependencies such as drivers and libraries for running vLLMs efficiently, and offers built-in support for [Elastic Fabric Adapter](https://aws.amazon.com/hpc/efa/) (EFA) for high-performance multi-node inference workloads. You don’t have to build the inference environment from scratch anymore. Instead, you can install the vLLM DLC and it will automatically set up and configure the environment, and you can start deploying the inference workloads at scale.
In this post, we demonstrate how to deploy the DeepSeek-R1-Distill-Qwen-32B model using AWS DLCs for vLLMs on Amazon EKS, showcasing how these purpose-built containers simplify deployment of this powerful open source inference engine. This solution can help you solve the complex infrastructure challenges of deploying LLMs while maintaining performance and cost-efficiency.
## AWS DLCs
AWS DLCs provide generative AI practitioners with optimized Docker environments to train and deploy generative AI models in their pipelines and workflows across Amazon EC2, Amazon EKS, and Amazon ECS. AWS DLCs are targeted for self-managed machine learning (ML) customers who prefer to build and maintain their AI/ML environments on their own, want instance-level control over their infrastructure, and manage their own training and inference workloads. DLCs are available as Docker images for training and inference, and also with PyTorch and TensorFlow.DLCs are kept current with the latest version of frameworks and drivers, are tested for compatibility and security, and are offered at no additional cost. They are also quickly customizable by following our recipe guides. Using AWS DLCs as a building block for generative AI environments reduces the burden on operations and infrastructure teams, lowers TCO for AI/ML infrastructure, accelerates the development of generative AI products, and helps the generative AI teams focus on the value-added work of deriving generative AI-powered insights from the organization’s data.
## Solution overview
The following diagram shows the interaction between Amazon EKS, GPU-enabled EC2 instances with EFA networking, and [Amazon FSx for Lustre](https://aws.amazon.com/fsx/lustre/) storage. Client requests flow through the Application Load Balancer (ALB) to the vLLM server pods running on EKS nodes, which access model weights stored on FSx for Lustre. This architecture provides a scalable, high-performance solution for serving LLM inference workloads with optimal cost-efficiency.
[![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-1-4.png)](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-1-4.png)
The following diagram illustrates the DLC stack on AWS. The stack demonstrates a comprehensive architecture from EC2 instance foundation through container runtime, essential GPU drivers, and ML frameworks like PyTorch. The layered diagram shows how CUDA, NCCL, and other critical components integrate to support high-performance deep learning workloads.
[![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-2-3.png)](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-2-3.png)
The vLLM DLCs are specifically optimized for high-performance inference, with built-in support for tensor parallelism and pipeline parallelism across multiple GPUs and nodes. This optimization enables efficient scaling of large models like DeepSeek-R1-Distill-Qwen-32B, which would otherwise be challenging to deploy and manage. The containers also include optimized CUDA configurations and EFA drivers, facilitating maximum throughput for distributed inference workloads. This solution uses the following AWS services and components:
***AWS DLCs for vLLMs**– Pre-configured, optimized Docker images that simplify deployment and maximize performance
***EKS cluster**– Provides the Kubernetes control plane for orchestrating containers
***P4d.24xlarge instances**– [EC2 P4d instances](https://aws.amazon.com/ec2/instance-types/p4/) with 8 NVIDIA A100 GPUs each, configured in a managed node group
***Elastic Fabric Adapter**– Network interface that enables high-performance computing applications to scale efficiently
***FSx for Lustre**– High-performance file system for storing model weights
***LeaderWorkerSet pattern**– Custom Kubernetes resource for deploying vLLM in a distributed configuration
***AWS Load Balancer Controller**– Manages the ALB for external access
By combining these components, we create an inference system that delivers low-latency, high-throughput LLM serving capabilities with minimal operational overhead.
## Prerequisites
Before getting started, make sure you have the following prerequisites:
* An [AWS account](https://portal.aws.amazon.com/billing/signup#/start/email) with access to EC2 P4 instances (you might need to [request a quota increase](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html))
* Access to a terminal that has the following tools installed:
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) version 2.11.0 or later
* [eksctl](https://eksctl.io/installation/) version 0.150.0 or later
* [kubectl](https://kubernetes.io/docs/tasks/tools/) version 1.27 or later
* [Helm](https://helm.sh/docs/intro/install/) version 3.12.0 or later
* An [AWS CLI profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) (vllm-profile) configured with an [AWS Identity and Access Management](https://aws.amazon.com/iam/) (IAM) role or user that has the following permissions:
* Create, manage, and delete EKS clusters and node groups (see [Create a Kubernetes cluster on the AWS Cloud](https://docs.aws.amazon.com/eks/latest/userguide/security-iam-id-based-policy-examples.html#policy-create-cluster) for more details)
* Create, manage, and delete EC2 resources, including virtual private clouds (VPCs), subnets, security groups, and internet gateways (see [Identity-based policies for Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-policies-for-amazon-ec2.html) for more details)
* Create and manage IAM roles (see [Identity-based policies and resource-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html) for more details)
* Create, update, and delete [AWS CloudFormation](http://aws.amazon.com/cloudformation) stacks
* Create, delete, and describe FSx file systems (see [Identity and access management for Amazon FSx for Lustre](https://docs.aws.amazon.com/fsx/latest/LustreGuide/security-iam.html) for more details)
* Create and manage Elastic Load Balancers
This solution can be deployed in AWS Regions where Amazon EKS, P4d instances, and FSx for Lustre are available. This guide uses the us-west-2 Region. The complete deployment process takes approximately 60–90 minutes.
Clone our GitHub repository containing the necessary configuration files:
# Clone the repository
git clone https://github.com/aws-samples/sample-aws-deep-learning-containers.git
cd vllm-samples/deepseek/eks
## Create an EKS cluster
First, we create an EKS cluster in the us-west-2 Region using the provided configuration file. This sets up the Kubernetes control plane that will orchestrate our containers. The cluster is configured with a VPC, subnets, and security groups optimized for running GPU workloads.
# Update the region in eks-cluster.yaml if needed
sed -i "s|region: us-east-1|region: us-west-2|g" eks-cluster.yaml
# Create the EKS cluster
eksctl create cluster -f eks-cluster.yaml --profile vllm-profile
This will take approximately 15–20 minutes to complete. During this time, eksctl creates a CloudFormation stack that provisions the necessary resources for your EKS cluster, as shown in the following screenshot.
[![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-3-2.png)](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-3-2.png)
You can validate the cluster creation with the following code:
# Verify cluster creation
eksctl get cluster --profile vllm-profile
Expected output:
NAME REGION EKSCTL CREATED
vllm-cluster us-west-2 True
You can also see the cluster created on the Amazon EKS console.
[![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-4-2.png)](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-4-2.png)
## Create a node group with EFA support
Next, we create a managed node group with P4d.24xlarge instances that have EFA enabled. These instances are equipped with 8 NVIDIA A100 GPUs each, providing substantial computational power for LLM inference. When deploying EFA-enabled instances like p4d.24xlarge for high-performance ML workloads, you must place them in private subnets to facilitate secure, optimized networking. By dynamically identifying and using a private subnet’s Availability Zone in your node group configuration, you can maintain proper network isolation while supporting the high-throughput, low-latency communication essential for distributed training and inference with LLMs. We identify the Availability Zone using the following code:
# Get the VPC ID from the EKS cluster
VPC_ID=$(aws --profile vllm-profile eks describe-cluster --name vllm-cluster \
--query "cluster.resourcesVpcConfig.vpcId" --output text)
# Find the one of private subnet's availability zone
PRIVATE_AZ=$(aws --profile vllm-profile ec2 describe-subnets \
--filters "Name=vpc-id,Values=$VPC_ID" "Name=map-public-ip-on-launch,Values=false" \
--query "Subnets[0].AvailabilityZone" --output text)
echo "Selected private subnet AZ: $PRIVATE_AZ"
# update the nodegroup_az section with the private AZ value
sed -i "s|availabilityZones: \[nodegroup_az\]|availabilityZones: \[\"$PRIVATE_AZ\"\]|g" large-model-nodegroup.yaml
# Verify the change
grep "availabilityZones" large-model-nodegroup.yaml
# Create the node group with EFA support
eksctl create nodegroup -f large-model-nodegroup.yaml --profile vllm-profile
This will take approximately 10–15 minutes to complete. The EFA configuration is particularly important for multi-node deployments, because it enables high-throughput, low-latency networking between nodes. This is crucial for distributed inference workloads where communication between GPUs on different nodes can become a bottleneck. After the node group is created, configure kubectl to connect to the cluster:
# Configure kubectl to connect to the cluster
aws eks update-kubeconfig --name vllm-cluster --region us-west-2 --profile vllm-profile
Verify that the nodes are ready:
# Check node status
kubectl get nodes
The following is an example of the expected output:
NAME STATUS ROLES AGE VERSION
ip-192-168-xx-xx.us-west-2.compute.internal Ready <none> 5m v1.31.7-eks-xxxx
ip-192-168-yy-yy.us-west-2.compute.internal Ready <none> 5m v1.31.7-eks-xxxx
You can also see the node group created on the Amazon EKS console.
## [![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-5-3.png)](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-5-3.png)
## Check NVIDIA device pods
Because we’re using an Amazon EKS optimized AMI with GPU support (ami-0ad09867389dc17a1), the NVIDIA device plugin is already included in the cluster, so there’s no need to install it separately. Verify that the NVIDIA device plugin is running:
# Check NVIDIA device plugin pods
kubectl get pods -n kube-system | grep nvidia
The following is an example of the expected output:
nvidia-device-plugin-daemonset-xxxxx 1/1 Running 0 3m48s
nvidia-device-plugin-daemonset-yyyyy 1/1 Running 0 3m48s
Verify that GPUs are available in the cluster:
# Check available GPUs
kubectl get nodes -o json | jq '.items[].status.capacity."nvidia.com/gpu"'
The following is our expected output:
"8"
"8"
## Create an FSx for Lustre file system
For optimal performance, we create an FSx for Lustre file system to store our model weights. FSx for Lustre provides high-throughput, low-latency access to data, which is essential for loading large model weights efficiently. We use the following code:
# Create a security group for FSx Lustre
FSX_SG_ID=$(aws --profile vllm-profile ec2 create-security-group --group-name fsx-lustre-sg \
--description "Security group for FSx Lustre" \
--vpc-id $(aws --profile vllm-profile eks describe-cluster --name vllm-cluster \
--query "cluster.resourcesVpcConfig.vpcId" --output text) \
--query "GroupId" --output text)
echo "Created security group: $FSX_SG_ID"
# Add inbound rules for FSx Lustre
aws --profile vllm-profile ec2 authorize-security-group-ingress --group-id $FSX_SG_ID \
--protocol tcp --port 988-1023 \
--source-group $(aws --profile vllm-profile eks describe-cluster --name vllm-cluster \
--query "cluster.resourcesVpcConfig.clusterSecurityGroupId" --output text)
aws --profile vllm-profile ec2 authorize-security-group-ingress --group-id $FSX_SG_ID \
--protocol tcp --port 988-1023 \
--source-group $FSX_SG_ID
# Create the FSx Lustre filesystem
SUBNET_ID=$(aws --profile vllm-profile eks describe-cluster --name vllm-cluster \
--query "cluster.resourcesVpcConfig.subnetIds[0]" --output text)
echo "Using subnet: $SUBNET_ID"
FSX_ID=$(aws --profile vllm-profile fsx create-file-system --file-system-type LUSTRE \
--storage-capacity 1200 --subnet-ids $SUBNET_ID \
--security-group-ids $FSX_SG_ID --lustre-configuration DeploymentType=SCRATCH_2 \
--tags Key=Name,Value=vllm-model-storage \
--query "FileSystem.FileSystemId" --output text)
echo "Created FSx filesystem: $FSX_ID"
# Wait for the filesystem to be available (typically takes 5-10 minutes)
echo "Waiting for filesystem to become available..."
aws --profile vllm-profile fsx describe-file-systems --file-system-id $FSX_ID \
--query "FileSystems[0].Lifecycle" --output text
# You can run the above command periodically until it returns "AVAILABLE"
# Example: watch -n 30 "aws --profile vllm-profile fsx describe-file-systems --file-system-id $FSX_ID --query FileSystems[0].Lifecycle --output text"
# Get the DNS name and mount name
FSX_DNS=$(aws --profile vllm-profile fsx describe-file-systems --file-system-id $FSX_ID \
--query "FileSystems[0].DNSName" --output text)
FSX_MOUNT=$(aws --profile vllm-profile fsx describe-file-systems --file-system-id $FSX_ID \
--query "FileSystems[0].LustreConfiguration.MountName" --output text)
echo "FSx DNS: $FSX_DNS"
echo "FSx Mount Name: $FSX_MOUNT"
The file system is configured with 1.2 TB of storage capacity, SCRATCH_2 deployment type for high performance, and security groups that allow access from our EKS nodes. You can also check the FSx for Lustre file system on the FSx for Lustre console.
[![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-6.png)](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-6.png)
## Install the AWS FSx CSI Driver
To mount the FSx for Lustre file system in our Kubernetes pods, we install the AWS FSx CSI Driver. This driver enables Kubernetes to dynamically provision and mount FSx for Lustre volumes.
# Add the AWS FSx CSI Driver Helm repository
helm repo add aws-fsx-csi-driver https://kubernetes-sigs.github.io/aws-fsx-csi-driver/
helm repo update
# Install the AWS FSx CSI Driver
helm install aws-fsx-csi-driver aws-fsx-csi-driver/aws-fsx-csi-driver --namespace kube-system
Verify that the AWS FSx CSI Driver is running:
# Check AWS FSx CSI Driver pods
kubectl get pods -n kube-system | grep fsx
The following is an example of the expected output:
fsx-csi-controller-xxxx 4/4 Running 0 24s
fsx-csi-controller-yyyy 4/4 Running 0 24s
fsx-csi-node-xxxx 3/3 Running 0 24s
fsx-csi-node-yyyy 3/3 Running 0 24s
## Create Kubernetes resources for FSx for Lustre
We create the necessary Kubernetes resources to use our FSx for Lustre file system:
# Update the storage class with your subnet and security group IDs
sed -i "s|<subnet-id>|$SUBNET_ID|g" fsx-storage-class.yaml
sed -i "s|<sg-id>|$FSX_SG_ID|g" fsx-storage-class.yaml
# Update the PV with your FSx Lustre details
sed -i "s|<fs-id>|$FSX_ID|g" fsx-lustre-pv.yaml
sed -i "s|<fs-id>.fsx.us-west-2.amazonaws.com|$FSX_DNS|g" fsx-lustre-pv.yaml
sed -i "s|<mount-name>|$FSX_MOUNT|g" fsx-lustre-pv.yaml
# Apply the Kubernetes resources
kubectl apply -f fsx-storage-class.yaml
kubectl apply -f fsx-lustre-pv.yaml
kubectl apply -f fsx-lustre-pvc.yaml
Verify that the resources were created successfully:
# Check storage class
kubectl get sc fsx-sc
# Check persistent volume
kubectl get pv fsx-lustre-pv
# Check persistent volume claim
kubectl get pvc fsx-lustre-pvc
The following is an example of the expected output:
NAME PROVISIONER RECLAIMPOLICY VOLUMEBINDINGMODE ALLOWVOLUMEEXPANSION AGE
fsx-sc fsx.csi.aws.com Retain Immediate false 1m
NAME CAPACITY ACCESS MODES RECLAIM POLICY STATUS CLAIM STORAGECLASS REASON AGE
fsx-lustre-pv 1200Gi RWX Retain Bound default/fsx-lustre-pvc fsx-sc 1m
NAME STATUS VOLUME CAPACITY ACCESS MODES STORAGECLASS AGE
fsx-lustre-pvc Bound fsx-lustre-pv 1200Gi RWX fsx-sc 1m
These resources include:
* A StorageClass that defines how to provision FSx for Lustre volumes
* A PersistentVolume that represents our existing FSx for Lustre file system
* A PersistentVolumeClaim that our pods will use to mount the file system
## Install the AWS Load Balancer Controller
To expose our vLLM service to the outside world, we install the AWS Load Balancer Controller. This controller manages ALBs for our Kubernetes services and ingresses. Refer to [Install AWS Load Balancer Controller with Helm](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html) for addition details.
# Download the IAM policy document
curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
# Create the IAM policy
aws --profile vllm-profile iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam-policy.json
# Create an IAM OIDC provider for the cluster
eksctl utils associate-iam-oidc-provider --profile vllm-profile --region=us-west-2 --cluster=vllm-cluster --approve
# Create an IAM service account for the AWS Load Balancer Controller
ACCOUNT_ID=$(aws --profile vllm-profile sts get-caller-identity --query "Account" --output text)
eksctl create iamserviceaccount \
--profile vllm-profile \
--cluster=vllm-cluster \
--namespace=kube-system \
--name=aws-load-balancer-controller \
--attach-policy-arn=arn:aws:iam::$ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
--override-existing-serviceaccounts \
--approve
# Install the AWS Load Balancer Controller using Helm
helm repo add eks https://aws.github.io/eks-charts
helm repo update
# Install the CRDs
kubectl apply -f https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml
# Install the controller
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
-n kube-system \
--set clusterName=vllm-cluster \
--set serviceAccount.create=false \
--set serviceAccount.name=aws-load-balancer-controller
Verify that the AWS Load Balancer Controller is running:
# Check AWS Load Balancer Controller pods
kubectl get pods -n kube-system | grep aws-load-balancer-controller
# Install the LeaderWorkerSet controller
helm install lws oci://registry.k8s.io/lws/charts/lws \
--version=0.6.1 \
--namespace lws-system \
--create-namespace \
--wait --timeout 300s
## Configure security groups for the ALB
We create a dedicated security group for the ALB and configure it to allow inbound traffic on port 80 from our client IP addresses. We also configure the node security group to allow traffic from the ALB security group to the vLLM service port.
# Create security group for the ALB
USER_IP=$(curl -s https://checkip.amazonaws.com)
VPC_ID=$(aws --profile vllm-profile eks describe-cluster --name vllm-cluster \
--query "cluster.resourcesVpcConfig.vpcId" --output text)
ALB_SG=$(aws --profile vllm-profile ec2 create-security-group \
--group-name vllm-alb-sg \
--description "Security group for vLLM ALB" \
--vpc-id $VPC_ID \
--query "GroupId" --output text)
echo "ALB security group: $ALB_SG"
# Allow inbound traffic on port 80 from your IP
aws --profile vllm-profile ec2 authorize-security-group-ingress \
--group-id $ALB_SG \
--protocol tcp \
--port 80 \
--cidr ${USER_IP}/32
# Get the node group security group ID
NODE_INSTANCE_ID=$(aws --profile vllm-profile ec2 describe-instances \
--filters "Name=tag:eks:nodegroup-name,Values=vllm-p4d-nodes-efa" \
--query "Reservations[0].Instances[0].InstanceId" --output text)
NODE_SG=$(aws --profile vllm-profile ec2 describe-instances \
--instance-ids $NODE_INSTANCE_ID \
--query "Reservations[0].Instances[0].SecurityGroups[0].GroupId" --output text)
echo "Node security group: $NODE_SG"
# Allow traffic from ALB security group to node security group on port 8000 (vLLM service port)
aws --profile vllm-profile ec2 authorize-security-group-ingress \
--group-id $NODE_SG \
--protocol tcp \
--port 8000 \
--source-group $ALB_SG
# Update the security group in the ingress file
sed -i "s|<sg-id>|$ALB_SG|g" vllm-deepseek-32b-lws-ingress.yaml
Verify that the security groups were created and configured correctly:
# Verify ALB security group
aws --profile vllm-profile ec2 describe-security-groups --group-ids $ALB_SG --query "SecurityGroups[0].IpPermissions"
The following is the expected output for the ALB security group:
[
{
"FromPort": 80,
"IpProtocol": "tcp",
"IpRanges": [
{
"CidrIp": "USER_IP/32"
}
],
"ToPort": 80
}
]
# Verify node security group rules
aws --profile vllm-profile ec2 describe-security-groups --group-ids $NODE_SG --query "SecurityGroups[0].IpPermissions"
## Deploy the vLLM server
Finally, we deploy the vLLM server using the LeaderWorkerSet pattern. The AWS DLCs provide an optimized environment that minimizes the complexity typically associated with deploying LLMs.The vLLM DLCs come preconfigured with the following features:
* Optimized CUDA libraries for maximum GPU utilization
* EFA drivers and configurations for high-speed node-to-node communication
* Ray framework setup for distributed computing
* Performance-tuned vLLM installation with support for tensor and pipeline parallelism
This prepackaged solution dramatically reduces deployment time, the need for complex environment setup, dependency management, and performance tuning that would otherwise require specialized expertise.
# Deploy the vLLM server
# First, verify that the AWS Load Balancer Controller is running
kubectl get pods -n kube-system | grep aws-load-balancer-controller
# Wait until the controller is in Running state
# If it's not running, check the logs:
# kubectl logs -n kube-system deployment/aws-load-balancer-controller
# Apply the LeaderWorkerSet
kubectl apply -f vllm-deepseek-32b-lws.yaml
The deployment will start immediately, but the pod might remain in ContainerCreating state for several minutes (5–15 minutes) while it pulls the large GPU-enabled container image. After the container starts, it will take additional time (10–15 minutes) to download and load the DeepSeek model.You can monitor the progress with the following code:
# Monitor pod status
kubectl get pods
# Check pod logs
kubectl logs -f <pod-name>
Here is the out put of one of the pods
Kubectl logs -f vllm-deepseek-32b-lws-0
[![](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-7.png)](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/08/04/image-7.png)
The following is the expected output when pods are running:
NAME READY STATUS RESTARTS AGE
vllm-deepseek-32b-lws-0 1/1 Running 0 10m
vllm-deepseek-32b-lws-0-1 1/1 Running 0 10m
We also deploy an ingress resource that configures the ALB to route traffic to our vLLM service:
# Apply the ingress (only after the controller is running)
kubectl apply -f vllm-deepseek-32b-lws-ingress.yaml
You can check the status of the ingress with the following code:
# Check ingress status
kubectl get ingress
The following is an example of the expected output:
NAME CLASS HOSTS ADDRESS PORTS AGE
vllm-deepseek-32b-lws-ingress alb * k8s-default-vllmdeep-xxxxxxxx-xxxxxxxxxx.us-west-2.elb.amazonaws.com 80 5m
## Test the deployment
When the deployment is complete, we can test our vLLM server. It provides the following API endpoints:
***/v1/completions**– For text completions
***/v1/chat/completions**– For chat completions
***/v1/embeddings**– For generating embeddings
***/v1/models**– For listing available models
# Test the vLLM server
# Get the ALB endpoint
export VLLM_ENDPOINT=$(kubectl get ingress vllm-deepseek-32b-lws-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "vLLM endpoint: $VLLM_ENDPOINT"
# Test the completions API
curl -X POST http://$VLLM_ENDPOINT/v1/completions \
-H "Content-Type: application/json" \
-d '{
"model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
"prompt": "Hello, how are you?",
"max_tokens": 100,
"temperature": 0.7
}'
The following is an example of the expected output:
{
"id": "cmpl-xxxxxxxxxxxxxxxxxxxxxxxx",
"object": "text_completion",
"created": 1717000000,
"model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
"choices": [
{
"index": 0,
"text": " I'm doing well, thank you for asking! How about you? Is there anything I can help you with today?",
"logprobs": null,
"finish_reason": "length",
"stop_reason": null,
"prompt_logprobs": null
}
],
"usage": {
"prompt_tokens": 5,
"total_tokens": 105,
"completion_tokens": 100
}
}
You can also test the chat completions API:
# Test the chat completions API
curl -X POST http://$VLLM_ENDPOINT/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
"model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
"messages": [{"role": "user", "content": "What are the benefits of using FSx Lustre with EKS?"}],
"max_tokens": 100,
"temperature": 0.7
}'
If you encounter errors, check the logs of the vLLM pods:
# Troubleshooting
kubectl logs -f <pod-name>
## Performance considerations
In this section, we discuss different performance considerations.
### Elastic Fabric Adapter
EFA provides significant performance benefits for distributed inference workloads:
***Reduced latency**– Lower and more consistent latency for communication between GPUs across nodes
***Higher throughput**– Higher throughput for data transfer between nodes
***Improved scaling**– Better scaling efficiency across multiple nodes
***Better performance**– Significantly improved performance for distributed inference workloads
### FSx for Lustre integration
Using FSx for Lustre for model storage provides several benefits:
***Persistent storage**– Model weights are stored on the FSx for Lustre file system and persist across pod restarts
***Faster loading**– After the initial download, model loading is much faster
***Shared storage**– Multiple pods can access the same model weights
***High performance**– FSx for Lustre provides high-throughput, low-latency access to the model weights
### Application Load Balancer
Using the AWS Load Balancer Controller with ALB provides several advantages:
***Path-based routing**– ALB supports routing traffic to different services based on the URL path
***SSL/TLS termination**– ALB can handle SSL/TLS termination, reducing the load on your pods
***Authentication**– ALB supports authentication through [Amazon Cognito](https://aws.amazon.com/cognito/) or OIDC
***AWS WAF**– ALB can be integrated with [AWS WAF](https://aws.amazon.com/waf/) for additional security
***Access logs**– ALB can log the requests to an [Amazon Simple Storage Service](http://aws.amazon.com/s3) (Amazon S3) bucket for auditing and analysis
## Clean up
To avoid incurring additional charges, clean up the resources created in this post. Run the provided ./cleanup.sh script to clean the Kubernetes resources (ingress, LeaderworkerSet, PersistentVolumeClaim, PersistentVolume, AWS Load Balancer Controller, and storage class), IAM resources, the FSX for Lustre file system, and the EKS cluster:
chmod +x cleanup.sh
./cleanup.sh
For more detailed cleanup instructions, including troubleshooting CloudFormation stack deletion failures, refer to the README.md file in the [GitHub repository](https://github.com/aws-samples/sample-aws-deep-learning-containers/blob/main/vllm-samples/deepseek/eks/README.md).
## Conclusion
In this post, we demonstrated how to deploy the DeepSeek-R1-Distill-Qwen-32B model on Amazon EKS using vLLMs, with GPU support, EFA, and FSx for Lustre integration. This architecture provides a scalable, high-performance system for serving LLM inference workloads.AWS Deep Learning Containers for vLLM provide a streamlined, optimized environment that simplifies LLM deployment by minimizing the complexity of environment configuration, dependency management, and performance tuning. By using these preconfigured containers, organizations can reduce deployment timelines and focus on deriving value from their LLM applications.By combining AWS DLCs with Amazon EKS, P4d instances with NVIDIA A100 GPUs, EFA, and FSx for Lustre, you can achieve optimal performance for LLM inference while maintaining the flexibility and scalability of Kubernetes.This solution helps organizations:
* Deploy LLMs efficiently at scale
* Optimize GPU resource utilization with container orchestration
* Improve networking performance between nodes with EFA
* Accelerate model loading with high-performance storage
* Provide a scalable, high performance inference API
The complete code and configuration files for this deployment are available in our[ GitHub repository](https://github.com/aws-samples/sample-aws-deep-learning-containers). We encourage you to try it out and adapt it to your specific use case.
* * *
### About the authors
