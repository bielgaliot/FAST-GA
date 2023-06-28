import warnings

warnings.filterwarnings(action="ignore")

import os.path as pth
import os
import openmdao.api as om
from fastoad import api as api_cs25
from fastga.command import api as api_cs23
import logging
from fastoad.gui import VariableViewer
import shutil

# Define relative path
DATA_FOLDER_PATH = "data"
WORK_FOLDER_PATH = "workdir"

# Remove work folder
#shutil.rmtree(WORK_FOLDER_PATH, ignore_errors=True)

# Define files
CONFIGURATION_FILE = pth.join(WORK_FOLDER_PATH, "oad_process_test.yml")
SOURCE_FILE = pth.join(DATA_FOLDER_PATH, "beechcraft_76.xml")

# For having log messages on screen
logging.basicConfig(level=logging.INFO, format="%(levelname)-8s: %(message)s")

# For using all screen width
from IPython.core.display import display, HTML

display(HTML("<style>.container { width:95% !important; }</style>"))


"""api_cs25.generate_configuration_file(
    CONFIGURATION_FILE,
    overwrite=True,
    distribution_name="fast-oad-cs23",
    sample_file_name="fastga.yml",
)"""


XDSM_FILE = pth.join(WORK_FOLDER_PATH, "xdsm.html")
api_cs25.write_xdsm(CONFIGURATION_FILE, XDSM_FILE, overwrite=True)
from IPython.display import IFrame

IFrame(src=XDSM_FILE, width="100%", height="500px")