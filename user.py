def get_credentials():

  first = input("First Name: ")
  last = input("Last Name: ")
  email = input("Email: ")
  pwd = input("Password: ")

  return first, last, email, pwd


def create_account(cursor):

  cred = get_credentials()

  valid = "northeastern.edu" in cred[2] and len(cred[0]) > 0 and len(cred[1]) > 0 and len(cred[3]) > 0

  if valid:
    cursor.callproc("create_user")
