'''
Evan Haines
April 29, 2022

This class represents a Section. A Section is an instance of a class offerred in 
a particular semester by a Professor.
'''
class Section():

  def __init__(self, cursor, sectionID):
    '''Instantiation of Section object.
    
    Arguments:
    cursor -- PyMySQL cursor to access MySQL database
    sectionID -- the unique ID of a section in the DB
    '''
    self.cursor = cursor
    self.sectionID = sectionID

  def get_sectionID(self):
    '''Takes in no arguments, returns the unique ID of this Section as an int'''
    return self.sectionID
  
  def get_course(self):
    '''Takes in no arguments, returns the Course associated with this section.
    If an Exception is thrown, returns the Exception instead'''
    try:
      self.cursor.callproc("get_section_course", (self.sectionID,))
      course = (self.cursor.fetchall()[0])["course"]
      return course
    except Exception as e:
      return e

  def get_section_professor(self):
    '''Takes in no arguments, returns the Professor that teaches this Section as a str.
    If an Exception is thrown, returns the Exception instead'''
    try:
      self.cursor.callproc("get_section_professor", (self.sectionID,))
      name = (self.cursor.fetchall()[0])["name"]
      return name
    except Exception as e:
      return e

  def get_section_term(self):
    '''Takes in no arguments, returns the term this section was taugth as a str.
    If an Exception is thrown, return the Exception instead'''
    try:
      self.cursor.callproc("get_section_term", (self.sectionID,))
      term = (self.cursor.fetchall()[0])["term"]
      return term
    except Exception as e:
      return e

  def get_section_reviews(self):
    '''Takes in no argments, returns the Reviews associated with this Section as a list of dicts.
    If an Exception is thrown, returns the Exception instead'''
    try:
      self.cursor.callproc("get_section_reviews", (self.sectionID,))
      all_reviews = self.cursor.fetchall()
      return all_reviews
    except Exception as e:
      return e