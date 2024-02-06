"""
Connecter avec la db et passer object connection.

"""

import mariadb
import sys

class MaConnect:
    conn = None

    def __init__(self):
        self.etablir_conn()

    def etablir_conn(self):

        """
        Connecter la db.

        :meta hide-value:

        :meta private:

        """

        # Connect to MariaDB Platform
        try:
            self.conn = mariadb.connect(
                user="jack",
                password="yoyo",
                host="localhost",
                port=3306,
                database="horaire"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

# Get Cursor
# mariadb pour cette version 1ere fois logger avec sudo + root sans pwd
#nouveau yoyo
