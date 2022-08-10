# Stdlib imports
from pathlib import Path

# Third-party app imports
import yaml

# Core Django imports
# Imports from my apps
from src.stations.util import MyDumper

from .models import StationsPlot

station_plot_path = Path(__file__).resolve().parent
station_plot_data_path = station_plot_path / "data"


def download(fparam_=station_plot_data_path / "plots.yaml"):
    """download plot from database and write plots.yaml

    Note:
        - plot from stations and dommains are downloaded to 'plots.yaml'.
    """
    dic = {}
    for plot in StationsPlot.objects.all():
        dic[plot.name] = {
            "command": plot.command,
            "options": plot.options,
            "description": plot.description,
        }

    header = """
# <plot name>:
#   command: <plot's command>
#   options: <plot's command options>
#   description: >
#     <description could be write on multilines>
"""

    # create parent directory if need be
    fparam_.mkdir(parents=True, exist_ok=True)
    with open(fparam_, "w") as stream:
        stream.write(header + "\n")
        yaml.dump(
            dic,
            stream=stream,
            Dumper=MyDumper,
            default_flow_style=False,
            sort_keys=False,
            indent=4,
        )
