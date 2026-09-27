mode: command
mode: dictation
mode: sleep
-

^dictation mode$: user.dictation_mode()
^command mode$: user.command_mode()
^mixed mode$: user.mixed_mode()
