import json
import numpy as np

from TesseractOCR import OCR_Processing

'''Numpy Arrays
Array[x,y] -> Used to Access Variables
    X = Row Index
    Y = Col Index

np.array([
   y0 [x0,x1,x2,x3],
   y1 [x0,x1,x2,x3],
   y2 [x0,x1,x2,x3]
])

'''



class Analyzer():
    def __init__(self, instructions_json, Pg_array):
        self.Pg_array = Pg_array # (Pg No, Img, Is Analyzed, pytext)

        self.instructions = instructions_json
        # (Form, Pg No, Found, Validated)
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

    def check_values(self, text,form, Values:list, Validation:list):
        '''Process
        1. Loop Through the Values that identify the form
        2. If you find those values, adjust the Form Array:
            2a. Mark the Form as Reviewed with a 1
            2b. Update the Page Number
        3. Check the Validation/Secondary Lookup
            3a. This is a last chance to identify the form, before the whole image has to be scanned with textract which will cost big $$.
            3b. If this page find the
        '''
        Found = 0
        for value in Values:
            if value.upper() in text: # If you find the text, then mark the form as found and the page you found it on
                for form_row in self.Form_array:
                    if form_row[0] == form:
                        form_row[1] = self.CurrentPG # Save Pg
                        form_row[2] = 1 # Set as Found
                        Found = 1
                        if Validation is not None: # If there is validation
                            for word in Validation:
                                if word.upper() in text:
                                    form_row[3] = 1 #Set as Validated
                                    form_row[1] = self.CurrentPG
                                    Found = 1
        return Found




    def find_forms(self): #PDF is the URL
        for i, row in enumerate(self.Pg_array):
            if i < self.CurrentPG:
                continue
            else:
                self.CurrentPG = row[0]
                self.Pgs_array[i, 2] = 1 #Set to "Yes Analyzed"
                form = self.current_form()

                match form:
                    case "IS":
                        # Get the Instructions for Form
                        Values: list = self.instructions[form]['Values']

                        #The Following Can be Null (None)
                        Validation: list = self.instructions[form]['Validation']
                        Reference: str = self.instructions[form]['Reference']
                        PgSearchAdj: int = self.instruction[form]['PgSearchAdj']
                        SingePgValidation: list = self.instruction[form]['SingePgValidation']

                        if Reference is None:
                            text = self.OCR.TessOcr2(row[1]).upper()
                            self.Pgs_array[i, 3] = text # Save the text
                            self.check_values(text, form, Values, Validation)
                        else:
                            Reference_Pg = self.CurrentPG + PgSearchAdj
                            text = self.OCR.TessOcr2(self.Pgs_array[Reference_Pg, 2]).upper()
                            if self.check_values(text, form, Values, Validation) == 1:
                                self.CurrentPg = Reference_Pg
                                # This will make the Current Page skip ahead of the last page, and because the loop first checks if I is less then current page, it would not scan this page in theory
                            else:
                                # Continue Scanning as Normal
                                text = self.OCR.TessOcr2(row[1]).upper()
                                self.check_values(text, form, Values, Validation)
                            self.Pgs_array[i, 3] = text # Save the text

                        

                    case None:
                        # Program is Finished. Break out of Page Loop and Porcess Data
                        pass
                    case _:
                        pass
