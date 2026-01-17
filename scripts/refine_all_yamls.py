
import os
import re

target_dir = r"e:\k8s-actions-task\k8s-yamls"

# Comprehensive Mapping
mapping = {
    # 0 - Pods
    "checks_volume_pod_svc.yaml": {
        "title": "Pod With Readiness Probe and Volume",
        "desc": "A Pod configuration including a readiness check and a persistent volume mount."
    },
    "emptydir_hostpath_volume.yaml": {
        "title": "Pod Using Multiple Volume Types",
        "desc": "A Pod configured with both EmptyDir and HostPath volumes for storage."
    },
    "minimal_pod.yaml": {
        "title": "Minimal Pod Configuration",
        "desc": "A basic Pod setup with essential configuration for a single container."
    },
    "multi_container_pod.yaml": {
        "title": "Multi Container Pod",
        "desc": "A Pod running multiple containers that share the same network and storage."
    },
    "one_container_pod.yaml": {
        "title": "Single Container Pod",
        "desc": "A standard Pod configuration for a single container application."
    },

    # 1 - deployment
    "checks-strategy.yaml": {
        "title": "Deployment With Strategy Checks",
        "desc": "A Deployment with configured health probes and a rollout strategy."
    },
    "minimal-dep.yaml": {
        "title": "Minimal Deployment Configuration",
        "desc": "A basic Deployment setup for managing container replicas."
    },
    "onecontainer-dep.yaml": {
        "title": "Single Container Deployment",
        "desc": "Deployment configuration for managing a single container application."
    },
    "primary-deployment.yaml": {
        "title": "Primary Application Deployment",
        "desc": "Comprehensive Deployment setup for a primary application workload."
    },
    "volume-dep.yaml": {
        "title": "Deployment With Volume Mounts",
        "desc": "A Deployment configuration that includes persistent volume mounts."
    },

    # 2 - services
    "mutliport-svc.yaml": {
        "title": "Multi Port Service",
        "desc": "A Service configuration exposing multiple ports for an application."
    },
    "services.yaml": {
        "title": "Standard LoadBalancer Service",
        "desc": "A Service used to expose an application externally or internally."
    },

    # 3 - namespace
    "namespace.yaml": {
        "title": "Namespace Resource",
        "desc": "Defines a Namespace to isolate resources within the cluster."
    },

    # 4 - configmap
    "key-value-cm.yaml": {
        "title": "ConfigMap Key Value Pairs",
        "desc": "Stores configuration data as a set of key-value pairs."
    },
    "multi-line-cm.yaml": {
        "title": "ConfigMap Multi Line Data",
        "desc": "Stores multi-line configuration files or data blocks."
    },

    # 5 - secrets
    "basic-auth.yaml": {
        "title": "Secret Basic Auth Credentials",
        "desc": "Securely stores username and password for basic authentication."
    },
    "opaque-sec.yaml": {
        "title": "Secret Opaque Data",
        "desc": "Stores arbitrary binary data or sensitive environment variables."
    },
    "sec-ssh.yaml": {
        "title": "Secret SSH Keys",
        "desc": "Securely stores SSH private or public keys."
    },
    "sec-tls.yaml": {
        "title": "Secret TLS Certificates",
        "desc": "Securely stores TLS certificates and private keys for encryption."
    },
    "svc-token.yaml": {
        "title": "Secret Service Account Token",
        "desc": "Stores a token used for Service Account authentication."
    },

    # 6 - serviceaccount
    "svc.yaml": {
        "title": "Standard Service Account",
        "desc": "Defines a Service Account to provide identity for workloads."
    },
    "svc-imagepull.yaml": {
        "title": "Service Account With Image Pull Secrets",
        "desc": "A Service Account configured to pull images from private registries."
    },

    # 7 - HPA
    "hpa.yaml": {
        "title": "Horizontal Pod Autoscaler",
        "desc": "Automatically scales the number of pod replicas based on metrics."
    },

    # 8 - resource-quota
    "object-count.yaml": {
        "title": "Resource Quota Object Limits",
        "desc": "Limits the total number of objects allowed in a namespace."
    },
    "resource-cpu-mem.yaml": {
        "title": "Resource Quota Compute Limits",
        "desc": "Limits the total CPU and memory resources available in a namespace."
    },
    "storage-quota.yaml": {
        "title": "Resource Quota Storage Limits",
        "desc": "Limits the total storage capacity allowed in a namespace."
    },

    # 9 - limitrange
    "limitrange-defaults.yaml": {
        "title": "LimitRange Container Defaults",
        "desc": "Sets default resource requests and limits for containers."
    },
    "pod-limit.yaml": {
        "title": "LimitRange Pod Constraints",
        "desc": "Sets minimum and maximum resource constraints for Pods."
    },

    # 10 - network-policy
    "allow-cidr-npc.yaml": {
        "title": "Network Policy External CIDR",
        "desc": "Allows ingress traffic from specific external IP ranges."
    },
    "allow-cross-npc.yaml": {
        "title": "Network Policy Cross Namespace",
        "desc": "Allows ingress traffic from pods in other namespaces."
    },
    "allow-deny.yaml": {
        "title": "Network Policy Multi Tier Rules",
        "desc": "Implements complex traffic flow rules between application tiers."
    },
    "network-policy.yaml": {
        "title": "Network Policy Standard Ingress",
        "desc": "Defines basic ingress rules for an application tier."
    },

    # 11 - pdb
    "max-pdb.yaml": {
        "title": "Pod Disruption Budget Max Unavailable",
        "desc": "Ensures high availability by limiting voluntary disruptions."
    },
    "min-pdb.yaml": {
        "title": "Pod Disruption Budget Min Available",
        "desc": "Ensures a minimum number of pods remain available during disruptions."
    },

    # 12 - deamonset
    "deamon-set.yaml": {
        "title": "DaemonSet For Node Level Workloads",
        "desc": "Runs a copy of a specific pod on every node in the cluster."
    },

    # 13 - jobs
    "jobs-env-volume.yaml": {
        "title": "Job With Environment And Volumes",
        "desc": "A task-based Job configured with env vars and storage."
    },
    "parellel-jobs.yaml": {
        "title": "Parallel Job Execution",
        "desc": "Runs multiple jobs in parallel to complete a task."
    },
    "resource-limits-jobs.yaml": {
        "title": "Job With Resource Management",
        "desc": "A Job configured with specific resource limits and deadlines."
    },
    "simple-jobs.yaml": {
        "title": "Simple Container Job",
        "desc": "A basic Job that runs a single task once."
    },

    # 14 - cronjobs
    "cronjobs.yaml": {
        "title": "Scheduled Container Job",
        "desc": "Runs a job automatically at defined time intervals."
    },

    # 15 - statefulset
    "headless-svc.yaml": {
        "title": "Headless Service For State Management",
        "desc": "Provided stable network identities for pods in a StatefulSet."
    },
    "statefulset.yaml": {
        "title": "StatefulSet Application",
        "desc": "Manages stateful applications with stable storage and network IDs."
    },

    # 16 - storageclass
    "aws-ebs-sc.yaml": {
        "title": "StorageClass AWS EBS",
        "desc": "Provides dynamic provisioning for AWS Elastic Block Store volumes."
    },
    "azure-sc.yaml": {
        "title": "StorageClass Azure Managed Disk",
        "desc": "Provides dynamic provisioning for Azure Managed Disks."
    },
    "gcp-sc.yaml": {
        "title": "StorageClass GCP Persistent Disk",
        "desc": "Provides dynamic provisioning for Google Cloud Persistent Disks."
    },

    # 17 - pvc
    "pvc.yaml": {
        "title": "Persistent Volume Claim",
        "desc": "Requests specific storage capacity and access modes from the cluster."
    }
}

# Fields to force view_type: dropdown
DROPDOWN_FIELDS = {
    "namespace": "",
    "serviceAccountName": "",
    "restartPolicy": "Always,OnFailure,Never",
    "imagePullPolicy": "IfNotPresent,Always,Never",
    "protocol": "TCP,UDP,SCTP",
    "accessModes": "ReadWriteOnce,ReadOnlyMany,ReadWriteMany",
    "reclaimPolicy": "Delete,Retain",
    "volumeBindingMode": "Immediate,WaitForFirstConsumer",
    "allowVolumeExpansion": "true,false",
    "automountServiceAccountToken": "true,false",
    "policyTypes": "Ingress,Egress",
    "type": {
        "Service": "ClusterIP,NodePort,LoadBalancer,ExternalName",
        "StorageClass": "", # Custom params
        "Secret": "Opaque,kubernetes.io/service-account-token,kubernetes.io/dockercfg,kubernetes.io/dockerconfigjson,kubernetes.io/basic-auth,kubernetes.io/ssh-auth,kubernetes.io/tls,bootstrap.kubernetes.io/token"
    }
}

def clean_desc(desc):
    # Remove image names like nginx, busybox, apache
    desc = re.sub(r'\b(nginx|busybox|apache|redis|mysql|postgres)\b', 'container', desc, flags=re.IGNORECASE)
    # Remove backticks around them
    desc = re.sub(r'`container`', 'container', desc)
    return desc

def process_file(filepath):
    filename = os.path.basename(filepath)
    if filename not in mapping:
        return

    m = mapping[filename]
    new_title = m["title"]
    new_desc = clean_desc(m["desc"])
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    current_kind = ""
    
    # First pass to find kind
    for line in lines:
        if line.strip().startswith("regex: ^") and line.strip().endswith("$"):
            val = line.strip().split("^")[-1].split("$")[0]
            # Simple heuristic to find Kind
            if val in ["Pod", "Deployment", "Service", "Secret", "ConfigMap", "DaemonSet", "Job", "CronJob", "StatefulSet", "StorageClass", "PersistentVolumeClaim", "Namespace", "HorizontalPodAutoscaler", "ResourceQuota", "LimitRange", "NetworkPolicy", "PodDisruptionBudget", "ServiceAccount"]:
                current_kind = val

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 1. Action Type
        if line.startswith("action_type:"):
            new_lines.append(f"action_type: {new_title}\n")
            i += 1
            continue
        
        # 2. Action Type Description
        if line.startswith("action_type_description:"):
            new_lines.append(f"action_type_description: {new_desc}\n")
            i += 1
            continue

        # 3. Namespace required: true
        if stripped == "namespace:":
            new_lines.append(line)
            i += 1
            # Look for required within next few lines
            while i < len(lines) and (lines[i].strip() or not lines[i].strip()):
                ls = lines[i].strip()
                if ls.startswith("required:"):
                    indent = lines[i][:lines[i].find("required:")]
                    new_lines.append(f"{indent}required: true\n")
                    i += 1
                    break
                if ls.endswith(":") and ls != "namespace:": # Hit next field
                    break
                new_lines.append(lines[i])
                i += 1
            continue

        # 4. Standardize Regex and Dropdowns
        if stripped.startswith("regex:"):
            val = stripped.split(":", 1)[1].strip()
            if val in [".*", "^.*$", "^.*", ".*$"]:
                i += 1
                continue # Remove generic regex
            # Remove slashes if missed
            if val.startswith("/") and val.endswith("/"):
                val = val[1:-1]
                new_lines.append(line[:line.find("regex:")] + f"regex: {val}\n")
                i += 1
                continue
        
        # 5. Dropdowns and values cleanup
        if "view_type:" in line:
            # Check if previous lines had a field name we care about
            # We look back or maintain state. For simplicity, we check field name in the block.
            pass

        # Field specific logic
        field_match = re.match(r'^(\s*)([a-zA-Z0-9]+):$', line)
        if field_match:
            indent = field_match.group(1)
            f_name = field_match.group(2)
            if f_name in DROPDOWN_FIELDS:
                new_lines.append(line)
                i += 1
                # Inside field block
                has_view_type = False
                has_dropdown_values = False
                block_indent = len(indent)
                
                while i < len(lines):
                    next_stripped = lines[i].strip()
                    next_indent = len(lines[i]) - len(lines[i].lstrip())
                    if next_indent <= block_indent and next_stripped:
                        break
                    
                    if next_stripped.startswith("view_type:"):
                        l_indent = lines[i][:lines[i].find("view_type:")]
                        new_lines.append(f"{l_indent}view_type: dropdown\n")
                        has_view_type = True
                        i += 1
                    elif next_stripped.startswith("dropdown_values:"):
                        l_indent = lines[i][:lines[i].find("dropdown_values:")]
                        vals = DROPDOWN_FIELDS[f_name]
                        if isinstance(vals, dict):
                            vals = vals.get(current_kind, "")
                        if vals:
                            new_lines.append(f"{l_indent}dropdown_values: {vals}\n")
                        else:
                            # Keep it if it has something, otherwise skip
                            if next_stripped == "dropdown_values:" or next_stripped == "dropdown_values: \"\"":
                                pass
                            else:
                                new_lines.append(lines[i])
                        has_dropdown_values = True
                        i += 1
                    else:
                        new_lines.append(lines[i])
                        i += 1
                
                # If finished block and missed fields
                if not has_view_type:
                    # Append it before leaving? Usually it's there.
                    pass
                continue

        new_lines.append(line)
        i += 1

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".yaml"):
            process_file(os.path.join(root, file))
