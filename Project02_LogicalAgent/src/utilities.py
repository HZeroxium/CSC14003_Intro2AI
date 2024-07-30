# utilities.py


def read_map_file(filename):
    with open(filename, "r") as file:
        data = file.readlines()
    return data


def log_action(action):
    print(f"Action: {action}")
