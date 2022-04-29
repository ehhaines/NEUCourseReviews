class Review():

  def __init__(self, cursor, reviewID):
    self.cursor = cursor
    self.reviewID = reviewID

  def get_review_id(self):
    return self.reviewID
  
  def get_date_posted(self):
    statement = "SELECT datePosted FROM review WHERE reviewID = %d ORDER BY datePosted DESC" % (self.reviewID)
    try:
      self.cursor.execute(statement)
      date = (self.cursor.fetchall()[0])["datePosted"]
      date_str = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
      return date_str
    except Exception as e:
      print(e)

  def get_section_reviewed(self):
    try:
      self.cursor.callproc("get_section_reviewed", (self.reviewID,))
      section_str = (self.cursor.fetchall()[0])["title"]
      return section_str
    except Exception as e:
      print(e)

  def get_review_data(self):
    try:
      self.cursor.callproc("get_review_data", (self.reviewID,))
      review_data = self.cursor.fetchall()
      return review_data
    except Exception as e:
      print(e)
      print("\n")
  
  def retrieve_reports(self):
    try:
      self.cursor.callproc("get_review_reports", (self.reviewID,))
      reports = self.cursor.fetchall()
      return reports
    except Exception as e:
      return e
  
  def retrieve_num_reports(self):
    try:
      self.cursor.callproc("get_num_reports", (self.reviewID,))
      num_reports = (self.cursor.fetchall()[0])["num_reports"]
      return num_reports
    except Exception as e:
      return e

if __name__ == "__main__":
  import pymysql
  from datetime import date

