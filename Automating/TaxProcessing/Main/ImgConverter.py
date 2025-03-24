''' When I have the Server Set Up
This Code will create Images of the PDFs becuase IMGs scan better and then those images will be pushed straight onto the Server

This will run independently from the rest of the code
'''
import os
from pdf2image import convert_from_path


class ImgProcess():
    def __init__(self):
        poppler_bin_path = r"C:\Program Files\poppler-24.08.0\Library\bin"
        if poppler_bin_path not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + poppler_bin_path

    def img_dict(self, path: str, dpi=300) -> dict:
        images = convert_from_path(path, dpi=dpi)
        images_dict = {i + 1: img for i, img in enumerate(images)}
        return images_dict
