def read_file(filepath):
    with open(filepath) as file:
        return [line.strip() for line in file.readlines()]
