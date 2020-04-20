# Kubeflow Pipelines: Simple MapReduce Example

This minimal pipeline makes a Monte Carlo estimate for pi.

**What does it do?**

- Executes a very parallel map step
- One aggregate step
- It passes all inputs and outputs as `json`.
- Stores all the output data in `minio` storage.

## The map step

This pipeline has two images, the **map** image, which generates one guess; it
generates a uniform-random number in the square $[-1,1]^2$, and then it guesses
`4` if $x^2 + y^2 \leq 1$, and $0$ otherwise. (One can see that there is a $\pi
\over 4$ chance of falling in the circle, so this gives an estimate for pi.)

## The reduce step

The reduce step simply averages the guesses over all the samples.

# How to run it

Simply set `export MINIO_SECRET=XXXXXX` in your Jupyter notebook (in Kubeflow)
and then run the script `compute-pi.py`. Check Kubeflow to see the progress!

# How do I make my own Map Reduce Pipeline?

Create your own *map* and *reduce* docker images, and then define the input
parameters for your map images by changing the `seed` function!
