def main():
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===")
    print("Initializing new storage unit: new_discovery.txt")

    try:
        file = open("new_discovery.txt", "w")
    except Exception as e:
        print(f"Error creating file {e}")
        return

    print("Storage unit created successfully...")
    print("Inscribing preservation data...")

    try:
        file.write("{[}ENTRY 001{]} New quantum algorithm discovered\n")
        file.write("{[}ENTRY 002{]} Efficiency increased by 347%\n")
        file.write("{[}ENTRY 003{]} Archived by Data Archivist trainee\n")
        print("Data inscription complete. Storage unit sealed.")
        print("Archive 'new_discovery.txt' ready for long-term preservation.")

    except Exception as e:
        print(f"Error writing file:\n {e}\n")
    finally:
        file.close()


if __name__ == "__main__":
    main()
