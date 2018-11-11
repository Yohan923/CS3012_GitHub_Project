import ast


def main():
    info = dict()
    with open('info.txt', 'r') as f:
        info = ast.literal_eval(f.read())


if __name__ == '__main__':
    main()
