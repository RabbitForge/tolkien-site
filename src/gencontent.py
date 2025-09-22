import os
from pathlib import Path
from mark_down import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown_content).to_html()
    print("html preview:", html[:120])  # temporary debug
    title = extract_title(markdown_content)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def extract_title(md):
    lines = md.split("\n")
    print(f"Debug: Found {len(lines)} lines")
    for i, line in enumerate(lines):
        print(f"Line {i}: '{line}'")
        if line.startswith("# "):
            title = line[2:]
            print(f"Found title: '{title}'")
            return title
    raise ValueError("no title found")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    root = Path(dir_path_content)
    dest_root = Path(dest_dir_path)

    def walk(curr: Path):
        for entry in curr.iterdir():
            if entry.is_dir():
                walk(entry)
            elif entry.is_file() and entry.suffix == ".md":
                rel = entry.relative_to(root)          
                dest = dest_root / rel
                dest = dest.with_suffix(".html")       
                dest.parent.mkdir(parents=True, exist_ok=True)
                generate_page(str(entry), template_path, str(dest))
    walk(root)
