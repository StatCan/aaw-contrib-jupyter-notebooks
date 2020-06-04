import argparse
import json
import pylab as plt

def parse_args():
    parser = argparse.ArgumentParser(description="Takes experiment results and combines them in a plot")
    parser.add_argument(
        "json",
        type=str,
        nargs="+",
        help="One or more json experiments",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="out.png",
        help="Filename to write output number to",
    )
    return parser.parse_args()

def generate_plot(output_file, experiments):
    """ 
    Plot the experiment results on a the 2 by 2 square
    containing the unit circle. Show how many points fell
    inside v.s. outside of the circle.
    """

    # Split the results into inside v.s. outside
    within  = [ e for e in experiments if e['x']**2 + e['y']**2 <= 1  ]
    outside = [ e for e in experiments if e['x']**2 + e['y']**2  > 1  ]
    

    # clear things for fresh plot
    ax = plt.gca()
    ax.cla() 
    
    # Set plot bounds
    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))
    
    # plots: inside and outside the circle
    plt.scatter(
        [ e['x'] for e in within ],
        [ e['y'] for e in within ],
        c="red"
    )

    plt.scatter(
        [ e['x'] for e in outside ],
        [ e['y'] for e in outside ],
        c="blue"
    )

    # bounding circle
    c = plt.Circle( (0,0), 1, color='black', fill=False)
    ax.add_artist(c)
    
    # write to disk
    plt.savefig(output_file)


if __name__ == '__main__':
    args = parse_args()
    generate_plot(
        output_file=args.output_file, 
        experiments=[ json.loads(s) for s in args.json ]
    )

    # Kubeflow doesn't render the .png file nicely in the browser
    # So need this to turn it into an ascii html page.
    import base64
    encoded = base64.b64encode(open(args.output_file, "rb").read()).decode('ascii')
    with open("out.html", "w") as f:
        f.write(f'<img src="data:image/png;base64,{encoded}" />')

    print("Done")
