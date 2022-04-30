'''
Evan Haines
April 29, 2022
'''
from curses.ascii import ismeta
from datetime import date

'''
This class represents a Person. A Person is either a Professor or a Student.
'''
class Person():

  def __init__(self, cursor, email):
    '''Instantiates a Person object.
    
    Arguments:
    cursor -- PyMySQL cursor to access MySQL database
    email -- The email of this Person
    '''
    self.cursor = cursor
    self.email = email
  
  def get_email(self):
    '''Takes in no arguments. Returns the email of this Person as a str'''
    return self.email
  
  def get_name(self):
    '''Takes in no arguments. Returns the full name of this Person as a str.
    If an Exception is thrown, returns the Exception instead'''
    try:
      self.cursor.callproc("get_person_name", (self.email,))
      name = (self.cursor.fetchall()[0])["name"]
      return name
    except Exception as e:
      return e


'''
This class represents a Professor. A Professor teaches a Section of a Course.
A Professor is not supposed to be an active user of the application.
'''
class Professor(Person):

  def __init__(self, cursor, email):
    '''Instantiates a Professor object. Inherits from Person.
    
    Arguments:
    cursor -- PyMySQL cursor to access MySQL database
    email -- The email of this Professor
    '''
    super().__init__(cursor, email)
  
  def get_sections_taught(self):
    '''Takes in no arguments, returns the Sections taught by this Professor as a list of dicts.
    If an Exception is thrown, returns the Exception instead.'''
    try:
      self.cursor.callproc("get_sections_taught", (self.email,))
      all_sections = self.cursor.fetchall()
      return all_sections
    except Exception as e:
      return e
  
'''
This class represent a Student. A Student takes Courses and can leave Reviews.
Students are the users of the application.
'''
class Student(Person):

  def __init__(self, cursor, email, password):
    '''Instantiates a Student object. Inherits from Person.
    
    Arguments:
    cursor -- PyMySQL cursor to access MySQL database
    email -- The email of this Student
    password -- This Student's password to the application
    '''
    super().__init__(cursor, email)
    self.password = password
  
  def login(self):
    '''Takes in no arguments, returns 1 if this Student's email and password combination exists
    in the database, 0 if it does not exist. If an Exception is thrown, returns 0'''
    try:
      self.cursor.callproc("get_matching_users", (self.email, self.password,))
      success = (self.cursor.fetchall()[0])["num"]
    except Exception as e:
      success = 0
    return success
  
  def create_user(self, first, last):
    '''Adds a Student to the database. Returns the number of users that match this Student's
    email and password combination. Automatically returns 1 if an Exception is thrown.

    Arguments:
    first -- the first name of this Student as a str
    last -- the last name of this Student as a str
    '''
    if len(first.split(" ")) > 0 and len(last.split(" ")) > 0:
      try:
        self.cursor.callproc("create_user", (self.email, first, last, self.password,))
        failure = (self.cursor.fetchall()[0])["success"]
      except:
        failure = 1
      return failure
    return 1
  
  def change_password(self, original, new):
    '''Changes this student's password in the database. Returns 1 if the update is successful,
    otherwise returns 0. If an Exception is thrown, it is printed.
    
    Arguments:
    original -- this Student's original password as a str
    new -- the password this Student wants to use instead as a str
    '''
    success = 0
    if self.password == original:
      try:
        self.cursor.callproc("change_password", (self.email, new,))
        success = 1
      except Exception as e:
        print(e)
        print("\n")
    return success
  
  def change_name(self, first, last):
    '''Updates this Student's name. Returns 1 if the change is successful, otherwise
    returns 0. If an Exception is thrown, prints Exception.
    
    Arguments:
    first -- This student's updated first name as a str
    last -- This student's updated last name as a str
    '''
    success = 0
    try:
      self.cursor.callproc("change_name", (self.email, first, last,))
      success = 1
    except Exception as e:
      print(e)
      print("\n")
      success = 0
    return success

  def change_email(self, new_email):
    '''Updates this Student's email and sets this.email to the new address.
    Returns 1 if update is successful and 0 if update fails. If an Exception
    is thrown, the Exception is printed.

    Arguments:
    new_email -- the email address this Student is trying to change to
    '''
    success = 0
    try:
      self.cursor.callproc("change_email", (self.email, new_email,))
      success = 1
      self.email = new_email
    except Exception as e:
      print(e)
      print("\n")
      success = 0
    return success

  def get_reviews(self):
    '''Takes in no arguments, returns all reviews submitted by this Student as a list of dicts'''
    try:
      self.cursor.callproc("get_user_reviews", (self.email,))
      user_reviews = self.cursor.fetchall()
      return user_reviews
    except:
      pass
  
  def add_professor(self, prof_first, prof_last, prof_email):
    '''Adds a Professor to the database. Returns the number of professors in the database that match
    the input. If an Exception is thrown, prints the Exception.
    
    Arguemnts:
    prof_first -- the Professor's first name as a str
    prof_last -- the Professor's last name as a str
    prof_email -- the Professor's email as a str. Must include '@northeastern.edu'
    '''
    exists = 0
    try:
      self.cursor.callproc("add_professor", (prof_first, prof_last, prof_email))
      exists = (self.cursor.fetchall()[0])["exist"]
    except Exception as e:
      exists = 1
      print(e)
      print("\n")
    return exists
  
  def add_course(self, subjectCode, courseCode, courseName):
    '''Adds a Course to the database. Returns the number of courses in the database that match
    the input. If an Exception is thrown, prints the Exception.

    Arguments:
    subjectCode -- the Subject code (ex. CS, PHYS)
    courseCode -- the Course code (ex 1101, 5200)
    courseName -- the name of the course
    '''
    exists = 0
    try:
      self.cursor.callproc("add_course", (subjectCode, courseCode, courseName,))
      exists = (self.cursor.fetchall()[0])["exist"]
    except Exception as e:
      print(e)
      print("\n")
      exists = 1
    return exists
  
  def add_section(self, subjectCode, courseCode, professor, year, semester):
    '''Adds a Section to the database. Returns the number of Sections in the database that match
    the input. If an Exception is thrown, prints the Exception.

    Arguments:
    subjectCode -- the Subject code (ex. CS, PHYS) as a str
    courseCode -- the Course code (ex 1101, 5200) as an int
    professor -- the email of the Professor who taught this Section as a str
    year -- the year this section was taught as an int
    semester -- the semester this section was taught as a str
    '''
    exists = 0
    try:
      self.cursor.callproc("add_section", (subjectCode, courseCode, professor, year, semester,))
      exists = (self.cursor.fetchall()[0])["exist"]
    except Exception as e:
      exists = 1
      print(e)
      print("\n")
    return exists
  
  def add_review(self, grade_received, is_major, time_spent, diff, course_qual, prof_qual, comments, section):
    '''Adds a Review to the database. Returns the number of Reviews in the database that match
    the input. If the Exception is thrown, prints the Exception.

    Arguments:
    grade_received -- the grade this Student received in the associated Section as str
    is_major -- whether this Student is taking the associated course to satisfy major requirements. 1 if
                yes, 0 is no
    time_spent -- the amount of time spent on this Section per week as an int
    diff -- the level of difficulty of this Section as an int
    course_qual -- the quality of this Section as an int
    prof_qual -- the quality of the Professor that taught this Section as an int
    comments -- additional comments about this Section as a str
    section -- the ID of the Section this Review concerns
    '''
    today = date.today()
    poster = self.email
    exists = 0
    try:
      self.cursor.callproc("add_review", (poster, today, grade_received, is_major, time_spent, diff, course_qual, prof_qual, comments, section,))
      exists = (self.cursor.fetchall()[0])["exist"]
    except Exception as e:
      exists = 1
      print(e)
      print("\n\n")
    return exists

  def report(self, review, comments):
    '''Adds a Report to the database. Returns the number of Reports in the database that match
    the input. If the Exception is thrown, prints the Exception.

    Arguments:
    review -- The ID of the Review that this Report concerns as an int
    comments -- The reason why this Report is being submitted as a str
    '''
    self.cursor.callproc("add_report", (self.email, review, comments,))
    exists = (self.cursor.fetchall()[0])["exist"]
    return exists

  def delete_review(self, review):
    '''Deletes a Review from the database. If an Exception is thrown,
    prints the Exception.

    Arguments:
    review -- the id of the Review to be deleted
    '''
    try:
      self.cursor.callproc("delete_review", (review,))
      print("\nSucessfully deleted review!\n\n")
    except Exception as e:
      print(e)
  
  def update_review(self, review, grade, is_major, time, difficulty, course_qual, prof_qual, comments):
    '''Updated a Review to the database. If the Exception is thrown, prints the Exception.

    Arguments:
    review -- the ID of the review to be updated as an int
    grade -- the grade this Student received in the associated Section as str
    is_major -- whether this Student is taking the associated course to satisfy major requirements. 1 if
                yes, 0 is no
    time -- the amount of time spent on this Section per week as an int
    difficulty -- the level of difficulty of this Section as an int
    course_qual -- the quality of this Section as an int
    prof_qual -- the quality of the Professor that taught this Section as an int
    comments -- additional comments about this Section as a str
    '''
    statement = "SELECT * FROM review WHERE reviewID = %d" % (review)
    self.cursor.execute(statement)
    fields = self.cursor.fetchall()[0]
    var_grade = grade if grade else fields["gradeReceived"]
    var_is_major = is_major if is_major == 0 or is_major == 1 else fields["isMajor"]
    var_time = time if time else fields["timeSpentOnClass"]
    var_diff = difficulty if difficulty else fields["courseDifficulty"]
    var_course_qual = course_qual if course_qual else fields["courseQuality"]
    var_prof_qual = prof_qual if prof_qual else fields["professorQuality"]
    var_comments = comments if comments else fields["comments"]
    try:
      self.cursor.callproc("edit_review", (review, var_grade, var_is_major, var_time, var_diff, var_course_qual, var_prof_qual, var_comments))
      print("\nSuccessfully updated review!")
    except Exception as e:
      print(e)
      print("\n")


if __name__ == "__main__":
  import pymysql

  cnx = pymysql.connect(host='localhost', user="root", password="password",
  db='ncr', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
  print("\n==========\nSuccessfully connected to the database.\n==========\n")
  cursor = cnx.cursor()

  student = Student(cursor, "test@b.com", "password")
  print(student.login())
