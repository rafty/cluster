# import aws_cdk.aws_ec2
from aws_cdk import core as cdk
from aws_cdk import aws_iam
from aws_cdk import aws_eks
from aws_cdk import aws_ec2
import yaml


class EksClusterStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 # vpc: aws_ec2.Vpc,  # from VPC Stack
                 vpc,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create master role for EKS Cluster
        iam_role = aws_iam.Role(
            scope=self,
            id=f'{construct_id}-iam',
            role_name=f'{construct_id}-iam',
            assumed_by=aws_iam.AccountRootPrincipal()
            # assumed_by=aws_iam.ServicePrincipal('eks.amazon.com'),
            # managed_policies=[
            #     aws_iam.ManagedPolicy.from_aws_managed_policy_name(
            #         "AmazonEKSClusterPolicy"
            #     ),
            #     aws_iam.ManagedPolicy.from_aws_managed_policy_name(
            #         "AmazonEKS_CNI_Policy"
            #     ),
            #     aws_iam.ManagedPolicy.from_aws_managed_policy_name(
            #         "AmazonEKSVPCResourceController"
            #     )
            # ]
        )

        # Creating Cluster with EKS
        eks_cluster = aws_eks.Cluster(
            scope=self,
            id=f'{construct_id}-cluster',
            cluster_name=f'{construct_id}-cluster',
            vpc=vpc,
            vpc_subnets=[
                aws_ec2.SubnetSelection(
                    subnet_type=aws_ec2.SubnetType.PUBLIC),
                aws_ec2.SubnetSelection(
                    subnet_type=aws_ec2.SubnetType.PRIVATE)
            ],
            masters_role=iam_role,
            default_capacity_instance=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.BURSTABLE2,
                aws_ec2.InstanceSize.MICRO),
            version=aws_eks.KubernetesVersion.V1_21,
            endpoint_access=aws_eks.EndpointAccess.PUBLIC
        )

        # output = cdk.CfnOutput(
        #     self,
        #     ""
        # )

        # Read the deployment config
        with open('cdk8s/dist/cdk8s-deployment.k8s.yaml', 'r') as stream:
            deployment_yaml = yaml.load(stream, Loader=yaml.FullLoader)

        eks_cluster.add_manifest(
            f'{construct_id}-app-deployment',
            deployment_yaml
        )

        # Read the service config
        with open('cdk8s/dist/cdk8s-service.k8s.yaml', 'r') as stream:
            service_yaml = yaml.load(stream, Loader=yaml.FullLoader)

        eks_cluster.add_manifest(
            f'{construct_id}-app-service',
            service_yaml
        )
