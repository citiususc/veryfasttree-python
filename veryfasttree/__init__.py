import os
import os.path
import platform
from importlib.metadata import distribution
from cpuinfo import get_cpu_info
import subprocess

__all__ = ['run', 'help', 'VFT_BINARY']
__doc__ = 'VeryFastTree: Efficient phylogenetic tree inference for massive taxonomic datasets'

_simd = 'sse2'

if platform.machine() == 'x86_64' or platform.machine() == 'AMD64':
    _flags = set(get_cpu_info()['flags'])
    for flag in ['avx512f', 'avx2']:
        if flag in _flags:
            _simd = flag
            break
    del _flags

_binary = 'veryfasttree/bin/VeryFastTree-' + _simd + ('.exe' if platform.system() == 'Windows' else '')
VFT_BINARY = distribution('veryfasttree').locate_file(_binary)
del _binary


def help():
    print(run(help=True))


def run(alignment=None, **kwargs):
    """
    Common options:
        :param alignment       : input file or string
        :param out             : print tree in output file
        :param n               : to analyze multiple alignments (phylip format only) (use for global bootstrap, with seqboot and CompareToBootstrap.pl)
        :param intree          : to set the starting tree(s)
        :param intree1         : to use this starting tree for all the alignments (for faster global bootstrap on huge alignments)
        :param quiet           : to suppress reporting information
        :param nopr            : to suppress progress indicator
        :param log             : save intermediate trees, settings, and model details
        :param quote           : allow spaces and other restricted characters (but not ' ) in sequence names and quote names in the output tree (fasta/fastq input only; VeryFastTree will not be able to read these trees back in)
        :param pseudo          : to use pseudocounts (recommended for highly gapped sequences)
        :param noml            : to turn off maximum-likelihood
        :param lg              : Le-Gascuel 2008 model (amino acid alignments only)
        :param wag             : Whelan-And-Goldman 2001 model (amino acid alignments only)
        :param gtr             : generalized time-reversible model (nucleotide alignments only)
        :param cat             : to specify the number of rate categories of sites (default 20) or -nocat to use constant rates
        :param gamma           : after optimizing the tree under the CAT approximation, rescale the lengths to optimize the Gamma20 likelihood
        :param nome            : to turn off minimum-evolution NNIs and SPRs (recommended if running additional ML NNIs with -intree), -nome -mllen with -intree to optimize branch lengths for a fixed topology
        :param nosupport       : to not compute support values
        :param fastest         : speed up the neighbor joining phase & reduce memory usage (recommended for >50,000 sequences)
        :param constraints     : to constrain the topology search constraintAlignment should have 1s or 0s to indicates splits
        :param threads         : number of threads (n) used in the parallel execution.
        :param double-precision: use double precision arithmetic. Therefore, it is equivalent to compile FastTree-2 with -DUSE_DOUBLE
        :param ext             : to speed up computations enabling the vector extensions. Available: AUTO(default), NONE, SSE, SSE3 , AVX, AVX2, AVX512 or CUDA
        :param expert          : return all available options

    The other parameters are the same as for VeryFastTree, you just need to specify the parameter without the hyphen.
    STDIN is replaced by the positional argument of the function, and STDOUT by the function return

    :return: tree (if not out) | matrix (if makematrix) | help (if h or help) | expert help (if expert)
    """

    args = [VFT_BINARY]
    for arg_name, value in kwargs.items():
        if isinstance(value, bool):
            if value:
                args.append(f'-{arg_name}')
        else:
            args.append(f'-{arg_name}')
            args.append(str(value))

    input = None
    if alignment is None and any([e in kwargs for e in ['h', 'help', 'expert']]):
        pass
    elif alignment is None:
        raise ValueError(f'Input file is None')
    elif '\n' in alignment:
        input = alignment
    elif not os.path.exists(alignment):
        raise ValueError(f'Input file {alignment} does not exist')
    else:
        args.append(alignment)

    result = subprocess.run(args, text=True, input=input, stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f'VeryFastTree fails, check logs for details')
    return result.stdout
