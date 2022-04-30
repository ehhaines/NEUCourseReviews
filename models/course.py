'''
Evan Haines
April 29, 2022

This class represents a Course. A Course can have many Sections offered by different Professors.
'''
class Course():

  def __init__(self, cursor, subject_code, course_code):
    '''Instantiates a Course object.

    Arguments:
    cursor -- PyMySQL cursor to access MySQL database
    subject_code -- The subject this Course is part of (ex. CS, BIOL, etc)
    course_code -- The 'level' of this Course (ex. 1101, 5200, etc)
    '''
    self.cursor = cursor
    self.subject_code = subject_code
    self.course_code = course_code
  
  def get_subject_code(self):
    '''Takes in no arguments, returns this Course's subject code as a str'''
    return self.subject_code
  
  def get_course_code(self):
    '''Takes in no arguments, returns this Course's course code as an int'''
    return self.course_code

  def get_course_name(self):
    '''Takes in no arguments, returns this Course's name as a list of dicts.
    If an Exception is thrown, returns the Exception instead'''
    try:
      self.cursor.callproc("get_course_name", (self.subject_code, self.course_code,))
      name = self.cursor.fetchall()
      return name
    except Exception as e:
      return e
  
  def get_course_sections(self):
    '''Takes in no arguments, returns this Course's Sections as a list of dicts.
    If an Exception is thrown, returns the Exception instead'''
    try:
      self.cursor.callproc("get_course_sections", (self.subject_code, self.course_code,))
      all_sections = self.cursor.fetchall()
      return all_sections
    except Exception as e:
      return e