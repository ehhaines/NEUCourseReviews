import os
import db
import user
import help
import filter

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


def auth(cursor):

  print(logo + "\n\n")
  print("Welcome to NEU Course Reviews! Based on Northeastern's TRACE Evaluations, NEU Course Reviews is \na course evalution system " +
  "made with students in mind. If you are new here, you can create an \naccount using the 'create account' command. Otherwise, " +
  "use the 'login' command to redirect to the \nlogin screen.\n")
  print("(You can always use the 'help' command if you are unsure of how to proceed)\n")

  account = None
  login_success = 0
  while (login_success == 0):
    login = input(">> ")
    login = login.lower()
    os.system('cls' if os.name == 'nt' else 'clear')
    if login == "create account":
      attempt = user.create_account(cursor)
      login_success = attempt[0]
      account = attempt[1]
    elif login == "login":
      attempt = user.login(cursor)
      login_success = attempt[0]
      account = attempt[1]
    elif login == "help":
      help.help()
      help.login_help()
    elif login == "exit":
      print("\nGoodbye!\n")
      cursor.close()
      exit()
    else:
      print("Error: invalid command. Use 'create account' command to create an account or 'login' to be \n" + 
      "redirected to the login screen\n")
  
  return account

# search by professor, class name, subject code + coursecode

def home(user, cursor):
  os.system('cls' if os.name == 'nt' else 'clear')
  cursor.callproc("find_user", (user,))
  name = (cursor.fetchall()[0])["firstName"]
  print("Welcome, " + name + "!\n")

def find_course(cursor):
  while(1):
    print("You can search for courses by 'professor', 'subject', 'course code', or 'course name'.")
    print("How would you like to search? (type one of the above commands in the prompt)\n\n")
    method = input(">> ")
    os.system('cls' if os.name == 'nt' else 'clear')
    if method == "help":
      help.home_help()
    elif method == "exit":
      print("\nGoodbye!\n")
      cursor.close()
      exit()
    elif method == "professor" or method == "prof":
      print("Home > By Professor\n\n")
      filter.by_professor(cursor)
    elif method == "subject" or method == "sub":
      print("Home > By Subject\n\n")
      filter.by_subject(cursor)
    elif method == "course code" or method == "cc":
      print("Home > By Code\n\n")
      filter.by_course_code(cursor)
    elif method == "course name" or method == "cn":
      print("Home > By Course\n\n")
      filter.by_course_name(cursor)
      pass
    elif method == "add":
      pass
    else:
      print("Error: Invalid command entered. Please enter 'help' if you need assistance.")


def main():
  cnx = db.db_connect()
  cursor = cnx.cursor()

  #user = auth(cursor)

  home("haines.e@northeastern.edu", cursor)

  find_course(cursor)

  # I close the database when 'exit' is input...this is just for good measure
  cursor.close()



if __name__ == "__main__":
  main()