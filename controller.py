'''
Evan Haines
April 29, 2022
'''
import models.person as mp
import models.section as ms
import models.review as rev
import models.subject as sub
import models.course as c

from curses.ascii import isdigit
import pymysql
import os
from progress.bar import ChargingBar

'''
This class represents the Database.
'''
class Database():

  def __init__(self):
    '''Instatiates a Database object. Connects to the database'''
    try:
      cnx = pymysql.connect(host='localhost', user='root', password='password',
      db='ncr', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
      print("\n==========\nSuccessfully connected to the database.\n==========\n")
    except pymysql.Error as e:
      print("Connection failed, Error: %d: %s" % (e.args[0], e.args[1]))
      exit()
    
    self.cursor = cnx.cursor()
  
  def get_cursor(self):
    '''Takes in no arguments, returns a Cursor object'''
    return self.cursor
  
  def close(self):
    '''Takes in no arguments and returns nothing. Closes the connection
    to the database'''
    self.cursor.close()


'''
This class represents a Session. A Session is the period of
time when a user is using the application.
'''
class Session():

  def __init__(self):
    '''
    Instantiates a Sessions class. Contains a Database object.
    '''
    database = Database()
    self.cursor = database.get_cursor()
    self.user = None
  
  def login(self):
    '''Passes login credential to the user so that the user can log itself in.
    Sets the user field to a Student and returns the user. Takes in no arguments.'''
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nLogin\n--------------------\n\n")

    username = input("Username: ")  # Gets Student's email
    if username.lower() == "back":
      os.system('cls' if os.name == 'nt' else 'clear')
      return

    password = input("Password: ")  # Gets Student's passwor
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
    '''Helper function for create account.'''
    print(statement)
    input("Press 'Enter' to continue")
    os.system('cls' if os.name == 'nt' else 'clear')
    return

  def create_account(self):
    '''Takes in no arguments, returns user. Gathers user input to feed into Student's
    create_account method'''
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nAccount Creation\n--------------------\n\n")
    first = input("First Name: ")   # Get Student's first name
    if (len(first) < 1):
      self.account_creation_error("ERROR: Input may not be empty.")
      return

    last = input("Last Name: ")     # Get Student's last name
    if (len(last) < 1):
      self.account_creation_error("ERROR: Input may not be empty.")
      return

    email = input("Email: ")        # Get Student's NEU email
    email = email.lower()
    if (len(email) < 1):
      self.account_creation_error("ERROR: Input may not be empty.")
      return
    if "@northeastern.edu" not in email:
      self.account_creation_error("ERROR: Email must contain '@northeastern.edu'")
      return

    password = input("Password: ")   # Get Student's password
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
    '''Displays text for help command in login screen. Takes in no argument and returns nothing'''
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
    '''Closes connection to the database and exists the application'''
    self.cursor.close()
    print("Connection to the database has closed")
    exit()
  
  def display_home(self):
    '''Displays the login screen and calls appropriate methods based on user input.
    Takes in no arguments, returns a Student object'''
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
    '''Create a Report about a review. Returns nothing.
    
    Arguments:
    review -- the ID (int) of the Review whose data will be displayed
    '''
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
    '''Uses the progress package to display data. Returns nothing.
    
    Arguments:
    label -- the label of the bar as a str
    quanity -- the fraction of the bar to be filled (out of 100) as an int
    '''
    with ChargingBar(label, suffix=str(quantity), max=100) as bar:
      for i in range(int(quantity * 10)):
        bar.next()
  
  def display_review_data(self, review):
    '''Displays data contained in a Review. Returns nothing.
    
    Arguments:
    review -- the ID of the Review whose data will be displayed
    '''
    review_data = review.get_review_data()[0]
    has_reports = review.retrieve_num_reports()
    os.system('cls' if os.name == 'nt' else 'clear')
    # Display data from a Review
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
  
  def add_review(self, section_id):
    '''Calls Student methods to add a Review to the database. Returns None.
    
    Arguments:
    section_id -- the id of the section and Review will be added under (int)
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nAdd A Review\n--------------------\n")
    print("Fill out the below prompts to add a review to the database.")
    print("You can choose to cancel the review once all prompts are completed.\n\n")

    valid_grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F", "I", "W", "P", "C", "NA"]
    grade = input("What grade did you receive in this class (use 'NA' for not applicable): ")
    grade = grade.upper()   
    if grade not in valid_grades:     # Grade received in course
      print("Grade entered is not valid: please choose from the following:")
      print(valid_grades)
      print("\n\n")
      input("Press 'Enter' to continue")
      return

    valid_is_major = ["y", "yes", "n", "no"]    # Is the Student a major?
    is_major = input("Did you take this class to fulfill major/minor requirements? ")
    if is_major.lower() not in valid_is_major:
      print("Response not valid: please choose from the following:")
      print(valid_is_major)
      print("\n\n")
      input("Press 'Enter' to continue")
      return
    is_major = 1 if (is_major.lower() == "y" or is_major.lower() == "yes") else 0

    time_spent = input("How much time did you spend on this class outside of class time per week? ")
    if not time_spent.isdigit() or float(time_spent) < 0:
      print("\nTime spent must be a positive integer.")     # Hours spent per week
      input("Press 'Enter' to continue")
      return
    time_spent = round(float(time_spent))

    diff = input("On a scale of 0 to 10, how difficult was this class (0 = Very Easy; 10 = Very Difficult)? ")
    if not diff.isdecimal() or float(diff) < 0 or float(diff) > 10:
      print("\nDifficulty must be a positive integer.")   # Level of difficulty
      input("Press 'Enter' to continue")
      return
    diff = round(float(diff))

    course_qual = input("On a scale of 0 to 10, how would you rate the quality of this course (0 = low quality; 10 = high quality)? ")
    if not course_qual.isdecimal() or float(course_qual) < 0 or float(course_qual) > 10:
      print("\nCourse quality must be a positive integer.")   # Course quality
      input("Press 'Enter' to continue")
      return
    course_qual = round(float(course_qual))

    prof_qual = input("On a scale of 0 to 10, how would you rate the quality of this professor (0 = low quality; 10 = high quality)? ")
    if not prof_qual.isdecimal() or float(prof_qual) < 0 or float(prof_qual) > 10:
      print("\nProfessor quality must be a positive integer.")    # Professor quality
      input("Press 'Enter' to continue")
      return
    prof_qual = round(float(prof_qual))

    comments = input("Additional Comments (max 1024 characters):\n\n")  # Addition comments

    while(1):
      submit = input("Do you wish to submit this review to the database? Enter 'yes' to proceed, 'no' to abort.")
      if submit.lower() == "yes" or submit.lower() == "y":
        break
      elif submit.lower() == "no" or submit.lower() == "n":
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    exists = self.user.add_review(grade, is_major, time_spent, diff, course_qual, prof_qual, comments, section_id)
    if not exists:
      print("Successfully added review to the database!\n")
    else:
      print("Could not add review to the database.\n")
    input("Press 'Enter' to continue")


  def get_section_reviews(self, section):
    '''Gets all the reviews in a Section. Returns None.

    Arguments:
    section -- A Section object
    '''
    all_reviews = section.get_section_reviews()   # Get all reviews from section
    if len(all_reviews) == 0:
      print("\n\nThere are no reviews for section %d\n" % (section.get_sectionID()))
      cont = input("Press 'Enter' to continue. Use 'add' command to add a review\n\n")
      if cont.lower() == "add":
        self.add_review(section.get_sectionID())
      return

    print("\nID\tDate Posted\n")
    review_ids = []
    for review in all_reviews:    # Iterate through reviews
      this_review = rev.Review(self.cursor, review["reviewID"])
      review_ids.append(this_review.get_review_id())
      print(str(this_review.get_review_id()) + "\t" + str(this_review.get_date_posted()))
    choice = input("\nSelect a review by its ID: ")
    if choice.lower() == "add":
      self.add_review(section.get_sectionID())
      return
    if not choice.isdigit() or int(choice) not in review_ids:
      print("\nERROR: Illegal value input")
      input("Press 'Enter' to continue")
      return
    out_review = rev.Review(self.cursor, int(choice))
    self.display_review_data(out_review)

  def add_section(self, subjectCode=None, courseCode=None, professor=None):
    '''Add a Section to the database. Returns None.
    
    Arguments:
    subjectCode -- the code of the subject being added (Default None)
    courseCode -- the code of the course being added (Default None)
    professor -- the email of the Professor who taught the section (Default None)
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nAdd A Section\n--------------------\n")
    print("Fill out the below prompts to add a section to the database.")
    print("Type 'abort' in any prompt to abort this process.\n\n")

    if not subjectCode:   # Prompts user for subject code if None
      subjectCode = input("Subject Code (ex. 'CS', 'PHYS', etc): ")
      if subjectCode.lower() == "abort":
        return

    if not courseCode:    # Prompts user for course code if None
      courseCode = input("Course Code (ex. 1101, 5200, etc.): ")
      if courseCode.lower() == "abort":
        return

    if not professor:   # Prompts user for prof email if None
      professor = input("Professor Email: ")
      if professor.lower() == "abort":
        return

    year = input("Year this section was offered: ")   # Prompts user for term data
    if year.lower() == "abort":
      return
    semester = input("Semester this course was offered (SPRING, SUMMER, FALL, WINTER): ")
    if semester.lower() == "abort":
      return

    os.system('cls' if os.name == 'nt' else 'clear')
    exists = self.user.add_section(subjectCode, courseCode, professor, year, semester)
    if not exists:
      print("\nThis section was added to the database!\n\n")
    else:
      print("There was a problem adding this section to the database.\n")
    input("Press 'Enter' to continue")
  
  def get_professor_sections(self, professor):
    '''Gets all sections taught by a professor. Returns None.
    
    Argument:
    professor -- the email of the professor whose sections we are retrieving
    '''
    sections = professor.get_sections_taught()  # Use Professor method to get sections from db
    if len(sections) == 0:  # If no sections
      print("\n\nThere are no sections under %s.\n" % (professor.get_name()))
      cont = input("Press 'Enter' to continue. Use the 'add' command to add a section\n\n")
      if cont.lower() == "add":
        self.add_section(professor=professor.get_email())
      return

    section_id = []
    print("\nID\tSection\n")
    for section in sections:    # Iterate through sections and display them to user
      this_section = ms.Section(self.cursor, section["sectionID"])
      print(str(this_section.get_sectionID()) + ":\t" + this_section.get_course() + " - " + this_section.get_section_term())
      section_id.append(this_section.get_sectionID())
    choice = input("\nChoose a section by inputting its section ID: ")

    if choice.lower() == "add":
      self.add_section(professor=professor.get_email())
      return
    if not choice.isdigit() or int(choice) not in section_id:
      print("\nERROR: Illegal value input")
      input("Press 'Enter' to conitnue")
      return
    out_section_id = int(choice)
    out_section = ms.Section(self.cursor, out_section_id)
    self.get_section_reviews(out_section)
    

  def choose_professor(self, professors):
    '''Selects a professor to get sections from. Returns None.
    
    Arguments:
    professors - a list of professors to choose from
    '''
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


  def add_professor(self):
    '''Adds a Professor to the database using user responses. Returns None.
    Takes no arguments'''
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nAdd A Professor\n--------------------\n")
    print("Fill out the below prompts to add a professor to the database.")
    print("Type 'abort' in any prompt to abort this process.\n\n")

    first = input("Professor First Name: ")     # First name
    if first.lower() == "abort" or not first:
      return

    last = input("Professor Last Name: ")     # Last name
    if last.lower() == "abort" or not last:
      return

    email = input("Professor Email (must contain '@northeastern.edu'): ")   # Email
    if email.lower() == "abort":
      return
    if "@northeastern.edu" not in email.lower():        # Email must be NEU affiliated
      print("\n\nEmail address must belong to NEU.\n")
      input("Press 'Enter' to continue")
      return

    exists = self.user.add_professor(first.capitalize(), last.capitalize(), email)
    os.system('cls' if os.name == 'nt' else 'clear')
    if not exists:
      print("Successfully added professor to the database!\n\n")
    else:
      print("A error occurred while adding this professor to the database.\n")
    input("Press 'Enter' to continue")


  def get_professors(self):
    '''Gets all Professors that match user input. Takes in no arguments, returns None'''
    professor = input("\nEnter the full or partial name of a professor: ")
    if professor.lower() == "abort" or professor.lower() == "a":
      return
    if professor.lower() == "add":
      self.add_professor()
      return

    try:
      self.cursor.callproc("get_matching_professors", (professor,))   # Retrieve profs from db
      all_matching = self.cursor.fetchall()
      if len(all_matching) == 0:
        print("\n\nThere are no professors that match your search. Consider adding one.")
        cont = input("\nPress 'Enter' to continue. Use 'add' command to add a professor\n\n")
        if cont.lower() == "add":
          self.add_professor()
          return
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
    '''Gets a sections created under a subject. Returns None.
    
    Arguments:
    subject -- A Subject object
    '''
    sections = subject.get_subject_sections()   # Calls subject method to get all sections
    if not len(sections):
      print("\n\nThere are no sections under %s.\n" % (subject.get_subject_name()))
      cont = input("Press 'Enter' to continue. Use the 'add' command to add a section\n\n")
      if cont.lower() == "add":
        self.add_section(subjectCode=subject.get_subject_code())
      return

    section_id = []
    print("\nID\tSection\n")
    for section in sections:    # Iterate through all sections
      this_section = ms.Section(self.cursor, section["sectionID"])
      print(str(this_section.get_sectionID()) + ":\t" + this_section.get_course() + " - " + this_section.get_section_term() + " - " + this_section.get_section_professor())
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
    '''Prompts user to choose a subject from a list of subjects. Returns None.
    
    Arguments:
    subjects -- A list of subjects
    '''
    count = 0
    print("Index\tSubject")
    for i in subjects:      # Iterate through list and print each subject
      print(str(count) + ":\t" + i["sub"])
      count = count + 1

    choice = input("\n\nUse the index number to chose a subject: ")
    if not choice.isdigit() or int(choice) > (count - 1):
      print("\n\nERROR: Illegal input value\n")
      input("Press 'Enter' to continue")
      return
    this_subject = (subjects[int(choice)])["subjectCode"]
    this_subject = sub.Subject(self.cursor, this_subject)
    self.get_subject_sections(this_subject)
  
  def start_sub_name(self):
    '''Method for beginning the process of searching for a review by subject name.
    Takes no arguments and returns None.'''
    subject = input("\nEnter the full or partial name of a subject: ")
    if subject.lower() == "abort" or subject.lower() == "a":
      return
    try:
      self.cursor.callproc("get_matching_subjects", (subject,))   # Find all subject like user input
      all_matching = self.cursor.fetchall()
      if len(all_matching) == 0:
        print("\n\nThere are no subjects that match your search.\n")
        input("Press 'Enter' to continue")
        return
      print("\n")
      self.choose_subject(all_matching)
    except Exception as e:
      print(e)

  def get_course_sections(self, course):
    '''Finds all sections under a given course. Returns None.
    
    Arguments:
    course -- A Course object
    '''
    all_sections = course.get_course_sections()   # Use Course method to get all sections
    if len(all_sections) == 0:    # Check to make sure there is at least one section
      print("\n\nThere are no sections under %s.\n" % (course.get_course_name()))
      cont = input("Press 'Enter' to continue. Use the 'add' command to add a section\n\n")
      if cont.lower() == "add":
        self.add_section(subjectCode=course.get_subject_code(), courseCode=course.get_course_code())
      return

    section_id = []
    print("\nID\tSection\n")
    for section in all_sections:  # Iterate through and print list of sections
      this_section = ms.Section(self.cursor, section["sectionID"])
      print(str(this_section.get_sectionID()) + ":\t" + this_section.get_course() + " - " + this_section.get_section_term() + " - " + this_section.get_section_professor())
      section_id.append(this_section.get_sectionID())
    choice = input("\nChoose a section by inputting its section ID: ")
    if choice.lower() == "add":
      self.add_section(subjectCode=course.get_subject_code(), courseCode=course.get_course_code())
      return
    if not choice.isdigit() or int(choice) not in section_id:
      print("\nERROR: Illegal value input")
      input("Press 'Enter' to conitnue")
      return
    out_section_id = int(choice)
    out_section = ms.Section(self.cursor, out_section_id)
    self.get_section_reviews(out_section)

  
  def choose_course(self, courses):
    '''Prompts user to choose a course from a list of courses. Returns None.
    
    Arguments:
    courses -- list of courses
    '''
    print("Index\tCourse")
    count = 0
    for i in courses:     # Iterates through list of courses and prints them
      print(str(count) + "\t" + i["name"])
      count = count + 1

    choice = input("\n\nSelect a course by entering its index value: ")   # User chooses course
    if not choice.isdigit() or int(choice) > (count-1):
      print("\n\nERROR: Illegal input value\n")
      input("Press 'Enter' to continue.")
      return

    this_course_code = (courses[int(choice)])["courseCode"]
    this_subject_code = (courses[int(choice)])["subjectCode"]
    this_course = c.Course(self.cursor, this_subject_code, this_course_code)
    self.get_course_sections(this_course)
  
  def add_course(self):
    '''Calls user method to add a course to the database. Takes no arguments,
    returns None'''
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nAdd A Course\n--------------------\n")
    print("Fill out the below prompts to add a course to the database.")
    print("Type abort in any prompt to abort this process.\n\n")
    subject = input("Subject Code (ex. CS, PHYS, etc.): ")

    if subject.lower() == "abort":      # Get course info from user input
      return
    code = input("Course Code (ex. 1101, 5200, etc.): ")
    if not code.isdigit(): 
      print("\n!Course Code must be a digit - Aborting process!\n")
      input("Press 'Enter' to continue")
      return
    if code.lower() == "abort":
      return
    name = input("Course Name (ex. Database Management Systems): ")
    if name.lower() == "abort":
      return

    exists = self.user.add_course(subject, code, name)  # exists >= 1 -> course already exists
    os.system('cls' if os.name == 'nt' else 'clear')    # exists = 0 -> course can be added
    if not exists:
      print("Your course has been added to the database!\n\n")
    else:
      print("A problem occured while adding your course to the database.\n\n")
    input("Press 'Enter' to continue")


  def start_course_name(self):
    '''Begins process of searching for reviews by course name. Takes no arguments,
    returns None'''
    course_name = input("\nEnter the full or partial name of a course: ")
    if course_name.lower() == "add":
      self.add_course()
      return
    try:
      self.cursor.callproc("get_matching_course_names", (course_name,)) # Finds all courses with
      all_matching = self.cursor.fetchall()                             # course names like the user input
      if len(all_matching) == 0:
        print("\n\nThere are no course names that match your search.\n")
        command = input("Press 'Enter' to continue or use the 'add' command to add a course.\n\n")
        if command.lower() == "add":
          self.add_course()
        return
      print("\n")
      self.choose_course(all_matching)
    except Exception as e:
      print(e)
  
  def start_course_code(self):
    '''Begins process of searching for reviews by course code. Takes no arguments,
    returns None'''
    course_code = input("\nEnter the full or partial code of a course (ex. CS5200): ")
    if course_code.lower() == "add":
      self.add_course()
      return
    course_code = course_code.replace(" ", "")
    try:
      self.cursor.callproc("get_matching_course_codes", (course_code,))   # Finds all courses with
      all_matching = self.cursor.fetchall()                               # course codes like the user input
      if len(all_matching) == 0:
        print("\n\nThere are no course codes that match your search.\n")
        command = input("Press 'Enter' to continue or use the add command to add a course\n\n")
        if command.lower() == "add":
          self.add_course()
        return
      print("\n")
      self.choose_course(all_matching)
    except Exception as e:
      print(e)

  def change_password(self):
    '''Calls Student method to update password. Takes no arguments, returns none'''
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nUpdate Password\n--------------------\n")
    old_pass = input("Enter your old password: ")
    if old_pass.lower() == "abort":
      return
    new_pass = input("Enter your new password: ")   # new password
    if new_pass.lower() == "abort":
      return
    os.system('cls' if os.name == 'nt' else 'clear')
    success = self.user.change_password(old_pass, new_pass)   # Student method
    if success:
      print("Successfully changed password!\n\n")
    else:
      print("Password change failed.\n\n")
    input("Press 'Enter' to continue")
  
  def delete_review(self, user_reviews, chosen_review):
    '''Calls Student method to delete review. Returns none
    
    Arguments:
    user_reviews -- a list of all reviews from this Student
    chosen_review -- the ID of the review to be deleted
    '''
    if chosen_review not in user_reviews:
      print("\nYou do not have access to review %s\n\n" % (chosen_review))
    else:
      decision = input("\nDo you really want to delete this review? Use 'abort' command to opt out. Otherwise, press 'Enter'\n")
      if decision.lower() == "abort":
        return
      self.user.delete_review(int(chosen_review))
    input("Press 'Enter' to continue")

  def update_review(self, user_reviews, chosen_review):
    '''Calls student method to update a review. Returns none
    
    Arguments:
    user_reviews -- a list of reviews from this Student
    chosen_revie -- the ID of the review to be updated
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    if chosen_review not in user_reviews:
      print("\nYou do not have access to review %s\n\n" % (chosen_review))
    else:
      print("--------------------\nUpdate Review %s\n--------------------\n" % (chosen_review))
      print("You will be shown your original answers to each prompt in the review.")
      print("If you do not wish to modify your response to a prompt, simply leave it blank and press 'Enter'.")
      print("If you wish to modify your response, write your new response in the space provided and then press 'Enter'.")
      print("You will have the option to abort this process once all prompts are shown.\n\n")

      this_review = rev.Review(self.cursor, int(chosen_review))
      data = this_review.get_review_data()[0]

      print("Grade Received: " + data["gradeReceived"])   # Grade received
      grade = input(">> ")
      grade = grade.upper()
      if grade:
        valid_grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F", "I", "W", "P", "C", "NA"]
        if grade not in valid_grades:
          print("\nIllegal response...terminating process. Valid grades are listed below:")
          print(valid_grades)
          input("\nPress 'Enter' to continue")
          return

      is_major = "Yes" if data["isMajor"] else "No"   # Is major
      print("\nDid you take this class to satisfy major/minor requirements? %s" % (is_major))
      is_major_response = input(">> ")
      if is_major_response:
        if is_major_response.lower() == "yes" or is_major_response.lower() == "y":
          is_major_response = 1
        else:
          is_major_response = 0

      print("\nHow many hours did you spend on this class outside of class time? %d" % (data["timeSpentOnClass"]))
      time_spent = input(">> ")   # Hours spent on class
      if time_spent:
        if not time_spent.isdigit() or float(time_spent) < 0 or float(time_spent) > 10:
          print("\nTime spent must be a positive integer.")
          input("Press 'Enter' to continue")
          return
        time_spent = round(float(time_spent))

      print("\nOn a scale from 0 to 10, how difficult was this course (0 = Very Easy; 10 = Very Difficult)? %d" % (data["courseDifficulty"]))
      diff = input(">> ")   # Difficulty of class
      if diff:
        if not diff.isdecimal() or float(diff) < 0 or float(diff) > 10:
          print("\nDifficulty must be a positive integer.")
          input("Press 'Enter' to continue")
          return
        diff = round(float(diff))

      print("\nOn a scale of 0 to 10, how would you rate the quality of this course (0 = low quality; 10 = high quality)? %d" % (data["courseQuality"]))
      course_qual = input(">> ")    # Course quality
      if course_qual:
        if not course_qual.isdecimal() or float(course_qual) < 0 or float(course_qual) > 10:
          print("\nCourse quality must be a positive integer.")
          input("Press 'Enter' to continue")
          return
        course_qual = round(float(course_qual))

      print("\nOn a scale of 0 to 10, how would you rate the quality of this professor (0 = low quality; 10 = high quality)? %d" % (data["professorQuality"]))
      prof_qual = input(">> ")    # Professor quality
      if prof_qual:
        if not prof_qual.isdecimal() or float(prof_qual) < 0 or float(prof_qual) > 10:
          print("\nProfessor quality must be a positive integer.")
          input("Press 'Enter' to continue")
          return
        prof_qual = round(float(prof_qual))

      print("\nAdditional Comments: ")    # Additional comments
      print(data["comments"])
      comments = input("\n>> ")

      os.system('cls' if os.name == 'nt' else 'clear')
      self.user.update_review(int(chosen_review), grade, is_major_response, time_spent, diff, course_qual, prof_qual, comments)
      input("\nPress 'Enter' to continue")

  def change_name(self):
    '''Calls Student method to change Student's name. Takes no arguments, return None'''
    os.system('cls' if os.name == 'nt' else 'clear')

    first = input("First Name: ")     # First name
    if len(first.split()) == 0:
      print("\nFirst name must not be null.")
      input("Press 'Enter' to continue")
      return

    last = input("Last Name: ")     # Last name
    if len(last.split()) == 0:
      print("\nLast name must not be null.")
      input("Press 'Enter' to continue")
      return

    decision = input("\nAre you sure you would like to change your name? Use command 'abort' to terminate. Otherwise press 'Enter'.")
    if decision.lower() == "abort":
      return

    os.system('cls' if os.name == 'nt' else 'clear')
    success = self.user.change_name(first, last)
    if success:
      print("Your name has been updated!\n")
    else:
      print("Failed to change name.\n")
    input("Press 'Enter' to continue")
  
  def change_email(self):
    '''Calls Student method to change Student's email. Takes no arguments, return None'''
    os.system('cls' if os.name == 'nt' else 'clear')
    new_email = input("Enter you updated email address: ")
    if "@northeastern.edu" not in new_email:
      print("\nYour email must contain '@northeastern.edu'.")
      input("Press 'Enter' to continue")
      return
    decision = input("\nAre you sure you would like to change your name? Use command 'abort' to terminate. Otherwise press 'Enter'.")
    if decision.lower() == "abort":
      return
    os.system('cls' if os.name == 'nt' else 'clear')
    success = self.user.change_email(new_email)
    if success:
      print("Your email has been changed!\n")
    else:
      print("An error occurred while updating your email address.\n")
    input("Press 'Enter' to continue")


  def view_account(self):
    '''Interface to interact with account page. Takes no arguments, returns none'''
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------\nUser Account\n--------------------\n")

    print("Here you can view your personal information. All your reviews are displayed as well.")
    print("Use the 'update <reviewID>' command to update a review.")
    print("Use the 'delete <reviewID>' command to delete a review.")
    print("Use the 'change pwd' command to change your password, 'change name' to change your name,\nand 'change email' to update your email.")
    print("Press 'Enter' to return to the home screen.")

    print("\n\nName: %s" % (self.user.get_name()))
    print("Email: %s" % (self.user.get_email()))
    print("\nYour Reviews:\n")
    all_reviews = self.user.get_reviews()
    print("ReviewID\tReview Info")
    review_ids = []
    for i in all_reviews:
      id = str(i["reviewID"])
      review_ids.append(id)
      print(id + "\t\t" + i["course"] + " - " + i["term"] + " - " + i["prof"])
    command = input("\n\n>> ")
    if command.lower() == "change pwd":
      self.change_password()
      return
    elif command.lower() == "change name":
      self.change_name()
      return
    elif command.lower() == "change email":
      self.change_email()
      return
    command = command.split()
    if not len(command):
      return
    elif command[0].lower() == "delete":
      if len(command) == 2:
        chosen_rev = command[1]
        self.delete_review(review_ids, chosen_rev)
        return
    elif command[0].lower() == "update":
      if len(command) == 2:
        chosen_rev = command[1]
        self.update_review(review_ids, chosen_rev)
        return
    
   
  def display_main(self, user):
    '''Interface to interact with the search page. Takes no arguments, returns none'''
    while(1):
      os.system('cls' if os.name == 'nt' else 'clear')
      print("Welcome, %s!\n" % user.get_name())
      print("""
      You can search for courses using the 'professor', 'subject name', 'course name', and 'course code' commands.
      You can also use the 'account' command to view and update your account information.
      Use the 'help' command if you need assistant, and 'exit' or 'quit' to logout.\n
      Enter a command below to begin!
      """)
      command = input(">> ")
      command = command.lower()
      if command == "professor" or command == "prof" or command == "p":
        self.get_professors()
      elif command == "subject name" or command == "subject" or command == "sub" or command == "s":
        self.start_sub_name()
      elif command == "course name" or command == "cn":
        self.start_course_name()
      elif command == "course code" or command == "cc":
        self.start_course_code()
      elif command == "account" or command == "a":
        self.view_account()
      elif command == "quit" or command == "exit" or command == "q":
        self.cursor.close()
        self.exit()



