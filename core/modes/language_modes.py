from talon import Context, Module, actions, app

# Maps language mode names to the extensions that activate them. Only put things
# here which have a supported language mode; that's why there are so many
# commented out entries. TODO: make this a csv file?
language_extensions = {
    # 'assembly': 'asm s',
    # 'bash': 'bashbook sh',
    "batch": "bat",
    "c": "c h",
    # 'cmake': 'cmake',
    # 'cplusplus': 'cpp hpp',
    "csharp": "cs",
    "aspnetcorerazor": "razor cshtml",
    "css": "css",
    # 'elisp': 'el',
    # 'elm': 'elm',
    "gdb": "gdb",
    "go": "go",
    # 'html': 'html',
    "java": "java",
    "javascript": "js",
    "javascriptreact": "jsx",
    # 'json': 'json',
    "kotlin": "kt",
    "lua": "lua",
    "markdown": "md",
    # 'perl': 'pl',
    "php": "php",
    # 'powershell': 'ps1',
    "python": "py",
    "protobuf": "proto",
    "r": "r",
    # 'racket': 'rkt',
    "ruby": "rb",
    "rust": "rs",
    "scala": "scala",
    "scss": "scss",
    # 'snippets': 'snippets',
    "sql": "sql",
    "stata": "do ado",
    "talon": "talon",
    "talonlist": "talon-list",
    "terraform": "tf",
    "tex": "tex",
    "typescript": "ts",
    "typescriptreact": "tsx",
    # 'vba': 'vba',
    "vimscript": "vim vimrc",
}

# Override speakable forms for language modes. If not present, a language mode's
# name is used directly.
language_name_overrides = {
    "cplusplus": ["see plus plus"],
    "csharp": ["see sharp"],
    "css": ["c s s"],
    "gdb": ["g d b"],
    "go": ["go", "go lang", "go language"],
    "r": ["are language"],
    "tex": ["tech", "lay tech", "latex"],
}
from .code_languages import code_languages, code_special_file_map

mod = Module()
ctx = Context()

ctx_forced = Context()
ctx_forced.matches = r"""
tag: user.code_language_forced
"""


mod.tag("code_language_forced", "This tag is active when a language mode is forced")
mod.list("language_mode", desc="Name of a programming language mode.")

# Maps spoken forms to language ids
ctx.lists["user.language_mode"] = {
    spoken_form: language.id
    for language in code_languages
    for spoken_form in language.spoken_forms
}

# Maps extension to language ids
extension_lang_map = {
    f".{ext}": lang.id for lang in code_languages for ext in lang.extensions
}

language_ids = {lang.id for lang in code_languages}
forced_language = ""


@ctx.action_class("code")
class CodeActions:
    def language():
        file_name = actions.win.filename()
        if file_name in code_special_file_map:
            return code_special_file_map[file_name]

        file_extension = actions.win.file_ext()
        return extension_lang_map.get(file_extension, "")


@ctx_forced.action_class("code")
class ForcedCodeActions:
    def language():
        return forced_language


@mod.action_class
class Actions:
    def code_set_language_mode(language: str):
        """Sets the active language mode, and disables extension matching"""
        global forced_language
        assert language in language_ids
        forced_language = language
        # Update tags to force a context refresh. Otherwise `code.language` will not update.
        # Necessary to first set an empty list otherwise you can't move from one forced language to another.
        ctx.tags = []
        ctx.tags = ["user.code_language_forced"]

    def code_clear_language_mode():
        """Clears the active language mode, and re-enables code.language: extension matching"""
        global forced_language
        forced_language = ""
        ctx.tags = []

    def code_show_forced_language_mode():
        """Show the active language for this context"""
        if forced_language:
            app.notify(f"Forced language: {forced_language}")
        else:
            app.notify("No language forced")
