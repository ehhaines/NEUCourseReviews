from curses.ascii import ismeta
from datetime import date

class Person():

  def __init__(self, cursor, email):
    self.cursor = cursor
    self.email = email
  
  def get_email(self):
    return self.email
  
  def get_name(self):
    try:
      self.cursor.callproc("get_person_name", (self.email,))
      name = (self.cursor.fetchall()[0])["name"]
      return name
    except Exception as e:
      return e


class Professor(Person):

  def __init__(self, cursor, email):
    super().__init__(cursor, email)
  
  def get_sections_taught(self):
    try:
      self.cursor.callproc("get_sections_taught", (self.email,))
      all_sections = self.cursor.fetchall()
      return all_sections
    except Exception as e:
      return e
  

class Student(Person):

  def __init__(self, cursor, email, password):
    super().__init__(cursor, email)
    self.password = password
  
  def login(self):
    try:
      self.cursor.callproc("get_matching_users", (self.email, self.password,))
      success = (self.cursor.fetchall()[0])["num"]
    except Exception as e:
      success = 0
    return success
  
  def create_user(self, first, last):
    if len(first.split(" ")) > 0 and len(last.split(" ")) > 0:
      try:
        self.cursor.callproc("create_user", (self.email, first, last, self.password,))
        failure = (self.cursor.fetchall()[0])["success"]
      except:
        failure = 1
      return failure
    return 1
  
  def change_password(self, original, new):
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
    try:
      self.cursor.callproc("get_user_reviews", (self.email,))
      user_reviews = self.cursor.fetchall()
      return user_reviews
    except:
      pass
  
  def add_professor(self, prof_first, prof_last, prof_email):
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
    self.cursor.callproc("add_report", (self.email, review, comments,))
    exists = (self.cursor.fetchall()[0])["exist"]
    return exists

  def delete_review(self, review):
    try:
      self.cursor.callproc("delete_review", (review,))
      print("\nSucessfully deleted review!\n\n")
    except Exception as e:
      print(e)
  
  def update_review(self, review, grade, is_major, time, difficulty, course_qual, prof_qual, comments):
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
