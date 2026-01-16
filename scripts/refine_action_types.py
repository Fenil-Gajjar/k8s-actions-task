
import os

target_dir = r"e:\k8s-actions-task\k8s-yamls"

# Mapping filename -> Descriptive Action Type
# We match loosely on filename string
mapping = {
    # 6 - serviceaccount
    "svc.yaml": "Standard Service Account",
    "svc-imagepull.yaml": "Service Account with Image Pull Secrets",
    
    # 7 - HPA
    "hpa.yaml": "Horizontal Pod Autoscaler (CPU/Memory)",
    
    # 8 - resource-quota
    "object-count.yaml": "Resource Quota: Object Count Limits",
    "resource-cpu-mem.yaml": "Resource Quota: Compute Resource Limits",
    "storage-quota.yaml": "Resource Quota: Storage Limits",
    
    # 9 - limitrange
    "limitrange-defaults.yaml": "LimitRange: Container Defaults",
    "pod-limit.yaml": "LimitRange: Pod Resource Limits",
    
    # 10 - network-policy
    "allow-cidr-npc.yaml": "Network Policy: Allow External CIDR",
    "allow-cross-npc.yaml": "Network Policy: Allow Cross-Namespace Traffic",
    "allow-deny.yaml": "Network Policy: Multi-Tier Allow/Deny Rules",
    "network-policy.yaml": "Network Policy: Frontend to Backend Ingress",
    
    # 11 - pdb
    "max-pdb.yaml": "Pod Disruption Budget: Max Unavailable",
    "min-pdb.yaml": "Pod Disruption Budget: Min Available",
    
    # 12 - deamonset
    "deamon-set.yaml": "DaemonSet: Nginx on All Nodes",
    
    # 13 - jobs
    "jobs-env-volume.yaml": "Job with Env Vars and Volumes",
    "parellel-jobs.yaml": "Parallel Job Execution",
    "resource-limits-jobs.yaml": "Job with Resource Limits and Deadline",
    "simple-jobs.yaml": "Simple BusyBox Job",
    
    # 14 - cronjobs
    "cronjobs.yaml": "Scheduled CronJob (Daily Backup)",
    
    # 15 - statefulset
    "headless-svc.yaml": "Headless Service for StatefulSet",
    "statefulset.yaml": "StatefulSet with PVC Templates",
    
    # 16 - storageclass
    "aws-ebs-sc.yaml": "StorageClass: AWS EBS gp3",
    "azure-sc.yaml": "StorageClass: Azure Managed Disk",
    "gcp-sc.yaml": "StorageClass: GCP PD SSD",
    
    # 17 - pvc
    "pvc.yaml": "Persistent Volume Claim (ReadWriteOnce)"
}

def process_file(filepath):
    filename = os.path.basename(filepath)
    
    if filename not in mapping:
        print(f"Skipping {filename} (no mapping found)")
        return

    new_title = mapping[filename]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    modified = False
    
    for line in lines:
        if line.startswith("action_type:"):
            # Replace the entire line
            new_lines.append(f"action_type: {new_title}\n")
            modified = True
            print(f"Updated {filename}: action_type -> {new_title}")
        else:
            new_lines.append(line)
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".yaml"):
            process_file(os.path.join(root, file))
