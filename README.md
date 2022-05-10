![Lines of code](https://img.shields.io/tokei/lines/github/vnhns/NEUCourseReviews) ![Twitter Follow](https://img.shields.io/twitter/follow/vn_hns?style=social) ![YouTube Video Views](https://img.shields.io/youtube/views/kF0w8zHGmjI?style=social)

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

```bash
python3 app.py
```

The application should run now.

## Usage

![Login Page](/images/login.png)

You can navigate through this application using a series of commands. At the login screen, where you will first be directed when launching the program, there are three commands you may enter: 'login', 'create account', and 'help'. These commands are self-explanatory. If you would prefer not to create an account, you can login with the default test account (username: test@test.com  password: password).

![Home Page](/images/home.png)

Once on the homepage, you can start searching for reviews. There are four ways you can search for reviews: via professor, subject, course name, or course code. You will then be prompted with a series of options to choose from. The above example outlines the process of searching by professor; a similar sequence of prompts will appear when searching by the other methods. You may also add items to the database using the add command in the appropritate prompts.

![Review](/images/review.png)

A review will display the responses of the reviewer and are publicly available to any user of the program. The reviewer's identity, however, is confidential to everyone except the database administrator. Pressing 'enter' on your keyboard will return you to the homepage. Using the 'report' command while on the review page will allow you to report the review. Reports are intended to be used as a system of checks and balances - if a review is offensive or highly erroneous, a user should submit a report.

![Account](/images/account.png)

A user can also access information about their own account using the 'account' command. Here, a user can update their email address or name as well as update or delete any of their own reviews.

## Credits

NEUCourseReviews was created as a final project for CS5200 - Database Management Systems. I would like to thank Professor Kathleen Durant for an amazing semester.