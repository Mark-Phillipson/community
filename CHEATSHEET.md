# Talon Community — Compact Cheatsheet

This single-file cheatsheet extracts the most-used/global Talon commands and common lists from this repository (`community`). It's meant for quick reference in a widescreen editor. It does not list every command in the repo — instead it highlights core/global commands and the most useful app-specific sections (Edit, Text, VSCode, Tabs/Windows, Navigation). For full details see the source `.talon` files under the `core/`, `apps/`, and `plugin/` folders.

## Global / Core commands 🌐
| Spoken form                      |                    Action (call) | Scope              | Notes                                               |
| -------------------------------- | -------------------------------: | ------------------ | --------------------------------------------------- |
| select that                      |          edit.copy() / selection | Global (core/edit) | Copies current selection                            |
| cut that                         |                       edit.cut() | Global (core/edit) | Cuts selection                                      |
| (pace                           |                      paste) that | edit.paste()       | Global (core/edit)                                  | Paste (also `paste enter`) |
| undo that                        |                      edit.undo() | Global (core/edit) | Undo                                                |
| redo that                        |                      edit.redo() | Global (core/edit) | Redo                                                |
| new line below / slap            |          edit.line_insert_down() | Global (core/edit) | Insert new line below                               |
| go <number> (left/right/up/down) |          edit navigation helpers | Global (core/edit) | `go <user.navigation_step>` supports repeated steps |
| zoom in / zoom out               | edit.zoom_in() / edit.zoom_out() | Global (core/edit) | Editor zooming                                      |

## Text & Formatting
| Spoken form                                    |                           Action | Scope                | Notes                                        |
| ---------------------------------------------- | -------------------------------: | -------------------- | -------------------------------------------- |
| phrase <user.text>                             | user.add_phrase_to_history(text) | core/text            | Insert a text phrase and track it in history |
| {user.prose_formatter} <user.prose>            |       user.insert_formatted(...) | core/text/formatters | Insert formatted prose or code snippets      |
| recent list / recent close / recent repeat <n> |           phrase-history helpers | core/text            | Browse & insert recent phrases               |

## Keys & Typing helpers
| Spoken form            |            Action | Scope     | Notes                                               |
| ---------------------- | ----------------: | --------- | --------------------------------------------------- |
| <letter>               |       key(letter) | core/keys | Type letters, supports formats (ship/uppercase)     |
| press <user.modifiers> |    key(modifiers) | core/keys | Press modifier-only combos (e.g., `press ctrl alt`) |
| <user.function_key>    | key(function_key) | core/keys | F1..F12 list is defined in `core/keys` lists        |

## Tabs & Window management

| Spoken form             |                              Action | Scope                      | Notes              |
| ----------------------- | ----------------------------------: | -------------------------- | ------------------ |
| tab open                |                      app.tab_open() | core/windows_and_tabs/tabs | Open a new tab     |
| tab next / tab previous | app.tab_next() / app.tab_previous() | core/windows_and_tabs/tabs | Cycle tabs         |
| tab close               |            user.tab_close_wrapper() | core/windows_and_tabs/tabs | Close active tab   |
| go tab <number>         |               user.tab_jump(number) | core/windows_and_tabs/tabs | Jump to tab number |

## Navigation (file / cursor)

| Spoken form                  |                               Action | Scope     | Notes              |
| ---------------------------- | -----------------------------------: | --------- | ------------------ |
| go word left / go word right | edit.word_left() / edit.word_right() | core/edit | Word navigation    |
| go line start / go line end  |  edit.line_start() / edit.line_end() | core/edit | Jump to line edges |
| go page up / go page down    |    edit.page_up() / edit.page_down() | core/edit | Page navigation    |
| go way up / go way down      |  edit.file_start() / edit.file_end() | core/edit | File start/end     |

## VS Code (app: vscode) — selected highlights

These come from `apps/vscode/vscode.talon`. They assume the `app: vscode` scope and many tags in `vscode.talon` enable additional command groups.

| Spoken form                                     |                                                Action | Notes                                   |
| ----------------------------------------------- | ----------------------------------------------------: | --------------------------------------- |
| window reload                                   |          user.vscode("workbench.action.reloadWindow") | Reload window                           |
| file hunt [<text>]                              | user.vscode("workbench.action.quickOpen") then insert | Quick file open                         |
| suggest show                                    |           user.vscode("editor.action.triggerSuggest") | Trigger completions                     |
| format that                                     |           user.vscode("editor.action.formatDocument") | Format file                             |
| terminal new / terminal split / terminal toggle |                                     terminal controls | Terminal management                     |
| git push / git pull / git fetch                 |                          user.vscode("git.push") etc. | Common git actions via VS Code commands |

## Draft editor (plugin) quick commands
| Spoken form                                       |                         Action | Scope                                          |
| ------------------------------------------------- | -----------------------------: | ---------------------------------------------- |
| draft this                                        |       user.draft_editor_open() | plugin/draft_editor (open draft for selection) |
| draft all / draft line / draft top / draft bottom |       selects then opens draft | plugin/draft_editor                            |
| draft submit                                      | user.draft_editor_paste_last() | paste last draft back                          |

## Lists & Captures (representative)
Below are some of the commonly referenced lists/captures used across many commands. They live in `lang/` and `core/keys` and `tags/` folders. This list is not exhaustive but covers the ones you'll hit most frequently.

- `user.letters` — letters (a..z) (see `core/keys/letter.talon-list`)
- `user.function_key` — F1..F12 (`core/keys/function_key.talon-list`)
- `user.special_key` / `user.modifiers` — platform special/modifier keys (see `core/keys` subfolders)
- `user.code_keyword`, `user.code_common_function`, `user.code_common_method` — language keywords & common identifiers (in `lang/*/*.talon-list`)
- `emoji`, `emoticon`, `kaomoji` lists — in `tags/emoji/*.talon-list`
- `window_split_positions`, `window_snap_positions` — window layout helpers (`core/windows_and_tabs/*.talon-list`)

If you need to inspect a list file directly, open any `*.talon-list` under `lang/`, `core/keys/`, or `tags/`.

## Quick Tips (VS Code shortcuts)
- Toggle Markdown preview: Ctrl+Shift+V (Open Preview) or Ctrl+K V (Open Preview to the Side)
- Toggle Full Screen: F11
- Toggle Zen Mode: Ctrl+K Z (press the two-key chord: Ctrl+K then Z)

## Filtering & REPL examples
If you want to programmatically extract or filter commands from this repo, two small examples are below.

1) Talon Python REPL (quick lookup using the Talon registry inside Talon):

```
# In the Talon Python REPL
from talon import registry
for ctx in registry.contexts():
    if 'app: vscode' in ctx.scopes:
        print('Context:', ctx)
        for cmd in ctx.commands:
            print(cmd.key, '->', cmd.action)

```

2) Plain Python snippet to list `.talon` commands and captures locally (runs outside Talon):

```
import re, pathlib
root = pathlib.Path(__file__).resolve().parent
for p in sorted(root.glob('**/*.talon')):
    text = p.read_text(encoding='utf8')
    for m in re.finditer(r"^([\w\s<>{}_\-\|\[\]\(\)']+):", text, re.M):
        spoken = m.group(1).strip()
        print(f"{p.relative_to(root)}: {spoken}")

```

Notes: the regex above is intentionally permissive and intended only for quick scanning — use a more precise parser for production extraction.

## Where to find the full commands
- Core text/edit/keys: `core/text/text.talon`, `core/edit/edit.talon`, `core/keys/keys.talon`.
- VS Code: `apps/vscode/vscode.talon` (lots of app-scoped commands).
- Lists: `lang/*/*.talon-list`, `core/keys/*.talon-list`, `tags/*/*.talon-list`.

## Completion summary
- What changed: added `CHEATSHEET.md` with a concise markdown cheatsheet for the repository.
- Verified sources: commands and lists were referenced from `core/` and `apps/vscode` files.

If you'd like a more exhaustive, alphabetized cheatsheet (every command grouped by scope) I can generate a full scan and produce a larger `README`-style cheatsheet — tell me how verbose you want it. 
