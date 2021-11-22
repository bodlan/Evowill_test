import io
import unittest
import unittest.mock

from .expenses import *


class TestExpenses(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, func, expense, expected_output, mock_stdout):
        func(expense)
        self.assertIn(expected_output, mock_stdout.getvalue())

    def setUp(self) -> None:
        self.user_1 = Expenses(1, db_connection())
        self.user_2 = Expenses(2, db_connection())

    def tearDown(self) -> None:
        print("tearDown\n")

    def test_print_data(self):
        self.assertRaises(ValueError, self.user_1.print_data, 1)
        self.assertRaises(ValueError, self.user_1.print_data, 'F')
        self.assertRaises(ValueError, self.user_1.print_data, 'Foood')
        self.assertRaises(ValueError, self.user_1.add_data, 1, '250', '2021-11-04')
        self.assertRaises(ValueError, self.user_1.add_data, 'foo', '250', '2021-11-04')

    def test_data_add(self):
        self.assert_stdout(self.user_1.print_data, 'food', '20 November 2021')
        self.assert_stdout(self.user_1.print_data, 'clothes', '19 November 2021')
        self.assert_stdout(self.user_1.print_data, '-1', '20 November 2021')
        get_all_query = f"""
        SELECT * FROM expenses
        WHERE user_id={self.user_1.id}
        """
        with self.user_1.db.cursor() as cursor:
            cursor.execute(get_all_query)
            result1 = cursor.fetchall()
            print("result1=", result1)
            self.user_1.add_data('taxes', 189, '2021-10-04')
            cursor.execute(get_all_query)
            result2 = cursor.fetchall()
            print("result2=", result2)
            self.assertNotEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()
