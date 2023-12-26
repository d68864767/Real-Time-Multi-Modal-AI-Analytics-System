```python
# Import necessary libraries
import os
from kubernetes import client, config

# Load kube config
config.load_kube_config()

# Create a Kubernetes API client
api = client.CoreV1Api()

# Define the deployment
def create_deployment_object():
    # Configureate Pod template container
    container = client.V1Container(
        name="multimodal-ai-analytics",
        image="multimodal-ai-analytics:latest",
        ports=[client.V1ContainerPort(container_port=80)],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "200Mi"},
            limits={"cpu": "500m", "memory": "500Mi"}
        )
    )

    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "multimodal-ai-analytics"}),
        spec=client.V1PodSpec(containers=[container])
    )

    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=3,
        template=template,
        selector={'matchLabels': {'app': 'multimodal-ai-analytics'}}
    )

    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="multimodal-ai-analytics"),
        spec=spec
    )

    return deployment

# Create deployment
def create_deployment(api, deployment):
    # Create deployement
    api.create_namespaced_deployment(
        body=deployment,
        namespace="default"
    )
    print("Deployment created")

# Update deployment
def update_deployment(api, deployment):
    # Update the deployment
    api.replace_namespaced_deployment(
        name="multimodal-ai-analytics",
        namespace="default",
        body=deployment
    )
    print("Deployment updated")

def main():
    # Create a deployment object
    deployment = create_deployment_object()

    # Create a deployment
    create_deployment(api, deployment)

    # Update the deployment
    update_deployment(api, deployment)

if __name__ == "__main__":
    main()
```
