class Subject():

  def __init__(self, cursor, code):
    self.cursor = cursor
    self.code = code
  
  def get_subject_code(self):
    return self.code
  
  def get_subject_name(self):
    statement = "SELECT subjectName FROM subject WHERE subjectCode = '%s'" % (self.code)
    try:
      self.cursor.execute(statement)
      subject_name = (self.cursor.fetchall()[0])["subjectName"]
      return subject_name
    except Exception as e:
      print(e)
  
  def get_subject_sections(self):
    try:
      self.cursor.callproc("get_subject_sections", (self.code,))
      all_sections = self.cursor.fetchall()
      return all_sections
    except Exception as e:
      print(e)