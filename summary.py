import data
import os

def summarize(cursor, section):
  cursor.callproc("summarize", (section,))
  summary = cursor.fetchall()
  cursor.callproc("time_distribution", (section,))
  time_dist = cursor.fetchall()

  lt3 = 0
  lt7 = 0
  lt11 = 0
  lt15 = 0
  lt20 = 0
  lt25 = 0
  gt25 = 0

  for i in time_dist:
    if i["timeSpentOnClass"] <= 3:
      lt3 += i["num"]
    elif i["timeSpentOnClass"] <= 7:
      lt7 += i["num"]
    elif i["timeSpentOnClass"] <= 11:
      lt11 += i["num"]
    elif i["timeSpentOnClass"] <= 15:
      lt15 += i["num"]
    elif i["timeSpentOnClass"] <= 20:
      lt20 += i["num"]
    elif i["timeSpentOnClass"] <= 25:
      lt25 += i["num"]
    else:
      gt25 += i["num"]

  print("Time (hours) spent outside of class:")
  print("t <= 3: %d" % lt3)
  print("3 < t <= 7: %d" % lt7)
  print("7 < t <= 11: %d" % lt11)
  print("11 < t <= 15: %d" % lt15)
  print("15 < t <= 20: %d" % lt20)
  print("20 < t <= 25: %d" % lt25)
  print("t > 25: %d" % gt25)

  print("\nAvg time spent: %d hours\n" % (summary[0])["time"])
  print("Average Course Difficulty:")
  data.make_data_bar("", (summary[0])["difficulty"])
  print("Average Course Quality:")
  data.make_data_bar("", (summary[0])["courseQuality"])
  print("Average Professor Quality:")
  data.make_data_bar("", (summary[0])["profQual"])

  print("\n\nYou may need to scroll up to see complete summary.\nPress 'Enter' key to begin new search.\nUse command 'exit' to terminate program.")
  user_input = input(">> ")
  if user_input.lower() == "exit":
    cursor.close()
    print("Goodbye!")
    exit()
  os.system('cls' if os.name == 'nt' else 'clear')
  