# CWSR — Customer Wise Sales Report

**CWSR (Customer Wise Sales Report)** is a Python/Jupyter Notebook automation tool for processing Excel sales data and generating a clean, customer-wise sales report.

The script reads an `input.xls` or `input.xlsx` file, automatically detects the table header using the `CUSTOMER PHONE` column, cleans and sorts customer records by phone number, identifies customers with multiple purchases, and produces a formatted Excel report with color-coded frequent buyers.

## Features

- Supports both `.xls` and `.xlsx` input files.
- Automatically searches for `input.xlsx` first, then `input.xls`.
- Detects the header row automatically by looking for `CUSTOMER PHONE`.
- Searches the first 30 rows for the header.
- Preserves non-empty metadata appearing above the detected header.
- Cleans customer phone-number values.
- Sorts sales records by customer phone number.
- Identifies frequent buyers based on repeated phone numbers.
- Uses six rotating colors to group frequent buyers.
- Generates a formatted `Customer Sales Report` worksheet.
- Creates a separate `Legend` worksheet.
- Applies predefined column widths for common sales fields.
- Freezes the data header for easier navigation.
- Automatically generates an output filename using the previous day's date.
- Prints processing progress and a final summary to the console.

## How It Works

The overall workflow is:

```text
Input Excel File
      │
      ▼
Find input.xls / input.xlsx
      │
      ▼
Detect "CUSTOMER PHONE" header
      │
      ▼
Preserve metadata above header
      │
      ▼
Load and clean sales data
      │
      ▼
Sort by customer phone
      │
      ▼
Find repeated phone numbers
      │
      ▼
Assign rotating highlight colors
      │
      ▼
Create formatted Excel workbook
      │
      ├── Customer Sales Report
      │
      └── Legend
      │
      ▼
Save dated .xlsx report
```

## Requirements

- Python 3.x
- Jupyter Notebook / JupyterLab
- pandas
- openpyxl
- xlrd

Install the dependencies with:

```bash
pip install pandas openpyxl xlrd
```

The notebook contains the installation command:

```python
pip install pandas openpyxl xlrd
```

## Input File

The script expects an Excel file in the same folder as the notebook or executed Python script.

Supported filenames:

```text
input.xlsx
```

or:

```text
input.xls
```

If both files are present, `input.xlsx` takes priority.

### Required Column

The input workbook must contain a column named:

```text
CUSTOMER PHONE
```

The script searches the first **30 rows** to locate this header.

This allows the workbook to contain report titles, company information, dates, or other metadata before the actual table.

## Example Input Structure

The input workbook may look conceptually like:

```text
Company Name
Sales Report
Report Date: 12-05-2026

DATE | CUSTOMER CODE | CUSTOMER NAME | CUSTOMER PHONE | SALESMAN | ...
-----|---------------|---------------|----------------|----------|-----
...  | ...           | ...           | ...            | ...      |
...  | ...           | ...           | ...            | ...      |
```

The script detects the row containing `CUSTOMER PHONE` and treats it as the table header.

## Phone Number Cleaning

Customer phone values are normalized before sorting and frequency analysis.

The script:

- Converts numeric Excel values into integer-style strings when possible.
- Removes surrounding whitespace from text values.
- Converts blank or `NaN` values to an empty string.
- Leaves non-numeric phone values as cleaned text.

For example:

```text
01712345678
```

remains a phone-number string, while an Excel numeric representation may be converted to its integer-style representation.

## Sorting

Records are sorted by:

```text
CUSTOMER PHONE
```

Phone values containing more than four characters are considered valid for the primary sorting logic.

Values that are blank or contain four or fewer characters are placed after the valid phone numbers.

## Frequent Buyer Detection

A customer is classified as a **frequent buyer** when the same valid customer phone number appears more than once.

The relevant logic is:

```python
valid = df['CUSTOMER PHONE'][df['CUSTOMER PHONE'].str.len() > 4]
counts = valid.value_counts()
frequent = set(counts[counts > 1].index)
```

Therefore:

- Phone number length ≤ 4 → excluded from frequency analysis.
- Phone number length > 4 and appears once → regular customer.
- Phone number length > 4 and appears more than once → frequent buyer.

## Color Coding

Frequent buyers are assigned one of six rotating colors:

| Color | Purpose |
| --- | --- |
| Yellow | Frequent buyer group |
| Orange | Frequent buyer group |
| Green | Frequent buyer group |
| Blue | Frequent buyer group |
| Purple | Frequent buyer group |
| Pink | Frequent buyer group |

The same phone number receives the same assigned color across all of its rows.

The color assignment cycles through the six available colors.

## Generated Workbook

The output workbook contains two worksheets.

### 1. Customer Sales Report

This is the primary report.

It contains:

- Preserved metadata
- A sorting/highlighting note
- Sales table
- Formatted headers
- Customer records
- Highlighted frequent buyers
- Optimized column widths
- Frozen panes

The worksheet is named:

```text
Customer Sales Report
```

### 2. Legend

The second worksheet explains the color coding.

It contains:

- Color legend
- Meaning of highlighted rows
- Number of frequent-buyer phone numbers
- Explanation that each color group represents the same customer/phone number

The worksheet is named:

```text
Legend
```

## Output Filename

The report is automatically named:

```text
Customer Wise Sales Report of DD-MM-YYYY.xlsx
```

The date is calculated as **yesterday's date**.

For example, if the script is run on:

```text
13-05-2026
```

the output filename will be:

```text
Customer Wise Sales Report of 12-05-2026.xlsx
```

The generated workbook is saved in the same folder as the input file.

## Formatting

### Main Report

The report uses:

- Arial font
- Bold white header text
- Dark blue header background
- Centered and wrapped header text
- Individual customer-group highlight colors
- Predefined column widths
- Frozen panes

### Metadata

The first metadata line is displayed in a larger, bold font.

Additional metadata lines use a smaller Arial font.

### Report Note

The report includes:

```text
Sorted by Customer Phone  |  Highlighted = Frequent Buyer
```

## Supported Column Widths

The script contains predefined widths for commonly used sales-report columns:

| Column | Width |
| --- | ---: |
| DATE | 13 |
| CUSTOMER CODE | 15 |
| CUSTOMER NAME | 24 |
| CUSTOMER PHONE | 16 |
| SALESMAN | 13 |
| EMPLOYER NAME | 18 |
| INVOICE NO | 17 |
| COST VALUE | 12 |
| TOTAL | 12 |
| VAT AMT | 11 |
| DISC AMT | 11 |
| EXG AMT | 11 |
| RTN AMT | 11 |
| ADJ AMT | 11 |
| NET AMT | 12 |
| CASH AMT | 12 |
| CARD AMT | 12 |
| PAYMENT TYPE | 14 |
| RTN INV REF | 15 |
| ADV AMT | 11 |
| RDM VAL | 11 |

Any other column receives a default width of `13`.

## Usage

### Option 1 — Run in Jupyter Notebook

1. Open `CWSR.ipynb`.
2. Place `input.xlsx` or `input.xls` in the notebook's working folder.
3. Run the dependency-installation cell if necessary.
4. Run the main code cell.
5. Check the generated `.xlsx` report.

### Option 2 — Export to Python

The notebook's main code can be exported to a Python script and executed from the same directory as the input file.

A typical structure is:

```text
project-folder/
├── CWSR.ipynb
├── input.xlsx
└── Customer Wise Sales Report of DD-MM-YYYY.xlsx
```

## Console Output

A successful execution produces output similar to:

```text
Input  : C:\...\input.xls
Output : C:\...\Customer Wise Sales Report of 12-05-2026.xlsx

[1/4] Reading file...
        56,037 data rows loaded.
[2/4] Sorting by phone number...
[3/4] Identifying frequent buyers...
        12,628 unique phone numbers with multiple purchases.
[4/4] Writing output.xlsx...

  ✓ Done!
  Total rows      : 56,037
  Frequent buyers : 12,628
  Saved to        : C:\...\Customer Wise Sales Report of 12-05-2026.xlsx
```

The numbers shown above are illustrative; actual values depend on the input workbook.

## Error Handling

### Input File Not Found

If neither supported filename exists, the script reports:

```text
ERROR: No input file found.
Place your file in: ...
and name it: input.xls OR input.xlsx
```

### Required Header Not Found

If `CUSTOMER PHONE` cannot be found within the first 30 rows, the script stops and reports:

```text
ERROR: Could not find 'CUSTOMER PHONE' column in the file.
Make sure the file has the correct column headers.
```

## Important Notes

- The original input workbook is not modified directly.
- The script creates a new Excel workbook for the report.
- `input.xlsx` takes precedence over `input.xls` when both are present.
- Only the first 30 rows are searched for the required header.
- The frequency logic depends on `CUSTOMER PHONE`.
- Phone numbers with four or fewer characters are excluded from frequent-buyer detection.
- The generated workbook is created with `openpyxl`.
- `.xls` files are read using `xlrd`.
- `.xlsx` files are read using `openpyxl`.
- The report reconstructs the relevant data rather than preserving every feature of the original Excel workbook.

## Limitations

The current implementation does not attempt to preserve:

- Original workbook formatting
- Original formulas
- Charts
- Images
- Excel macros
- Existing worksheets
- Workbook-level properties

The output is a newly generated reporting workbook based on the extracted sales data and metadata.

## Performance

The script uses pandas for data processing and `openpyxl` for workbook creation.

For large sales files, the main processing stages are:

1. Reading the Excel workbook.
2. Sorting the DataFrame.
3. Counting repeated phone numbers.
4. Writing every record into the new workbook.

Very large datasets may therefore require additional time and memory during workbook generation.

## Project Structure

Recommended structure:

```text
CWSR/
├── CWSR.ipynb
├── input.xlsx
└── Customer Wise Sales Report of DD-MM-YYYY.xlsx
```

## Technologies Used

| Technology | Purpose |
| --- | --- |
| Python | Core programming language |
| Jupyter Notebook | Interactive development/execution |
| pandas | Excel reading and data processing |
| openpyxl | Excel workbook creation and formatting |
| xlrd | Reading legacy `.xls` files |

## License

This project is for internal workplace use.

## Author

Created as a workplace automation tool for Excel-to-Excel automation utility for finding similarities to prevent suspicious activities.
