import warnings

warnings.filterwarnings(action="ignore")

import os.path as pth
import os
import openmdao.api as om
from fastoad import api as api_cs25
from fastga.command import api as api_cs23

import time

# Define relative path
DATA_FOLDER_PATH = "data"
WORK_FOLDER_PATH = "workdir"


os.remove(WORK_FOLDER_PATH, "problem_outputs.txt")

# Define files
CONFIGURATION_FILE = pth.join(WORK_FOLDER_PATH, "oad_process.yml")
SOURCE_FILE = pth.join(DATA_FOLDER_PATH, "beechcraft_76.xml")




api_cs25.generate_inputs(CONFIGURATION_FILE, SOURCE_FILE, overwrite=True)

starting = time.time()
eval_problem = api_cs25.evaluate_problem(CONFIGURATION_FILE, overwrite=True)

print('\n Problem ran in ', time.time() - starting , ' seconds \n')