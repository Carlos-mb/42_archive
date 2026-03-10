import sys
import os
from importlib import import_module


def c_import_mod(module: str,
                 description: str,
                 expected_version: str) -> bool:

    ok: bool = True

    try:
        imported = import_module(module)
        version = getattr(imported, "__version__", "unknown")
        print(f"[OK] {module} ({version}) - {description} Ready")
        print(f"- Installed: {version} | Expected: {expected_version}")
    except ModuleNotFoundError:
        print(f"[MISSING] {module} - Install required")
        ok = False

    return ok


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:\n")

    # Change versions to force error and show comparison
    modules = {"pandas": ("Data manipulation", "2.0"),
               "requests": ("Network access", "2.31"),
               "matplotlib": ("Visualization", "3.7")}

    ok: bool = True
    for module, (description, expected_version) in modules.items():
        ok = c_import_mod(module, description, expected_version) and ok

    if not ok:
        print("\nInstall with pip:")
        print(" pip install -r requirements.txt")
        print("     - python3 -m venv yourenvname")
        print("     - source matrix_env/bin/activate")
        print("")
        print("\nOr with Poetry:")
        print(" poetry install")
        print("     - poetry run python loading.py")
        print("")

        return

    import pandas
    import numpy
    from matplotlib import pyplot

    print("Analyzing Matrix data...\n")

    x = numpy.arange(0, 50)
    y = x ** 2
    df = pandas.DataFrame({
        "cycle": x,
        "energy": y
    })

    print(f"Processing {len(df)} data points...")

    # Visualization
    pyplot.plot(df["cycle"], df["energy"])
    pyplot.title("Matrix Energy Growth")
    pyplot.xlabel("Cycle")
    pyplot.ylabel("Energy Level")

    output_file = "matrix_analysis.png"
    pyplot.savefig(output_file)

    print(f"Results saved to: {output_file}")

    # Detect if running inside a Poetry-managed virtual environment
    # If manage the name have the poetry text, but user can create
    # an standar env called "poetry" :)
    # Otherway is to check a Vairable, but it can be set manually
    print("")
    if (("poetry" in sys.executable.lower()
            or "pypoetry" in sys.prefix.lower())
            and os.getenv("POETRY_ACTIVE") == "1"):
        print("Environment detected: Poetry-managed virtual environment\n")
    else:
        print("Environment detected: pip/system Python environment\n")


if __name__ == "__main__":
    main()
