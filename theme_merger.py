#!/bin/python
import json5  # Allows trailing commas
import os
from typing import Union, List, Dict, Any

def load_theme(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r', encoding='utf-8') as f:
        theme = json5.load(f)

    if "include" in theme:
        include_path = os.path.join(os.path.dirname(file_path), theme["include"])
        included_theme = load_theme(include_path)
        theme.pop("include")
        theme = merge_themes(included_theme, theme)

    return theme

def merge_themes(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, dict) and key in base:
            base[key] = merge_themes(base[key], value)
        elif key == "tokenColors" and isinstance(value, list):
            base[key] = merge_token_colors(base.get(key, []), value)
        else:
            base[key] = value
    return base

def merge_token_colors(base: List[Dict[str, Any]], override: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    base_scopes: Dict[Union[str, tuple], Dict[str, Any]] = {}

    # Normalize scopes to tuples for base
    for entry in base:
        scopes = entry.get('scope')
        if scopes is not None:
            if isinstance(scopes, list):
                scopes = tuple(scopes)
            base_scopes[scopes] = entry

    # Update base_scopes with override entries
    for entry in override:
        scopes = entry.get('scope')
        if scopes is not None:
            if isinstance(scopes, list):
                scopes = tuple(scopes)
            if scopes in base_scopes:
                base_scopes[scopes].update(entry)
            else:
                base_scopes[scopes] = entry

    # Convert the base_scopes back to a list
    merged_token_colors = list(base_scopes.values())
    return merged_token_colors

def main(main_theme_path: str):
    combined_theme = load_theme(main_theme_path)

    # Remove file extension from main_theme_path
    # and append _merged.json to the end
    new_filename = os.path.splitext(main_theme_path)[0] + "_merged.json"

    with open(new_filename, 'w', encoding='utf-8') as f:
        json5.dump(combined_theme, f, indent=4, trailing_commas=False, quote_keys=True)

if __name__ == "__main__":
    main("light_modern.json")
