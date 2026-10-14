# PDF Converter & PDF Tools

A modern, fast, and easy-to-use web application built with Python and Streamlit for converting documents and images, as well as managing PDF files.

---

## Features

### Document & Image Conversions
- **PDF to Word**: Convert PDF documents into editable Word (`.docx`) files.
- **Word to PDF**: Convert Word documents (`.docx`) into high-quality PDF files.
- **Image to PDF**: Combine or convert image files into PDF format.
- **PDF to Image**: Extract pages from PDF documents as standalone image files.
- **PDF to Excel**: Extract structured table data from PDF files into Excel spreadsheets (`.xlsx`).
- **PDF to PowerPoint**: Convert PDF presentations and documents into PowerPoint slides (`.pptx`).
- **PDF to TXT**: Extract plain text content from PDF files into `.txt` documents.

### PDF Tools
- **Merge PDF**: Combine multiple PDF files into a single unified document.
- **Split PDF**: Extract specific page ranges or split a PDF into separate files.
- **Compress PDF**: Optimize and reduce the file size of PDF documents.
- **Rotate PDF**: Rotate PDF pages to the desired orientation (90°, 180°, or 270°).
- **Password Protect**: Encrypt and secure sensitive PDF files with password protection.

---

## Technologies Used

- **Language**: Python
- **Web Framework**: [Streamlit](https://streamlit.io/)
- **PDF & Document Processing**:
  - `pypdf` & `pymupdf` (PDF manipulation, rendering, and text extraction)
  - `pdf2docx` & `python-docx` (Word conversion and generation)
  - `docx2pdf` (Word to PDF conversion)
  - `Pillow` (Image processing and conversion)
  - `openpyxl` & `pandas` (Excel export and table handling)
  - `python-pptx` (PowerPoint presentation generation)

---

## Installation (Windows)

Follow these steps to set up and run the project locally on Windows using PowerShell.

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system. You can verify your installation by running:
```powershell
python --version
```

### 2. Clone or Navigate to the Project Directory
Open **Windows PowerShell** and navigate to your project folder:
```powershell
cd c:\Users\Malaika\Desktop\pdf-converter
```

### 3. Create a Virtual Environment
Create a dedicated virtual environment named `.venv`:
```powershell
python -m venv .venv
```

---

## Activating the Virtual Environment

Activate the virtual environment in PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

> **Note**: If you receive a script execution policy error in PowerShell, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```
> and then re-run the activation command.

When activated, you will see `(.venv)` displayed at the start of your terminal prompt line.

---

## Installing Dependencies

With the virtual environment active, install all required dependencies listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

---

## Running the App

Start the Streamlit application using the following command:
```powershell
python -m streamlit run app.py
```

Once started, the application will automatically open in your default browser at:
```
http://localhost:8501
```

---

## Project Structure

```text
pdf-converter/
├── .venv/               # Virtual environment directory (generated)
├── app.py               # Main Streamlit web application
├── requirements.txt     # Python project dependencies
├── .gitignore           # Git ignore configuration
└── README.md            # Project documentation
```

---

## Future Improvements

- **OCR (Optical Character Recognition)**: Extract text and tables from scanned image-based PDFs.
- **Batch Processing**: Support converting and processing larger batches of files simultaneously.
- **Page Reordering & Deletion**: Drag-and-drop interactive page organization before saving or merging.
- **Watermarking**: Add customizable text or image watermarks to PDF pages.
- **Digital Signatures**: Sign and verify PDF documents with digital signatures.
- **Cloud Storage Integration**: Direct import and export to Google Drive, Dropbox, or OneDrive.
