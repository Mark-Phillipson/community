os: mac
-
settings():
     user.system_portal_name = "chrome"
     user.system_messaging_application_name = "messages"
     user.system_settings_application_name = "settings"

spy [<user.text>]: 
     txt = text or ""
     user.system_search()
     sleep(100ms)
     insert("{txt}")

spy app [<user.text>]:     
     txt = text or ""
     user.system_search()
     sleep(100ms)
     insert("kind: app {txt}")

spy file [<user.text>]:  
     txt = text or ""   
     user.system_search()
     sleep(100ms)
     insert("kind: doc {txt}")

     
# spy service [<user.text>]:  
#      txt = text or ""   
#      user.system_search()
#      insert("!{txt}")

# spy process [<user.text>]:  
#      txt = text or ""   
#      user.system_search()
#      insert("<{txt}")

spy setting [<user.text>]:  
     txt = text or ""   
     user.system_search()
     sleep(100ms)
     insert("kind: pref {txt}")

# spy code [<user.text>]:
#      txt = text or ""   
#      user.system_search()
#      insert("{{{txt}")
 