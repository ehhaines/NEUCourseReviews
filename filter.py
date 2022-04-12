import os
import data
import summary

def get_reviews(cursor, section):
  statement = "SELECT * FROM review WHERE section = %d" % (section)
  cursor.execute(statement)
  
  count = 0
  all_reviews = cursor.fetchall()
  for i in all_reviews:
    print(str(count) + "  " + str(i["reviewID"]))
    count += 1

  selected = input("\n\nSelect a review using the numbers of the left: ")
  if selected.lower() == "summary" or selected.lower() == "sum":
    print("\n==========\nSUMMARY\n==========\n\n")
    summary.summarize(cursor, section)
  else:
    selected = int(selected)
    reviewID = (all_reviews[selected])["reviewID"]

    statement2 = "SELECT * FROM review WHERE reviewID = %d" % (reviewID)
    cursor.execute(statement2)

    this_review = cursor.fetchall()

    grade_received  = (this_review[0])["gradeReceived"]
    time_spent = (this_review[0])["timeSpentOnClass"]
    difficulty = (this_review[0])["courseDifficulty"]
    course_quality = (this_review[0])["courseQuality"]
    professor_quality = (this_review[0])["professorQuality"]
    comments = (this_review[0])["comments"]

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\n====================\nREVIEW\n====================\n\n")
    print("Grade Received:\n" + str(grade_received) + "\n")
    print("Weekly hours spent on class: \n" + str(time_spent) + "\n")
    print("Course difficulty (0 = Very easy...10 = Very Difficult)")
    data.make_data_bar("", difficulty)
    print("\nCourse quality (0 = Poor...10 = Excellent)")
    data.make_data_bar("", course_quality)
    print("\nProfessor quality (0 = Poor...10 = Excellent)")
    data.make_data_bar("", professor_quality)
    print("\nComments:\n" + comments)

    print("\n\nYou may need to scroll up to see complete review.\nPress 'Enter' key to begin new search.\nUse command 'exit' to terminate program.")
    user_input = input(">> ")
    if user_input.lower() == "exit":
      cursor.close()
      print("Goodbye!")
      exit()


def by_course_name(cursor):
  print("Enter the name (or keyword in the name) of a course...\n")
  course_name = input(">> ")
  print("\n")
  cursor.callproc("filter_by_course_name", (course_name,))
  all_courses = cursor.fetchall()

  count = 0
  for i in all_courses:
    print(str(count) + "\t" + i["subjectCode"] + str(i["courseCode"]) + " - " + i["courseName"])
    count += 1
  
  this_course = int(input("\n\nChoose a course: "))
  course_code = (all_courses[this_course])["courseCode"]
  subject_code = (all_courses[this_course])["subjectCode"]
  os.system('cls' if os.name == 'nt' else 'clear')
  print("Home > By Code > " + subject_code + str(course_code) + "\n\n")

  statement = "SELECT * FROM section WHERE subjectCode = '%s' AND courseCode = %d" % (subject_code, course_code)
  cursor.execute(statement)

  all_sections = cursor.fetchall()
  count = 0
  profs = []
  terms = []
  for i in all_sections:
    cursor.execute("SELECT CONCAT(firstName, ' ', lastName) AS name FROM professor WHERE email = '%s'" % (i["professor"]))
    prof = (cursor.fetchall()[0])["name"]
    profs.append(prof)
    terms.append(str(i["semester"]) + " " + str(i["year"]))
    print(str(count) + "\t" + prof + "\t" + str(i["semester"]) + " " + str(i["year"]))
    count += 1
  
  this_section = int(input("\n\nChoose a section: "))

  os.system('cls' if os.name == 'nt' else 'clear')
  print("Home > By Code > " + subject_code + str(course_code) + " > " + profs[this_section] + " " + terms[this_section] + "\n\n")
  this_section = (all_sections[this_section])["sectionID"]

  get_reviews(cursor, this_section)
  


def by_subject(cursor):
  print("Enter the subject which your course falls under...\n")
  subject = input(">> ")
  print("\n")
  cursor.callproc("filter_by_subject", (subject,))
  all_subjects = cursor.fetchall()

  count = 0
  for i in all_subjects:
    print(str(count) + "\t" + i["subjectName"] + "    " + i["subjectCode"])
    count += 1
  
  this_subject = int(input("\n\nChoose a subject: "))
  this_subject = (all_subjects[this_subject])["subjectCode"]

  statement = "SELECT * FROM course WHERE subjectCode = '%s'" % this_subject
  cursor.execute(statement)
  all_courses = cursor.fetchall()

  count = 0
  for i in all_courses:
    print(str(count) + "\t" + i["subjectCode"] + str(i["courseCode"]) + " - " + i["courseName"])
    count += 1
  
  this_course = int(input("\n\nChoose a course: "))
  sub_code = (all_courses[this_course])["subjectCode"]
  course_code = (all_courses[this_course])["courseCode"]

  by_course_code(cursor, sub_code, course_code)


def by_course_code(cursor, subject=None, course=None):
  if not subject or not course:
    print("Enter the code or partial code of the course you wish to view...\n")
    code = input(">> ")
    print("\n")

    cursor.callproc("filter_by_code", (code,))
    all_courses = cursor.fetchall()

    count = 0
    for i in all_courses:
      print(str(count) + "  " + i["code"] + " - " + i["courseName"])
      count += 1
    
    selected_course = int(input("\n\nChoose a course using the number on the left: "))
    this_code = (all_courses[selected_course])["code"]
    subjectCode = (all_courses[selected_course])["subjectCode"]
    courseCode = (all_courses[selected_course])["courseCode"]

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Home > By Code > " + this_code + "\n\n")

    statement = "SELECT * FROM section WHERE subjectCode = '%s' AND courseCode = %d ORDER BY year" % (subjectCode, courseCode)
  else:
    statement = "SELECT * FROM section WHERE subjectCode = '%s' AND courseCode = %d ORDER BY year" % (subject, course)


  cursor.execute(statement)

  all_sections = cursor.fetchall()
  count = 0
  profs = []
  terms = []
  for i in all_sections:
    cursor.execute("SELECT CONCAT(firstName, ' ', lastName) AS name FROM professor WHERE email = '%s'" % (i["professor"]))
    prof = (cursor.fetchall()[0])["name"]
    profs.append(prof)
    terms.append(str(i["semester"]) + " " + str(i["year"]))
    print(str(count) + "\t" + prof + "\t" + str(i["semester"]) + " " + str(i["year"]))
    count += 1

  this_section = int(input("\n\nSelect a section by the index: "))
  os.system('cls' if os.name == 'nt' else 'clear')
  if not subject or not course:
    print("Home > By Code > " + this_code + " > " + profs[this_section] + " " + terms[this_section] + "\n\n")
  this_section = (all_sections[0])["sectionID"]
  get_reviews(cursor, this_section)


def by_professor(cursor):
  print("Enter the name, or partial name, of the instructor of your class...")
  print("Names should this format: First Last")
  print("You may also simply enter the first or last name of the professor and choose from the results.\n")
  prof = input(">> ")
  print("\n")
  cursor.callproc("filter_by_professor", (prof,))

  all_prof = cursor.fetchall()
  count = 0
  for i in all_prof:
    print(str(count) + "  " + i["name"] + "  -  " + i["email"])
    count += 1

  choice = int(input("\nSelect a professor (by entering the number next to their name): "))
  choice_name = (all_prof[choice])["name"]
  choice_email = (all_prof[choice])["email"]

  os.system('cls' if os.name == 'nt' else 'clear')
  print("Home > By Professor > " + choice_name + "\n\n")

  cursor.callproc("section_by_professor", (choice_email,))
  all_sections = cursor.fetchall()

  count = 0
  for i in all_sections:
    cursor.execute("SELECT courseName FROM course WHERE subjectCode = '%s' AND courseCode = %d" % (i["subjectCode"], i["courseCode"]))
    title = (cursor.fetchall()[0])["courseName"]
    print(str(count) + "  " + i["subjectCode"] + str(i["courseCode"]) + " - " + title + " - " + str(i["semester"]) + " " + str(i["year"]))
    count += 1
  
  selected_course = int(input("\n\nEnter the number of the course you would like to view: "))

  section_id = (all_sections[selected_course])["sectionID"]

  os.system('cls' if os.name == 'nt' else 'clear')

  print("Home > By Professor > " + choice_name + " > " + (all_sections[selected_course])["subjectCode"] + str((all_sections[selected_course])["courseCode"]))
  
  get_reviews(cursor, section_id)

 

