# Project 1 - Sequence allignment

The goal of this project is to use [Needleman–Wunsch's algorithm](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm) to solve sequence allignment problem.

Program takes as input 2 sequences, scoring config and outputs best allignments. One allignment consists of 2 sequences of same length built from input sequences. The score of allignment is scored based on operations needed to transform input.

# Config

```json
{
    "same": 5,
    "diff": -5,
    "gap": -5,
    "max_number_of_paths": 0,
    "max_sequence_length": 20
}
```

* `same` - how many score points should be added if corresponding elements are the same.
* `diff` - how many score points should be added if corresponding elements differs.
* `gap` - how many score points should be added if one of corresponding element is empty.
* `max_number_of_paths` - how many allignments should be outputed. 0 means all allignmens.
* `max_sequence_length` - how long input sequence can be

# Application

Program is a console application and takes following arguments:

```console
usage: bio.py [-h] [--input1 INPUT1] [--input2 INPUT2] [--config CONFIG] [--output OUTPUT]
              [--logging {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

optional arguments:
  -h, --help            show this help message and exit
  --input1 INPUT1       Path to the file where first sequence is stored
  --input2 INPUT2       Path to the file where second sequence is stored
  --config CONFIG       Path to the config file. Format must be json.
  --output OUTPUT       Path to the output file. Format will be json.
  --logging {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level
```

# Sample usage

Input:
```bash
python bio.py  --loggin INFO --input1 ../data/in1.txt --input2 ../data/in2.txt --output ../output/output.json
```

Output:
```bash
INFO:root:User args: Namespace(config='../configs/config.json', input1='../data/in1.txt', input2='../data/in2.txt', logging='INFO', output='../output/output.json')
INFO:root:Config is:
{'diff': -5,
 'gap': -5,
 'max_number_of_paths': 0,
 'max_sequence_length': 20,
 'same': 5}
INFO:root:Solving score matrix for:
INFO:root:Sequence 1: MARS
INFO:root:Sequence 2: SMART
INFO:root:Alignments score: 0.0
INFO:root:[A0000] -MAR-S
INFO:root:[A0000] SMART-
INFO:root:[A0001] -MARS-
INFO:root:[A0001] SMAR-T
INFO:root:Saved output to ../output/output.json
```

User can display more details using `--logging DEBUG`.

```bash
INFO:root:User args: Namespace(config='../configs/config.json', input1='../data/in1.txt', input2='../data/in2.txt', logging='DEBUG', output='../output/output.json')
INFO:root:Config is:
{'diff': -5,
 'gap': -5,
 'max_number_of_paths': 0,
 'max_sequence_length': 20,
 'same': 5}
INFO:root:Solving score matrix for:
INFO:root:Sequence 1: MARS
INFO:root:Sequence 2: SMART
DEBUG:root:Score matrix:
array([[  0.,  -5., -10., -15., -20., -25.],
       [ -5.,  -5.,   0.,  -5.,  -5.,  -5.],
       [-10.,  -5.,  -5.,   5.,   0.,  -5.],
       [-15.,  -5.,  -5.,   0.,  10.,   5.],
       [-20., -10.,  -5.,  -5.,   5.,   0.]])
DEBUG:root:Nodes mapping: (target_node): [(parent_node),...]
{(0, 1): [(0, 0)],
 (0, 2): [(0, 1)],
 (0, 3): [(0, 2)],
 (0, 4): [(0, 3)],
 (0, 5): [(0, 4)],
 (1, 0): [(0, 0)],
 (1, 1): [(0, 0)],
 (1, 2): [(0, 1)],
 (1, 3): [(0, 2), (1, 2)],
 (1, 4): [(0, 3)],
 (1, 5): [(0, 4)],
 (2, 0): [(1, 0)],
 (2, 1): [(1, 0)],
 (2, 2): [(1, 1), (1, 2)],
 (2, 3): [(1, 2)],
 (2, 4): [(2, 3)],
 (2, 5): [(1, 4), (2, 4)],
 (3, 0): [(2, 0)],
 (3, 1): [(2, 0)],
 (3, 2): [(2, 1)],
 (3, 3): [(2, 3)],
 (3, 4): [(2, 3)],
 (3, 5): [(3, 4)],
 (4, 0): [(3, 0)],
 (4, 1): [(3, 0), (3, 1)],
 (4, 2): [(3, 1)],
 (4, 3): [(3, 2), (3, 3)],
 (4, 4): [(3, 4)],
 (4, 5): [(3, 5), (4, 4)]}
INFO:root:Alignments score: 0.0
DEBUG:root:Resolving alignment for path [(4, 5), (3, 5), (3, 4), (2, 3), (1, 2), (0, 1), (0, 0)]
DEBUG:root:Moving up and appending S and -
DEBUG:root:Moving left and appending - and T
DEBUG:root:Moving left and up and appending R and R
DEBUG:root:Moving left and up and appending A and A
DEBUG:root:Moving left and up and appending M and M
DEBUG:root:Moving left and appending - and S
DEBUG:root:Resolving alignment for path [(4, 5), (4, 4), (3, 4), (2, 3), (1, 2), (0, 1), (0, 0)]
DEBUG:root:Moving left and appending - and T
DEBUG:root:Moving up and appending S and -
DEBUG:root:Moving left and up and appending R and R
DEBUG:root:Moving left and up and appending A and A
DEBUG:root:Moving left and up and appending M and M
DEBUG:root:Moving left and appending - and S
INFO:root:[A0000] -MAR-S
INFO:root:[A0000] SMART-
INFO:root:[A0001] -MARS-
INFO:root:[A0001] SMAR-T
INFO:root:Saved output to ../output/output.json
```
