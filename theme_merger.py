#!/bin/python
import json5 # Allows trailing commas
import os

def load_theme(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        theme = json5.load(f)

    if "include" in theme:
        include_path = os.path.join(os.path.dirname(file_path), theme["include"])
        included_theme = load_theme(include_path)
        theme.pop("include")
        theme = merge_themes(included_theme, theme)

    return theme

def merge_themes(base: dict, override: dict) -> dict:
    for key, value in override.items():
        if isinstance(value, dict) and key in base:
            base[key] = merge_themes(base[key], value)
        else:
            base[key] = value
    return base

def main(main_theme_path: str):
    combined_theme = load_theme(main_theme_path)

    # Remove file extension from main_theme_path
    # and append _merged.json to the end
    new_filename = os.path.splitext(main_theme_path)[0] + "_merged.json"

    with open(new_filename, 'w', encoding='utf-8') as f:
        json5.dump(combined_theme, f, indent=4, trailing_commas=False, quote_keys=True)

if __name__ == "__main__":
    main("light_modern.json")
