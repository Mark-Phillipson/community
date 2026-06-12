from __future__ import annotations

import argparse
import ast
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

CAPTURE_REF_RE = re.compile(r"<([A-Za-z_][A-Za-z0-9_.]*)>")
LIST_REF_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_.]*)\}")
ACTION_CALL_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)\s*\(")

MANUAL_START = "<!-- MANUAL_NOTES_START -->"
MANUAL_END = "<!-- MANUAL_NOTES_END -->"


@dataclass
class Location:
    path: Path
    line: int


@dataclass
class SymbolRecord:
    symbol: str
    kinds: set[str] = field(default_factory=set)
    definitions: list[Location] = field(default_factory=list)
    usages: list[Location] = field(default_factory=list)
    options: list[str] = field(default_factory=list)
    rules: set[str] = field(default_factory=set)
    refs: set[str] = field(default_factory=set)
    dynamic_notes: set[str] = field(default_factory=set)


class CaptureExtractor:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.records: dict[str, SymbolRecord] = {}
        self._list_symbol_by_stem: dict[str, set[str]] = defaultdict(set)

    def canonical_symbol(self, symbol: str) -> str:
        symbol = symbol.strip()
        if not symbol:
            return symbol
        if "." not in symbol:
            return f"user.{symbol}"
        if symbol.startswith("self."):
            return f"user.{symbol.split('.', 1)[1]}"
        return symbol

    def get_record(self, symbol: str) -> SymbolRecord:
        canonical = self.canonical_symbol(symbol)
        record = self.records.get(canonical)
        if record is None:
            record = SymbolRecord(symbol=canonical)
            self.records[canonical] = record
        return record

    def add_definition(self, symbol: str, kind: str, path: Path, line: int) -> SymbolRecord:
        record = self.get_record(symbol)
        record.kinds.add(kind)
        record.definitions.append(Location(path=path, line=line))
        return record

    def add_usage(self, symbol: str, path: Path, line: int) -> None:
        record = self.get_record(symbol)
        record.usages.append(Location(path=path, line=line))

    def add_option(self, symbol: str, option: str) -> None:
        option = option.strip()
        if not option:
            return
        record = self.get_record(symbol)
        if option not in record.options:
            record.options.append(option)

    def add_dynamic_note(self, symbol: str, note: str) -> None:
        record = self.get_record(symbol)
        record.dynamic_notes.add(note)

    def add_rule(self, symbol: str, rule: str) -> None:
        if not rule:
            return
        normalized = " ".join(rule.split())
        record = self.get_record(symbol)
        record.rules.add(normalized)
        for list_ref in LIST_REF_RE.findall(normalized):
            record.refs.add(self.canonical_symbol(list_ref))
        for capture_ref in CAPTURE_REF_RE.findall(normalized):
            record.refs.add(self.canonical_symbol(capture_ref))

    def scan(self) -> None:
        for path in self.root.rglob("*.talon-list"):
            self.scan_talon_list(path)

        for path in self.root.rglob("*.py"):
            self.scan_python(path)

        for path in self.root.rglob("*.talon"):
            self.scan_talon(path)

    def scan_talon_list(self, path: Path) -> None:
        stem = path.stem
        symbol = f"user.{stem}"
        self._list_symbol_by_stem[stem].add(symbol)
        self.add_definition(symbol, "list", path, 1)

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(encoding="latin-1").splitlines()

        for index, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if ":" in stripped:
                spoken, value = stripped.split(":", 1)
                spoken = spoken.strip()
                value = value.strip()
                if spoken and value:
                    self.add_option(symbol, f"{spoken} -> {value}")
                elif spoken:
                    self.add_option(symbol, spoken)
            else:
                self.add_option(symbol, stripped)

    def _extract_call_name(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = self._extract_call_name(node.value)
            if base:
                return f"{base}.{node.attr}"
            return node.attr
        return None

    def _extract_string(self, node: ast.AST | None) -> str | None:
        if node is None:
            return None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        return None

    def _extract_subscript_key(self, node: ast.Subscript) -> str | None:
        slice_node = node.slice
        if isinstance(slice_node, ast.Constant) and isinstance(slice_node.value, str):
            return slice_node.value
        if isinstance(slice_node, ast.Index):
            value = slice_node.value
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                return value.value
        return None

    def _dynamic_options_preview(self, node: ast.AST) -> tuple[list[str], bool]:
        if isinstance(node, ast.Dict):
            values: list[str] = []
            for key in node.keys:
                key_str = self._extract_string(key)
                if key_str:
                    values.append(key_str)
            return values[:40], True
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            values = []
            for elt in node.elts:
                item = self._extract_string(elt)
                if item:
                    values.append(item)
            return values[:40], True
        return [], False

    def scan_python(self, path: Path) -> None:
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            source = path.read_text(encoding="latin-1")

        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                call = node.value
                call_name = self._extract_call_name(call.func)
                if call_name and call_name.endswith(".list") and call.args:
                    list_name = self._extract_string(call.args[0])
                    if list_name:
                        symbol = list_name if "." in list_name else f"user.{list_name}"
                        self.add_definition(symbol, "list", path, node.lineno)
                        self._list_symbol_by_stem[symbol.split(".")[-1]].add(symbol)

            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if not isinstance(target, ast.Subscript):
                        continue
                    if not isinstance(target.value, ast.Attribute):
                        continue
                    attr = target.value
                    if attr.attr != "lists":
                        continue
                    symbol = self._extract_subscript_key(target)
                    if not symbol:
                        continue
                    record = self.add_definition(symbol, "list", path, node.lineno)
                    values, parsed = self._dynamic_options_preview(node.value)
                    for option in values:
                        self.add_option(symbol, option)
                    if not parsed:
                        record.dynamic_notes.add("Values populated dynamically at runtime")

            if isinstance(node, ast.ClassDef):
                is_action_class = False
                for deco in node.decorator_list:
                    if isinstance(deco, ast.Call):
                        name = self._extract_call_name(deco.func)
                        if name and name.endswith(".action_class"):
                            is_action_class = True
                    elif isinstance(deco, ast.Attribute):
                        name = self._extract_call_name(deco)
                        if name and name.endswith(".action_class"):
                            is_action_class = True

                if is_action_class:
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            symbol = f"user.{item.name}"
                            self.add_definition(symbol, "action", path, item.lineno)

            if isinstance(node, ast.FunctionDef):
                for deco in node.decorator_list:
                    if isinstance(deco, ast.Call):
                        call_name = self._extract_call_name(deco.func)
                        if not call_name or not call_name.endswith(".capture"):
                            continue

                        if call_name.startswith("ctx.capture") and deco.args:
                            explicit = self._extract_string(deco.args[0])
                            symbol = explicit if explicit else f"user.{node.name}"
                        else:
                            symbol = f"user.{node.name}"

                        self.add_definition(symbol, "capture", path, node.lineno)
                        rule = None
                        for kw in deco.keywords:
                            if kw.arg == "rule":
                                rule = self._extract_string(kw.value)
                                break
                        if rule:
                            self.add_rule(symbol, rule)

                    elif isinstance(deco, ast.Attribute):
                        call_name = self._extract_call_name(deco)
                        if call_name and call_name.endswith(".capture"):
                            symbol = f"user.{node.name}"
                            self.add_definition(symbol, "capture", path, node.lineno)

    def scan_talon(self, path: Path) -> None:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(encoding="latin-1").splitlines()

        for index, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            command_part = None
            action_part = None

            if ":" in line and not line.startswith((" ", "\t")):
                command_part, action_part = line.split(":", 1)
            elif line.startswith((" ", "\t")):
                action_part = stripped

            if command_part:
                for capture in CAPTURE_REF_RE.findall(command_part):
                    self.add_usage(capture, path, index)

                for list_ref in LIST_REF_RE.findall(command_part):
                    self.add_usage(list_ref, path, index)

            if action_part:
                for action in ACTION_CALL_RE.findall(action_part):
                    self.add_usage(action, path, index)

    def line_link(self, location: Location) -> str:
        uri = location.path.resolve().as_uri()
        return f"{uri}#L{location.line}"

    def display_path(self, location: Location) -> str:
        return location.path.resolve().relative_to(self.root).as_posix()

    def _sort_locations(self, locations: Iterable[Location]) -> list[Location]:
        unique = {(loc.path.resolve(), loc.line): loc for loc in locations}
        return sorted(unique.values(), key=lambda loc: (self.display_path(loc), loc.line))

    def _kind_order(self, symbol: str) -> tuple[int, str]:
        record = self.records[symbol]
        if "capture" in record.kinds:
            return (0, symbol)
        if "list" in record.kinds:
            return (1, symbol)
        if "action" in record.kinds:
            return (2, symbol)
        return (3, symbol)

    def spoken_forms_for_symbol(
        self, symbol: str, _seen: frozenset[str] | None = None
    ) -> list[str]:
        """Return all spoken forms that can trigger a capture or list.

        For lists this is the option keys.  For captures it descends into
        referenced lists (one level, cycle-safe) and concatenates their
        options.  Captures that only reference other captures (no lists)
        return the rule string as a fallback.
        """
        if _seen is None:
            _seen = frozenset()
        if symbol in _seen:
            return []
        _seen = _seen | {symbol}

        record = self.records.get(symbol)
        if record is None:
            return []

        # List — return spoken option keys (strip ' -> value' part)
        if record.options:
            spoken: list[str] = []
            for opt in record.options:
                key = opt.split(" -> ")[0].strip() if " -> " in opt else opt.strip()
                if key and key != "-":
                    spoken.append(key)
            return spoken

        # Capture — expand referenced lists recursively, dedupe while keeping order
        if record.refs:
            seen_words: set[str] = set()
            all_words: list[str] = []
            for ref in sorted(record.refs):
                for word in self.spoken_forms_for_symbol(ref, _seen):
                    if word not in seen_words:
                        seen_words.add(word)
                        all_words.append(word)
            if all_words:
                return all_words

        # Fallback: return the raw rule strings so at least something shows
        return sorted(record.rules) if record.rules else []

    def symbols_used_in_file(self, talon_path: Path) -> list[str]:
        target = talon_path.resolve()
        per_symbol_first_line: dict[str, int] = {}

        for symbol, record in self.records.items():
            for usage in record.usages:
                if usage.path.resolve() != target:
                    continue
                current = per_symbol_first_line.get(symbol)
                if current is None or usage.line < current:
                    per_symbol_first_line[symbol] = usage.line

        return [
            symbol
            for symbol, _ in sorted(
                per_symbol_first_line.items(), key=lambda item: (item[1], item[0])
            )
        ]

    def render(self, manual_notes: str) -> str:
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        text_talon_path = self.root / "core" / "text" / "text.talon"
        text_talon_symbols = self.symbols_used_in_file(text_talon_path)

        lines: list[str] = []
        lines.append("# Talon Capture Cheat Sheet")
        lines.append("")
        lines.append(f"Generated: {generated_at}")
        lines.append("")
        lines.append(
            "This document is generated from .talon, .py, and .talon-list files. "
            "It includes clickable links back to definition and usage lines."
        )
        lines.append("")

        lines.append("## Focus: core/text/text.talon")
        lines.append("")
        lines.append(
            f"Source file: [{text_talon_path.relative_to(self.root).as_posix()}]"
            f"({text_talon_path.resolve().as_uri()})"
        )
        lines.append("")

        if text_talon_symbols:
            lines.append("Symbols used in this file:")
            lines.append("")
            for symbol in text_talon_symbols:
                record = self.records[symbol]
                anchor = symbol.replace(".", "")
                kind_text = ", ".join(sorted(record.kinds)) or "unknown"
                lines.append(f"- [{symbol}](#{anchor}) ({kind_text})")

                definitions = self._sort_locations(record.definitions)
                if definitions:
                    first_definition = definitions[0]
                    lines.append(
                        "  - Definition: "
                        f"[{self.display_path(first_definition)}:{first_definition.line}]"
                        f"({self.line_link(first_definition)})"
                    )

                usages_in_text_talon = [
                    usage
                    for usage in self._sort_locations(record.usages)
                    if usage.path.resolve() == text_talon_path.resolve()
                ]
                if usages_in_text_talon:
                    usage_links = ", ".join(
                        f"[{self.display_path(usage)}:{usage.line}]({self.line_link(usage)})"
                        for usage in usages_in_text_talon[:5]
                    )
                    lines.append(f"  - Used here: {usage_links}")

                if "capture" in record.kinds and record.rules:
                    for rule in sorted(record.rules):
                        lines.append(f"  - Rule: `{rule}`")
                    spoken = self.spoken_forms_for_symbol(symbol)
                    if spoken:
                        spoken_preview = spoken[:15]
                        suffix = " ..." if len(spoken) > 15 else ""
                        lines.append(
                            "  - Matches: " + " | ".join(spoken_preview) + suffix
                        )
                    elif record.dynamic_notes:
                        lines.append("  - Matches: (populated at runtime)")
                elif record.options:
                    lines.append(
                        "  - Options: "
                        + ", ".join(record.options[:5])
                        + (" ..." if len(record.options) > 5 else "")
                    )

                if record.dynamic_notes:
                    lines.append(
                        "  - Dynamic: " + "; ".join(sorted(record.dynamic_notes))
                    )
            lines.append("")
        else:
            lines.append("No symbols were detected for core/text/text.talon.")
            lines.append("")

        symbols = sorted(self.records.keys(), key=self._kind_order)

        lines.append("## Symbol Index")
        lines.append("")
        for symbol in symbols:
            anchor = symbol.replace(".", "")
            kind_text = ", ".join(sorted(self.records[symbol].kinds)) or "unknown"
            lines.append(f"- [{symbol}](#{anchor}) ({kind_text})")
        lines.append("")

        lines.append("## Symbols")
        lines.append("")

        for symbol in symbols:
            record = self.records[symbol]
            anchor = symbol.replace(".", "")
            lines.append(f"### {anchor}")
            lines.append("")
            lines.append(f"- Symbol: {symbol}")
            lines.append(f"- Kind: {', '.join(sorted(record.kinds)) or 'unknown'}")

            definitions = self._sort_locations(record.definitions)
            if definitions:
                lines.append("- Definitions:")
                for loc in definitions[:40]:
                    lines.append(
                        f"  - [{self.display_path(loc)}:{loc.line}]({self.line_link(loc)})"
                    )
                if len(definitions) > 40:
                    lines.append(f"  - ... {len(definitions) - 40} more definitions")

            usages = self._sort_locations(record.usages)
            if usages:
                lines.append("- Usages:")
                for loc in usages[:80]:
                    lines.append(
                        f"  - [{self.display_path(loc)}:{loc.line}]({self.line_link(loc)})"
                    )
                if len(usages) > 80:
                    lines.append(f"  - ... {len(usages) - 80} more usages")

            if record.rules:
                lines.append("- Rules:")
                for rule in sorted(record.rules):
                    lines.append(f"  - `{rule}`")

            if "capture" in record.kinds:
                spoken = self.spoken_forms_for_symbol(symbol)
                if spoken:
                    lines.append(f"- Spoken forms ({len(spoken)} total):")
                    for word in spoken[:60]:
                        lines.append(f"  - {word}")
                    if len(spoken) > 60:
                        lines.append(f"  - ... {len(spoken) - 60} more")
                elif record.dynamic_notes:
                    lines.append("- Spoken forms: (populated at runtime — see dynamic notes)")

            if record.refs:
                lines.append("- Referenced symbols:")
                for ref in sorted(record.refs):
                    lines.append(f"  - {ref}")

            if "list" in record.kinds and record.options:
                lines.append(f"- Options ({len(record.options)}):")
                for option in record.options[:40]:
                    lines.append(f"  - {option}")
                if len(record.options) > 40:
                    lines.append(f"  - ... {len(record.options) - 40} more options")

            if record.dynamic_notes:
                lines.append("- Dynamic/runtime notes:")
                for note in sorted(record.dynamic_notes):
                    lines.append(f"  - {note}")

            lines.append("")

        lines.append("## Runtime Caveats")
        lines.append("")
        lines.append("- Lists populated through ctx.lists assignments can change at runtime.")
        lines.append("- Captures that call external state (for example clipboard or contacts) are not exhaustive.")
        lines.append("- This sheet reflects static repository analysis plus simple literal extraction.")
        lines.append("")

        lines.append(MANUAL_START)
        lines.append(manual_notes.strip() if manual_notes.strip() else "Add your own notes here.")
        lines.append(MANUAL_END)
        lines.append("")

        return "\n".join(lines)


def load_manual_notes(output_path: Path) -> str:
    if not output_path.exists():
        return ""

    try:
        content = output_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = output_path.read_text(encoding="latin-1")

    pattern = re.compile(
        re.escape(MANUAL_START) + r"(.*?)" + re.escape(MANUAL_END), re.DOTALL
    )
    match = pattern.search(content)
    if not match:
        return ""
    return match.group(1).strip()


def default_output_path() -> Path:
    return Path.home() / "Documents" / "Talon" / "Talon-Capture-Cheat-Sheet.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Talon capture cheat sheet")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root to scan",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output_path(),
        help="Output markdown file path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output = args.output.expanduser().resolve()

    extractor = CaptureExtractor(root=root)
    extractor.scan()

    manual_notes = load_manual_notes(output)
    content = extractor.render(manual_notes)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")

    print(f"Generated cheat sheet with {len(extractor.records)} symbols")
    print(f"Output: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
