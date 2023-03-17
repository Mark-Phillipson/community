from talon import ui, Module, Context, registry, actions, imgui, cron, app, scope

mod = Module()
ctx_zoom_mouse_enabled = Context()
ctx_zoom_mouse_enabled.matches = r"""
not user.running: Optikey Mouse
and not tag: talon_plugins.eye_zoom_mouse.zoom_mouse_activated
"""


ctx_zoom_mouse_triggered = Context()
ctx_zoom_mouse_triggered.matches = r"""
tag: talon_plugins.eye_zoom_mouse.zoom_mouse_enabled
and tag: talon_plugins.eye_zoom_mouse.zoom_mouse_activated
#and not tag: talon_plugins.eye_zoom_mouse.zoom_mouse_pedal
"""


def sleep_or_wake():
    if not actions.speech.enabled():
        actions.speech.enable()
        actions.user.microphone_preferred()
        actions.user.mouse_wake()
        # todo: remove when the talon_hud perf is fixed on rust branch
        if "user.talon_hud_available" in scope.get("tag"):
            if "rust" != app.branch:
                actions.user.hud_enable()
        actions.user.connect_ocr_eye_tracker()
        # actions.user.clickless_mouse_enable()
    else:
        actions.user.sleep_all()
        actions.sound.set_microphone("None")
        actions.user.mouse_sleep()
        # todo: remove when the talon_hud perf is fixed on rust branch
        if "user.talon_hud_available" in scope.get("tag"):
            if "rust" != app.branch:
                actions.user.hud_disable()

        actions.user.disconnect_ocr_eye_tracker()
        actions.user.disconnect_ocr_eye_tracker()
        actions.user.hide_gaze_ocr_options()
        # actions.user.clickless_mouse_disable()


def trigger_home_row():
    if app.platform == "mac":
        # actions.key("cmd-shift-space")
        if "user.homerow_search" not in registry.tags:
            actions.user.homerow_search("")
        else:
            actions.key("escape")
    elif app.platform == "windows":
        actions.key("ctrl-m")


@mod.action_class
class Actions:
    def keypad0():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()

    def keypad1():
        """document string goes here"""
        trigger_home_row()

    def keypad2():
        """document string goes here"""
        actions.user.system_switcher()

    def keypad3():
        """document string goes here"""
        actions.edit.undo()

    def keypad4():
        """document string goes here"""
        actions.core.repeat_command(1)

    def keypad5():
        """document"""
        actions.user.move_cursor_to_gaze_point()

    def keypad6():
        """document string goes here"""
        actions.tracking.control_zoom_toggle()

    def keypad7():
        """document string goes here"""
        actions.user.dictation_or_command_toggle()

    def keypad8():
        """document string goes here"""
        actions.user.microphone_toggle()

    def keypad9():
        """document string goes here"""
        sleep_or_wake()


@ctx_zoom_mouse_enabled.action_class("user")
class WindowsZoomMouseInactiveActions:
    def keypad0():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()

    def keypad1():
        """document string goes here"""
        trigger_home_row()

    def keypad2():
        """document string goes here"""
        actions.user.system_switcher()

    def keypad3():
        """document string goes here"""
        actions.edit.undo()

    def keypad4():
        """document string goes here"""
        actions.core.repeat_command(1)

    def keypad5():
        """document"""
        actions.user.move_cursor_to_gaze_point()

    def keypad6():
        """document string goes here"""
        actions.tracking.control_zoom_toggle()

    def keypad7():
        """document string goes here"""
        actions.user.dictation_or_command_toggle()

    def keypad8():
        """document string goes here"""
        actions.user.microphone_toggle()

    def keypad9():
        """document string goes here"""
        sleep_or_wake()


@ctx_zoom_mouse_triggered.action_class("user")
class WindowsZoomMouseTriggerActions:
    def keypad0():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_trigger()

    def keypad1():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.right_click()

    def keypad2():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.double_click()

    def keypad3():
        """document string goes here"""
        print("triple")
        actions.talon_plugins.eye_zoom_mouse.triple_click()

    def keypad4():
        """document string goes here"""
        actions.talon_plugins.eye_zoom_mouse.mouse_drag()

    def keypad5():
        """document"""
        actions.talon_plugins.eye_zoom_mouse.mouse_move()

    def keypad6():
        """document string goes here"""

    def keypad7():
        """document string goes here"""
