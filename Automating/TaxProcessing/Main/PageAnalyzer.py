import json
import numpy as np

from TesseractOCR import OCR_Processing

'''Numpy Arrays
Array[x,y] -> Used to Access Variables
    X = Col Index
    Y = Row Index

np.array([
   X0 [y0,y1,y2,y3],
   X1 [y0,y1,y2,y3],
   X2 [y0,y1,y2,y3]
])

'''


class Analyzer():
    def __init__(self, instructions_json, Pg_array):
        self.Pg_array = Pg_array # (Pg No, Img, Is Analyzed, pytext) Starting at 0

        self.instructions = instructions_json
        # (Form, Pg No, Found, Validated) # for Statements the last column will be for last page index
        data = [(key, 0, 0, 0) for key in self.instructions.keys()]
        self.Form_array = np.array(data, dtype=object)

        self.CurrentPG = self.Pg_array[0,0]
        self.CurrentForm = self.Form_array[0,0]

        self.OCR = OCR_Processing()

    def current_form(self):
        for item in self.Form_array:
            if item[1] == 0:
                return item
        return None  # Return None if all forms have been checked.

    def check_values(self, text,form, Values:list, Validation:list = None, Pg:int = None):
        '''Process
        1. Loop Through the Values that identify the form
        2. If you find those values, adjust the Form Array:
            2a. Mark the Form as Reviewed with a 1
            2b. Update the Page Number
        3. Check the Validation/Secondary Lookup
            3a. This is a last chance to identify the form, before the whole image has to be scanned with textract which will cost big $$.
            3b. If this page find the
        '''
        Found: int = 0
        for value in Values:
            if value.upper() in text: # If you find the text, then mark the form as found and the page you found it on
                for i, form_row in enumerate(self.Form_array):
                    if form_row[0] == form:
                        self.Form_array[1,i] = self.CurrentPG if Pg is None else Pg # Save Pg
                        self.Form_array[2,i] = 1 # Set as Found
                        Found = 1
                        if Validation is not None: # If there is validation
                            for word in Validation:
                                if word.upper() in text:
                                    self.Form_array[3,i] = 1 #Set as Validated
                                    if form != "Statements":
                                        self.Form_array[1,i] = self.CurrentPG if Pg is None else Pg # Save Pg
                                        Found = 1
                                    else:
                                        self.Form_array[3,i] = self.CurrentPG if Pg is None else Pg # Save Pg
                                        self.Pgs_array[3, i] = text # save text
                                        # I am editing this at 5:03 3/27/25
        return Found




    '''Issues that might arise
    - The Check_values function uses the global current page, so when


    '''


    def find_forms(self): #PDF is the URL
        found_stmt = False
        for i, row in enumerate(self.Pg_array):
            if i < self.CurrentPG:
                continue
            else:
                self.Pgs_array[2, i] = 1 #Set to "Yes Analyzed"
                form: object = self.current_form()
                self.CurrentPG: int = row[0]

                match form:

                    case None:
                        # Program is Finished. Break out of Page Loop and Porcess Data
                        # To start I want to just print the data and see if it works
                        pass

                    case "Statements":
                        # This will first loop until it find the statements, and then
                        Values: list = self.instructions[form]['Values']
                        if found_stmt == False:
                            text = self.OCR.TessOcr2(row[1]).upper()

                            if self.check_values(text, form, Values) == 1:
                                self.Pgs_array[3, i] = text # Save the text
                                found_stmt = True
                            else:
                                pass

                        else: # It found the statements section and will loop through the statements
                            loop = 1
                            pg = i
                            while loop = 1:
                                text = self.OCR.TessOcr2(row[1]).upper()
                                if self.check_values(text, form, Values, pg) == 1:
                                    self.Pgs_array[3, i] = text # Save the text



                    case _:
                        # Get the Instructions for Form
                        Values: list = self.instructions[form]['Values']

                        #The Following Can be Null (None)
                        Validation: list = self.instructions[form]['Validation']
                        Reference: str = self.instructions[form]['Reference']
                        PgSearchAdj: int = self.instruction[form]['PgSearchAdj']
                        SingePgValidation: list = self.instruction[form]['SingePgValidation']

                        if Reference is None:
                            text = self.OCR.TessOcr2(row[1]).upper()
                            self.Pgs_array[3, i] = text # Save the text
                            self.check_values(text, form, Values, Validation)
                        else:
                            Reference_Pg: int = self.CurrentPG + PgSearchAdj
                            text = self.OCR.TessOcr2(self.Pgs_array[2,Reference_Pg]).upper()
                            if self.check_values(text, form, Values, Validation) == 1:
                                self.CurrentPg = Reference_Pg
                                # This will make the Current Page skip ahead of the last page, and because the loop first checks if I is less then current page, it would not scan this page in theory
                            else:
                                # Continue Scanning as Normal
                                text = self.OCR.TessOcr2(row[1]).upper()
                                self.check_values(text, form, Values, Validation)
                            self.Pgs_array[3, i] = text # Save the text

                        if SingePgValidation is None:
                            continue # Finished Loop for One Page
                        else:
                            Sndpg = self.CurrentPG +  1 # Look at the next page to see if it is continued form first
                            text = self.OCR.TessOcr2(self.Pgs_array[2, Sndpg]).upper()
                            self.check_values(text, form, SingePgValidation, Pg=Sndpg)
