class Course():

  def __init__(self, cursor, subject_code, course_code):
    self.cursor = cursor
    self.subject_code = subject_code
    self.course_code = course_code
  
  def get_subject_code(self):
    return self.subject_code
  
  def get_course_code(self):
    return self.course_code

  def get_course_name(self):
    try:
      self.cursor.callproc("get_course_name", (self.subject_code, self.course_code,))
      name = self.cursor.fetchall()
      return name
    except Exception as e:
      return e
  
  def get_course_sections(self):
    try:
      self.cursor.callproc("get_course_sections", (self.subject_code, self.course_code,))
      all_sections = self.cursor.fetchall()
      return all_sections
    except Exception as e:
      return e