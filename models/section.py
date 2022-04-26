class Section():

  def __init__(self, cursor, sectionID):
    self.cursor = cursor
    self.sectionID = sectionID

  def get_sectionID(self):
    return self.sectionID
  
  def get_course(self):
    try:
      self.cursor.callproc("get_section_course", (self.sectionID,))
      course = (self.cursor.fetchall()[0])["course"]
      return course
    except Exception as e:
      return e

  def get_section_professor(self):
    try:
      self.cursor.callproc("get_section_professor", (self.sectionID,))
      name = (self.cursor.fetchall()[0])["name"]
      return name
    except Exception as e:
      return e

  def get_section_term(self):
    try:
      self.cursor.callproc("get_section_term", (self.sectionID,))
      term = (self.cursor.fetchall()[0])["term"]
      return term
    except Exception as e:
      return e

  def get_section_reviews(self):
    try:
      self.cursor.callproc("get_section_reviews", (self.sectionID,))
      all_reviews = self.cursor.fetchall()
      return all_reviews
    except Exception as e:
      return e