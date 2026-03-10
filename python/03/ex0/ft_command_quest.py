import sys


if __name__ == "__main__":
    """Entry point for Command Quest.

    Processes command line arguments and displays information about them.
    Prints the program name, number of arguments received, and details
    of each argument.
    """
    arg_len: int = len(sys.argv)
    print("=== Command Quest ===")

    if arg_len == 1:
        print("No arguments provided!")

    print("Program name: " + sys.argv[0])

    if arg_len > 1:
        print(f"Arguments received: {arg_len - 1}")
        i: int = 0
        for arg in sys.argv:
            if i > 0:
                print(f"Argument {i}: {arg}")
            i += 1

    print(f"Total arguments: {arg_len}")
