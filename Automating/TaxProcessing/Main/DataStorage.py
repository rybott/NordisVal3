import pandas as pd
import sqlite3 as sql
from datetime import datetime
import json
import numpy as np

from ImgConverter import ImgProcess
from PageAnalyzer import Analyzer

'''Intermediary Tables
The Int Table for Line Items will have
    - Line Item Amount - REAL
    - Statement No - INT (0 Default, not attached to statement)
'''

# S Corp, C Corp, Partnership, Sole Prop, Real Estate, etc.
taxtype_qry = '''
CREATE TABLE IF NOT EXISTS TaxType (
    TaxType_ID INTEGER PRIMARY KEY,
    Name TEXT
);
'''

# Line Item Type States The location of the line item (1st Pg IS, BS Current Assets, Other Deductions,Form M-2 etc.)
lineitemtype_qry = '''
CREATE TABLE IF NOT EXISTS LineItemType (
    LIT_ID INTEGER PRIMARY KEY,
    Type TEXT
);
'''

# This will house the information for the PDFs
taxdoc_qry = '''
CREATE TABLE IF NOT EXISTS TaxDocs (
    TaxDoc_ID INTEGER PRIMARY KEY,
    Customer_ID INTEGER,
    Date_Uploaded DATE,
    Date_Analyzed DATE,
    TaxType_ID INTEGER,
    Tax_Year INTEGER,
    Scanned INTEGER,
    FOREIGN KEY (TaxType_ID) REFERENCES TaxType(TaxType_ID)
);
'''

# This has PG information as well as links the exps to a report
taxpg_qry = '''
CREATE TABLE IF NOT EXISTS TaxPgs (
    TaxPg_ID INTEGER PRIMARY KEY,
    TaxDoc_ID INTEGER,
    PgNumber INTEGER,
    Textract_Output TEXT,
    FOREIGN KEY (TaxDoc_ID) REFERENCES TaxDocs(TaxDoc_ID)
);
'''

PgJoinExp_qry = '''
CREATE TABLE IF NOT EXISTS PgJoinExp (
    LIT_ID INTEGER,
    TaxPg_ID INTEGER,
    Amount REAL,
    StatementNo INTEGER,
    PRIMARY KEY (LIT_ID, TaxPg_ID),
    FOREIGN KEY (LIT_ID) REFERENCES LineItemType(LIT_ID),
    FOREIGN KEY (TaxPg_ID) REFERENCES TaxPgs(TaxPg_ID)
);
'''


class Storage():
    def __init__(self,DB, Pdf, CustomerID, Year, Type, Date_Up, instructions_json):
        # Make sure theres a Database
        self.conn = sql.connect(DB)
        self.cursor = self.conn.cursor()
        self.cursor.execute(taxtype_qry)
        self.cursor.execute(lineitemtype_qry)
        self.cursor.execute(taxdoc_qry)
        self.cursor.execute(taxpg_qry)
        self.cursor.execute(PgJoinExp_qry)
        self.conn.commit()

        with open(instructions_json, 'r') as file:
            self.instructions = json.load(file)


        # Add New Record, Make records for pages, Make Textract Null until you analyze it.
        # Array = (Pg No, Img, [Analyzed = 1, Not = 0], Pytesseract Text)

        self.DictOf_Imgs:dict = ImgProcess().img_dict(Pdf)
        data = [(key, value, 0, "") for key, value in self.DictOf_Imgs.items()]
        self.Pgs_array = np.array(data, dtype=object)


        # Update your tables with the new information

        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        UpdateDocQry = '''
            INSERT INTO TaxDocs (Customer_ID,Date_Uploaded,Date_Analyzed, TaxType_ID,Tax_Year,Scanned)
            VALUES (?,?,?,?,?,NULL);
            '''
        self.cursor.execute(UpdateDocQry,(CustomerID,Date_Up,today,Type,Year))
        self.conn.commit()

        Doc_ID = self.cursor.lastrowid

        UpdatePgQry = '''
            INSERT INTO TaxPgs (TaxDoc_ID,PgNumber,Textract_Output)
            VALUES (?,?,NULL);
            '''
        for key in self.DictOf_Imgs.keys():
            self.cursor.execute(UpdatePgQry,(Doc_ID,key))
        self.conn.commit()


    def analyze(self):
        self.Analyzer = Analyzer(self.instructions, self.Pgs_array)
        self.Analyzer.find_forms()

    def update_analyzed(self, form, analyzed:bool=False, validated:bool=False):
        if analyzed == True:
            self.AnalyzedForms_df.loc[self.AnalyzedForms_df['Form'] == form, 'Analyzed'] = 1
        if validated == True:
            self.AnalyzedForms_df.loc[self.AnalyzedForms_df['Form'] == form, 'Validated'] = 1

    def close_connection(self):
        self.conn.close()
