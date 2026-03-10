import math

if __name__ == "__main__":

    print("=== Game Coordinate System ===")

    coord: tuple[int, int, int] = (10, 20, 5)
    orig: tuple[int, int, int] = (0, 0, 0)

    dist = math.sqrt((coord[0] - orig[0]) ** 2
                     + (coord[1] - orig[1]) ** 2
                     + (coord[2] - orig[2]) ** 2)

    print("")
    print(f"Position created: {coord}")
    print(f"Distance between {orig} and {coord}: {dist:.2f}")

    coord_str = "3,4,0"
    print("")
    print(f'Parsing coordinates: "{coord_str}"')

    coord_split = coord_str.split(",")
    try:
        coord = (int(coord_split[0]), int(coord_split[1]), int(coord_split[2]))

        dist = math.sqrt((coord[0] - orig[0]) ** 2
                         + (coord[1] - orig[1]) ** 2
                         + (coord[2] - orig[2]) ** 2)

        print(f"Parsed position: {coord}")
        print(f"Distance between {orig} and {coord}: {dist:.2f}")

    except ValueError as e:
        print(f"Error parsing coordinates: {e}")
        print(f"Error details - Type: {type(e).__name__}, Args: {e.args}")

    print("")
    print("Unpacking demonstration:")
    x, y, z = coord
    print(f"Player at x={x}, y={y}, z={z}")
    print(f"Coordinates: X={x}, Y={y}, Z={z}")

    invalid_string = "abc,def,ghi"
    print("")

    print(f'Parsing invalid coordinates: "{invalid_string}"')

    try:
        coord_str = invalid_string.split(",")
        coord = (int(coord_str[0]), int(coord_str[1]), int(coord_str[2]))

    except ValueError as e:
        print(f"Error parsing coordinates: {e}")
        print(f"Error details - Type: {type(e).__name__}, Args: {e.args}")
