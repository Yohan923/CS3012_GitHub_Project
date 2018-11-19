from DataParser.data_parser import DataParser


def main(db_name, db_password):
    DataParser().parse(db_name, db_password)


if __name__ == '__main__':
    import sys
    args = sys.argv
    main(args[1], args[2])
