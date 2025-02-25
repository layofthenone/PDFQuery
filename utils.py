import os
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import glob
import sqlite3
from multiprocessing import Pool, cpu_count

# Initialize the SQLite database for caching extracted text
def init_db():
    conn = sqlite3.connect("pdf_cache.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pdf_texts 
                 (pdf_path TEXT, page_num INTEGER, text TEXT, PRIMARY KEY (pdf_path, page_num))''')
    conn.commit()
    conn.close()

# Extract text from a PDF file (both direct text and OCR from images)
def extract_text_from_pdf(pdf_path):
    conn = sqlite3.connect("pdf_cache.db")
    c = conn.cursor()
    c.execute("SELECT page_num, text FROM pdf_texts WHERE pdf_path=?", (pdf_path,))
    cached_data = c.fetchall()
    
    if cached_data:
        conn.close()
        return {page_num: text for page_num, text in cached_data}

    text_data = {}
    try:
        with open(pdf_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            num_pages = len(pdf.pages)
            for page_num in range(num_pages):
                page = pdf.pages[page_num]
                text = page.extract_text() or ""
                if len(text) < 50:  # If text is too short, attempt OCR
                    try:
                        images = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1, dpi=100)
                        for img in images:
                            text += "\n" + pytesseract.image_to_string(img)
                    except Exception as ocr_error:
                        print(f"OCR error: {pdf_path} - {ocr_error}")
                text_data[page_num + 1] = text.strip()
                c.execute("INSERT OR REPLACE INTO pdf_texts VALUES (?, ?, ?)", 
                          (pdf_path, page_num + 1, text.strip()))
        conn.commit()
    except Exception as e:
        print(f"Text extraction error: {pdf_path} - {e}")
    conn.close()
    return text_data

# Search within a single PDF file in parallel
def search_in_pdf(args):
    pdf_path, query = args
    text_data = extract_text_from_pdf(pdf_path)
    results = []
    for page_num, text in text_data.items():
        if query.lower() in text.lower():
            results.append({
                "pdf_path": pdf_path,
                "page_num": page_num,
                "snippet": text[:200] + "..." if len(text) > 200 else text
            })
    return results

# Search across all PDFs in a folder using multiprocessing
def search_in_pdfs(folder_path, query):
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    with Pool(cpu_count()) as pool:
        results = pool.map(search_in_pdf, [(pdf, query) for pdf in pdf_files])
    return [item for sublist in results for item in sublist]

# Display a specific page of a PDF as an image
def display_pdf_page(pdf_path, page_num):
    try:
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            return None
        images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=100)
        if not images:
            print(f"Image could not be generated: {pdf_path} - Page {page_num}")
            return None
        print(f"Image successfully loaded: {pdf_path} - Page {page_num}")
        return images[0]
    except Exception as e:
        print(f"PDF display error: {e}")
        return None