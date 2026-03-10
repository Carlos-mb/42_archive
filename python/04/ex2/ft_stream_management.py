#!/usr/bin/env python3
import sys


def main():
    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===")
    print("")

    arch_id: str = input("Input Stream active. Enter archivist ID: ")
    status: str = input("Input Stream active. Enter status report: ")

    sys.stdout.write("{[}STANDARD{]} "
                     f"Archive status from {arch_id}: {status}\n")
    sys.stderr.write("{[}ALERT{]} System diagnostic: "
                     "Communication channels verified\n")
    sys.stdout.write("{[}STANDARD{]} Data transmission complete\n")
    print("")
    sys.stdout.write("Three-channel communication test successful.\n")


if __name__ == "__main__":
    main()
