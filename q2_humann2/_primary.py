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
    print(table)
    cmd = ["humann2_renorm_table", "-i", "%s" % table, "-o", "%s" % output,
           "-u", "%s" % method]
    subprocess.run(cmd, check=True)


def humann2(samples: SingleLanePerSampleSingleEndFastqDirFmt,
            threads: int=1) -> (biom.Table, biom.Table, biom.Table):

    tmp = tempfile.mkdtemp()
    for path, view in samples.sequences.iter_views(FastqGzFormat):
        _single_sample(str(view), threads, tmp)

    for name in ['genefamilies', 'pathcoverage', 'pathabundance']:
        _join_tables(tmp, os.path.join(tmp, "%s.biom" % name), name)

    final_tables = []
    for (name, method) in [('genefamilies', 'cpm'),
                           ('pathcoverage', 'relab'),
                           ('pathabundance', 'relab')]:

        table_path = os.path.join(tmp, "%s.biom" % name)
        result_path = os.path.join(tmp, "%s.%s.biom" % (name, method))
        _renorm(table_path, method, result_path)
        final_tables.append(biom.load_table(result_path))

    #TODO: drop temp?
    gene_families, pathcoverage, pathabundance = final_tables
    return (gene_families, pathcoverage, pathabundance)
