import pymysql

def db_connect():
  try:
    cnx = pymysql.connect(host='localhost', user='root', password='password',
    db='ncr', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print("\n==========\nSuccessfully connected to the database.\n==========\n")
    return cnx
  except pymysql.Error as e:
    print("Connection failed, Error: %d: %s" % (e.args[0], e.args[1]))
    exit()
    
