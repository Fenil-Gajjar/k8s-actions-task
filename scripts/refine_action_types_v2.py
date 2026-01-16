
import os

target_dir = r"e:\k8s-actions-task\k8s-yamls"

# Mapping filename -> Descriptive Action Type (Letters/Spaces only, Generic terms)
mapping = {
    # 0 - Pods
    "checks_volume_pod_svc.yaml": "Pod With Volume Check",
    "emptydir_hostpath_volume.yaml": "Pod With EmptyDir And HostPath",
    "minimal_pod.yaml": "Minimal Pod Configuration",
    "multi_container_pod.yaml": "Multi Container Pod",
    "one_container_pod.yaml": "Single Container Pod",

    # 1 - deployment
    "checks-strategy.yaml": "Deployment With Strategy Checks",
    "minimal-dep.yaml": "Minimal Deployment",
    "onecontainer-dep.yaml": "Single Container Deployment",
    "primary-deployment.yaml": "Primary Deployment",
    "volume-dep.yaml": "Deployment With Volumes",
    
    # 2 - services
    "mutliport-svc.yaml": "Multi Port Service",
    "services.yaml": "Standard Service",

    # 3 - namespace
    "namespace.yaml": "Namespace Configuration",
    
    # 4 - configmap
    "key-value-cm.yaml": "ConfigMap Key Value Pairs",
    "multi-line-cm.yaml": "ConfigMap Multi Line Data",
    
    # 5 - secrets
    "basic-auth.yaml": "Secret Basic Auth",
    "opaque-sec.yaml": "Secret Opaque Data",
    "sec-ssh.yaml": "Secret SSH Auth",
    "sec-tls.yaml": "Secret TLS Config",
    "svc-token.yaml": "Secret Service Account Token",

    # 6 - serviceaccount
    "svc.yaml": "Standard Service Account",
    "svc-imagepull.yaml": "Service Account With Image Pull Secrets",
    
    # 7 - HPA
    "hpa.yaml": "Horizontal Pod Autoscaler CPU Memory",
    
    # 8 - resource-quota
    "object-count.yaml": "Resource Quota Object Count Limits",
    "resource-cpu-mem.yaml": "Resource Quota Compute Resource Limits",
    "storage-quota.yaml": "Resource Quota Storage Limits",
    
    # 9 - limitrange
    "limitrange-defaults.yaml": "LimitRange Container Defaults",
    "pod-limit.yaml": "LimitRange Pod Resource Limits",
    
    # 10 - network-policy
    "allow-cidr-npc.yaml": "Network Policy Allow External CIDR",
    "allow-cross-npc.yaml": "Network Policy Allow Cross Namespace Traffic",
    "allow-deny.yaml": "Network Policy Multi Tier Allow Deny Rules",
    "network-policy.yaml": "Network Policy Frontend To Backend Ingress",
    
    # 11 - pdb
    "max-pdb.yaml": "Pod Disruption Budget Max Unavailable",
    "min-pdb.yaml": "Pod Disruption Budget Min Available",
    
    # 12 - deamonset
    "deamon-set.yaml": "DaemonSet Running Containers On All Nodes",
    
    # 13 - jobs
    "jobs-env-volume.yaml": "Job With Env Vars And Volumes",
    "parellel-jobs.yaml": "Parallel Job Execution",
    "resource-limits-jobs.yaml": "Job With Resource Limits And Deadline",
    "simple-jobs.yaml": "Simple Container Job",
    
    # 14 - cronjobs
    "cronjobs.yaml": "Scheduled CronJob Daily Backup",
    
    # 15 - statefulset
    "headless-svc.yaml": "Headless Service For StatefulSet",
    "statefulset.yaml": "StatefulSet With PVC Templates",
    
    # 16 - storageclass
    "aws-ebs-sc.yaml": "StorageClass AWS EBS General Purpose",
    "azure-sc.yaml": "StorageClass Azure Managed Disk",
    "gcp-sc.yaml": "StorageClass GCP Persistent Disk SSD",
    
    # 17 - pvc
    "pvc.yaml": "Persistent Volume Claim ReadWriteOnce"
}

def process_file(filepath):
    filename = os.path.basename(filepath)
    
    if filename not in mapping:
        # Try to match by lowercase or normalization if strict match fails? 
        # For now assume exact filename match
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
