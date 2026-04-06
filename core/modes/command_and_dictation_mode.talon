mode: command
mode: dictation
mode: sleep
-

^dictation mode$: user.dictation_mode()
^command mode$: user.command_mode()
^mixed mode$:
    mode.disable("sleep")
    mode.enable("dictation")
    mode.enable("command")
