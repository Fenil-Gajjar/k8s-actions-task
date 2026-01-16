
import os

target_dir = r"e:\k8s-actions-task\k8s-yamls"

# Mapping filename -> Generic Description
mapping = {
    # 0 - Pods
    "checks_volume_pod_svc.yaml": "Pod having a readiness check and a volume mount.",
    "emptydir_hostpath_volume.yaml": "Pod using EmptyDir and HostPath volumes.",
    "minimal_pod.yaml": "A minimal Pod configuration with a single container.",
    "multi_container_pod.yaml": "A Pod running multiple containers side-by-side.",
    "one_container_pod.yaml": "A standard Pod running a single container.",

    # 1 - deployment
    "checks-strategy.yaml": "Deployment with liveness/readiness probes and update strategy.",
    "minimal-dep.yaml": "A minimal Deployment configuration.",
    "onecontainer-dep.yaml": "Deployment managing a single-container application.",
    "primary-deployment.yaml": "Primary Deployment configuration for an application.",
    "volume-dep.yaml": "Deployment with persistent volume mounts.",
    
    # 2 - services
    "mutliport-svc.yaml": "Service exposing multiple ports.",
    "services.yaml": "Standard Service exposing an application.",

    # 3 - namespace
    "namespace.yaml": "Namespace to isolate resources.",
    
    # 4 - configmap
    "key-value-cm.yaml": "ConfigMap storing configuration as key-value pairs.",
    "multi-line-cm.yaml": "ConfigMap storing multi-line configuration data.",
    
    # 5 - secrets
    "basic-auth.yaml": "Secret storing basic authentication credentials.",
    "opaque-sec.yaml": "Secret storing arbitrary opaque data.",
    "sec-ssh.yaml": "Secret storing SSH authentication keys.",
    "sec-tls.yaml": "Secret storing TLS certificates.",
    "svc-token.yaml": "Secret storing a Service Account token.",

    # 6 - serviceaccount
    "svc.yaml": "Service Account for workload identity.",
    "svc-imagepull.yaml": "Service Account configured with image pull secrets.",
    
    # 7 - HPA
    "hpa.yaml": "Horizontal Pod Autoscaler based on CPU and memory usage.",
    
    # 8 - resource-quota
    "object-count.yaml": "Resource Quota limiting the count of objects in a namespace.",
    "resource-cpu-mem.yaml": "Resource Quota limiting total CPU and memory usage.",
    "storage-quota.yaml": "Resource Quota limiting total storage consumption.",
    
    # 9 - limitrange
    "limitrange-defaults.yaml": "LimitRange setting default requests and limits for containers.",
    "pod-limit.yaml": "LimitRange setting minimum and maximum limits for Pods.",
    
    # 10 - network-policy
    "allow-cidr-npc.yaml": "Network Policy allowing traffic from specific IP ranges.",
    "allow-cross-npc.yaml": "Network Policy allowing traffic from specific namespaces.",
    "allow-deny.yaml": "Network Policy with complex allow and deny rules.",
    "network-policy.yaml": "Network Policy allowing ingress from frontend to backend.",
    
    # 11 - pdb
    "max-pdb.yaml": "Pod Disruption Budget specifying maximum unavailability.",
    "min-pdb.yaml": "Pod Disruption Budget specifying minimum availability.",
    
    # 12 - deamonset
    "deamon-set.yaml": "DaemonSet running a pod replica on every node.",
    
    # 13 - jobs
    "jobs-env-volume.yaml": "Job using environment variables and volumes.",
    "parellel-jobs.yaml": "Job running multiple pods in parallel.",
    "resource-limits-jobs.yaml": "Job configured with resource limits and active deadline.",
    "simple-jobs.yaml": "A simple Job running a defined task.",
    
    # 14 - cronjobs
    "cronjobs.yaml": "CronJob running a scheduled task at specified intervals.",
    
    # 15 - statefulset
    "headless-svc.yaml": "Headless Service providing stable network IDs for StatefulSet.",
    "statefulset.yaml": "StatefulSet managing stateful application with PVC templates.",
    
    # 16 - storageclass
    "aws-ebs-sc.yaml": "StorageClass for AWS EBS volumes.",
    "azure-sc.yaml": "StorageClass for Azure Managed Disks.",
    "gcp-sc.yaml": "StorageClass for GCP Persistent Disks.",
    
    # 17 - pvc
    "pvc.yaml": "Persistent Volume Claim requesting storage."
}

def process_file(filepath):
    filename = os.path.basename(filepath)
    
    if filename not in mapping:
        print(f"Skipping {filename} (no mapping found)")
        return

    new_desc = mapping[filename]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    modified = False
    
    for line in lines:
        if line.startswith("action_type_description:"):
            # Replace the entire line
            new_lines.append(f"action_type_description: {new_desc}\n")
            modified = True
            print(f"Updated {filename}: description -> {new_desc}")
        else:
            new_lines.append(line)
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".yaml"):
            process_file(os.path.join(root, file))
