def read_file(file_name: str) -> None:
    try:
        with open(file_name) as fd:
            output = fd.read()
            print(f'SUCCESS: Archive recovered - "{output}"')
            print("STATUS: Normal operations resumed")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable")
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintained")


def main():
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===")
    print("")
    print("CRISIS ALERT: Attempting access to 'lost_archive.txt'...")
    read_file("lost_archive.txt")
    print("")
    print("CRISIS ALERT: Attempting access to 'classified_data.txt'...")
    # use chmod -r to generate error
    read_file("classified_data.txt")
    print("")
    print("ROUTINE ACCESS: Attempting access to 'standard_archive.txt'...")
    read_file("standard_archive.txt")
    print("")
    print("All crisis scenarios handled successfully. Archives secure.    ")


if __name__ == "__main__":
    main()
