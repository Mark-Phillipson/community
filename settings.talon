settings():
    # how long a pause talon waits before deciding you've finished speaking Default: 0.150 (150 milliseconds)
    speech.timeout = 0.4
    # Adjust the scale of the imgui to my liking
    imgui.scale = 1.3
    #Stop blinding me
    imgui.dark_mode = true
    # Enable if you'd like the picker gui to automatically appear when explorer has focus
    user.file_manager_auto_show_pickers = 0
    #Stop blinding me
    imgui.dark_mode = true
    # Enable if you'd like the picker gui to automatically appear when explorer has focus
    user.file_manager_auto_show_pickers = 0

    # Set the number of command lines to display per help page
    user.help_max_command_lines_per_page = 40

#     # If `true`, automatically show the picker GUI when the file manager has focus
#     user.file_manager_auto_show_pickers = false

    # Uncomment to always sort help contexts alphabetically.
    # user.help_sort_contexts_by_specificity = false

    # Set the scroll amount for continuous scroll/gaze scroll
    user.mouse_continuous_scroll_amount = 60

#     # Set the number of contexts to display per help page
#     user.help_max_contexts_per_page = 20

    # Choose how pop click should work in 'control mouse' mode
    # 0 = off
    # 1 = on with eyetracker but not zoom mouse mode
    # 2 = on but not with zoom mouse mode
    user.mouse_enable_pop_click = 1

    # Set the scroll amount for continuous scroll/gaze scroll
    user.mouse_continuous_scroll_amount = 8

#     # If `true`, stop continuous scroll/gaze scroll with a pop
#     user.mouse_enable_pop_stops_scroll = true

#     # If `true`, stop mouse drag with a pop
#     user.mouse_enable_pop_stops_drag = true

#     # Choose how pop click should work in 'control mouse' mode
#     # 0 = off
#     # 1 = on with eyetracker but not zoom mouse mode
#     # 2 = on but not with zoom mouse mode
#     user.mouse_enable_pop_click = 1

    # Set the amount to scroll left/right
    user.mouse_wheel_horizontal_amount = 60

#     # If `true`, hide the continuous scroll/gaze scroll GUI
#     user.mouse_hide_mouse_gui = false

#     # If `true`, hide the cursor when enabling zoom mouse
#     user.mouse_wake_hides_cursor = false

#     # Set the amount to scroll up/down
#     user.mouse_wheel_down_amount = 120

#     # Set the amount to scroll left/right
#     user.mouse_wheel_horizontal_amount = 40

    # Uncomment to insert text longer than 10 characters (customizable) by pasting from
    # the clipboard. This is often faster than typing.
    user.paste_to_insert_threshold = 10

#     # Set the default number of command history lines to display
#     user.command_history_display = 10

#     # Set the total number of command history lines to display
#     user.command_history_size = 50

    # Puts Talon into sleep mode if no commands are spoken for a defined period of time.
    user.listening_timeout_minutes = 3

# Uncomment to enable the curse yes/curse no commands (show/hide mouse cursor).
# See issue #688 for more detail: https://github.com/talonhub/community/issues/688
# tag(): user.mouse_cursor_commands_enable

# Uncomment the below to disable support for saying numbers without a prefix.
# By default saying "one" would write "1", however many users find this behavior
# prone to false positives. If you uncomment this, you will need to say
# "numb one" to write "1". Note that this tag will eventually be activated by default
# tag(): user.prefixed_numbers
