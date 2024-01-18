from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.microsoft_edge = r"""
os: windows
and app.exe: msedge.exe
"""

ctx.matches = r"""
os: windows
app: microsoft_edge
"""

# @mod.action_class
# class Actions:
