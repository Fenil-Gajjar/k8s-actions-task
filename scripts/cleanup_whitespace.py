
import os

target_dir = r"e:\k8s-actions-task\k8s-yamls"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    modified = False
    
    for line in lines:
        # Check if current line is 'view_type:'
        # It usually has indentation, e.g. "    view_type: text_field"
        if "view_type:" in line:
            # Check if *last* line added was empty
            # We assume standard python string processing where lines usually end with \n
            while new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
                modified = True
        
        new_lines.append(line)
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Cleaned {os.path.basename(filepath)}")

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".yaml"):
            process_file(os.path.join(root, file))
