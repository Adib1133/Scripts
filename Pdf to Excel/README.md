# PDF → Excel Converter

A Python/Jupyter Notebook utility that automatically converts **every PDF file in the notebook's folder** into an individual `.xlsx` workbook.

The converter uses `pdfplumber` to extract tables and text from each PDF and `openpyxl` to create a formatted Excel workbook.

## Features

- Automatically finds all `.pdf` files in the notebook's folder.
- Converts each PDF into its own Excel workbook.
- Extracts tables from PDF pages when tables are detected.
- Extracts text lines from pages that do not contain tables.
- Preserves page separation in the generated workbook.
- Labels multiple tables found on the same page.
- Applies consistent Excel formatting.
- Alternates row shading for table readability.
- Adds borders, fonts, alignment, and header styling.
- Automatically adjusts column widths.
- Creates a `Content` worksheet for each converted PDF.
- Reports successful and failed conversions in the console.
- Continues processing other PDFs if one file fails.

## How It Works

The notebook follows this workflow:

```text
PDF files in folder
        │
        ▼
Find all *.pdf files
        │
        ▼
Open PDF with pdfplumber
        │
        ▼
Process each page
   ┌────┴────┐
   │         │
Tables     Text
   │         │
   └────┬────┘
        ▼
Create Excel workbook
        │
        ▼
Apply formatting
        │
        ▼
Save as <PDF name>.xlsx
```

## Requirements

- Python 3.x
- Jupyter Notebook or JupyterLab
- `pdfplumber`
- `openpyxl`
- `pypdf`

Install the dependencies with:

```bash
pip install pdfplumber openpyxl pypdf
```

The notebook also contains an installation cell:

```python
%pip install pdfplumber openpyxl pypdf --quiet
```

## Usage

### 1. Open the Notebook

Open:

```text
Pdf to Excel(1).ipynb
```

in Jupyter Notebook, JupyterLab, or another compatible notebook environment.

### 2. Add Your PDFs

Place one or more PDF files in the same folder as the notebook.

For example:

```text
project-folder/
├── Pdf to Excel(1).ipynb
├── invoice.pdf
├── report.pdf
└── statement.pdf
```

### 3. Run the Notebook

Run the cells from top to bottom.

The notebook automatically searches the working directory for files matching:

```text
*.pdf
```

Each PDF is processed independently.

### 4. Find the Excel Files

For every successfully processed PDF, an Excel file is created using the same base filename.

Example:

```text
invoice.pdf
report.pdf
statement.pdf
```

becomes:

```text
invoice.xlsx
report.xlsx
statement.xlsx
```

The generated files are saved in the same directory as the PDFs.

## PDF Processing

Each PDF is opened using `pdfplumber`.

For every page, the notebook attempts to extract:

### Tables

The converter calls:

```python
page.extract_tables()
```

If tables are found, they are written to the Excel worksheet as structured rows and columns.

### Text

The converter also extracts page text using:

```python
page.extract_text()
```

Text is split into individual non-empty lines.

When a page contains **no detected tables**, its extracted text lines are written to Excel.

This behavior is intentional: it avoids writing the same page content twice when a table has already been extracted.

## Excel Output

Each PDF generates one workbook containing a worksheet named:

```text
Content
```

The worksheet includes:

- PDF filename as the document title
- Page labels
- Extracted tables
- Extracted text for pages without tables
- Table labels when multiple tables occur on a page
- Blank spacing between sections

### Example Layout

A generated workbook may look conceptually like:

```text
DOCUMENT NAME

  Page 1

Table 1
┌──────────┬──────────┬──────────┐
│ Header 1 │ Header 2 │ Header 3 │
├──────────┼──────────┼──────────┤
│ Data     │ Data     │ Data     │
│ Data     │ Data     │ Data     │
└──────────┴──────────┴──────────┘


  Page 2

Text extracted from the page...
Additional text...
```

## Formatting

The generated Excel workbook uses predefined styles for readability.

### Table Headers

Headers use:

- Arial
- Bold text
- White font
- Blue background
- Center alignment
- Thin borders
- Wrapped text

### Table Data

Data cells use:

- Arial 10pt
- Left alignment
- Wrapped text
- Thin borders

Alternate table rows receive a light fill to improve readability.

### Page Labels

Each page is identified using a blue page label such as:

```text
Page 1
```

### Document Title

The PDF filename is placed at the top of the worksheet using a larger, bold font.

## Automatic Column Widths

After all content has been written, the notebook automatically calculates column widths based on the content.

The width is constrained between:

```text
Minimum: 12
Maximum: 60
```

This prevents extremely short columns while also preventing very long text from creating excessively wide worksheets.

## Multiple Tables on a Page

If a PDF page contains more than one detected table, each table is processed separately.

The workbook labels them as:

```text
Table 1
Table 2
Table 3
```

and places them sequentially in the `Content` worksheet.

## Pages Without Extractable Content

If a page contains neither detected tables nor extractable text, the workbook records:

```text
(no extractable content on this page)
```

This makes it clear that the page was processed but did not provide content that the extraction libraries could read.

## Batch Conversion

The notebook is designed for batch processing.

If a folder contains:

```text
January.pdf
February.pdf
March.pdf
April.pdf
```

the notebook attempts to convert all four files during a single run.

The console reports the result for every file and provides a final summary:

```text
---------------------------------------------
  Converted : 4
  Failed    : 0
  Location  : ...
```

## Error Handling

If no PDFs are found, the notebook displays:

```text
No PDF files found in: ...
Place your PDFs in the same folder as this notebook and re-run.
```

If an individual PDF fails during processing, the error is reported and the notebook continues with the remaining PDFs.

Example:

```text
  Converting : damaged.pdf
  Output     : damaged.xlsx
  ✗ Failed: ...
```

This means one problematic file does not necessarily prevent other PDFs from being converted.

## Example Console Output

A successful conversion produces output similar to:

```text
Found 2 PDF(s) in: C:\...\project-folder

  Converting : invoice.pdf
  Output     : invoice.xlsx
  ✓ Done  (5 page(s), 8 table(s))

  Converting : report.pdf
  Output     : report.xlsx
  ✓ Done  (3 page(s), 2 table(s))

---------------------------------------------
  Converted : 2
  Failed    : 0
  Location  : C:\...\project-folder
```

The actual number of pages and tables depends on the input PDFs.

## Project Structure

A basic project setup:

```text
project-folder/
├── Pdf to Excel(1).ipynb
├── document1.pdf
├── document2.pdf
├── document1.xlsx
└── document2.xlsx
```

## Important Notes

### PDF Type Matters

This notebook relies on text/table extraction through `pdfplumber`.

It works best with PDFs containing actual selectable text and structured tables.

Scanned PDFs or image-only PDFs may not produce useful text or table extraction without an OCR step.

### Complex PDF Layouts

PDFs do not inherently store information in the same row-and-column structure as Excel files. Complex layouts, merged cells, multi-column documents, floating text, or unusual table structures may therefore require additional processing.

### Formatting Preservation

The converter creates a **new Excel workbook**. It does not attempt to reproduce the original PDF's exact visual design.

Instead, it applies a consistent spreadsheet-oriented format optimized for readability.

### Output File Names

The output filename is generated from the PDF filename:

```text
example.pdf → example.xlsx
```

If an Excel file with the same name already exists, the current implementation saves to that path and may overwrite the existing workbook.

## Limitations

- No OCR processing is included.
- Image-only/scanned PDFs may not extract correctly.
- Highly complex tables may not be reconstructed perfectly.
- Original PDF visual formatting is not preserved exactly.
- PDF graphics and images are not exported as Excel objects.
- The extraction quality depends on the structure and encoding of the source PDF.
- The notebook processes PDFs found in its resolved working directory; it does not provide a graphical file-selection interface.

## Technologies Used

| Technology | Purpose |
| --- | --- |
| Python | Core programming language |
| Jupyter Notebook | Interactive execution environment |
| pdfplumber | PDF text and table extraction |
| openpyxl | Excel workbook generation and formatting |
| pathlib | File and directory handling |
| pypdf | PDF-related dependency installed by the notebook |

## License

This project is for internal workplace use.

## Author

Created as a workplace automation tool for PDF-to-Excel automation utility for batch extraction and spreadsheet generation.