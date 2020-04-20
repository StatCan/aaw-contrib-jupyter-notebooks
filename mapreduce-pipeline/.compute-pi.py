#!/bin/python3

# Pipeline to estimate pi, in the most rediculously parallel way possible.
#
# Implemented as a map-reduce. Input to the map operation
# is a mandatory seed integer --- otherwise each container
# will product the same number.
#
# The map operation picks a random point in a square,
# then returns 1 if it is in the circle.
#
# After the map operation, the estimates are averaged.

import json
import re
nicename = re.compile('^[0-9a-zA-Z_-]+$')
bucketname = re.compile('^[0-9a-z_-]+$')

SAMPLES = 300

EXPERIMENT_NAME = "compute-pi"
assert nicename.match(EXPERIMENT_NAME)


OUTPUT_BUCKET = 'pi-digitsanalysis'
assert bucketname.match(OUTPUT_BUCKET)

SAMPLE_IMAGE_NAME = "blair-kf-pipeline-pi-sample"
SAMPLE_PIPELINE_NAME = "one-pi-estimate"
assert nicename.match(SAMPLE_PIPELINE_NAME)


AVERAGE_IMAGE_NAME = "blair-kf-pipeline-pi-average"
AVERAGE_PIPELINE_NAME = "aggregate-pi-estimate"
assert nicename.match(AVERAGE_PIPELINE_NAME)



def seeds(how_many=SAMPLES):
    """ Define the seeds for the algorithms """
    for i in range(how_many):
        yield { "seed" : 3 * i }


###################################
### DON'T EDIT:                 ###
### Create the Experiment       ###
###################################
import kfp
client = kfp.Client()
exp = client.create_experiment(name=EXPERIMENT_NAME)


###################################
### DON'T EDIT:                 ###
### Register our storage output ###
###################################
import defaults
defaults.make_bucket(OUTPUT_BUCKET)

###################################
### You can change below this   ###
### Create the pipeline         ###
###################################
from kfp import dsl

def sample_op(params, output):
    return dsl.ContainerOp(
        name=SAMPLE_PIPELINE_NAME,
        image=f'k8scc01covidacr.azurecr.io/{SAMPLE_IMAGE_NAME}',
        arguments=[
            '--params', params,
            '--output', output,
        ],
        file_outputs={
            'data': '/output/out.json'
        }
    ).set_memory_request(
        "100M"
    ).set_memory_limit(
        "150M"
    ).set_cpu_request(
        "0.1"
    ).set_cpu_limit(
        "1"
    )


def average_op(l, output):
    return dsl.ContainerOp(
        name=AVERAGE_PIPELINE_NAME,
        image=f'k8scc01covidacr.azurecr.io/{AVERAGE_IMAGE_NAME}',
        arguments=[
            '--output',
            output,
            '--numbers',
            *l
        ],
        file_outputs={
            'data': '/output/pi.json'
        }
    )


@dsl.pipeline(
    name="Fatality of Infected Ratio Analysis",
    description='Test sesitivity to the wIFR'
)
def compute_pi(output):
    """ Compute Pi """

    results = [
        sample_op(json.dumps(param), f'{output}/samples/{i}')
        for (i, param) in enumerate(seeds())
    ]

    average = average_op([r.output for r in results], f"{output}/estimate/pi")

    # Do you need this?
    defaults.inject_env_vars()



from kfp import compiler
compiler.Compiler().compile(
    compute_pi,
    EXPERIMENT_NAME + '.zip'
)


###################################
### DON'T EDIT:                 ###
### Ship the pipeline to run    ###
###################################

import datetime
import time

run = client.run_pipeline(
    exp.id,
    EXPERIMENT_NAME + '-' + time.strftime("%Y%m%d-%H%M%S"),
    EXPERIMENT_NAME + '.zip',
    params={
        'output': OUTPUT_BUCKET
    }
)
