def main():
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===")
    print("")
    print("Initiating secure vault access...")
    with open("classified_data.txt", "r") as file:
        print("Vault connection established with failsafe protocols")
        print("")
        print("SECURE EXTRACTION:")
        content = file.read()
        print(content)

    # There is no information in subject, so I open to add in order to
    # check that it's working
    with open("security_protocols.txt", "a") as file:
        print("")
        print("SECURE PRESERVATION:")
        print("[CLASSIFIED] New security protocols archived")
        file.write("\n[CLASSIFIED] New security protocols archived")
        print("Vault automatically sealed upon completion")

    print("final security confirmation")


if __name__ == "__main__":
    main()
