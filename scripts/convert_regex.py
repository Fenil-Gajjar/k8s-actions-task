
import os
import re

target_dir = r"e:\k8s-actions-task\k8s-yamls"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    modified = False
    
    for line in lines:
        # Check if line contains regex key with slashes
        # pattern: whitespace + regex: + space + / + content + / + optional whitespace + newline
        match = re.match(r'^(\s*regex:\s*)/(.*)/(\s*)$', line)
        if match:
            # group(1) is "  regex: "
            # group(2) is the pattern inside slashes
            # group(3) is trailing whitespace
            prefix = match.group(1)
            content = match.group(2)
            suffix = match.group(3)
            
            # Reconstruct without slashes
            new_line = f"{prefix}{content}{suffix}\n"
            new_lines.append(new_line)
            modified = True
            print(f"Modifying in {filepath}: {line.strip()} -> {new_line.strip()}")
        else:
            new_lines.append(line)
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".yaml"):
            process_file(os.path.join(root, file))
