settings():
    # Define the default date format for all date commands using Python strftime codes.
    # Use an explicit pattern to avoid ambiguous locale output.
    # Examples of common formats:
    #   US:   %m-%d-%Y   -> 09-26-2026
    #   UK:   %d-%m-%Y   -> 26-09-2026
    #   ISO:  %Y-%m-%d   -> 2026-09-26
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    user.date_format = "%Y-%m-%d"

date insert:
    user.deprecate_command("2026-05-10", "date insert", "date today")
    insert(user.time_format("%Y-%m-%d"))

date insert UTC:
    user.deprecate_command("2026-05-10", "date insert UTC", "date today UTC")
    insert(user.time_format_utc("%Y-%m-%d"))

date today UTC: insert(user.time_format_utc("%Y-%m-%d"))

timestamp insert: insert(user.time_format("%Y-%m-%d %H:%M:%S"))
timestamp insert high resolution: insert(user.time_format("%Y-%m-%d %H:%M:%S.%f"))
timestamp insert UTC: insert(user.time_format_utc("%Y-%m-%d %H:%M:%S"))
timestamp insert UTC high resolution:
    insert(user.time_format_utc("%Y-%m-%d %H:%M:%S.%f"))

# Date entry commands using day, month, year lists

# Insert date using preferred mode from settings
^date <number_small> {user.month} <number>$:
    user.insert_date_from_parts(number_small, month, number)

# Insert date as US format mm/dd/yyyy
# (defaults remains dd/mm/yyyy for standard use)
^date <number_small> {user.month} <number> us$:
    user.insert_date_formatted_us(number_small, month, number)

# Insert date as ISO format yyyy-mm-dd
^date <number_small> {user.month} <number> iso$:
    user.insert_date_formatted_iso(number_small, month, number)

# Relative date commands
# Today/now uses the configured default format from settings.
date (today | now): user.insert_date_today()

# Relative day modifiers
date tomorrow: user.insert_date_relative(1, 0, 0)
date yesterday: user.insert_date_relative(-1, 0, 0)
date day after tomorrow: user.insert_date_relative(2, 0, 0)
date three days ago: user.insert_date_relative(-3, 0, 0)

# Relative week commands
date next week: user.insert_date_relative(7, 0, 0)
date last week: user.insert_date_relative(-7, 0, 0)

# Relative month/year
date next month: user.insert_date_relative(0, 1, 0)
date last month: user.insert_date_relative(0, -1, 0)
date next year: user.insert_date_relative(0, 0, 1)
date last year: user.insert_date_relative(0, 0, -1)

# Month boundaries
# Useful for forms, reports, and calendar work.
date first of [the] month: user.insert_date_first_of_month()
date last day of [the] month: user.insert_date_last_day_of_month()

# Next weekday
# (weekday list defined in weekdays.talon-list)
^date next {user.weekday}$: user.insert_date_next_weekday(weekday)
