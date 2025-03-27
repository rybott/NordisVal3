import json
from pdf2image import convert_from_path
import boto3
import os

# Setup Paths
pdf_path = r"/workspaces/NordisVal3/Automating/Data/PDFs/2017 S Corp/111 Full S Corp Tax Return.pdf"
poppler_bin_path = r"C:\Program Files\poppler-24.08.0\Library\bin"

# Add Poppler to Path if Not Already
if poppler_bin_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + poppler_bin_path

# Convert PDF to images
images = convert_from_path(pdf_path, dpi=300)
print("Converted PDF to images.")

# Initialize Textract client
textract_client = boto3.client("textract")

for i, image in enumerate(images):
    print(f"Processing Image {i}...")
    image.save(f"page_{i}.jpg", "JPEG")

    # Process each image with Textract
    with open(f"page_{i}.jpg", "rb") as file:
        response = textract_client.analyze_document(
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
    with open(f"table_page_{i}.json", "w") as f:
        json.dump(table_data, f, indent=4)

    print(f"Table extracted from Image {i} and saved as JSON.")
    break  # Only process the first page for testing
