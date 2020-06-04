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
        help="Filename to write output number to",
    )
    return parser.parse_args()

def compute_average(numbers):
    """ Average input numbers
        Return: { 'average' : average }
    """
    print(f"Averaging numbers: {numbers}")
    avg = { 'average' : sum(numbers) / len(numbers) }
    print(json.dumps(avg))
    return avg

if __name__ == '__main__':
    args = parse_args()
    main(output_file=args.output_file, numbers=args.numbers)

    print(f"Writing output to {output_file}")
    with open(output_file, 'w') as fout:
        json.dump(avg, fout)

    print("Done")
