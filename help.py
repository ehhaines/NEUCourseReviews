
def help():
  print("++++++++++ HELP ++++++++++\n\n")

def login_help():
  help = "Welcome to NEU Course Reviews. At this screen, you have three possible commands: "
  cmd1 = """login - If you have already registered an account with NEU Course reviews, use this command to  
  be directed to the login screen."""
  cmd2 = """create account - If this is your first time visiting NEU Course Reviews, you need to create
  an account. Enter this command to do so."""
  cmd3 = """help - If you are on this page, then you are familiar with this command!"""

  print(help + "\n")
  print(cmd1 + "\n")
  print(cmd2 + "\n")
  print(cmd3+ "\n")

def home_help():
  print("In the home screen, you are prompted how you would like to search for a class.")
  print("You can search for a class by searching for a professor's name, searching for the class's name, "
  + "searching for the class's code (ex. CS5200), or by searching for the subject.\n")

  print("'professor' - prompts the program to search by professor. You will enter a professor's name, or part of their name \n"
  + "and will be presented with a list of professors whose names contain your input\n")

  print("'subject' - searches for all subjects that match the input\n")

  print("'class name' - searches for all classes whose names match or partially match the input\n")

  print("'class code' - Searches and displays all classes whose class codes match or partially match the input\n")

  print("'add' - prompts you to add either a professor, course, or course section to the database\n")

  print("'exit' - terminates the program\n")
