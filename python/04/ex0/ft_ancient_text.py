def main():
    """Entry point"""
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===")
    print("Accessing Storage Vault: ancient_fragment.txt")

    try:
        file = open("ancient_fragment.txt", "r")
        print("Connection established...")
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")
        return

    content = file.read()
    print("RECOVERED DATA:")
    print(content)
    file.close()
    print("Data recovery complete. Storage unit disconnected.")


if __name__ == "__main__":
    main()
