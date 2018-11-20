from populate_db import PopulateDB
from create_db import CreateDB


def main(db_name, auth, db_password):

    # CreateDB().create_db(db_name, db_password)

    PopulateDB().populate(db_name, auth, db_password)


if __name__ == '__main__':
    import sys

    args = sys.argv
    main(args[1], args[2], args[3])
