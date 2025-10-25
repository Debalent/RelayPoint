# RelayPoint Elite Helm Chart

This Helm chart deploys the RelayPoint Elite platform on Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- PV provisioner support in the underlying infrastructure

## Getting Started

### Add the Helm repository

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

### Install the chart

```bash
# Create namespace
kubectl create namespace relaypoint

# Install chart with release name "relaypoint"
helm install relaypoint ./helm/relaypoint --namespace relaypoint
```

## Configuration

See [values.yaml](values.yaml) for configuration options.

## Upgrading

```bash
helm upgrade relaypoint ./helm/relaypoint --namespace relaypoint
```