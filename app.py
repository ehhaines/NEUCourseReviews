import controller as c
import os

def main():
  os.system('cls' if os.name == 'nt' else 'clear')
  session = c.Session()
  user = session.display_home()
  session.display_main(user)

if __name__ == "__main__":
  main()
