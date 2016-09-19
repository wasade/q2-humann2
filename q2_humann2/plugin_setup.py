import qiime.plugin
from q2_types import (SampleData, SequencesWithQuality, FeatureTable,
                      Frequency, RelativeFrequency)

import q2_humann2


plugin = qiime.plugin.Plugin(
    name='humann2',
    version=q2_humann2.__version__,
    website='http://huttenhower.sph.harvard.edu/humann2',
    package='q2_humann2',
    user_support_text=("To get help with HUMAnN2, please post a question to "
                       "the HUMAnN Google Group form: "
                       "https://groups.google.com/forum/#!forum/humann-users"),
    citation_text=None
)


plugin.methods.register_function(
    function=q2_humann2.run,
    inputs={'demultiplexed_seqs': SampleData[SequencesWithQuality]},
    parameters={'threads': qiime.plugin.Int},
    name='Characterize samples using HUMAnN2',
    outputs=[('genefamilies', FeatureTable[Frequency]),
             ('pathcoverage', FeatureTable[RelativeFrequency]),
             ('pathabundance', FeatureTable[RelativeFrequency])],
    description='Execute the HUMAnN2'
)
