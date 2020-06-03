import argparse
import random
import json
from pathlib import Path

def simulation(seed):
    """ Generate a random (x,y) coordinate in [-1,1] × [-1,1]

        Return 4 (area of [-1,1] × [-1,1]) if within the unit circle
        Return 0 Otherwise

        Write results to file at the end.
    """

    print(f"Choosing a coordinate in the square [-1, 1] in (x, y) using seed {seed}")
    random.seed(seed)

    # x,y ~ Uniform([-1,1])
    x = random.random() * 2 - 1
    y = random.random() * 2 - 1
    print(f"Sample selected: ({x}, {y})")

    if (x ** 2 + y ** 2) <= 1:
        print(f"Random point is inside the unit circle")
        result = 4
    else:
        print(f"Random point is outside the unit circle")
        result = 0

    return { 
        'seed' : seed, 
        'x' : x, 
        'y' : y, 
        'result' : result
    }


def write_output(output_path, x=0, y=0, seed=0, result=0):
    """
    Writes the program outputs:
        output_file.json: json for { x,y, result, seed }
    """
    output_path = Path(output_path)

    output = { 
        'seed' : seed, 
        'x' : x, 
        'y' : y, 
        'result' : result
    }

    output_file = output_path / "output.json"

    print(f"Writing results to {output_file}")
    with output_file.open('w') as fout:
        json.dump(output, fout)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Randomly chooses a coordinate in the [-1, 1] square and returns 4 if "
                    "the coordinate is inside the unit circle, else returns 0.  Results "
                    "are written to output_file.json"
    )

    parser.add_argument(
        "seed",
        type=float,
        help="Seed used for generating the random coordinate",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="./",
        help="Location to write output_file.json outputs",
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    experiment = simulation(args.seed) 
    write_output(args.output_path, **experiment)
    print("Done")
