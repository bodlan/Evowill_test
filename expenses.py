from datetime import datetime
from mysql.connector import connect, Error
import calendar


class Expenses:
    def __init__(self, user_id, connection):
        self.id = user_id
        self.db = connection

    def print_data(self, extraction=''):
        words=['food', 'transport', 'taxes', 'clothes']
        if extraction == str(-1):
            extract_data_query = f"""
            SELECT * FROM expenses
            WHERE user_id='{self.id}'
            """
        elif extraction in (words or [expense.istitle() for expense in words]
                                  or [expense.upper() for expense in words]):
            extract_data_query = f"""
            SELECT {extraction}, date FROM expenses
            WHERE user_id='{self.id}'
            """
        else:
            raise ValueError

        with self.db.cursor() as cursor:
            cursor.execute(extract_data_query)
            result = cursor.fetchall()
            for row in result:
                if extraction != str(-1):
                    raw_date = str(row[1]).split('-')
                    print(f"{extraction} = {row[0]} in {raw_date[2]} "
                          f"{calendar.month_name[int(raw_date[1])]} {raw_date[0]}")
                else:
                    raw_date = str(row[5]).split('-')
                    print(f"food={row[1]}, transport={row[2]}, "
                          f"taxes={row[3]}, clothes={row[4]}"
                          f" in {raw_date[2]} {calendar.month_name[int(raw_date[1])]} {raw_date[0]}")

    def get_statistics(self, year, month, day):
        if month == -1:
            get_statistics_query = f"""
            SELECT * FROM expenses 
            WHERE user_id={self.id}
            AND date BETWEEN '{year}-01-1' AND '{year}-12-31'
            """
        elif day == -1:
            get_statistics_query = f"""
                        SELECT * FROM expenses
                        WHERE user_id='{self.id}'
                        AND date BETWEEN '{year}-{month}-1' 
                        AND '{year}-{month}-{calendar.monthrange(year, month)[1]}'
                        """
        else:
            get_statistics_query = f"""
                        SELECT * FROM expenses
                        WHERE user_id='{self.id}'
                        AND date='{year}-{month}-{day}'
                        """
        with self.db.cursor() as cursor:
            cursor.execute(get_statistics_query)
            result = cursor.fetchall()
            for row in result:
                raw_date = str(row[5]).split('-')
                print(f"food={row[1]}, transport={row[2]}, "
                      f"taxes={row[3]}, clothes={row[4]}"
                      f" in {raw_date[2]} {calendar.month_name[int(raw_date[1])]} {raw_date[0]}")

    def delete_data_from_db(self):
        delete_data_query = f"""
        DELETE FROM expenses WHERE user_id='{self.id}'
        """
        with self.db.cursor() as cursor:
            cursor.execute(delete_data_query)
            cursor.fetchall()
            self.db.commit()
        print(f"Data for user with id: {self.id} was deleted!")

    def add_data(self, expense, amount, time):
        words = ['food', 'transport', 'taxes', 'clothes']
        if expense in (words or [expense.istitle() for expense in words]
                              or [expense.upper() for expense in words]):
            check_if_exists_query = f"""
            SELECT * FROM expenses 
            WHERE date='{time}' AND user_id={self.id}
            """
            with self.db.cursor() as cursor:
                cursor.execute(check_if_exists_query)
                result = cursor.fetchall()
                l = [row for row in result]
                if l:
                    update_expense_query = f"""
                    UPDATE expenses SET {expense}={amount} 
                    WHERE date='{time}' AND user_id={self.id}
                    """
                    cursor.execute(update_expense_query)
                    self.db.commit()
                else:
                    add_expense_query = f"""
                    INSERT INTO expenses (user_id,{expense},date)
                    VALUES ({self.id},'{amount}','{time}')
                    """
                    cursor.execute(add_expense_query)
                    self.db.commit()
        else:
            raise ValueError


def db_connection():
    try:
        connection = connect(
            user=input('Enter username: '),
            host="localhost",
            password=input("Enter password: "),
            database="expenses"
        )
        return connection
    except Error as e:
        print(e)


def main():
    connection = db_connection()
    user_id = -1
    choice = int(input("Add user to system - 1\nUse existed user - 2\n"))
    if choice == 1:
        first_name = input("Add user first name: ")
        last_name=input("Add user last name: ")
        add_user_query = f"""
        INSERT INTO users(first_name, last_name)
        VALUES('{first_name}','{last_name}')
        """
        show_user_id_query = f"""
        SELECT user_id FROM users
        WHERE first_name='{first_name}'
        """
        with connection.cursor() as cursor:
            cursor.execute(add_user_query)
            cursor.execute(show_user_id_query)
            result = cursor.fetchall()
            connection.commit()
            for row in result:
                user_id = int(row[0])
    elif choice == 2:
        show_users_query = """
        SELECT * FROM users
        """
        with connection.cursor() as cursor:
            cursor.execute(show_users_query)
            result = cursor.fetchall()
            for row in result:
                print(row)
            user_id = int(input("Choose user_id: "))
    else:
        print("Wrong input!")
        return -1
    user = Expenses(user_id, connection)
    while True:
        choice = int(input("What to do?\nLook up data - 1\nAdd expense - 2\n"
                           "Delete all data - 3\nGet statistics - 4\nExit - 0\n"))
        if choice == 1:
            extraction = input("What to look?\n"
                               "For example: \"food\"\nOr -1 if extract all\n")
            user.print_data(extraction)
        elif choice == 2:
            expense = input("Enter expense name: ")
            amount = int(input("Specify amount: "))
            time = datetime.strptime(input("Enter date:\nFor example \"Nov 19 2021\"\n"), '%b %d %Y')
            user.add_data(expense, amount, time)
        elif choice == 3:
            user.delete_data_from_db()
        elif choice == 4:
            year = int(input("Specify year: "))
            month = int(input("Specify month in number.\n"
                              "For example \"11\" equals to November"
                              " or-1 if no need\n"))
            if month == -1:
                day = -1
                user.get_statistics(year, month, day)
            else:
                day = int(input("Specify day: "))
                if day == -1:
                    user.get_statistics(year, month, day)
        elif choice == 0:
            break


if __name__ == '__main__':
    main()
