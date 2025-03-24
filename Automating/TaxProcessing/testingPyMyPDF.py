import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import time

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

t1 = time.time()
# Path to your PDF file
pdf_path = r"C:\Design Folder\RBGithub\NordisVal\Automating\Data\PDFs\2017 S Corp\111 Full S Corp Tax Return.pdf"

Forms = ["Gross Profit",
"1120S","1120s","2017"]

# Open the PDF file
doc = fitz.open(pdf_path)

# Create a string to hold all the text
all_text = ""

# Loop through each page
for page_number in range(len(doc)):
    # Get the page
    page = doc.load_page(page_number-1)

    # Render the page to an image
    pix = page.get_pixmap()

    # Convert the image pixmap to a PIL image object
    img = Image.open(io.BytesIO(pix.tobytes('png')))

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    text = text.upper()

    if "INCORPORATE" in text and "ASSET" in text:
        print(f"Found 1st pg on pg {page_number}.")

    print(text)
    break

    '''
    for form in Forms:
        if form.upper() in text:
            print(f"Found Form {form} on pg {page_number}.")
    '''


# Close the document
doc.close()

print(f"Total Time Taken: {time.time()-t1}")
