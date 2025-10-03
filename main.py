import argparse
import json
import os
from pathlib import Path

class TreeGenerator:
    """Generates a file structure tree from a given path."""

    def __init__(self, root_path, max_depth=-1, dir_only=False, show_hidden=False, exclude=None):
        self.root_path = Path(root_path)
        self.max_depth = max_depth
        self.dir_only = dir_only
        self.show_hidden = show_hidden
        self.exclude = exclude if exclude else []

    def _build_tree(self, current_path, prefix="", depth=0):
        """Recursively builds the plain text tree."""
        if self.max_depth != -1 and depth > self.max_depth:
            return

        items = sorted(list(current_path.iterdir()))
        pointers = ['├── '] * (len(items) - 1) + ['└── ']

        for pointer, item in zip(pointers, items):
            if not self.show_hidden and item.name.startswith('.'):
                continue
            if item.name in self.exclude:
                continue

            if item.is_dir():
                yield prefix + pointer + item.name
                extension = '│   ' if pointer == '├── ' else '    '
                yield from self._build_tree(item, prefix + extension, depth + 1)
            elif not self.dir_only:
                yield prefix + pointer + item.name

    def _build_tree_md(self, current_path, depth=0):
        """Recursively builds the Markdown tree."""
        if self.max_depth != -1 and depth > self.max_depth:
            return ""

        tree_str = ""
        indent = "    " * depth
        items = sorted(list(current_path.iterdir()))

        for item in items:
            if not self.show_hidden and item.name.startswith('.'):
                continue
            if item.name in self.exclude:
                continue

            if item.is_dir():
                tree_str += f"{indent}*   {item.name}\n"
                tree_str += self._build_tree_md(item, depth + 1)
            elif not self.dir_only:
                tree_str += f"{indent}*   {item.name}\n"
        return tree_str

    def _build_tree_json(self, current_path, depth=0):
        """Recursively builds the JSON tree."""
        if self.max_depth != -1 and depth > self.max_depth:
            return None

        tree = {
            "name": current_path.name,
            "type": "directory",
            "contents": []
        }

        items = sorted(list(current_path.iterdir()))
        for item in items:
            if not self.show_hidden and item.name.startswith('.'):
                continue
            if item.name in self.exclude:
                continue

            if item.is_dir():
                subtree = self._build_tree_json(item, depth + 1)
                if subtree:
                    tree["contents"].append(subtree)
            elif not self.dir_only:
                tree["contents"].append({"name": item.name, "type": "file"})
        return tree

    def generate(self, format='text'):
        """Generates the tree in the specified format."""
        if format == 'text':
            tree_lines = [self.root_path.name]
            tree_lines.extend(self._build_tree(self.root_path))
            return "\n".join(tree_lines)
        elif format == 'markdown':
            return f"*   {self.root_path.name}\n" + self._build_tree_md(self.root_path)
        elif format == 'json':
            return json.dumps(self._build_tree_json(self.root_path), indent=2)
        else:
            raise ValueError("Unsupported format. Choose 'text', 'markdown', or 'json'.")

def main():
    parser = argparse.ArgumentParser(description="Generate a file structure tree.")
    parser.add_argument("path", nargs='?', default=None, help="The root directory to generate the tree from.")
    parser.add_argument("-o", "--output", help="Output file name (saved in 'exports' folder).")
    parser.add_argument("-d", "--depth", type=int, default=-1, help="Maximum recursion depth (-1 for unlimited).")
    parser.add_argument("-f", "--format", choices=['text', 'markdown', 'json'], default='text', help="Output format.")
    parser.add_argument("-D", "--dir-only", action="store_true", help="Only show directories.")
    parser.add_argument("--show-hidden", action="store_true", help="Show hidden files and directories.")
    parser.add_argument("--exclude", nargs='+', help="Files or directories to exclude.")
    args = parser.parse_args()

    if args.path:
        root_dir = args.path
    else:
        root_dir = input("Enter the root directory path: ")

    if not Path(root_dir).is_dir():
        print(f"Error: Directory not found at '{root_dir}'")
        return

    generator = TreeGenerator(
        root_path=root_dir,
        max_depth=args.depth,
        dir_only=args.dir_only,
        show_hidden=args.show_hidden,
        exclude=args.exclude
    )

    try:
        output = generator.generate(args.format)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if args.output:
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        output_file = exports_dir / args.output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Tree structure saved to {output_file}")
    else:
        print(output)

if __name__ == "__main__":
    main()