
class Report():

  def __init__(self, cursor, reporter, review):
    self.cursor = cursor
    self.reporter = reporter
    self.review = review

  def get_reporter(self):
    return self.reporter
  
  def get_review(self):
    return self.review
  
  def get_comments(self):
    comments = None
    try:
      self.cursor.callproc("get_report_comments", (self.reporter, self.review,))
      comments = (self.cursor.fetchall()[0])["reportReason"]
    except Exception as e:
      comments = e
    return comments


