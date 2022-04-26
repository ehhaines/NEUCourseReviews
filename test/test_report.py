from models import report
import pymysql
import unittest

class TestReportMethods(unittest.TestCase):

  def setUp(self):
    cnx = pymysql.connect(host='localhost', user="root", password="password",
    db='lotrfinal_1', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print("\n==========\nSuccessfully connected to the database.\n==========\n")
    cursor = cnx.cursor()
    self.report = report.Report(cursor, "test@test.com", 1)
  
  def test_get_reporter(self):
    self.assertEqual(self.report.get_reporter(), "test@test.com")
  
  def test_get_review(self):
    self.assertEqual(self.report.get_review(), 1)