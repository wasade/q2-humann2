import qiime.plugin
from q2_types import (SampleData, SequencesWithQuality, FeatureTable,
                      Frequency, RelativeFrequency)

import q2_humann2


plugin = qiime.plugin.Plugin(
    name='humann2',
    version=q2_humann2.__version__,
    website='http://huttenhower.sph.harvard.edu/humann2',
    package='q2_humann2',
    user_support_text=None,
    citation_text=None
)


plugin.methods.register_function(
    function=q2_humann2.humann2,
    inputs={'samples': SampleData[SequencesWithQuality]},
    parameters={},
    name='humann2',
    outputs=[('genefamilies', FeatureTable[Frequency]),
             ('pathcoverage', FeatureTable[RelativeFrequency]),
             ('pathabundance', FeatureTable[RelativeFrequency])],
    description='Execute the HUMAnN2'
)
