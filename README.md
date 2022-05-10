# NEUCourseReviews

NEUCourseReviews is a course reviewal application for Northeastern students based on Northeastern's
TRACE Evaluations system. NEUCourseReviews aims to provide only relevent information about classes
to help streamline the process of registering for courses, and presents this information in an easily 
digesitble format.

## Installation

This application was built using Python 3.9 and is meant to run in the terminal. It is therefore imperative to have at least Python 3.9 installed as well as access to the command line. For Windows users, I recommend installing [PuTTY](https://www.putty.org/).

There are a couple of non-standard packages imported in my controller.py file. These are the pymysql and progress packages. To install them, use the package manager:

```bash 
pip3 install <package>
```

You will also need to download MySQLWorkbench and a MySQL server. The database for this app should be run locally. In the controller.py file, look for the Database class. You will need to change the values of 'user' and 'password' in the __init__ method in order to successfully connect to the database.

Download and unzip the zip file in this repo. Next, use the terminal to navigate to the directory called 'NEUCourseReviews". Once in the appropriate directory, you can run the program using

'''bash
python3 app.py
'''

The application should run now.