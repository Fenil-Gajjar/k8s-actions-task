
import os
import re

target_dir = r"e:\k8s-actions-task\k8s-yamls"

def get_pretty_name(filename):
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Replace separators with spaces
    name = name.replace('-', ' ').replace('_', ' ')
    # Title case
    return name.title()

def process_file(filepath):
    filename = os.path.basename(filepath)
    pretty_name = get_pretty_name(filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    
    # State tracking for namespace block
    # Structure is usually:
    # metadata:
    #   namespace:
    #     ...
    #     required: ...
    
    in_metadata = False
    in_namespace = False
    metadata_indent = 0
    namespace_indent = 0
    
    for line in lines:
        stripped = line.strip()
        current_indent = len(line) - len(line.lstrip())
        
        # 1. Update action_type
        if line.startswith("action_type:"):
            # Preserve existing line up to colon if needed, but usually it's just "action_type: ..."
            # We overwrite the value
            new_lines.append(f"action_type: {pretty_name}\n")
            continue
            
        # 2. Remove generic regex
        # Checks for: regex: .* or regex: ^.*$ or regex: ^.*$ (with possible whitespace)
        if "regex:" in line:
            # key, value split
            parts = stripped.split(":", 1)
            if len(parts) == 2:
                val = parts[1].strip()
                # Remove if value is basically "match all"
                if val in ['.*', '^.*$', '^.*', '.*$']:
                    continue
        
        # 3. Namespace required: true
        # Track context
        if stripped.startswith("metadata:"):
            in_metadata = True
            metadata_indent = current_indent
            in_namespace = False # Reset child scope
        elif in_metadata and stripped.startswith("namespace:"):
            # check indent is deeper than metadata
            if current_indent > metadata_indent:
                in_namespace = True
                namespace_indent = current_indent
        elif in_namespace:
            # Check if we left the namespace block (indentation check)
            if current_indent <= namespace_indent and stripped:
                in_namespace = False
            
            # If still in namespace, look for required
            if in_namespace and stripped.startswith("required:"):
                # Force true
                new_line = line[:line.find("required:")] + "required: true\n"
                new_lines.append(new_line)
                continue
        
        # Append line if not modified/skipped above
        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Processed {filename}")

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".yaml"):
            process_file(os.path.join(root, file))
