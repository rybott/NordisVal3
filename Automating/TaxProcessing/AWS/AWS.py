import json
from pdf2image import convert_from_path
import boto3


class textextract():
    def __init__(self, region="us-east-1"):  # Specify your preferred AWS region
        self.textract_client = boto3.client("textract", region_name=region)
    def pdfconvert(self,url):
        return convert_from_path(url, dpi=300)

    def pdfIdentify(self,url):
        self.imgs = self.pdfconvert(url)
        PDF_map = {}
        for i, image in enumerate(self.imgs):
            pg_no = i+1
            



    def IS(self,url):
        self.imgs = self.pdfconvert(url)
        for i, image in enumerate(self.imgs):
            image.save(f"page_{i}.jpg", "JPEG")

            # Process each image with Textract
            with open(f"page_{i}.jpg", "rb") as file:
                response = self.textract_client.analyze_document(
                    Document={"Bytes": file.read()},
                    FeatureTypes=["TABLES"]
                )

            # Extract Tables
            blocks = response["Blocks"]

            # Store table data
            table_data = []

            # Create a mapping of cell contents
            cell_map = {}
            for block in blocks:
                if block["BlockType"] == "CELL":
                    row = block.get("RowIndex", 0)
                    col = block.get("ColumnIndex", 0)
                    text = ""
                    if "Relationships" in block:
                        for rel in block["Relationships"]:
                            if rel["Type"] == "CHILD":
                                for child_id in rel["Ids"]:
                                    for b in blocks:
                                        if b["Id"] == child_id and b["BlockType"] == "WORD":
                                            text += b["Text"] + " "
                    text = text.strip()
                    cell_map[(row, col)] = text

            # Convert to a structured table
            max_row = max([key[0] for key in cell_map.keys()])
            max_col = max([key[1] for key in cell_map.keys()])

            for row in range(1, max_row + 1):
                row_data = []
                for col in range(1, max_col + 1):
                    row_data.append(cell_map.get((row, col), ""))
                table_data.append(row_data)

            # Save table as a readable format
            with open(f"Automating/TaxProcessing/AWS/DownloadedAWS/IS_table_page_{i}.json", "w") as f:
                json.dump(table_data, f, indent=4)
            return table_data
