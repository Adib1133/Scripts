# Excel Modification and Sorting

A Python-based Excel automation script that reads a sales workbook,
detects the data header automatically, cleans and sorts customer records
by phone number, identifies frequent buyers, and generates a formatted
customer-wise sales report.

## Overview

This project is designed to automate a recurring Excel sales-reporting
task.

The script:

-   Supports `.xls` and `.xlsx` input files.
-   Automatically searches for `input.xlsx` or `input.xls`.
-   Detects the header row by locating the `CUSTOMER PHONE` column.
-   Preserves non-empty information appearing above the detected header
    as report metadata.
-   Cleans customer phone-number values.
-   Sorts records by customer phone number.
-   Identifies customers whose phone number appears more than once.
-   Highlights frequent buyers using six rotating colors.
-   Creates a formatted Excel workbook with optimized column widths.
-   Freezes the report header for easier navigation.
-   Adds a `Legend` worksheet explaining the color coding.
-   Names the output using the previous day's date.

## Requirements

-   Python 3.10+ recommended
-   pandas
-   openpyxl
-   xlrd

Install the required packages with:

``` bash
pip install pandas openpyxl xlrd
```

The notebook itself uses Python 3 and was developed/tested with Python
3.14.2.

## Input File

Place one of the following files in the same folder as the
notebook/script:

``` text
input.xlsx
```

or

``` text
input.xls
```

If both files exist, `input.xlsx` is selected first.

### Required Column

The workbook must contain a column named:

``` text
CUSTOMER PHONE
```

The script checks the first 30 rows to locate the header row. This
allows it to handle files where report information or other metadata
appears above the actual table header.

## How It Works

### 1. Locate the Input File

The script checks the working folder for:

1.  `input.xlsx`
2.  `input.xls`

If neither file is found, the program stops and displays the expected
location and filenames.

### 2. Detect the Header

The first 30 rows are inspected for the `CUSTOMER PHONE` column.

Once found, that row is treated as the Excel table header.

### 3. Preserve Metadata

Non-empty values appearing above the detected header are collected and
written near the top of the generated report.

### 4. Clean Phone Numbers

Phone values are normalized where possible. Numeric values such as
Excel-style numeric phone values are converted to integer-like strings,
while other values are stripped of surrounding whitespace.

Blank phone values are retained as blank.

### 5. Sort Customer Records

Records are sorted by `CUSTOMER PHONE`.

Phone values with five or fewer characters are placed after valid
phone-number values.

### 6. Identify Frequent Buyers

A customer is considered a **frequent buyer** when the same valid phone
number appears more than once.

Phone numbers with more than four characters are included in the
frequency calculation.

### 7. Highlight Frequent Buyers

Frequent buyers are assigned one of six rotating highlight colors:

-   Yellow
-   Orange
-   Green
-   Blue
-   Purple
-   Pink

All rows belonging to the same phone number receive the same assigned
color.

### 8. Generate the Report

The output workbook contains two worksheets:

#### `Customer Sales Report`

Contains:

-   Preserved metadata
-   A report note
-   The sorted sales data
-   Formatted headers
-   Highlighted frequent buyers
-   Optimized column widths
-   Frozen panes for easier scrolling

#### `Legend`

Explains:

-   Unhighlighted rows = customer purchased once
-   Highlighted rows = phone number appears more than once
-   The six rotating colors used for customer groups

## Output

The generated workbook is named:

``` text
Customer Wise Sales Report of DD-MM-YYYY.xlsx
```

The date used is **yesterday's date**.

For example, if the script runs on May 13, 2026, the output will be:

``` text
Customer Wise Sales Report of 12-05-2026.xlsx
```

The output is saved in the same folder from which the script is running.

## Expected Input Structure

The exact input workbook can contain report information above the table,
followed by a header similar to:

  -----------------------------------------------------------------------
  DATE        CUSTOMER    CUSTOMER    CUSTOMER    SALESMAN    INVOICE NO.
              CODE        NAME        PHONE                   
  ----------- ----------- ----------- ----------- ----------- -----------
  ...         ...         ...         ...         ...         ...

  -----------------------------------------------------------------------

The script does not require the header to be on the first row, but
`CUSTOMER PHONE` must appear within the first 30 rows.

## Supported Columns

The script has predefined widths for commonly used sales-report columns,
including:

-   `DATE`
-   `CUSTOMER CODE`
-   `CUSTOMER NAME`
-   `CUSTOMER PHONE`
-   `SALESMAN`
-   `EMPLOYER NAME`
-   `INVOICE NO`
-   `COST VALUE`
-   `TOTAL`
-   `VAT AMT`
-   `DISC AMT`
-   `EXG AMT`
-   `RTN AMT`
-   `ADJ AMT`
-   `NET AMT`
-   `CASH AMT`
-   `CARD AMT`
-   `PAYMENT TYPE`
-   `RTN INV REF`
-   `ADV AMT`
-   `RDM VAL`

Other columns are assigned a default width.

## Running the Notebook

Open the notebook:

``` text
Excel Modification and Sorting.ipynb
```

Run the installation cell first if the required packages are not
installed, then execute the main code cell.

Alternatively, the code can be exported to a Python script and executed
from the same folder as the input Excel file.

## Example Console Output

A successful run reports information similar to:

``` text
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

The numbers above are an example from a previous execution and will vary
depending on the input workbook.

## Error Handling

The script currently handles the main expected input problems:

### No input file

If `input.xls` or `input.xlsx` cannot be found, the script displays the
folder where the file should be placed.

### Missing `CUSTOMER PHONE` column

If the required column cannot be found within the first 30 rows, the
script stops and reports that the expected header could not be located.

## Project Structure

A simple setup can look like this:

``` text
project-folder/
├── Excel Modification and Sorting.ipynb
├── input.xlsx
└── Customer Wise Sales Report of DD-MM-YYYY.xlsx
```

If the notebook is converted into a Python script:

``` text
project-folder/
├── Excel Modification and Sorting.py
├── input.xlsx
└── Customer Wise Sales Report of DD-MM-YYYY.xlsx
```

## Important Notes

-   The script creates a new workbook rather than modifying the original
    input workbook in place.
-   The original Excel file is not overwritten.
-   The script currently searches for fixed filenames: `input.xlsx` and
    `input.xls`.
-   The header detection depends on the presence of `CUSTOMER PHONE`.
-   Phone-number cleaning is designed primarily for numeric/text values
    commonly encountered in Excel exports.
-   The generated workbook uses `openpyxl` for formatting and writing.
-   `.xls` files are read using `xlrd`, while `.xlsx` files are read
    using `openpyxl`.
-   The notebook's current implementation reconstructs the report and
    preserves textual metadata found above the header; it does not
    preserve all original Excel workbook-level formatting, formulas,
    charts, or workbook properties.

## License

This project is for internal workplace use.



## Author

Created as a workplace automation tool for processing and organizing
Excel sales data.
