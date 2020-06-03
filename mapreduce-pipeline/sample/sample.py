import argparse
import math
import random
from pathlib import Path


def main(output_path, seed):
    x, y = choose_coordinate(seed)

    if is_inside_unit_circle(x, y):
        print(f"Random point is inside the unit circle")
        result = 4
    else:
        print(f"Random point is outside the unit circle")
        result = 0

    write_output(output_path, x, y, seed, result)


def choose_coordinate(seed):
    """
    Returns an (x, y) coordinate in a [-1, 1] square
    """
    print(f"Choosing a coordinate in the square [-1, 1] in (x, y) using seed {seed}")
    random.seed(seed)
    x = pick_random_point()
    y = pick_random_point()
    print(f"Chose random point ({x}, {y})")
    return x, y


def pick_random_point():
    """
    Returns a random point between -1 and 1
    """
    return random.random() * 2 - 1


def is_inside_unit_circle(x, y):
    """
    Returns a boolean indicating whether the (x, y) coordinate is within the unit circle
    """
    return math.sqrt(x ** 2 + y ** 2) <= 1


def write_output(output_path, x, y, seed, result):
    """
    Writes the program outputs:
        output_result.txt: Result value of this test (0 if outside circle, 4 if inside)
        output_coordinate.txt: Coordinate chosen for test
        input_seed.txt: Seed used for test
    """
    output_path = Path(output_path)
    result_file = output_path / "output_result.txt"
    coordinate_file = output_path / "output_coordinate.txt"
    seed_file = output_path / "input_seed.txt"

    print(f"Writing results to {result_file}, {coordinate_file}, and {seed_file}")

    with result_file.open('w') as fout:
        fout.write(str(result))

    with coordinate_file.open('w') as fout:
        fout.write(f"({x}, {y})")

    with seed_file.open('w') as fout:
        fout.write(str(seed))


def parse_args():
    parser = argparse.ArgumentParser(description="Randomly chooses a coordinate in the [-1, 1] square and returns 4 if "
                                                 "the coordinate is inside the unit circle, else returns 0.  Results "
                                                 "are written to output_result.txt, with the chosen coordinate written "
                                                 "to output_coordinate.txt and the random seed used to input_seed.txt")
    parser.add_argument(
        "seed",
        type=float,
        help="Seed used for generating the random coordinate",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="./",
        help="Location to write output_result.txt, input_seed.txt, and output_coordinate.txt outputs",
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(output_path=args.output_path, seed=args.seed)
    print("Done")