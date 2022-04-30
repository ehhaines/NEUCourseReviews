'''
Evan Haines
April 29, 2022

Represents a Report. Reports are meant as a system of checks and
balances for reviews.
'''
class Report():

  def __init__(self, cursor, reporter, review):
    self.cursor = cursor
    self.reporter = reporter
    self.review = review

  def get_reporter(self):
    '''Takes in no argument, returns the email of the user who submitted this Report'''
    return self.reporter
  
  def get_review(self):
    '''Takes in no argument, returns the ID of the review that the user reported'''
    return self.review
  
  def get_comments(self):
    '''Takes in no argument, returns the reason why this Report was submitted as a String.
    If an Exception is thrown, returns the Exception'''
    comments = None
    try:
      self.cursor.callproc("get_report_comments", (self.reporter, self.review,))
      comments = (self.cursor.fetchall()[0])["reportReason"]
    except Exception as e:
      comments = e
    return comments


