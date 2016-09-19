import subprocess
import tempfile
import os

import biom
from q2_types import FeatureTable, Frequency
from q2_types.per_sample_sequences import \
        SingleLanePerSampleSingleEndFastqDirFmt, FastqGzFormat


def _single_sample(sample: str, threads: int, output: str) -> None:
    """Run a single sample through humann2"""
    cmd = ["humann2", "-i", "%s" % sample, "-o", "%s" % output,
           "--threads", "%d" % threads,
           "--output-format", "biom"]
    subprocess.run(cmd, check=True)


def _join_tables(table: str, output: str, name: str) -> None:
    """Merge multiple sample output into single tables"""
    tmp_output = output + '-actual'
    cmd = ["humann2_join_tables", "-i", table, "-o", tmp_output,
           "--file_name", "%s" % name]
    subprocess.run(cmd, check=True)

    # doing convert manually as we need to filter out the leading comment as
    # humann2_renorm_table cannot handle comment lines
    for_convert = biom.load_table(tmp_output)
    lines = for_convert.to_tsv().splitlines()
    lines = lines[1:]  # drop leading comment
    with open(output, 'w') as fp:
        fp.write('\n'.join(lines))
        fp.write('\n')

    #cmd = ["biom", "convert", "-i", tmp_output, "-o", output, "--to-tsv"]
    #subprocess.run(cmd, check=True)


def _renorm(table: str, method: str, output: str) -> None:
    """Renormalize a table"""
    cmd = ["humann2_renorm_table", "-i", "%s" % table, "-o", "%s" % output,
           "-u", "%s" % method]
    subprocess.run(cmd, check=True)


def run(demultiplexed_seqs: SingleLanePerSampleSingleEndFastqDirFmt,
        threads: int=1) -> (biom.Table, biom.Table, biom.Table):
    """Run samples through humann2

    Parameters
    ----------
    samples : SingleLanePerSampleSingleEndFastqDirFmt
        Samples to process
    threads : int
        The number of threads that humann2 should use

    Notes
    -----
    This command consumes per-sample FASTQs, and takes those data through
    "humann2", then through "humann2_join_tables" and finalizes with
    "humann2_renorm_table".

    Returns
    -------
    biom.Table
        A gene families table normalized using "cpm"
    biom.Table
        A pathway coverage table normalized by relative abundance
    biom.Table
        A pathway abundance table normalized by relative abundance
    """
    import sys
    from distutils.spawn import find_executable
    if find_executable('metaphlan2.py') is None:
        sys.stderr.write(("Cannot find metaphlan2.py in $PATH. Please install "
                          "metaphlan2 prior to installing the q2-humann2 plugin "
                          "as it is a required dependency. Details can be found "
                          "here: https://bitbucket.org/biobakery/metaphlan2."))
        sys.exit(1)

    tmp = tempfile.mkdtemp()
    for path, view in demultiplexed_seqs.sequences.iter_views(FastqGzFormat):
        _single_sample(str(view), threads, tmp)

    final_tables = {}
    for (name, method) in [('genefamilies', 'cpm'),
                           ('pathcoverage', 'relab'),
                           ('pathabundance', 'relab')]:

        joined_path = os.path.join(tmp, "%s.biom" % name)
        result_path = os.path.join(tmp, "%s.%s.biom" % (name, method))

        _join_tables(tmp, joined_path, name)
        _renorm(joined_path, method, result_path)

        final_tables[name] = biom.load_table(result_path)

    #TODO: drop temp?
    return (final_tables['genefamilies'],
            final_tables['pathcoverage'],
            final_tables['pathabundance'])
