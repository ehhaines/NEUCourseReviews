import pymysql
import models.person as mp
import models.section as ms
import models.review as rev
import models.subject as sub
import models.course as c
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
    self.user = None
  
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
    self.user = user
    return user
  
  def account_creation_error(self, statement):
    print(statement)
    input("Press 'Enter' to continue")
    os.system('cls' if os.name == 'nt' else 'clear')
    return

  def create_account(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nAccount Creation\n--------------------\n\n")
    first = input("First Name: ")
    if (len(first) < 1):
      self.account_creation_error("ERROR: Input may not be empty.")
      return
    last = input("Last Name: ")
    if (len(last) < 1):
      self.account_creation_error("ERROR: Input may not be empty.")
      return
    email = input("Email: ")
    email = email.lower()
    if (len(email) < 1):
      self.account_creation_error("ERROR: Input may not be empty.")
      return
    if "@northeastern.edu" not in email:
      self.account_creation_error("ERROR: Email must contain '@northeastern.edu'")
      return
    password = input("Password: ")
    if (len(password) < 1):
      self.account_creation_error("ERROR: Input may not be empty.")
      return
    user = mp.Student(self.cursor, email, password)
    success = user.create_user(first, last)
    if not success:
      self.account_creation_error("ERROR: Account creation failed")
      return
    self.user = user
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
    user = None

    while not user:
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
  
  def generate_report(self, review):
    print("\n\n------------------\nSubmit a report for review %d\n------------------\n\n" % (review.get_review_id()))
    print("Reports can be submitted about a review if the review is offensive or overtly erroneous." +
    " Please complete the below prompts so we can better understand the report. Enter 'abort' command to opt out.\n\n")
    reason = input("Why are you reporting this review? (1024 character max)\n\n")
    if reason.lower() == "abort":
      return
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
      exists = self.user.report(review.get_review_id(), reason)
      if not exists:
        print("Review successfully reported! Thanks for your time!\n\n")
      else:
        print("You have already reported this review!\n\n")
    except Exception as e:
      print(e)
      print("\n")
    input("Press 'Enter' to continue")
  
  def display_bar(self, label, quantity):
    with ChargingBar(label, suffix=str(quantity), max=100) as bar:
      for i in range(int(quantity * 10)):
        bar.next()
  
  def display_review_data(self, review):
    review_data = review.get_review_data()[0]
    has_reports = review.retrieve_num_reports()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nReport for %s\n--------------------" % (review.get_section_reviewed()))
    print("Review ID: %d" % review.get_review_id())
    print("Posted: %s\n\n" % (review.get_date_posted()))
    if has_reports:
      print("!!!!!Caution - this review has been reported %d time(s).!!!!!\n!!!!!Information in this review could be erroneous or offensive!!!!!\n\n" % (has_reports))
    print("Grade Received: %s\n" % (review_data["gradeReceived"]))
    if review_data["isMajor"]:
      print("Is Major: Yes\n")
    else:
      print("Is Major: No\n")
    print("Weekly hours spent outside of class: %d\n" % (review_data["timeSpentOnClass"]))
    print("Course Difficulty (0 = Very Easy; 10 = Very Difficult):")
    self.display_bar("", review_data["courseDifficulty"])
    print("\nCourse quality (0 = Poor Quality; 10 = Excellent Quality):")
    self.display_bar("", review_data["courseQuality"])
    print("\nProfessor quality: (0 = Poor Quality; 10 = Excellent Quality):")
    self.display_bar("", review_data["professorQuality"])
    print("\nComments:\n")
    print(review_data["comments"])
    choice = input("\n\nPress 'Enter' to continue or use 'report' command to report this review.\n\n")
    if choice.lower() == "report" or choice.lower() == "r":
      self.generate_report(review)
    
  
  def get_section_reviews(self, section):
    all_reviews = section.get_section_reviews()
    if len(all_reviews) == 0:
      print("\n\nThere are no reviews for section %d\n" % (section.get_sectionID()))
      cont = input("Press 'Enter' to continue. Use 'add' command to add a review\n\n")
      if cont.lower() == "add":
        pass
      return
    print("\nID\tDate Posted\n")
    review_ids = []
    for review in all_reviews:
      this_review = rev.Review(self.cursor, review["reviewID"])
      review_ids.append(this_review.get_review_id())
      print(str(this_review.get_review_id()) + "\t" + str(this_review.get_date_posted()))
    choice = input("\nSelect a review by its ID: ")
    if not choice.isdigit() or int(choice) not in review_ids:
      print("\nERROR: Illegal value input")
      input("Press 'Enter' to continue")
      return
    out_review = rev.Review(self.cursor, int(choice))
    self.display_review_data(out_review)

  
  def get_professor_sections(self, professor):
    sections = professor.get_sections_taught()
    if len(sections) == 0:
      print("\n\nThere are no sections under %s.\n" % (professor.get_name()))
      cont = input("Press 'Enter' to continue. Use the 'add' command to add a section\n\n")
      if cont.lower() == "add":
        pass
      return
    section_id = []
    print("\nID\tSection\n")
    for section in sections:
      this_section = ms.Section(self.cursor, section["sectionID"])
      print(str(this_section.get_sectionID()) + ":\t" + this_section.get_course() + " - " + this_section.get_section_term())
      section_id.append(this_section.get_sectionID())
    choice = input("\nChoose a section by inputting its section ID: ")
    if not choice.isdigit() or int(choice) not in section_id:
      print("\nERROR: Illegal value input")
      input("Press 'Enter' to conitnue")
      return
    out_section_id = int(choice)
    out_section = ms.Section(self.cursor, out_section_id)
    self.get_section_reviews(out_section)
    

  def choose_professor(self, professors):
    count = len(professors) - 1
    choice = input("\nSelect the index of the professor you wish to search: ")
    if not choice.isdigit():
      print("\nERROR: Input must be a positive digit")
      input("Press 'Enter' to continue")
      return
    choice = int(choice)
    if choice > count:
      print("\nError: Value exceeds input range")
      input("Press 'Enter' to continue")
      return
    professor = professors[choice]
    professor = mp.Professor(self.cursor, professor["email"])
    self.get_professor_sections(professor)

  def get_professors(self):
    professor = input("\nEnter the full or partial name of a professor: ")
    if professor.lower() == "abort" or professor.lower() == "a":
      return
    try:
      self.cursor.callproc("get_matching_professors", (professor,))
      all_matching = self.cursor.fetchall()
      if len(all_matching) == 0:
        print("\n\nThere are no professors that match your search. Consider adding one.")
        cont = input("\nPress 'Enter' to continue. Use 'add' command to add a professor\n\n")
        if cont.lower() == "add":
          pass
        return
      count = 0
      print("\n")
      for i in all_matching:
        print(str(count) + ": " + "\t" + i["name"])
        count = count + 1
      self.choose_professor(all_matching)
    except Exception as e:
      print(e)
      return
  
  def get_subject_sections(self, subject):
    sections = subject.get_subject_sections()
    if len(sections) == 0:
      print("\n\nThere are no sections under %s.\n" % (subject.get_subject_name()))
      cont = input("Press 'Enter' to continue. Use the 'add' command to add a section\n\n")
      if cont.lower() == "add":
        pass
      return
    section_id = []
    print("\nID\tSection\n")
    for section in sections:
      this_section = ms.Section(self.cursor, section["sectionID"])
      print(str(this_section.get_sectionID()) + ":\t" + this_section.get_course() + " - " + this_section.get_section_term())
      section_id.append(this_section.get_sectionID())
    choice = input("\nChoose a section by inputting its section ID: ")
    if not choice.isdigit() or int(choice) not in section_id:
      print("\nERROR: Illegal value input")
      input("Press 'Enter' to conitnue")
      return
    out_section_id = int(choice)
    out_section = ms.Section(self.cursor, out_section_id)
    self.get_section_reviews(out_section)

  
  def choose_subject(self, subjects):
    count = 0
    print("Index\tSubject")
    for i in subjects:
      print(str(count) + ":\t" + i["sub"])
      count = count + 1
    choice = input("\n\nUse the index number to chose a subject: ")
    if not choice.isdigit() or int(choice) > count:
      print("\n\nERROR: Illegal input value\n")
      input("Press 'Enter' to continue")
    this_subject = (subjects[int(choice)])["subjectCode"]
    this_subject = sub.Subject(self.cursor, this_subject)
    self.get_subject_sections(this_subject)
  
  def start_sub_name(self):
    subject = input("\nEnter the full or partial name of a subject: ")
    if subject.lower() == "abort" or subject.lower() == "a":
      return
    try:
      self.cursor.callproc("get_matching_subjects", (subject,))
      all_matching = self.cursor.fetchall()
      if len(all_matching) == 0:
        print("\n\nThere are no subjects that match your search.\n")
        input("Press 'Enter' to continue")
        return
      print("\n")
      self.choose_subject(all_matching)
    except Exception as e:
      print(e)
  
  def choose_course(self, courses):
    pass

  def start_course_name(self):
    course_name = input("\nEnter the full or partial name of a course: ")
    try:
      self.cursor.callproc("get_matching_course_names", (course_name,))
      all_matching = self.cursor.fetchall()
      if len(all_matching) == 0:
        print("\n\nThere are no course names that match your search.\n")
        input("Press 'Enter' to continue")
        return
      print("\n")
      self.choose_course(all_matching)
    except Exception as e:
      print(e)
    

  def display_main(self, user):
    while(1):
      os.system('cls' if os.name == 'nt' else 'clear')
      print("Welcome, %s!\n\n" % user.get_name())
      print("""
      You can search for courses by professor, subject name, course name, or course code.\n
      How would you like to search?
      """)
      command = input(">> ")
      command = command.lower()
      if command == "professor" or command == "prof" or command == "p":
        self.get_professors()
      elif command == "subject name" or command == "subject" or command == "sub" or command == "s":
        self.start_sub_name()
      elif command == "course name" or command == "cn":
        pass
      elif command == "course code" or command == "cc":
        pass
      elif command == "account" or command == "a":
        pass
      elif command == "quit" or command == "exit" or command == "q":
        self.cursor.close()
        self.exit()
      else:
        pass



