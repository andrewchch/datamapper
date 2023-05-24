import PyPDF2


def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        text = ''
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()

        return text


# Provide the path to your PDF file
pdf_file_path = 'JSMS database.pdf'
extracted_text = extract_text_from_pdf(pdf_file_path)

with open('JSMS_db.txt', 'w') as out:
    out.write(extracted_text)

out.close()

