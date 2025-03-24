''' List of Functions
1. ScanDoc - Run Pytesseract
2. GetShape - Get the height and width
3. GreyScale - Make it Grey Scale
4. Binarization - Convert image into a black-and-white (binary) format
5. Noise - Reduce Noise
6. Morpho - noise removal, edge enhancement, and text sharpening by applying operations like dilation, erosion, opening, and closing
7. Deskew - Rotate Image
'''

import cv2
import pytesseract
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCR_Processing():
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


    def TessOcr2(self, pil_img, config:str=None) -> str:
        '''Config Settings
            OEM
            '1' - Neural Net LSTM Only -> Uses the LSTM OCR engine only.
            '3' - Default (LSTM + Best Mode Selection) -> Automatically selects the best available mode.

            | Option | Page Segmentation Mode (PSM) | Description
            0  - Orientation and Script Detection (OSD)
                - Detects page orientation and script automatically.
            1  - Automatic Page Segmentation (OSD)
                - Segments the page into text and non-text regions.
            2  - Automatic Page Segmentation
                - No OSD, assumes only text is present.
            3  - Fully Automatic Page Segmentation
                - Similar to `1`, but assumes a single column of text.
            4  - Assume a Single Column of Text
                - Treats the image as a single column of text.
            5  - Assume a Single Uniform Block of Text
                - Assumes a uniform block of text (useful for receipts, invoices).
            6  - Assume a Single Line of Text
                - Assumes the image contains a single text line.
            7  - Treat as a Single Word
                - Assumes the image contains a single word.
            8  - Treat as a Single Digit
                - Assumes the image contains a single character.
            9  - Sparse Text Detection
                - Allows sparse text in any orientation.
            10 - Sparse Text with OSD
                - Sparse text detection with orientation script detection.
            11 - Raw Line OCR
                - OCR is done line-by-line, but no word segmentation is performed.
        '''
        img_arrary = np.array(pil_img)
        self.converted_img = cv2.cvtColor(img_arrary, cv2.COLOR_RGB2BGR)

        if config == None:
            custom_config = custom_config = r'--oem 3 --psm 6'
        else:
            custom_config = config

        text = pytesseract.image_to_string(self.converted_img, config=custom_config)
        return text

    # Preprocessing Steps
    def GetShape(self, img) -> dict:
        img_height, img_width, _ = img.shape
        return {"height":img_height,"width":img_width}

    def GreyScale(self, img) -> object:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    def Binarization(self, img) -> object:
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def Noise(self, img) -> object:
        denoised = cv2.medianBlur(img, 3)
        return denoised

    # Morphological Transformations
    def Morpho(self, img) -> object:
        kernel = np.ones((2,2), np.uint8)
        opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return opened

    def Deskew(self, img,img_width,img_height) -> object:
        coords = np.column_stack(np.where(img > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        center = (img_width // 2, img_height // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        deskewed = cv2.warpAffine(img, M, (img_width, img_height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return deskewed
