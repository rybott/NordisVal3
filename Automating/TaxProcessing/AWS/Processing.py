import pandas as pd
import re

from Datamask import datamask

data = datamask()

class regex():
    def __init__(self):
        pass
    def parse(self,type,AWSjson):
        match type:
            case "IS":
                parsed_data = [data.IS_2017_Scorp(line) for line in AWSjson if data.IS_2017_Scorp(line)]
                return pd.DataFrame(parsed_data)
            case _:
                return "Unknown Type"

    def validate(self):
        pass
