# Kubernetes Actions Validation with Argo CD

## Description

This repository is designed to test and validate Kubernetes resource actions in a GitOps-based workflow using [Argo CD](https://argo-cd.readthedocs.io/). It enables a streamlined method for managing and deploying Kubernetes resources while ensuring controlled and deterministic behavior during testing and validation.

### Goals
- **Pre-define Kubernetes resource manifests** for different actions.
- **Validate each action independently** for both correctness and compatibility.
- **Synchronize and apply resources** using Argo CD.
- **Simplify deployments for non-technical users** by abstracting YAML configurations via a future frontend/UI integration.

The repository focuses on a step-by-step testing mechanism for Kubernetes resource manifests and Argo CD synchronization (steps 3–7).

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<org>/<repo>.git
   cd <repo>
   ```

2. Ensure Argo CD is installed and configured on your Kubernetes cluster. Refer to the [official Argo CD documentation](https://argo-cd.readthedocs.io/).

3. Confirm `kubectl` is installed and configured to communicate with your cluster.

---

## Usage

### Step-by-Step Testing Workflow

1. **YAML Creation**
   - Generate Kubernetes resource YAML manifests with realistic and production-oriented configurations (e.g., resource limits, probes, selectors).

2. **Server-Side Validation**
   - Use the `kubectl apply` dry-run mode to validate the YAML manifest:
     ```bash
     kubectl apply --dry-run=server -f <file>.yaml
     ```
   - This ensures schema correctness, API compatibility, and validity of fields.

3. **Git Commit**
   - Add the validated YAML to the repository:
     ```bash
     git add actions/<action>/
     git commit -m "test(<action>): add manifest"
     git push
     ```

4. **Argo CD Synchronization**
   - Argo CD automatically detects changes in Git and synchronizes the manifests with the Kubernetes cluster.

5. **Resource Verification**
   - Verify the applied resource using commands such as:
     ```bash
     kubectl get <resource>
     kubectl describe <resource>
     kubectl logs <pod>
     kubectl auth can-i ...
     ```

6. **Drift & Rollback Testing**
   - Introduce manual changes to the live resource and confirm that Argo CD self-heals.
   - Revert Git changes and ensure Argo CD prunes the resource as intended.

---

## Repository Structure

The repository is organized into two main folders:

```
.
├── actions/
│   └── # Contains pure Kubernetes resource manifests.
├── argocd-app/
│   └── # Contains Argo CD Application manifests.
└── README.md
```

### `actions/` Folder
Contains predefined Kubernetes resource manifests, each action organized into a separate folder. All YAML files are:
1. Independently testable.
2. Kubernetes-valid and production-ready.
3. Designed to be synced and managed by Argo CD.

**Covered Actions**
| Category              | Folder                  | Resource                     |
|-----------------------|-------------------------|------------------------------|
| **Core Workloads**    | `0 - Pods`             | Pod                          |
|                       | `1 - deployment`       | Deployment                   |
|                       | `12 - daemonset`       | DaemonSet                    |
|                       | `15 - statefulset`     | StatefulSet                  |
|                       | `13 - jobs`            | Job                          |
|                       | `14 - cronjobs`        | CronJob                      |
| **Networking**        | `2 - services`         | Service                      |
|                       | `10 - network-policy`  | NetworkPolicy                |
| **Configuration & Secrets** | `4 - configmap`  | ConfigMap                   |
|                       | `5 - secrets`          | Secret (multiple types)      |
| **Scaling & Availability** | `7 - HPA`         | HorizontalPodAutoscaler      |
|                       | `11 - pdb`             | PodDisruptionBudget          |
| **Security & Identity** | `6 - serviceaccount` | ServiceAccount               |
|                       | `8 - resource-quota`   | ResourceQuota                |
|                       | `9 - limitrange`       | LimitRange                   |
| **Storage**           | `16 - storageclass`    | StorageClass                 |
|                       | `17 - pvc`             | PersistentVolumeClaim        |

### `argocd-app/` Folder
Contains Argo CD Application manifests, with each folder mapping to its respective Kubernetes action in the `actions/` folder. Every Argo CD Application is designed for:
- Independent synchronization and rollback.
- Clear isolation for debugging and future UI integration.

**Example Structure**:
```
argocd-app/
└── 1 - deployment/
    └── deployment-app.yaml
```

**Sample Argo CD Application Manifest**:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: deployment-test
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/<org>/<repo>.git
    targetRevision: main
    path: actions/deployment/simple-dep
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## Features

- **Action-Wise GitOps Workflow**:
  - Each Kubernetes action is pre-defined, validated, and tested independently.
  
- **Separation of Logic and Configuration**:
  - Actions (`actions/`) and Argo CD Applications (`argocd-app/`) are clearly separated for modular control and scalability.

- **Drift Management and Rollbacks**:
  - Argo CD ensures automatic self-healing and easy rollback with Git as the source of truth.

- **Future Frontend Integration**:
  - Designed to enable a UI/Frontend for users to deploy actions without exposing YAML configurations.

- **Scalability**:
  - Ideal for evolving Kubernetes environments with increasing complexity.

---

## Status Tracking

- **Git Commit History**:
  - Serves as a log of testing and deployment activities.

- **Argo CD Application Status**:
  - Provides visibility into synchronization and health states.

- **Kubernetes Resource Health**:
  - Verification of resources directly in the cluster ensures reliability.

This setup guarantees full auditability, reproducibility, and ease of debugging.

---

## License

This repository is licensed under the [MIT License](LICENSE).