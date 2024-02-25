import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import csv
import os

def extract_data_from_pdf(pdf_file_path):
    extracted_data = {}

    # Open the PDF file
    with fitz.open(pdf_file_path) as pdf_document:
        for page_num in range(len(pdf_document)):

            page = pdf_document.load_page(page_num)
            page_text = page.get_text()

            # Process text to extract key-value pairs
            lines = page_text.split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':')
                    extracted_data[key.strip()] = value.strip()

    return extracted_data

def extract_data_from_image(image_file_path):
    # Open the image file
    with Image.open(image_file_path) as image:
        # Use pytesseract to extract text from the image
        image_text = pytesseract.image_to_string(image)

        # Process text to extract key-value pairs
        extracted_data = {}
        lines = image_text.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':')
                extracted_data[key.strip()] = value.strip()

    return extracted_data

def save_to_csv(data, csv_file_path):
    # Extract keys from the first item in the data dictionary
    fieldnames = data.keys()

    # Write data to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)

def main():
    # Path to the input file (PDF or image)
    input_file_path = r'C:\Users\Vedansh\OneDrive\Desktop\PDF\Ex\OD330470225634931100.pdf'
  # Change this to your input file path

    # Determine the type of input file (PDF or image)
    file_extension = os.path.splitext(input_file_path)[1].lower()

    # Extract data from the input file based on its type
    if file_extension == '.pdf':
        extracted_data = extract_data_from_pdf(input_file_path)
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        extracted_data = extract_data_from_image(input_file_path)
    else:
        print("Unsupported file format.")
        return

    # Path to save CSV file
    csv_file_path = 'output_data.csv'

    # Save extracted data to CSV file
    save_to_csv(extracted_data, csv_file_path)

    print("Data extracted and saved to CSV successfully!")

if __name__ == "__main__":
    main()
