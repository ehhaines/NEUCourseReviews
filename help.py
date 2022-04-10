
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
