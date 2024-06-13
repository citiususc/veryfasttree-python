# VeryFastTree Python Bindings

The VeryFastTree Python Bindings provide an interface to the VeryFastTree software for rapid construction of phylogenetic trees. This package allows you to easily integrate VeryFastTree into your Python workflows, enabling efficient handling of large datasets and quick tree generation.


### Installation

To install the VeryFastTree Python Bindings, you can use pip:

```bash
pip install veryfasttree
```

**\*The Linux version requires the OpenMP library (libgomp) to be installed on the system.**

### Usage

Here is a basic example of how to use the VeryFastTree Python Bindings:

```python
import veryfasttree

# Define input file
input_alignment = 'path/to/your/alignment.fasta'

# Run VeryFastTree
tree = veryfasttree.run(input_alignment, gtr=True, nt=True)

print(tree)
```

The input to the function can be a file or a text string containing the aligned sequences. The other function arguments 
are the same as the VeryFastTree command-line arguments, omitting the hyphens (-). Flags should be specified with the 
value True. 


VeryFastTree can also be called using the command line interface provided by the Python module:

```bash
python3 -m veryfasttree [arguments]
```

The command-line arguments follow the same convention as the VeryFastTree.

### Contributing

Contributions are welcome! Please submit pull requests or issues on the 
[GitHub repository](https://github.com/citiususc/veryfasttree).