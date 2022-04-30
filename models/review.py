'''
Evan Haines
April 29, 2022

Represents a Review. A Review is a questionnaire of sorts which a 
student can use to provide information and personal opinions on a class.
'''
class Review():

  def __init__(self, cursor, reviewID):
    '''Instantiation of Review object.

    Arguments:
    cursor -- PyMySQL cursor to access MySQL database
    reviewID -- the unique ID of a review in the DB
    '''
    self.cursor = cursor
    self.reviewID = reviewID

  def get_review_id(self):
    '''Takes in no arguments, returns the unique ID of this Review as an int'''
    return self.reviewID
  
  def get_date_posted(self):
    '''Takes in no arguments, returns the date this Review was posted as a str formatted YY-MM-DD.
    If an Exception is thrown, prints the Exception instead of returning anything'''
    statement = "SELECT datePosted FROM review WHERE reviewID = %d ORDER BY datePosted DESC" % (self.reviewID)
    try:
      self.cursor.execute(statement)
      date = (self.cursor.fetchall()[0])["datePosted"]
      date_str = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
      return date_str
    except Exception as e:
      print(e)

  def get_section_reviewed(self):
    '''Takes in no arguments, returns the Course Section concerning this Review.
    If an Exception is thrown, prints the Exception instead of returning anything'''
    try:
      self.cursor.callproc("get_section_reviewed", (self.reviewID,))
      section_str = (self.cursor.fetchall()[0])["title"]
      return section_str
    except Exception as e:
      print(e)

  def get_review_data(self):
    '''Takes in no arguments, returns the user's responses in this Review as a list of dictionaries.
    If an Exception is thrown, prints the Exception instead of returning anything'''
    try:
      self.cursor.callproc("get_review_data", (self.reviewID,))
      review_data = self.cursor.fetchall()
      return review_data
    except Exception as e:
      print(e)
      print("\n")
  
  def retrieve_reports(self):
    '''Takes in no arguments, returns the Reports associated with this Review as a list of dictionaries.
    If an Exception is thrown, returns the Exception instead'''
    try:
      self.cursor.callproc("get_review_reports", (self.reviewID,))
      reports = self.cursor.fetchall()
      return reports
    except Exception as e:
      return e
  
  def retrieve_num_reports(self):
    '''Takes in no arguments, returns the number of reports associated with this Review as an int.
    Returns an Exception instead if one is thrown'''
    try:
      self.cursor.callproc("get_num_reports", (self.reviewID,))
      num_reports = (self.cursor.fetchall()[0])["num_reports"]
      return num_reports
    except Exception as e:
      return e


