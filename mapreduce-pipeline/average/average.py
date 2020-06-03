import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser(description="Returns the average of one or more numbers as a JSON file")
    parser.add_argument(
    "numbers",
    type=float,
    nargs="+",
    help="One or more numbers",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="out.json",
        help="Filename to write JSON results to",
    )
    # parser.add_argument(
    #     "--number_key",
    #     type=str,
    #     default="result",
    #     help="Key in numbers JSON strings to pull the numbers from for averaging.  Default is 'result'"
    # )
    return parser.parse_args()


def main(output_file, numbers):
    avg = sum(numbers) / len(numbers)

    with open(output_file, 'w') as fout:
        json.dump()



if __name__ == '__main__':
    args = parse_args()
    main(output_file=args.output_file, numbers=args.numbers)

