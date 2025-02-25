# PDFQuery

A Streamlit-based application to search through PDF files in a folder and either view specific pages within the app or open them in a browser at the exact page where the search term was found.

## Features
- **Fast Search**: Uses multiprocessing to search through multiple PDFs simultaneously.
- **Text Extraction**: Extracts text directly from PDFs and uses OCR (via Tesseract) for scanned images.
- **View PDF**: Displays a specific PDF page as an image within the app.
- **Open PDF**: Opens the PDF in a browser at the exact page where the search term appears.
- **Modern UI**: A clean and responsive interface with customizable styling.

## Prerequisites
Before running the application, ensure you have the following installed:

### System Dependencies
1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **Poppler** - For converting PDFs to images:
   - **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases), extract, and add `bin` folder to your system PATH (e.g., `C:\poppler\bin`).
   - **Linux**: `sudo apt-get install poppler-utils`
   - **Mac**: `brew install poppler`
3. **Tesseract OCR** - For extracting text from images:
   - **Windows**: Download from [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki), install, and add to PATH (e.g., `C:\Program Files\Tesseract-OCR`).
   - **Linux**: `sudo apt-get install tesseract-ocr`
   - **Mac**: `brew install tesseract`

### Python Dependencies
Install the required Python packages using pip:
`pip install streamlit PyPDF2 pdf2image pytesseract pillow`


Note: Ensure NumPy is compatible with your setup. If you encounter issues with NumPy 2.x, downgrade to a 1.x version:
`pip install "numpy<2`
### Installation
#### Clone the Repository:
`git clone https://github.com/your-username/PDFQuery.git`
`cd PDFQuery`

#### Install Python Dependencies:

`pip install -r requirements.txt`
(Optional: Create a requirements.txt file with the above packages if you want to include it.)
#### Set Up System Dependencies:
Install Poppler and Tesseract as described in the Prerequisites section.

#### Verify installations:
`pdftoppm -v`  # Should return Poppler version
`tesseract --version`  # Should return Tesseract version


### Usage
#### Run the Application:

`streamlit run main.py`
This will launch the app in your default browser at `http://localhost:8501`.
#### Using the App:

Enter the folder path containing your PDF files (e.g., C:/Users/YourName/pdfs).
Type a search term and click "Search".
View results with snippets of matching text.
Click "View PDF" to see the page in the app or "Open PDF" to open it in a browser at the correct page.
