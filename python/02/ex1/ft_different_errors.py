def garden_operations() -> None:
    """Trigger and catch several garden-themed exception examples."""
    print("Testing ValueError...")
    try:
        int("")
    except ValueError as e:
        print("Caught ValueError:", e)
    print("")
    print("Testing ZeroDivisionError...")
    try:
        42 / 0
    except ZeroDivisionError as e:
        print("Caught ZeroDivisionError:", e)
    print("")
    print("Testing FileNotFoundError...")
    try:
        raise FileNotFoundError("No such file 'missing.txt'")
    except FileNotFoundError as e:
        print("Caught FileNotFoundError:", e)
    print("")
    print("Testing KeyError...")
    # Flake8 doesn't allow simple \
    wrong_key = "mising\\_plant"
    try:
        d: dict[str, str] = {}
        print(d[wrong_key])
    except KeyError as e:
        # printng e does not process "\\" as scaped sequence
        print(f"Caught KeyError: '{e.args[0]}'")


def test_error_types() -> None:
    """Run `garden_operations` and show recovery from grouped exceptions."""

    print("=== Garden Error Types Demo ===")
    print("")
    garden_operations()
    print("")
    print("Testing multiple errors together...")

    try:
        1 / 0
        int("abc")
    except (ValueError, ZeroDivisionError):
        print("Caught an error, but program continues!")
    print("")
    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
