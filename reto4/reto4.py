# Globals:
INPUT_FILE = "input.txt"


# Functions:
def main():
    with open(INPUT_FILE) as f:
        for line in f:
            pre, post = None, None
            line = line.strip()
            if "=" in line:
                pre, post = line.split("=")
            else:
                pre = line

            print(pre, post)

# Classes:
class Asgardian(object):

    def __init__(self):
        self.father = None
        self.mother = None
        self.has_power = None

    def give_power(self):
        self.has_power = True


# Main:
if __name__ == "__main__":
    main()
