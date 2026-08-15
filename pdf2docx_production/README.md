# PDF to DOCX Converter


- OCR support for scanned pages
- Fidelity checking to verify output matches source
- Layout diagnostics for troubleshooting
- OCR text recovery (makes scanned text searchable)
- Batch processing capabilities
- Command-line interface
- Advanced pdf2docx options for complex layouts

## Installation

```bash
pip install pdf2docx-production
```

Or install from source:

```bash
git clone https://github.com/example/pdf2docx-production.git
cd pdf2docx-production
pip install -e .
```

## System Dependencies

For full functionality, install these system dependencies:

### OCR Support (Tesseract)
- Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

### Fidelity Check (LibreOffice)
- Ubuntu/Debian: `sudo apt-get install libreoffice`
- macOS: `brew install --cask libreoffice`
- Windows: Download from https://www.libreoffice.org/download/download/

### Optional Enhancements
- Unpaper (image cleaning for OCR): `sudo apt-get install unpaper` or `brew install unpaper`
- Ghostscript (OCR quality improvement): `sudo apt-get install ghostscript` or `brew install ghostscript`

## Usage

### Command Line Interface

```bash
# Convert a single file with fidelity check
pdf2docx convert input.pdf output.docx --verify

# Convert all PDFs in a folder
pdf2docx convert input_pdfs/ --output-dir output_docs/

# Convert specific pages (0-indexed, end is exclusive)
pdf2docx convert input.pdf output.docx --start-page 1 --end-page 4

# Force OCR even if the file appears to have text
pdf2docx convert input.pdf output.docx --force-ocr

# Process a password-protected PDF
pdf2docx convert input.pdf output.docx --password secret123

# Enable advanced table detection
pdf2docx convert input.pdf output.docx --extract-stream-table

# Use multiprocessing for large files
pdf2docx convert input.pdf output.docx --multi-processing --cpu-count 4

# Check system capabilities
pdf2docx info --verbose
```

### As a Python Module

```python
from pdf2docx import convert_pdf_to_docx, convert_pdfs

# Single file conversion
result = convert_pdf_to_docx("input.pdf", "output.docx", verify=True)
print(result.summary())

# Batch conversion
results = convert_pdfs("input_pdfs/", output_dir="output_docs/")
for r in results:
    print(r.summary())
```

## Features

### OCR Support
Automatically detects scanned pages and applies OCR when Tesseract is available. OCR text is appended as a searchable supplement to maintain text accessibility.

### Fidelity Verification
When LibreOffice is available, performs visual comparison between source PDF and converted DOCX to verify formatting accuracy.

### Advanced Layout Options
- `extract_stream_table`: Better detection of tables without clear borders
- `extract_font`: Preserve font information (increases file size)
- `extract_margin`: Crop margins during conversion
- `extract_pages`: Convert specific non-consecutive pages
- `img_dpi`: Control image extraction resolution
- `multi_processing`: Speed up conversion on multi-core systems

## Output

The converter returns structured results including:
- Success/failure status
- OCR usage information
- Fidelity report (text similarity, page counts, character counts)
- Warning messages for potential issues
- Visual comparison images (when fidelity checking is enabled)

## Limitations

- PDF2DOCX cannot reconstruct editable layout from scanned pages — it embeds them as pictures
- Complex layouts (multi-column magazine-style pages) may shift
- Text-similarity score is a rough signal; check rendered comparison images for visual accuracy
- Forms or interactive elements may not convert perfectly

## License

MIT License - see LICENSE file for details.
