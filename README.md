# PDF AI Dashboard (Gyandeep)

This project is a powerful web application designed to upload, extract, read, and summarize large PDF documents using dynamic Optical Character Recognition (OCR) and the **Sarvam AI** cloud API. It is tailored for building rich contexts from messy scans and PDFs meant for further Retrieval-Augmented Generation (RAG) tasks.

## 🚀 Features

- **Upload & Read:** Seamless PDF uploads and reading interface right in the browser.
- **Dynamic OCR Text Extraction:** Employs PyMuPDF natively and scales up to PyTesseract OCR if the document lacks embedded text formats.
- **Chunk-Based Global Analysis:** Processes large books in chunks (20-page blocks in parallel) to bypass AI token limits and memory limits.
- **Progressive Outputs:** Synthesized context is continuously appended to `context.txt` so no data is lost mid-processing.
- **Interactive Chat Interface:** Ask questions directly to your uploaded PDF context.

## 🧩 The Pipeline Architecture

- PDF --> OCR --> Model --> synthetic data conversion --> context.txt


Our backend relies on FastAPI and asynchronous operations. Here operates the core pipeline:

1. **Upload Phase (`/api/upload`):** Let users upload their document. The system analyzes PyMuPDF metadata and returns the Table of Contents and page counts.
2. **Chunking Mechanism:** When doing a global analysis (`/api/analyze_global`), the PDF is iterated in 20-page blocks.
3. **Concurrent Processing:** 
    - A concurrency semaphore natively pools up to 20 workers simultaneously.
    - `extract_page_async` tries to fetch plain text via `fitz`.
    - If the raw text is suspiciously minimal (less than 20 chars), we pivot and apply high-DPI `pytesseract` OCR to the page image natively.
4. **Synthetic Data Generation:** 
    - The cleaned and OCR'd 20-page payload is structured into a prompt and routed to the **`sarvam-30b`** model over the Sarvam AI cloud via asyncio.
5. **Progressive Storage:** The response is safely captured and directly written/appended into `context.txt`. If the API denies content (due to moderation filters, etc.), the pipeline gracefully inserts an error placeholder instead of crashing.
6. **Chat Application (`/api/ask`):** User queries are matched directly against the completely structured `context.txt` data via stream responses using the same Sarvam AI endpoints.

## ⚙️ Installation & Setup

1. **Clone the Repository**

2. **Install System Dependencies**
    - Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
    - Ensure it is located in `C:\Program Files\Tesseract-OCR\tesseract.exe` (or modify `app.py` appropriately).

3. **Install Python Libraries**
    ```bash
    pip install -r requirements.txt
    ```

4. **Environment Variables**
    - Create a `.env` file in the root directory.
    - Set `SARVAMAI_KEY=your_api_key` using your valid API key.

5. **Run the Dashboard**
    ```bash
    python app.py
    ```
    Navigate to `http://localhost:8000` in your web browser.

## 🗄️ Core Dependencies

- **FastAPI / Uvicorn:** For high performance async routes.
- **PyMuPDF (`fitz`):** For blazingly fast PDF splitting and text mining.
- **PyTesseract:** Intelligent fallback for scanned images and bad quality pages.
- **Sarvam AI Python Client:** Cloud communication for high-performance Large Language models (`sarvam-30b`).
