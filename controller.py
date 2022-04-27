import pymysql
import models.person as mp
import os
from progress.bar import ChargingBar

class Database():

  def __init__(self):
    try:
      cnx = pymysql.connect(host='localhost', user='root', password='password',
      db='ncr', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
      print("\n==========\nSuccessfully connected to the database.\n==========\n")
    except pymysql.Error as e:
      print("Connection failed, Error: %d: %s" % (e.args[0], e.args[1]))
      exit()
    
    self.cursor = cnx.cursor()
  
  def get_cursor(self):
    return self.cursor
  
  def close(self):
    self.cursor.close()


class Session():

  def __init__(self):
    database = Database()
    self.cursor = database.get_cursor()
  
  def login(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nLogin\n--------------------\n\n")
    username = input("Username: ")
    if username.lower() == "back":
      os.system('cls' if os.name == 'nt' else 'clear')
      return
    password = input("Password: ")
    if password.lower() == "back":
      os.system('cls' if os.name == 'nt' else 'clear')
      return 
    user = mp.Student(self.cursor, username, password)
    exists = user.login()
    os.system('cls' if os.name == 'nt' else 'clear')
    if not exists:
      print("ERROR: Login failed\n\n")
      input("Press 'Enter' to continue")
      os.system('cls' if os.name == 'nt' else 'clear')
      return
    return user

  def create_account(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nAccount Creation\n--------------------\n\n")
    first = input("First Name: ")
    if (len(first) < 1):
      print("ERROR: Input may not be empty.")
      return
    last = input("Last Name: ")
    if (len(last) < 1):
      print("ERROR: Input may not be empty.")
      return
    email = input("Email: ")
    email = email.lower()
    if (len(email) < 1):
      print("ERROR: Input may not be empty.")
      return
    if "@northeastern.edu" not in email:
      print("ERROR: Email must contain '@northeastern.edu'")
      return
    password = input("Password: ")
    if (len(password) < 1):
      print("ERROR: Input may not be empty.")
      return
    user = mp.Student(self.cursor, email, password)
    success = user.create_user(first, last)
    if not success:
      print("ERROR: Account creation failed")
      return
    return user

  def home_help(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    help = """
          'help' - Displays all commands for the relevant screen\n\n
          'login' - Brings user to the login screen\n\n
          'create account' - Brings user to the account creation screen\n\n\n
          """
    print(help)
    input("Press 'Enter' to continue")
    os.system('cls' if os.name == 'nt' else 'clear')

  def exit(self):
    self.cursor.close()
    print("Connection to the database has closed")
    exit()
  
  def display_home(self):
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
    print(logo)

    user = None

    while not user:
      print("\n\nWelcome to NEU Course Reviews! Based on Northeastern's TRACE Evaluations, NEU Course Reviews is \na course evalution system " +
      "made with students in mind. If you are new here, you can create an \naccount using the 'create account' command. Otherwise, " +
      "use the 'login' command to redirect to the \nlogin screen.\n")
      print("(You can always use the 'help' command if you are unsure of how to proceed)\n")
      command = input(">> ").lower()
      if command == "login":
        user = self.login()
      elif command == "create account":
        user = self.create_account()
      elif command == "help":
        self.home_help()
      elif command == "exit" or command == "quit" or command == "q":
        self.exit()
      else:
        print("ERROR: Invalid command entered\n\n")
        input("Press 'Enter' to continue")
        os.system('cls' if os.name == 'nt' else 'clear')
    
    return user
        
  def display_main(self, user):
    os.system('cls' if os.name == 'nt' else 'clear')
    while(1):
      print("Home\n\n")
      print("""
      You can search for courses by professor, subject name, course name, or course code.\n
      How would you like to search?\n\n
      """)
      command = input(">> ")
      



