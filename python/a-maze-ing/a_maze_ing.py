from renderer import Renderer
import sys
from typing import cast

try:
    from mazegen.generator import MazeGenerator
except ImportError as e:
    print(f"Error importing MazeGenerator: {e}")
    sys.exit(1)


def read_config() -> dict[str, str | int | tuple[int, int]] | None:
    """Read and validate maze configuration from a file path in CLI args.

    The function expects exactly one CLI argument: the config file path.
    It parses `KEY=VALUE` pairs, applies defaults, converts values to typed
    fields, and validates coordinate bounds.

    Returns:
        dict[str, str | int | tuple[int, int]] | None:
            A normalized configuration dictionary if valid, otherwise `None`.
    """

    output: dict = {}

    mandatory = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    ]

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return None

    try:
        with open(sys.argv[1]) as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" not in line:
                        msg = (
                            f"Error: invalid config line {i}. "
                            "Expected KEY=VALUE"
                        )
                        raise ValueError(msg)
                    key, value = line.split("=", 1)
                    output[key.strip()] = value.strip()

        for item in mandatory:
            if "" == output.get(item, ""):
                raise ValueError(f"{item} required and"
                                 " not present in config file")

    except FileNotFoundError:
        print("ERROR: config file does not exist")
        return None
    except ValueError as e:
        print(e)
        return None
    except Exception:
        print("Undefined error. Usage: python3 a_maze_ing.py config.txt")
        return None

    try:
        output["WIDTH"] = int(output.get("WIDTH", "20"))
        output["HEIGHT"] = int(output.get("HEIGHT", "20"))
        if output["WIDTH"] < 2 or output["HEIGHT"] < 2:
            raise ValueError("Error: Width and Height must be >= 2")

        output["ENTRY"] = tuple(map(
                                int, output.get("ENTRY", "0,0").split(",")))
        if len(output["ENTRY"]) != 2:
            raise ValueError("Error: ENTRY must be int, int")

        if output["ENTRY"][0] < 0 or output["ENTRY"][1] < 0 or\
           output["ENTRY"][0] > output["HEIGHT"] - 1 or\
           output["ENTRY"][1] > output["WIDTH"] - 1:

            raise ValueError("Error: ENTRY must be inside maze limits")

        output["EXIT"] = tuple(map(int, output.get("EXIT", "0,0").split(",")))
        if len(output["EXIT"]) != 2:
            raise ValueError("Error: EXIT must be int, int")

        if output["EXIT"][0] < 0 or output["EXIT"][1] < 0 or\
           output["EXIT"][0] > output["HEIGHT"] - 1 or\
           output["EXIT"][1] > output["WIDTH"] - 1:

            raise ValueError("Error: EXIT must be inside maze limits")

        if output["ENTRY"][0] == output["EXIT"][0] and\
           output["ENTRY"][1] == output["EXIT"][1]:
            raise ValueError("Error: ENTRY and EXIT must be different points")

        # output["OUTPUT_FILE"] = output.get("OUTPUT_FILE", "maze.txt")

        output["PERFECT"] = output.get("PERFECT", "true").lower()
        if output["PERFECT"] not in ("true", "false"):
            raise ValueError("Error: PERFECT should be true | false")
        output["PERFECT"] = output["PERFECT"] == "true"

        output["SHOWDRAW"] = output.get("SHOWDRAW", "true").lower()
        if output["SHOWDRAW"] not in ("true", "false"):
            raise ValueError("Error: SHOWDRAW should be true | false")
        output["SHOWDRAW"] = output["SHOWDRAW"] == "true"

        output["SEED"] = int(output.get("SEED", "94"))

        output["GRAPHIC_MODE"] = output.get("GRAPHIC_MODE", "Mlx")

        if output["GRAPHIC_MODE"] not in ("ASCII", "Mlx"):
            raise ValueError("Error: GRAPHIC_MODE should be ASCII | Mlx")

        output["CAMERA_SPEED"] = int(output.get("CAMERA_SPEED", "32"
                                                ))
        if output["CAMERA_SPEED"] <= 0 or output["CAMERA_SPEED"] is None:
            raise ValueError("Error: CAMERA_SPEED must be > 0")
        output["CANVAS_WIDTH"] = int(output.get("CANVAS_WIDTH", "0"))
        if output["CANVAS_WIDTH"] < 160:
            raise ValueError("Error: CANVAS_WIDTH must be >= 160")
        output["CANVAS_HEIGHT"] = int(output.get("CANVAS_HEIGHT", "0"))
        if output["CANVAS_HEIGHT"] < 144:
            raise ValueError("Error: CANVAS_HEIGHT must be >= 144")

    except ValueError as e:
        print(e)
        return None

    return output


def export_file(maze: MazeGenerator, outputfile: str) -> None:
    """Export maze structure and solution to a file.

    Writes the maze matrix in hexadecimal format, along with entry/exit
    coordinates and the shortest path direction string.

    Args:
        maze (MazeGenerator): The generated and solved maze instance.
        outputfile (str): Path to the output file.
        If empty, no file is written.

    Returns:
        None

    Raises:
        IOError: If the file cannot be written.
        OSError: If there are OS-level file operation errors.

    Note:
        The output format consists of:
        - Hexadecimal maze grid (one row per line)
        - Empty line
        - Entry coordinates (col,row)
        - Exit coordinates (col,row)
        - Direction string (N/E/S/W sequence)
    """
    directions: str = maze.directions

    if not maze:
        return

    hex_matrix: list[str] = []

    for row in maze.matrix:
        hex_matrix.append("")
        for cell in row:
            hex_matrix[-1] += cell.to_hex()

    if outputfile != "":
        try:
            with open(outputfile, "w") as f:
                for row2 in hex_matrix:
                    f.write(row2 + "\n")
                f.write("\n")
                f.write(str(maze.entry[0]) + "," + str(maze.entry[1]) + "\n")
                f.write(str(maze.exit[0]) + "," + str(maze.exit[1]) + "\n")
                f.write(directions + "\n")
        except (IOError, OSError) as e:
            print(f"Error writing output file: {e}")
            raise


def main() -> None:
    """Run the maze application entry point.

    Orchestrates the complete maze generation workflow:
    1. Reads and validates configuration from CLI argument
    2. Initializes maze generator and renderer
    3. Generates the maze structure
    4. Solves for shortest path
    5. Exports results to file
    6. Renders visualization (ASCII or MLX)

    Returns:
        None

    Raises:
        KeyboardInterrupt: If user interrupts execution with Ctrl+C.
        ValueError: If configuration values are invalid.
        TypeError: If configuration types don't match expected types.
        IOError: If file operations fail.
        OSError: If OS-level errors occur.

    Note:
        Requires exactly one CLI argument: path to configuration file.
    """
    config: dict[str, str | int | tuple[int, int]] | None = read_config()
    if config is None:
        return

    try:
        mz: MazeGenerator = MazeGenerator(
            cols=cast(int, config["WIDTH"]),
            rows=cast(int, config["HEIGHT"]),
            seed=cast(int, config["SEED"]),
            perfect=cast(bool, config["PERFECT"]),
            entry=cast(tuple[int, int], config["ENTRY"]),
            exit=cast(tuple[int, int], config["EXIT"]))

        graphic_mode = cast(str, config["GRAPHIC_MODE"])
        is_ascii = graphic_mode == "ASCII"
        render: Renderer = Renderer(mz,
                                    ascii=is_ascii,
                                    showdraw=cast(bool, config["SHOWDRAW"]),
                                    win_w=cast(int, config["CANVAS_WIDTH"]),
                                    win_h=cast(int, config["CANVAS_HEIGHT"]),
                                    speed_cam=cast(int, config["CAMERA_SPEED"])
                                    )

        filename: str = cast(str, config["OUTPUT_FILE"])
        mz.generate()
        if len(mz.coords42) == 0:
            print("Not able to print 42 pattern")
        mz.solve()
        export_file(mz, filename)
        render.render()

    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    except (ValueError, TypeError) as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except (IOError, OSError) as e:
        print(f"File operation error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Runtime error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
