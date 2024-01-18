import datetime
import locale
import calendar
from tests_connection import ma_connect
import unittest


class TestTest_temps(unittest.TestCase):
    #
    # def test_semaine(self):
    #     t = test_semaine('2024-08-02 12:00')
    #     x = datetime.datetime(2024,8,2,12,0)
    #     self.assertEqual(t.week, '31')
    #     self.assertEqual(t.auj, x)

    # def test_post_init(self):
    #     t = test_semaine('2024-08-02 12:00')
    #     self.assertNotEqual(t.conn, None)

    def test_etablir_conn(self):
        la_conn = ma_connect()
        self.assertNotEqual(la_conn.conn, None)


if __name__ == "__main__":
    unittest.main(verbosity=2)

