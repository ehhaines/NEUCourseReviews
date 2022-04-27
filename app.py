import controller as c

def main():
  session = c.Session()
  user = session.display_home()
  session.display_main(user)

if __name__ == "__main__":
  main()
