import os
import db

logo = '''
   _  ________  __              
  / |/ / __/ / / /              
 /    / _// /_/ /               
/_/|_/___/\____/                
 / ___/__  __ _________ ___     
/ /__/ _ \/ // / __(_-</ -_)    
\___/\___/\_,_/_/_/___/\__/     
  / _ \___ _  __(_)__ _    _____
 / , _/ -_) |/ / / -_) |/|/ (_-<
/_/|_|\__/|___/_/\__/|__,__/___/'''



if __name__ == "__main__":
  
  cnx = db.db_connect()
  cursor = cnx.cursor

  print(logo + "\n\n")
  print("Welcome to NEU Course Reviews! Based on Northeastern's TRACE Evaluations, NEU Course Reviews is \na course evalution system" +
  "made with students in mind. If you are new here, you can create an \naccount using the 'create account' command. Otherwise, " +
  "use the 'login' command to redirect to the \nlogin screen.\n")
  print("(You can always use the 'help' command if you are unsure of how to proceed)\n")

  login = input(">> ")
  login = login.lower()

  if login == "create account":
    pass
  elif login == "login":
    pass
  else:
    print("Error: invalid command. Use 'create account' command to create an account or 'login' to be \n" + 
    "redirected to the login screen\n")
  
