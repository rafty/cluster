#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart
from imports import k8s


class MyChart(Chart):
    def __init__(self, scope: Construct, id: str):

        # Label used for tagging pods to link in the service
        label = {'app': 'cdk8s'}

        # ----------------------------------------------------------
        # デプロイ用YAML
        # for cdk8s-deployment.k8s.yaml
        # Creates the deployment to spin up pods with your container
        # ----------------------------------------------------------
        super().__init__(scope, f'{id}-deployment')

        sample_container = k8s.Container(
            name='cdk8s',
            image='public.ecr.aws/s9u7u6x1/sample_app_001:no-db',
            ports=[k8s.ContainerPort(container_port=80)]
        )

        spec = k8s.DeploymentSpec(
            replicas=2,
            selector=k8s.LabelSelector(match_labels=label),
            template=k8s.PodTemplateSpec(
                metadata=k8s.ObjectMeta(labels=label),
                spec=k8s.PodSpec(
                    containers=[sample_container]
                )
            )
        )

        k8s.KubeDeployment(
            scope=self,
            id='deployment',
            spec=spec,
        )

        # ----------------------------------------------------------
        # サービス設定用YAML
        # for cdk8s-deployment.k8s.yaml
        # Creates the service to expose the pods to traffic
        # from the load balancer
        # ----------------------------------------------------------
        super().__init__(scope, f"{id}-service")

        service_spec = k8s.ServiceSpec(
            type='LoadBalancer',
            ports=[
                k8s.ServicePort(
                    port=80,
                    target_port=k8s.IntOrString.from_number(80)
                )
            ],
            selector=label
        )

        k8s.KubeService(
            scope=self,
            id='service',
            spec=service_spec
        )


app = App()
MyChart(app, "cdk8s")

app.synth()
