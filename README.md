This program needs MySQL server to run.
MySQL database contains 2 tables: `expenses` and `users`.
To run the program simply write: `python expenses.py`
At the start it's required to connect to MySQL Server with username and password.
Then there is a choice between creating new user or using existing one.
Enter 1 for new user, then program ask create user first and last name.
Enter 2 for existing user, then program ask for user id which is shown in terminal with their names.
After user is created you have couple of choices what to do with DB:
1 - Look up for data in current user, then enter what specifically you are looking for acceptable words: `food`,`transport`,`taxes`,`clothes` with lowercase or uppercase or -1 if looking for everything.
2 - Add new expense to database, firstly add expense name with suitable words as shown above, then specify amount for expense, finally enter date of expense for example `Sep 5 2021` in this case date is 5th of September 2021.
3 - Deletes all data of current user.
4 - Get statistics of specified year, month or day. Note: year is required to be filled, everything else is not mandatory, simply type -1 if not needed.
0 - Exit the program
Examples of database:
![Expenses table](/screenshots/expenses.jpg?raw=true "Expenses table")
![Users table](/screenshots/users.jpg?raw=true "Users table")
![described tables](/screenshots/describe_expenses_users.jpg?raw=true "Described tables")
![new user](/screenshots/working_example_new_user.jpg?raw=true "working example of adding new user")
![existed user1](/screenshots/working_example_existed_user_1.jpg?raw=true "working example of existing user part1")
![existed user2](/screenshots/working_example_existed_user_2.jpg?raw=true "working example of existing user part2")