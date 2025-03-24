import pandas as pd
import os

from AWS import textextract
from Processing import regex

poppler_bin_path = r"C:\Program Files\poppler-24.08.0\Library\bin"
if poppler_bin_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + poppler_bin_path

# Data Loading, To be Replaced with a system to call this program and fetch data to import into this project.(i.e. When Client Docs Uploaded >> Run the following program)

ISpdf_path = r"C:\Design Folder\RBGithub\NexusVS\Testing Automatic Processes\Data\PDFs\2017 S Corp\111 S Corp Tax Return IS no Statements.pdf"

AllReturn_path = r"C:\Design Folder\RBGithub\NexusVS\Testing Automatic Processes\Data\PDFs\2017 S Corp\111 Full S Corp Tax Return.pdf"

ISpdf2_path = r"C:\Users\rybot\OneDrive\Desktop\tax2017.pdf"

# ISpdf2018_path = r""

# Running the Program

extract = textextract()
json = extract.IS(ISpdf2_path)

# There is where you write an algorithm to determine with Yr/Type it is, but the algorithm is mostly getting the data from the client information, you just need to determine which page is what and parse accordingly.

processing = regex()
df = processing.parse("IS",json)
print(df)
