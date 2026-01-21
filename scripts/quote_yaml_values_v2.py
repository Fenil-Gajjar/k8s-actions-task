
import os
import re

TARGET_KEYS = {
    'action_type',
    'action_type_description',
    'action_type_descriptions',
    'label',
    'description',
    'view_type',
    'dropdown_values'
}

IGNORED_KEYS = {
    'required',
    'editable',
    'regex',
    'type',
    'apiVersion', 
    'kind', 
    'metadata',
    'name',      # name in metadata is often a string, but user didn't explicitly ask for it.
                 # User said: "for each fields, if its values is sstring then double quote it."
                 # Then gave examples. "e.g: action_type... then for label... description... view_type... dropdown_values"
                 # Did they mean ONLY these?
                 # "so maybe you understood. so go through all yamls and follow the same thing."
                 # The phrase "for each fields, if its values is sstring then double quote it" sounds global.
                 # BUT "e.g: ..." list specific ones.
                 # AND "for fields like , required and editable ... dont dobule quote"
                 # "for regex ... dont do anythign"
                 # "for type field too ... dont do anythign"
                 #
                 # If I quote `apiVersion: "v1"`, is that bad? Usually fine.
                 # But if I quote `name: "mypod"`, usually fine.
                 #
                 # However, the user specifically listed a set of fields to quote and a set to ignore.
                 # The prompt is slightly ambiguous: "for each fields... e.g. X, Y, Z... follow the same thing"
                 # If I act on ALL fields except ignored ones, I might touch 'provisioner', 'reclaimPolicy', 'volumeBindingMode', 'allowVolumeExpansion', 'parameters', 'skuName', 'fsType'.
                 # 
                 # In `azure-sc.yaml`:
                 # `provisioner: kubernetes.io/azure-disk` -> String. Should I quote it?
                 # `reclaimPolicy: Delete` -> String.
                 # 
                 # Given the user's phrasing "fields in each yamls... for each fields... e.g: ...", and later "follow the same thing", strictly implies the rule applies to ALL string fields unless excepted.
                 # 
                 # However, the "e.g." list covers a subset.
                 # Let's look at the structure again.
                 # The user listed `action_type`, `action_type_descriptions`, `label`, `description`, `view_type`, `dropdown_values`.
                 # These look like "schema definition" fields (custom fields for some UI).
                 # `provisioner` is a standard K8s field.
                 # `reclaimPolicy` is standard.
                 # `apiVersion` is standard.
                 #
                 # Hypothesis: The user only wants to modify the "custom UI definition" fields.
                 # The fields `label`, `description`, `view_type`, `dropdown_values`, `editable`, `required`, `regex`, `type` seem to form a schema for a UI generator.
                 # 
                 # If I quote standard fields like `apiVersion: "storage.k8s.io/v1"`, k8s is fine with it.
                 # But usually users asking for this specific cleanup are targeting their custom metadata config.
                 #
                 # Let's be careful. The user said "action_type, action_type_descriptions values is string so . double quote its values. then for lable value is string so double quote it. same for description, view_type ... for dropdown_values ... " 
                 # This sounds like an enumeration of the fields they care about.
                 # Use the enumerated list + `action_type`.
                 #
                 # If I miss some, the user might complain. If I do too many, they might complain.
                 # I will stick to the EXPLICITLY mentioned positive list + obvious variants.
                 #
                 # Explicit set: 
                 # action_type, action_type_descriptions, label, description, view_type, dropdown_values
                 #
                 # I will NOT quote `provisioner`, `kind`, `apiVersion` unless user asks.
                 # This is the safest path.
}

ALLOWED_KEYS = {
    'action_type',
    'action_type_description',
    'action_type_descriptions',
    'label',
    'description',
    'view_type',
    'dropdown_values'
}

def is_integer(s):
    return re.match(r'^-?\d+$', s) is not None

def is_boolean(s):
    return s.lower() in ('true', 'false')

def process_file(filepath):
    modified = False
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    # Regex to capture key-value pairs
    # Group 1: indent, Group 2: key, Group 3: separator + value
    # We look for "key:" followed by something
    kv_pattern = re.compile(r'^(\s*)([\w\-\d_]+):\s*(.*)$')

    for line in lines:
        # separate comment?
        # A full line comment
        if line.strip().startswith('#'):
            new_lines.append(line)
            continue
        
        match = kv_pattern.match(line)
        if match:
            indent = match.group(1)
            key = match.group(2)
            rest = match.group(3)
            
            # Check if key is in our target list
            if key in ALLOWED_KEYS:
                # We need to separate value from inline comment
                # Be careful with # inside string.
                # If it's already quoted, we parse carefully.
                # If not quoted, # starts comment.
                
                value_part = rest
                comment_part = ""
                
                # Simple heuristic for inline comment if NOT quoted
                # If the value starts with " or ', we assume the whole thing up to matching quote is value.
                # But we want to enforce double quotes.
                
                # Let's detect if it's already quoted
                stripped_rest = rest.strip()
                
                # Check for existing quotes
                if (stripped_rest.startswith('"') and stripped_rest.endswith('"')) or \
                   (stripped_rest.startswith("'") and stripped_rest.endswith("'")):
                       
                    # Already quoted.
                    # If single quotes, convert to double? "values is string so double quote it"
                    if stripped_rest.startswith("'"):
                        content = stripped_rest[1:-1]
                        # escape double quotes inside
                        content = content.replace('"', '\\"')
                        new_val = f'"{content}"'
                        # Preserve any trailing comment if it was outside the quotes?
                        # The regex `rest` captured everything including comments.
                        # e.g. 'foo' # comment
                        # stripped_rest is 'foo' # comment -> Wait, strip() doesn't remove comments.
                        pass
                
                # Reliable parsing of value vs comment:
                # If we assume no # inside the unquoted string value (standard YAML constraint for clean strings usually)
                
                idx_comment = -1
                # Check for comment marker #
                # If quoted, we need to respect quotes.
                
                in_double_quote = False
                in_single_quote = False
                escape = False
                value_end_index = len(rest)
                
                # Scan line to find where value ends and comment begins
                for i, char in enumerate(rest):
                    if escape:
                        escape = False
                        continue
                    if char == '\\':
                        escape = True
                        continue
                    
                    if char == '"' and not in_single_quote:
                        in_double_quote = not in_double_quote
                    elif char == "'" and not in_double_quote:
                        in_single_quote = not in_single_quote
                    elif char == '#' and not in_double_quote and not in_single_quote:
                        # Found comment start?
                        # In YAML, # must be preceded by space if it's not at start, 
                        # OR strictly speaking, standard parsers handle it.
                        # We'll assume yes.
                        value_end_index = i
                        break
                
                raw_value = rest[:value_end_index].strip()
                comment = rest[value_end_index:] # Includes #
                
                # Now process raw_value
                
                if not raw_value:
                    # Empty value? e.g. "key: " (null)
                    new_lines.append(line)
                    continue

                # Check if boolean or integer
                if is_boolean(raw_value) or is_integer(raw_value):
                    new_lines.append(line)
                    continue
                
                # Identify if quoted
                is_double = raw_value.startswith('"') and raw_value.endswith('"')
                is_single = raw_value.startswith("'") and raw_value.endswith("'")
                
                final_value = raw_value
                
                if is_double:
                    # Already perfect?
                    pass 
                elif is_single:
                    # Convert 'val' to "val"
                    inner = raw_value[1:-1]
                    inner = inner.replace('"', '\\"') # escape double quotes
                    final_value = f'"{inner}"'
                    modified = True
                else:
                    # Unquoted. Quote it.
                    # Escape existing double quotes?
                    inner = raw_value.replace('"', '\\"')
                    final_value = f'"{inner}"'
                    modified = True
                
                # Reconstruct line
                # Preserve spaces between key and value?
                # The regex consumed space in group(3)? No, `\s*(.*)`
                # Actually group(3) starts with the value part immediately if `\s*` checked space.
                # My regex: `:\s*(.*)`
                # So `rest` includes leading spaces if I didn't verify `\s+`.
                # Wait, regex: `:\s+(.*)` -> mandatory space?
                # In YAML `key:value` is allowed but `key: value` is standard.
                # Let's be careful with spacing.
                
                # Let's rebuild: indent + key + ": " + final_value + " " + comment
                # But we want to preserve original spacing if possible.
                # If I replaced `raw_value` in `line`?
                
                if final_value != raw_value:
                    # We changed something
                    # If we had comments, we need to put them back
                    if comment:
                         new_line = f"{indent}{key}: {final_value} {comment}"
                         # ensure stripping didn't lose a space before comment?
                         # Usually `comment` has leading space if `rest` had it? 
                         # No, `rest[:val_end]` stripped. `rest[val_end:]` starts with #.
                         # We need a space before # if it wasn't there?
                         if not comment.startswith(' '):
                             # original separation?
                             pass
                         new_line = f"{indent}{key}: {final_value} {comment}\n"
                    else:
                         new_line = f"{indent}{key}: {final_value}\n"
                    
                    new_lines.append(new_line)
                    # print(f"Modifying {filepath}: {key}: {raw_value} -> {final_value}")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if modified:
        print(f"Updating {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def run():
    root_dir = r"e:\k8s-actions-task\k8s-yamls"
    for r, d, f in os.walk(root_dir):
        for file in f:
            if file.endswith(".yaml") or file.endswith(".yml"):
                process_file(os.path.join(r, file))

if __name__ == '__main__':
    run()
