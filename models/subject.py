'''
Evan Haines
April 29, 2022

This class represents a subject. Subjects contain many Courses.
'''
class Subject():

  def __init__(self, cursor, code):
    '''Instantiates a Subject object.

    Arguments:
    cursor -- PyMySQL cursor to access MySQL database
    code -- The subject code (Ex. CS, PHYS, THTR, etc)
    '''
    self.cursor = cursor
    self.code = code
  
  def get_subject_code(self):
    '''Takes in no arguments, returns the subject code as a str'''
    return self.code
  
  def get_subject_name(self):
    '''Takes in no arguments, returns the name of the subject as a str.
    If an Exception is thrown, prints the Exception instead of returning anything'''
    statement = "SELECT subjectName FROM subject WHERE subjectCode = '%s'" % (self.code)
    try:
      self.cursor.execute(statement)
      subject_name = (self.cursor.fetchall()[0])["subjectName"]
      return subject_name
    except Exception as e:
      print(e)
  
  def get_subject_sections(self):
    '''Takes in no arguments, returns the Course Sections under this Subject as a list of dicts.
    If an Exception is thrown, prints the Exception instead of returning anything'''
    try:
      self.cursor.callproc("get_subject_sections", (self.code,))
      all_sections = self.cursor.fetchall()
      return all_sections
    except Exception as e:
      print(e)