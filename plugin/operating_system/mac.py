from talon import Context, actions, app, ui
from talon.mac import applescript
import os
import subprocess

ctx = Context()
ctx.matches = r"""
os: mac
"""

ctx.lists["self.system_setting"] = {}


def update_preferences_list():
    preferences = {}
    if app.platform == "mac":
        preferences_path = "/System/Library/PreferencePanes"
        if os.path.isdir(preferences_path):
            for name in os.listdir(preferences_path):
                path = os.path.join(preferences_path, name)

                preferences[
                    os.path.splitext(name)[0]
                ] = f"open -b com.apple.systempreferences {path}"

    ctx.lists["self.system_setting"] = actions.user.create_spoken_forms_from_map(
        preferences, generate_subsequences=True
    )


@ctx.action_class("user")
class UserActionsMac:
    def system_setting(system_setting: str):
        actions.user.exec(system_setting)
        
    def system_shutdown():
        applescript.run(
            r"""
        tell application "Finder"
            shut down
        end tell"""
        )

    def system_restart():
        applescript.run(
            r"""
        tell application "Finder"
            restart
        end tell"""
        )

    def system_hibernate():
        applescript.run(
            r"""
        tell application "Finder"
            sleep
        end tell"""
        )

    def system_lock():
        actions.key("ctrl-cmd-q")

    def system_show_desktop():
        actions.key("shift-f13")

    def system_task_manager():
        ui.launch(path="/System/Applications/Utilities/Activity Monitor.app")

    def system_task_view():
        actions.key("shift-f11")

    def system_switcher():
        actions.key("shift-f11")

    def system_search():
        actions.key("cmd-space")

    def system_open_directory(path):
        path = os.path.expanduser(path)
        if os.path.exists(path):
            subprocess.call(["open", path])
        else:
            actions.app.notify(f"requested path {path} does not exist")

    def system_show_clipboard():
        actions.key("cmd-shift-c")

    def system_kill_focused_application():
        """Kills the focused application"""
        for application in ui.apps(background=False):
            if application.name == actions.app.name():
                application.appscript().quit(waitreply=False)

    def system_show_settings():
        actions.user.launch_or_focus_bundle("com.apple.systempreferences")

    def system_show_taskmanager():
        actions.user.launch_or_focus_bundle("com.apple.ActivityMonitor")


def on_ready():
    update_preferences_list()


if app.platform == "mac":
    app.register("ready", on_ready)

ctx.lists["self.system_directories"] = {
    "applications": "/Applications",
    "bootcamp": "/Volumes/BOOTCAMP",
    "desk": os.path.expanduser("~/Desktop"),
    "docks": os.path.expanduser("~/Documents"),
    "downloads": os.path.expanduser("~/Downloads"),
    "pictures": os.path.expanduser("~/Pictures"),
    "user": os.path.expanduser("~"),
    "profile": os.path.expanduser("~"),
    "talent home": os.path.expanduser("~/.talon"),
    "talent user": os.path.expanduser("~/.talon/user"),
    "talent recordings": os.path.expanduser("~/.talon/recordings"),
    "talent plugins": "/Applications/Talon.app/Contents/Resources/talon_plugins",
    "root": "/",
}
