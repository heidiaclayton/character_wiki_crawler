import re


def print_dot(count, mod):
    if count % mod == 0:
        print(".")
    else:
        print(".", end="")


def get_number(string):
    match = re.search("\d+", string)

    return int(match.group()) if match is not None else 0
