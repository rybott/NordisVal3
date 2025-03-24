import pandas as pd
import re

class datamask():
    def __init__(self):
        pass
    def IS_2017_Scorp(self,entry):
        cleaned_data = [item for item in entry if item.strip()]
        if not cleaned_data:
            return None
        id_number = None
        category = None
        statement = None
        statement_number = None
        second_id = None
        amount = None

        # ID
        if re.match(r"^\d+[a-zA-Z]?$", cleaned_data[0]):
            id_number = cleaned_data.pop(0)

        # Category
        for i, item in enumerate(cleaned_data):
            if not re.match(r"^\d+[a-zA-Z]?$", item) and not re.match(r"^\d+(\,|\.)?\d*$", item):
                category = item
                del cleaned_data[i]
                break

        # Statements
        if "STATEMENT" in cleaned_data:
            statement_index = cleaned_data.index("STATEMENT")
            statement = "STATEMENT"
            statement_number = cleaned_data[statement_index + 1] if statement_index + 1 < len(cleaned_data) else None
            del cleaned_data[statement_index:statement_index + 2]  # Remove both from list

        # 2nd ID
        if cleaned_data and re.match(r"^\d+[a-zA-Z]?$", cleaned_data[0]):
            second_id = cleaned_data.pop(0)

        #Amount
        for i, item in enumerate(cleaned_data[-4:]):
            if item[-1] == ".":
                item = str(item[:-1])
            if re.match(r"^\d{1,3}(?:,\d{3})*(?:\.\d+)?$", item):
                a = cleaned_data.pop()
                amount = item
                print(amount)

        #Validation
        if amount == id_number:
            amount = None

        return {
            "ID": id_number,
            "Category": category,
            "Statement": statement,
            "Statement Number": statement_number,
            "Second ID": second_id,
            "Amount": amount
        }
