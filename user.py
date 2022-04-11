'''
DictCursor -> bool

Calls the 'create user' stored procedure in ncr database to insert a user. Needs a cursor object to
access the database. Returns True if the account is successfully created. Otherwise False.
'''
def create_account(cursor):

  print("==========\nAccount Creation\n==========\n")

  first = input("First Name: ")
  last = input("Last Name: ")
  email = input("Email: ")
  pwd = input("Password: ")

  valid = "northeastern.edu" in email and len(first) > 0 and len(last) > 0 and len(pwd) > 0

  if valid:
    try:
      cursor.callproc("create_user", (email, first, last, pwd))
      print("Successfully created account!")
    except Exception as e:
      valid = False
      print(e)
  else:
    print("There is something wrong with your login credentials. Make sure your email is a northeastern address. Also make sure that none of your fields are empty.")
  return valid, email


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
    cursor.callproc("login", (email, pwd))
    num_rows = (cursor.fetchall()[0])['num_rows']
  except Exception as e:
    print(e)
    print("Something went wrong trying to log you in...")
  
  if not num_rows:
    print("\nEmail or password incorrect.\n")

  return num_rows, email

import db
if __name__ == "__main__":
  cnx = db.db_connect()
  cursor = cnx.cursor()

  login(cursor)
  num_rows = cursor.fetchall()
  print(num_rows)
  num_rows = (num_rows[0])['num_rows']
  print(num_rows)
  cursor.close()

# haines.e@northeastern.edu
# password