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
    
    add spam protection. I am concerned with users spamming the bot to ddos the bot. Give me ideas on how to protect it
    /say is broken. line 91 error. 


