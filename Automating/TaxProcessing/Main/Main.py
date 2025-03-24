

'''
What you need to start

1. You will need the Customer ID
2. Path to PDF
3. Tax Year
4. Tax Type (1120, C-Corp, Sole Prop, etc.)
5. Date_Uploaded
6. Database connection
'''

import time
from datetime import datetime

from DataStorage import Storage


t1 = time.time()

pdf_path = r"C:\Design Folder\RBGithub\NordisVal\Automating\Data\PDFs\2017 S Corp\111 Full S Corp Tax Return.pdf"
db_file = "TaxDocDB.db"
CustomerID = 1
Year = 2017
Type = 1
today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
instructions = r"C:\Users\rybot\OneDrive\Desktop\Taxes for Code\Code\TaxProcessing\Main\TaxStructure.json"

db = Storage(db_file,pdf_path,CustomerID,Year,1,today, instructions)

print(f'Time To Process Imgs and Database: {time.time()-t1}')

db.analyze()

db.close_connection()

print(f'Total Time: {time.time()-t1}')
