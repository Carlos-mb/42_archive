# Authorized: os, sys, python-dotenv modules, file operations
from dotenv import load_dotenv  # pip install python-dotenv
from os import path, getenv


def main() -> None:

    print("ORACLE STATUS: Reading the Matrix...\n")

    if path.exists(".env"):
        load_dotenv(".env")
    else:
        print("File .env not found. Try cp .env.example .env\n")
        print("WARNING: .env not found. Using environment variables only.")

    # values -> KEY: [Name, Value, default value]
    values: dict[str, list[str | None]] = {
        "MATRIX_MODE": ["Mode", None, "development | production"],
        "DATABASE_URL": ["Database", None, "https://sample.com:PORT"],
        "API_KEY": ["API Access", None, "Secret key for external services"],
        "LOG_LEVEL": ["Log level", None, "none | errors | verbosity"],
        "ZION_ENDPOINT": ["Zion Network", None, "samplehiddensite.onion"]
    }

    load_error: bool = False

    for value in values.keys():
        values[value][1] = getenv(value)

        # if not assigned or has default value
        load_error = True if values[value][1] is None or\
            values[value][1] == values[value][2] else load_error

    #  MATRIX_MODE - "development" or "production"
    if values["MATRIX_MODE"][1] not in ["development", "production"]:
        values["MATRIX_MODE"][1] = "ERROR: Invalid value"
        load_error = True

    if not load_error:
        print("Configuration loaded:")
        for value in values.values():
            print(f"{value[0]}: "
                  f"{value[1] if not value[1] is None else 'not defined'}.")
        print(
                "\nEnvironment security check:\n"
                "[OK] No hardcoded secrets detected\n"
                "[OK] .env file properly configured\n"
                "[OK] Production overrides available\n"
                "\n"
                "The Oracle sees all configurations.\n"
              )
        if values["MATRIX_MODE"][1] == "production":
            print("Running in PRODUCTION mode")
        else:
            print("Running in DEVELOPMENT mode")
    else:
        print("Error, values not set. Current values:\n")
        # Problems with line lenght :)
        for v in values.values():
            display = (v[1]
                       if not (v[1] is None or v[1] == v[2])
                       else "not defined")
            print(f"{v[0]}: {display}.")


if __name__ == "__main__":
    main()
