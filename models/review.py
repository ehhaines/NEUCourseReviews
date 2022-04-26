class Review():

  def __init__(self, cursor, reviewID):
    self.cursor = cursor
    self.reviewID = reviewID

  def view_review_data(self):
    try:
      self.cursor.callproc("get_review_data", (self.reviewID,))
      review_data = self.cursor.fetchall()
      return review_data
    except Exception as e:
      return e
  
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

