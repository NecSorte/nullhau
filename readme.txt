known issues:
    multiple votes from one user
    
    users can vote without /badge me
 
    2024-07-15 14:29:59 ERROR    discord.client Ignoring exception in on_command_error
    Traceback (most recent call last):
    File "C:\Users\kevin\projects\nullhau\.venv\Lib\site-packages\discord\client.py", line 409, in _run_event
         await coro(*args, **kwargs)
    File "c:\Users\kevin\projects\nullhau\main.py", line 182, in on_command_error
         if isinstance(error, commands.CommandNotFound):
                          ^^^^^^^^^^^^^^^^^^^^^^^^
    AttributeError: 'Command' object has no attribute 'CommandNotFound'

    change fun_facts > role facts

    fix test mode. Allow all the functions to still work, but just shorter. make null make annoucments on the timeline of events. 
    
    add spam protection. provide spam warning 1 message every 5 seconds. if user breaks the 1 in 5 second rule, kick from discord. as long as its not sudo. And only in its in the DMs. Maybe reserach discord side security. 

    /say is broken. line 91 error. 


