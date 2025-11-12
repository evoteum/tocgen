#!/usr/bin/env python3
import re
import sys
import argparse
import yaml
from pathlib import Path

DEFAULT_START = "TOCGEN_TABLE_OF_CONTENTS_START"
DEFAULT_END = "TOCGEN_TABLE_OF_CONTENTS_END"
DEFAULT_INDENT = 4
DEFAULT_MIN_LEVEL = 2
DEFAULT_MAX_LEVEL = 6
DEFAULT_LIST_STYLE = "unordered"
DEFAULT_CONFIG_PATHS = [".tocgen.yml", ".github/tocgen.yml"]

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)")
MARKDOWN_COMMENT_PATTERN = re.compile(r"^\[//\]:\s*#\s*\(.*\)")
HTML_COMMENT_PATTERN = re.compile(r"^\s*<!--.*-->\s*$")


def heading_level(value):
    ivalue = int(value)
    if not 1 <= ivalue <= 6:
        raise argparse.ArgumentTypeError(
            f"Heading level must be in range [1, 6] (got {ivalue})"
        )
    return ivalue


def normalise_heading(text: str) -> str:
    return re.sub(r"\W", "", text.strip().lower())


def normalise_list_style(value: str) -> str:
    mapping = {
        "ordered": "ordered",
        "number": "ordered",
        "numbers": "ordered",
        "unordered": "unordered",
        "bullet": "unordered",
        "bullets": "unordered",
        "o": "ordered",
        "n": "ordered",
        "u": "unordered",
        "b": "unordered",
    }
    key = value.lower().strip()
    if key not in mapping:
        raise argparse.ArgumentTypeError(
            f"Invalid list style '{value}'. Must be one of: ordered, unordered, number, bullet"
        )
    return mapping[key]


def load_config_file(path=None):
    cfg = {}
    target = None
    if path:
        target = Path(path)
    else:
        for p in DEFAULT_CONFIG_PATHS:
            test_path = Path(p)
            if test_path.exists():
                target = test_path
                break
    if target and target.exists():
        with open(target, "r", encoding="utf-8") as f:
            try:
                cfg = yaml.safe_load(f) or {}
                print(f"📖 Loaded configuration from {target}")
            except yaml.YAMLError as e:
                print(f"⚠️  Failed to parse {target}: {e}", file=sys.stderr)
    return cfg


def extract_headings(
    markdown_text, min_level=2, max_level=6, include_toc_heading=False
):
    headings = []
    for line in markdown_text.splitlines():
        if MARKDOWN_COMMENT_PATTERN.match(line) or HTML_COMMENT_PATTERN.match(line):
            continue
        match = HEADING_PATTERN.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            if level < min_level or level > max_level:
                continue
            if (
                not include_toc_heading
                and normalise_heading(title) == "tableofcontents"
            ):
                continue
            headings.append((level, title))
    return headings


def slugify(text):
    slug = text.lower()
    slug = re.sub(r"[^\w\- ]+", "", slug)
    slug = slug.replace(" ", "-")
    return slug


def generate_toc(headings, indent_size, min_level, list_style):
    toc_lines = []
    ordered = list_style == "ordered"
    for level, title in headings:
        indent = " " * indent_size * (level - min_level)
        prefix = "1." if ordered else "-"
        toc_lines.append(f"{indent}{prefix} [{title}](#{slugify(title)})")
    return "\n".join(toc_lines)


def remove_code_blocks(text):
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def insert_toc(content, toc, start_marker, end_marker):
    start_pattern = re.escape(start_marker)
    end_pattern = re.escape(end_marker)
    lines = content.splitlines()
    start_idx = end_idx = None
    for i, line in enumerate(lines):
        if re.search(start_pattern, line) and start_idx is None:
            start_idx = i
        elif re.search(end_pattern, line) and end_idx is None:
            end_idx = i
        if start_idx is not None and end_idx is not None:
            break
    if start_idx is None or end_idx is None or end_idx <= start_idx:
        return None
    new_content_lines = (
        lines[: start_idx + 1] + [""] + toc.splitlines() + [""] + lines[end_idx:]
    )
    return "\n".join(new_content_lines) + ("\n" if content.endswith("\n") else "")


def process_file(
    path, start_marker, end_marker, indent_size, min_level, max_level, list_style
):
    text = Path(path).read_text(encoding="utf-8")
    headings = extract_headings(text, min_level, max_level)
    if not headings:
        return None
    toc = generate_toc(headings, indent_size, min_level, list_style)
    new_text = insert_toc(text, toc, start_marker, end_marker)
    if new_text:
        Path(path).write_text(new_text, encoding="utf-8")
        return True
    return False


def find_markdown_files_with_markers(start_marker, end_marker):
    start_pattern = re.escape(start_marker)
    end_pattern = re.escape(end_marker)
    result = []
    for md_file in Path("..").rglob("*.md"):
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        masked = remove_code_blocks(text)
        if re.search(start_pattern, masked) and re.search(end_pattern, masked):
            result.append(md_file)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Automatically generate and insert a Table of Contents into Markdown files."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="List of Markdown files to update (default: all Markdown files with markers).",
    )
    parser.add_argument(
        "--config",
        help="Path to YAML config file (default: .tocgen.yml or .github/tocgen.yml if found)",
    )
    parser.add_argument(
        "--start",
        default=DEFAULT_START,
        help="Custom start marker (default: %(default)s)",
    )
    parser.add_argument(
        "--end", default=DEFAULT_END, help="Custom end marker (default: %(default)s)"
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=DEFAULT_INDENT,
        help="Number of spaces for each TOC indent level (default: %(default)s)",
    )
    parser.add_argument(
        "--min-level",
        type=heading_level,
        default=DEFAULT_MIN_LEVEL,
        help="Minimum heading level to include (1–6, default: %(default)s)",
    )
    parser.add_argument(
        "--max-level",
        type=heading_level,
        default=DEFAULT_MAX_LEVEL,
        help="Maximum heading level to include (1–6, default: %(default)s)",
    )
    parser.add_argument(
        "--list-style",
        type=normalise_list_style,
        default=DEFAULT_LIST_STYLE,
        help="List style: ordered|unordered|number|bullet (default: %(default)s)",
    )
    args = parser.parse_args()

    config = load_config_file(args.config)
    start = config.get("start", args.start)
    end = config.get("end", args.end)
    indent = config.get("indent", args.indent)
    min_level = config.get("min_level", args.min_level)
    max_level = config.get("max_level", args.max_level)
    list_style_raw = config.get("list_style", args.list_style)
    list_style = normalise_list_style(list_style_raw)

    if min_level > max_level:
        parser.error("--min-level cannot be greater than --max-level")

    if args.files:
        files = [Path(f) for f in args.files]
    elif "files" in config:
        files = [Path(f) for f in config["files"]]
    else:
        print(
            "ℹ️  No file list provided; scanning all Markdown files containing TOC markers."
        )
        files = find_markdown_files_with_markers(start, end)

    if not files:
        print("No matching Markdown files found with TOC markers.")
        sys.exit(0)

    updated_count = 0
    for file in files:
        updated = process_file(
            file, start, end, indent, min_level, max_level, list_style
        )
        if updated:
            updated_count += 1
            print(f"✅ Updated TOC in: {file}")
        else:
            print(f"⚠️ Skipped {file} (no valid markers or no headings).")

    print(f"\nSummary: {updated_count}/{len(files)} files updated successfully.")


if __name__ == "__main__":
    main()
