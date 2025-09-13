# Copilot Instructions for Talon Community

This repository is the **Talon Community** voice command set - a comprehensive collection of voice commands, grammars, and actions for [Talon Voice](https://talonvoice.com/). It enables hands-free control of computers, applications, and coding tasks through spoken commands.

## Core Commands

### Testing & Quality Assurance
- **Run tests**: `pytest` (requires Python 3.9+)
- **Format code**: `pre-commit run` or `pre-commit run --all-files`
- **CI validation**: Tests run automatically via GitHub Actions on push/PR

### Development Workflow
- **Install dev dependencies**: `pip install -r requirements-dev.txt`
- **Pre-commit hooks**: `pre-commit install` (optional but recommended)
- **Test single file**: `pytest test/test_specific_file.py`

### Building & Deployment
- No traditional build process - this is a Talon user file set
- Deploy by installing in `~/.talon/user/community` (Unix) or `%AppData%\Talon\user\community` (Windows)
- Validation occurs through Talon's real-time script loading

## High-Level Architecture

### Core Structure
- **`apps/`** - Application-specific voice commands (80+ apps: VSCode, Chrome, Emacs, JetBrains, etc.)
- **`core/`** - Universal commands (editing, navigation, window management, help system)
- **`lang/`** - Programming language support (Python, JS/TS, Java, Rust, C#, etc.)
- **`plugin/`** - Extended functionality (mouse control, screenshots, macros, draft editor)
- **`tags/`** - Reusable command sets (file manager, terminal, messaging, splits)

### Key Components
- **Module system**: `talon.Module` classes define actions, lists, captures, and tags
- **Context system**: `talon.Context` classes apply commands conditionally (app/OS/language specific)
- **Action framework**: Hierarchical action system allowing language-specific implementations
- **List system**: Dynamic vocabularies (`.talon-list` files) for extensible command sets
- **Settings system**: Centralized configuration via `settings.talon`

### Data Flow
1. Voice input → Talon speech engine → Grammar matching
2. Grammar → Context matching → Action resolution
3. Action execution → Application interaction (key presses, mouse, API calls)

### External Integrations
- **Cursorless**: Advanced text editing via structural selection
- **Rango**: Browser navigation enhancement
- **gaze-ocr**: Eye tracking + OCR for cursor control
- **AXKit** (macOS): Native accessibility integration

## Repository-Specific Style Rules

### File Organization
- **Naming**: Use snake_case for files, match app/language names exactly
- **Structure**: Each app/language gets dedicated folder with `.py` + `.talon` files
- **Context matching**: Use specific matchers (`app.bundle` on macOS, `app.name` + `app.exe` on Windows)

### Code Style
- **Python**: Follow Black formatting (line length 88, target Python 3.10+)
- **Import style**: Use isort with Black profile
- **Type hints**: Use where beneficial, especially for action parameters
- **Docstrings**: Document action classes and complex functions

### Voice Command Patterns
- **Prefer object-verb**: `"file save"` over `"save file"` (P01 principle)
- **Consistency**: Use established patterns from existing commands
- **Naming**: Clear, pronounceable command names avoiding homophones
- **Modifiers**: Support ordinal repetition (`"go up fifth"` = go up 5 lines)

### Talon-Specific Conventions
- **Tag usage**: Apply appropriate tags (`user.code_*`, `user.tabs`, etc.)
- **Action implementation**: Implement all required actions for activated tags
- **List management**: Use `.talon-list` files for vocabularies, CSV for complex mappings
- **Settings**: Make features configurable via `settings.talon`

### Testing Requirements
- **Unit tests**: Test formatters, utilities, and core logic outside Talon environment
- **Stubbed APIs**: Use `test/stubs/talon/` for mocking Talon APIs
- **Real-world testing**: Manual verification in Talon environment required

## Development Guidelines

### Adding New Applications
1. Create `apps/{app_name}/{app_name}.py` with app matchers
2. Add `apps/{app_name}/{app_name}.talon` with voice commands
3. Implement required actions for any tags you activate
4. Follow platform-specific matcher patterns (P03, P04 principles)

### Adding Programming Languages
1. Add extension mapping in `core/modes/language_modes.py`
2. Create `lang/{language}/{language}.py` and `lang/{language}/{language}.talon`
3. Activate appropriate `user.code_*` tags and implement actions
4. Define language-specific types, keywords, and common functions

### Extending Core Functionality
- **Actions**: Define in appropriate module, implement in contexts
- **Lists**: Use `.talon-list` for simple mappings, CSV for complex data
- **Tags**: Create reusable command sets that can be mixed into apps/languages
- **Settings**: Add configurable options to `settings.talon`

### Migration & Compatibility
- Support incremental updates via migration helpers
- Maintain backward compatibility where possible
- Document breaking changes in `BREAKING_CHANGES.txt`

## Key Files & Patterns

### Essential Files
- **`settings.talon`** - Global configuration and feature toggles
- **`core/help/`** - Self-documenting help system (`help active`, `help search`)
- **`core/formatters/`** - Text formatting system (snake_case, camelCase, etc.)
- **`core/modes/`** - Mode switching and language detection

### Common Patterns
- **Context inheritance**: More specific contexts override general ones
- **Action chaining**: Actions can call other actions for composition
- **Conditional loading**: Use tags to enable/disable command sets
- **Override-friendly**: Design for user customization without conflicts

### Configuration Management
- **User overrides**: Create new `.talon-list` files rather than editing existing ones
- **Platform differences**: Handle OS-specific behaviors gracefully
- **Performance**: Avoid expensive operations in hot paths (speech recognition)

This codebase prioritizes reliability, discoverability, and extensibility to support the diverse needs of voice coding users across platforms and applications.
