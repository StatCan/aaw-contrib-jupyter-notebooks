import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(description="Returns the average of one or more numbers as a JSON file")
    parser.add_argument(
        "jsons",
        type=str,
        nargs="+",
        help="One or more json inputs with a 'result' field",
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
    avg = compute_average(
        numbers=[json.loads(s)['result'] for s in args.jsons]
    )

    print(f"Writing output to {args.output_file}")
    with open(args.output_file, 'w') as fout:
        json.dump(avg, fout)

    print("Done")
