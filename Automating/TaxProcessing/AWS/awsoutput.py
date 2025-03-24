import pandas as pd
import re

# Sample JSON data variations
Income_Statment_Data = [["", "Firm's name", "SAX LLP", "Firm's EIN", "81-2950760", "PTIN", "1c", "58,746,517."],
["", "Firm's address", "855 VALLEY ROAD CLIFTON, NJ 07013", "Phone no.", "973-472-6250", "P01386005", "2", "52,846,211."],
["", "3", "Gross profit. Subtract line 2 from line 1c", "", "", "", "3", "5,900,306."],
["", "4", "Net gain (loss) from Form 4797, line 17 (attach Form 4797)", "", "", "", "4", ""],
["", "5", "Other income (loss) (attach statement)", "", "", "", "5", ""],
["", "6", "Total income (loss). Add lines 3 through 5", "", "", "", "6", "5,900,306."],
["", "7", "Compensation of officers (see instrs. - attach Form 1125-E)", "", "", "", "7", "739,000."],
["", "8", "Salaries and wages (less employment credits)", "", "", "", "8", "1,446,387."],
["", "9", "Repairs and maintenance", "", "", "", "9", "147,914."],
["", "10", "Bad debts", "", "", "", "10", ""],
["", "11", "Rents", "", "", "", "11", "184,924."],
["", "12", "Taxes and licenses", "", "STATEMENT", "1", "12", "511,060."],
["", "13", "Interest", "", "", "", "13", "74,329."],
["", "14", "Depreciation not claimed on Form 1125-A or elsewhere on return (attach Form 4562)", "", "", "", "14", "183,106."],
["", "15", "Depletion (Do not deduct oil and gas depletion.)", "", "", "", "15", ""],
["", "16", "Advertising", "", "", "", "16", "56,914."],
["", "17", "Pension, profit-sharing, etc., plans", "", "", "", "17", ""],
["", "18", "Employee benefit programs", "", "", "", "18", "156,711."],
["", "19", "Other deductions (attach statement)", "", "STATEMENT", "2", "19", "1,336,900."],
["", "20", "Total deductions. Add lines 7 through 19", "", "", "", "20", "4,837,245."],
["", "21", "Ordinary business income (loss). Subtract line 20 from line 6", "", "", "", "21", "1,063,061."],
["", "22", "a Excess net passive income or LIFO recapture tax (see instructions)", "22a", "", "", "", ""],
["", "", "b Tax from Schedule D (Form 1120S)", "22b", "", "", "", ""],
["", "", "C Add lines 22a and 22b", "", "", "", "22c", ""],
["", "23", "a 2017 estimated tax payments and 2016 overpayment credited to 2017", "23a", "", "", "", ""],
["", "", "b Tax deposited with Form 7004", "23b", "", "", "", ""],
["", "", "C Credit for federal tax paid on fuels (attach Form 4136)", "23c", "", "", "", ""],
["", "", "d Add lines 23a through 23c", "", "", "", "23d", ""],
["", "24", "Estimated tax penalty (see instructions). Check if Form 2220 is attached", "", "", "", "24", ""],
["", "25", "Amount owed. If line 23d is smaller than the total of lines 22c and 24, enter amount", "owed", "", "", "25", ""],
["", "26", "Overpayment. If line 23d is larger than the total of lines 22c and 24, enter amount", "overpaid", "", "", "26", ""],
["", "27", "Enter amount from line 26 Credited to 2018 estimated tax", "", "", "Refunded", "27", ""] ]


# Function to parse JSON list
def parse_json_entry(entry):
    # Remove empty strings
    cleaned_data = [item for item in entry if item.strip()]

    if not cleaned_data:
        return None  # Ignore empty rows

    # Initialize placeholders
    id_number = None
    category = None
    statement = None
    statement_number = None
    second_id = None
    amount = None

    # Identify the first ID (it can be a number or number+letter)
    if re.match(r"^\d+[a-zA-Z]?$", cleaned_data[0]):
        id_number = cleaned_data.pop(0)

    # Identify category (first non-ID value)
    for i, item in enumerate(cleaned_data):
        if not re.match(r"^\d+[a-zA-Z]?$", item) and not re.match(r"^\d+(\,|\.)?\d*$", item):
            category = item
            del cleaned_data[i]  # Remove category from list
            break

    # Look for "STATEMENT" entries
    if "STATEMENT" in cleaned_data:
        statement_index = cleaned_data.index("STATEMENT")
        statement = "STATEMENT"
        statement_number = cleaned_data[statement_index + 1] if statement_index + 1 < len(cleaned_data) else None
        del cleaned_data[statement_index:statement_index + 2]  # Remove both from list

    # Check for a second occurrence of an ID
    if cleaned_data and re.match(r"^\d+[a-zA-Z]?$", cleaned_data[0]):
        second_id = cleaned_data.pop(0)

    # If the last item is a number (formatted as currency or numeric), treat it as the amount

    for i, item in enumerate(cleaned_data[-4:]):
        if item[-1] == ".":
            item = str(item[:-1])
        if re.match(r"^\d{1,3}(?:,\d{3})*(?:\.\d+)?$", item):
            a = cleaned_data.pop()
            amount = item
            print(amount)

    if amount == id_number:
        amount = None

    # Return structured data
    return {
        "ID": id_number,
        "Category": category,
        "Statement": statement,
        "Statement Number": statement_number,
        "Second ID": second_id,
        "Amount": amount
    }

def income_formatting(income_df):
    
    pass

# Process all JSON samples
parsed_data = [parse_json_entry(entry) for entry in Income_Statment_Data if parse_json_entry(entry)]

# Convert to DataFrame
income_df = pd.DataFrame(parsed_data)

print(income_df)
