#!/usr/bin/env python3
import os
from aws_cdk import core
from cluster.cluster_stack import EksClusterStack
from vpc.vpc_stack import VpcStack

app = core.App()

vpc_stack = VpcStack(
                scope=app,
                construct_id='eks-cluster-vpc-stack',
                env=core.Environment(
                    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                    region=os.getenv('CDK_DEFAULT_REGION'))
            )


eks_stack = EksClusterStack(
                scope=app,
                construct_id="eks-cluster-stack",
                vpc=vpc_stack.vpc,
                env=core.Environment(
                    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                    region=os.getenv('CDK_DEFAULT_REGION'))
            )

app.synth()
