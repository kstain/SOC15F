# SOC LAB12
Name: Weiyi Wang

Andrew ID: weiyiw

## Description
This lab is for Genetic Algorithm for workflow service selection.

**Extra point** User defined service and workflow dependencies is implemented.

It is written in python and uses [Deap](https://pypi.python.org/pypi/deap) package.

## How to run
### Environment
1. Install deap package using:
> pip install deap
2. Test the install by
> import deap

### Configuration
The config for the project includes the service generator config and the workflow file.

#### Random Service generator
The service generator configuration is a yaml file which includes the service class name
and the number of corresponding services. The example file is in data/service_list.yaml

    ---
    services:
      - name: s1
        count: 5
      - name: s2
        count: 3
      - name: s3
        count: 6
      - name: s4
        count: 4
      - name: s5
        count: 7
      - name: s6
        count: 2
      - name: s7
        count: 1

To generate the services, we need to run the following script:

    python service_util.py

It will read from data/service_list.yaml and output the services to data/service directory.
Each service class will be a distinct file including the concrete service instances in it.
For example in data/serive/s1 file:

    s1_1	133	12	19	53
    s1_2	54	80	3	94
    s1_3	192	78	2	30
    s1_4	120	96	2	17
    s1_5	174	76	7	30

The four numbers after it is the attributes of that service. The values are generated randomly.

#### Workflow graph input
The workflow is in format of yaml too. The graph is described as a dependency list, some what like
an edge table. For example, the workflow given in the example of the lab assignment is described in
data/workflow/w2.yaml

    ---
    source: s1
    sink: s3
    dependencies:
      - name: s2
        dependency:
          - s1
      - name: s3
        dependency:
          - s2
    weight:
      cost: 0.35
      reliability: 0.15
      performance: 0.3
      availability: 0.2

The graph is composed of source service, sink service as the begin and end of the workflow, and the dependencies
 of the graph. Every dependency is composed of the child name and the corresponding parents list. In this
 example, s2 is dependant on s1 and s3 on s1.

In data/workflow/w1.yaml we can see a more complex graph:

    ---
    source: s1
    sink:   s7
    dependencies:
      - name: s2
        dependency:
          - s1
      - name: s3
        dependency:
          - s1
      - name: s4
        dependency:
          - s2
          - s3
      - name: s5
        dependency:
          - s3
      - name: s6
        dependency:
          - s4
      - name: s7
        dependency:
          - s5
          - s6
    weight:
      cost: 0.5
      reliability: 0.15
      performance: 0.15
      availability: 0.2

In this graph, the relationship is like the following:

    s1 -- s2 ---+- s4 -- s6 - s7
     \         /             /
      +-- s3 -+-- s5 ------+

#### Run the program
When the services are generated and the workflow is defined, we can execute the following
script to get the result of the GA algorithm.

    python ga.py -w PATH_TO_WORKFLOW [-s PATH_TO_SERVICE_DIR]

The -w argument is the path to workflow file and the -s is the optional argument
which indicate the service directory.

## Misc
The screenshots are in ./screenshot directory. There are the configuration of the example and the
result of it. In the example, I used the w1 workflow and the services existed in the data/service dir.
