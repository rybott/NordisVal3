import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import time

from TaxProcessing.Main.ImgConverter import ImgProcess
from TaxProcessing.Main.TesseractOCR import OCR_Processing

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

t1 = time.time()
# Path to your PDF file
pdf_path = r"C:\Design Folder\RBGithub\NordisVal\Automating\Data\PDFs\2017 S Corp\111 Full S Corp Tax Return.pdf"

Forms = ["Gross Profit",
"1120S","1120s","2017"]

# Create a string to hold all the text
all_text = ""

OCR = OCR_Processing()
DictOf_Imgs = ImgProcess().Test(pdf_path)

print(f"Time to Convert PDF to Img Dict: {time.time()-t1}")

t2 = time.time()
for key in DictOf_Imgs.keys():
    page_number = key
    img = DictOf_Imgs[key]
    img = OCR.ScanImg(img)
    text = OCR.TessOcr2(img)
    Text_Up = text.upper()
    print(f"{key} was after {time.time()-t2} seconds")
    if "SCHEDULE B" in Text_Up:
        print(f"Found Sch. B on page {key}")

print(f"Total Time Taken: {time.time()-t1} seconds")
