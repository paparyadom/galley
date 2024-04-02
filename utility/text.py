pre_start = f'Complete registration to start.\nSend message in following format:\n/reg password name'
greeting = f"Welcome!"
incorrect_reg_pattern = f"Wrong data input.\nExample:\n /reg password name"
wrong_password = f"Wrong password!"
already_registered = f'You are already registered'
cmd_date_bad_args = f'Wrong data input or no such date.\nExample: /date yyyy-mm-dd, where\nyyyy - year\nmm - month\ndd - day.\nIf day or month in range of 1 to 9 add 0 before (e.g. 1 -> 01)'
help = (
    f'This bot is used for obtain information about workshifts, although for taking selected shift or leaving this shift. '
    f'By pressing button "Schedule" you will get information about shifts in current week.'
    f'\nYou can move between weeks by pressing "<" button - move to previous week or ">" button - move to next week'
    f'\nFor taking a shift:\n1.Choose shift\n2.Press button "This one"\n3.Choose day\n4.Choose shift\n5.Done\n\n'
    f'Commands:\nThere are a few commands\n/reset - drop your own selection steps (don`t ask what is it) and start choice again\n\n'
    f'/date - is used for getting information about week by entering date in format yyyy-mm-dd'
    f'\n\nIf you find mistakes or want to suggest new features write to group t.me/crybook')
not_found = f'Not found'
other_inputs = ('What?', 'Ok!', 'Got it!', 'I don`t think so', 'Back to work!', 'Did not catch it :(')
reset_message = f'Good idea to start all over ... again'
new_week_added = f'New week has been added'
