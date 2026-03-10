import sys


def main():
    arg_len: int = len(sys.argv)
    scores: list[int] = []
    i: int = 0
    int_arg: int = 0

    print("=== Player Score Analytics ===")

    if arg_len == 1:
        print("No scores provided. Usage: python3 "
              "ft_score_analytics.py <score1> <score2> ...")
    else:
        print("Scores processed: [", end="")
        i = 1
        for arg in sys.argv[1:]:
            try:
                int_arg = int(arg)
                scores.append(int_arg)
                print(arg, end="")
                if i < arg_len - 1:
                    print(", ", end="")
            except ValueError:
                print(f"\nOops! wrong param:'{arg}' not valid.")
                return
            i = i + 1
        print("]")
        print(f"Total players: {len(scores)}")
        print(f"Total score: {sum(scores)}")
        print(f"Average score: {sum(scores) / len(scores)}")
        print(f"High score: {max(scores)}")
        print(f"Low score: {min(scores)}")
        print(f"Score range: {max(scores) - min(scores)}")


if __name__ == "__main__":
    main()
