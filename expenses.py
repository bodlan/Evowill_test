# Задание можно выполнить на любом языке программирования, используя любую базу данных.
# Ваша цель - показать best practices в выбранных технологиях.
#
# Создайте консольное приложение для контроля расходов.
# В приложении должен быть следующий функционал:
# Возможность записывать расходы по категориям. Например: Еда - 250.
# Получать статистику расходов - по всем категориям сразу или по одной из них.
# Возможность очистить все данные.
# Посмотреть статистику расходов: за день, за месяц, за год
# Внести расходы за какой-то конкретный день. Например 12.12.2012 Еда - 250
# Добавить возможность иметь нескольких пользователей
# Написать юнит тесты для приложения
#
# Для того, чтобы тестовое считалось готовым, должны работать все основные функции.
# Должен быть репозиторий на GitHub/GitLab/Bitbucket и написан Readme файл с пошаговой инструкцией
# для запуска и использования программы. Можно приложить скрины, показывающие, как она работает.
from datetime import datetime
from mysql.connector import connect, Error
from getpass import getpass
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
            user="root",
            host="localhost",
            password="bodlan123987",
            database="expenses"
        )
        # user=input('Enter username: ')
        # password=getpass("Enter password: ")
        return connection
    except Error as e:
        print(e)


def main():
    connection = db_connection()
    user_id = -1
    choise = int(input("Add user to system - 1\nUse existed user - 2\n"))
    if choise == 1:
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
    elif choise == 2:
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
        choise = int(input("What to do?\nLook up data - 1\nAdd expense - 2\n"
                           "Delete all data - 3\nGet statistics - 4\nExit - 0\n"))
        if choise == 1:
            extraction = input("What to extract?\n"
                               "For example: \"food\"\nOr -1 if extract all\n")
            user.print_data(extraction)
        elif choise == 2:
            expense = input("Enter expense name: ")
            amount = int(input("Specify amount: "))
            time = datetime.strptime(input("Enter date:\nFor example \"Nov 19 2021\"\n"), '%b %d %Y')
            user.add_data(expense, amount, time)
        elif choise == 3:
            user.delete_data_from_db()
        elif choise == 4:
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
        elif choise == 0:
            break


if __name__ == '__main__':
    main()
