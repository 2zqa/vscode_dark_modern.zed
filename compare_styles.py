#!/bin/python
import json

# Load JSON content from file
with open('themes/vscode-modern-themes.json') as f:
    data = json.load(f)

def compare_styles(style1, style2, path=""):
    null_paths = []
    for key in style1:
        new_path = f"{path}/{key}" if path else key
        if key in style2:
            if isinstance(style1[key], dict) and isinstance(style2[key], dict):
                null_paths.extend(compare_styles(style1[key], style2[key], new_path))
            elif style2[key] is None and style1[key] is not None:
                null_paths.append(new_path)
    return null_paths

# Extract styles
style1 = data["themes"][0]["style"]
style2 = data["themes"][1]["style"]

# Compare styles and find null paths
null_paths = compare_styles(style1, style2)

# Print the result
first_style_name = data["themes"][0]["name"]
second_style_name = data["themes"][1]["name"]
print(f'Entries in "{first_style_name}" that are missing in "{second_style_name}":')
for path in null_paths:
    print(path)

# Compare styles and find null paths
print("\n")
print(f'Entries in "{second_style_name}" that are missing in "{first_style_name}":')
null_paths = compare_styles(style2, style1)
for path in null_paths:
    print(path)
