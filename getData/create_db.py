import MySQLdb

class CreateDB:

    def create_db(self, db_name, db_password):
        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd=db_password)
        cur = db.cursor()

        cur.execute("CREATE DATABASE github")

        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd=db_password,
                             database=db_name)
        cur = db.cursor()

        cur.execute("CREATE TABLE repositories ("
                    "id INT UNSIGNED NOT NULL, "
                    "owner VARCHAR(250) NOT NULL,"
                    "name VARCHAR(250) NOT NULL, "
                    "stars INT UNSIGNED NOT NULL, "
                    "forks INT UNSIGNED NOT NULL,"
                    "contributors JSON,"
                    "PRIMARY KEY (id))")

        cur.execute("CREATE TABLE contributor ("
                    "id INT UNSIGNED NOT NULL,"
                    "login VARCHAR(250) NOT NULL, "
                    "contribution INT UNSIGNED NOT NULL, "
                    "location VARCHAR(250) NOT NULL,"
                    "company VARCHAR(250) NOT NULL,"
                    "PRIMARY KEY (id))")

