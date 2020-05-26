**Tutorial Difficulty: Beginner**

# Kubeflow Pipelines: Simple MapReduce Example

This minimal pipeline makes a Monte Carlo estimate for pi.

**What does it do?**

- Applies a map-reduce pattern by:
	1. (map) executing a very parallel first step
	2. (reduce) aggregating all results from (1) in a second step
- It passes all inputs and outputs as `json` strings.

## The map step(s)

The **sample** container is used by the map step.  It generates a uniform-random number in the square $[-1,1]^2$, and then returns:
* `1` if $x^2 + y^2 \leq 1$
* `0` otherwise

The **sample** step has a $\pi \over 4$ chance of falling in the circle

## The reduce step

The reduce step uses the **average** image to compute 4x the average of the results from the **sample** steps.  

# How to run it

Check out Compute-Pi.ipynb!

# How do I make my own Map Reduce Pipeline?

Create your own *map* and *reduce* docker images, and then define the input
parameters for your map images by changing the `seed` function!
