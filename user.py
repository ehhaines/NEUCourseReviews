'''
None -> (String, String, String, String)

Gets the login information of a user and returns it as a tuple.
'''
def get_credentials():

  first = input("First Name: ")
  last = input("Last Name: ")
  email = input("Email: ")
  pwd = input("Password: ")

  return first, last, email, pwd


'''
DictCursor -> bool

Calls the 'create user' stored procedure in ncr database to insert a user. Needs a cursor object to
access the database. Returns True if the account is successfully created. Otherwise False.
'''
def create_account(cursor):

  print("==========\nAccount Creation\n==========\n")

  cred = get_credentials()
  valid = "northeastern.edu" in cred[2] and len(cred[0]) > 0 and len(cred[1]) > 0 and len(cred[3]) > 0

  if valid:
    try:
      cursor.callproc("create_user", cred)
    except Exception as e:
      valid = False
      print(e)

  return valid


'''
DictCursor -> int

Calls the 'login' stored function to count the number of users that match the
user-input email and password. Returns this number.
'''
def login(cursor):

  print("==========\nLogin\n==========\n")

  email = input("Email: ")
  pwd = input("Password: ")
  num_rows = 0

  try:
    num_rows = cursor.callproc("login", (email, pwd))
  except Exception as e:
    print(e + "\n")
    print("Something went wrong trying to log you in...")
  
  return num_rows
