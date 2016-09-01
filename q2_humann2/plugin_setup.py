import qiime.plugin

import q2_humann2

# These imports are only included to support the example methods and
# visualizers. Remove these imports when you are ready to develop your plugin.
#from q2_dummy_types import IntSequence1, IntSequence2, Mapping
#from ._dummy_method import concatenate_ints
#from ._dummy_visualizer import mapping_viz

def tests() -> None:
    return

def concatenate_ints() -> None:
    return

def mapping_viz(output_dir: str) -> None:
    return

plugin = qiime.plugin.Plugin(
    name='humann2',
    version=q2_humann2.__version__,
    website='http://huttenhower.sph.harvard.edu/humann2',
    package='q2_humann2',
    # Information on how to obtain user support should be provided as a free
    # text string via user_support_text. If None is provided, users will
    # be referred to the plugin's website for support.
    user_support_text=None,
    # Information on how the plugin should be cited should be provided as a
    # free text string via citation_text. If None is provided, users
    # will be told to use the plugin's website as a citation.
    citation_text=None
)

# The next two code blocks are examples of how to register methods and
# visualizers. Replace them with your own registrations when you are ready to
# develop your plugin.

plugin.methods.register_function(
    function=tests,
    inputs={},
    parameters={},
    outputs=[],
    name='tests',
    description='Execute the HUMAnN2 test suite.'
)

plugin.visualizers.register_function(
    function=mapping_viz,
    inputs={
       # 'mapping2': Mapping
    },
    parameters={
    },
    name='Visualize two mappings',
    description='This visualizer produces an HTML visualization of two '
                'key-value mappings, each sorted in alphabetical order by key.'
)
