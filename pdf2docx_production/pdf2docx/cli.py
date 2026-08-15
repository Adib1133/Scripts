#!/usr/bin/env python3
"""Command-line interface for the PDF to DOCX converter."""

import argparse
import sys
import os
import logging
from pathlib import Path

# Ensure we import our package, not the external one
# Get the directory where this script is located
_script_dir = Path(__file__).resolve().parent
_package_dir = _script_dir.parent  # pdf2docx_production directory
print(f"[DEBUG] Script dir: {_script_dir}")
print(f"[DEBUG] Package dir: {_package_dir}")
print(f"[DEBUG] Sys path before: {sys.path[:3]}...")
if str(_package_dir) not in sys.path:
    sys.path.insert(0, str(_package_dir))
    print(f"[DEBUG] Added package dir to sys.path")
print(f"[DEBUG] Sys path after: {sys.path[:3]}...")

# Import from our package
print(f"[DEBUG] Attempting to import from pdf2docx")
from pdf2docx import (
    convert_pdf_to_docx,
    convert_pdfs,
    ConversionResult,
    FidelityReport,
    CAPS,
    logger as pdf2docx_logger
)
print(f"[DEBUG] Import successful")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to DOCX with OCR support and fidelity checking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
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
        """
    )

    # Add global arguments
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--log-file', help='Log to file in addition to console')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert PDF to DOCX')
    convert_parser.add_argument('input', help='Input PDF file or directory')
    convert_parser.add_argument('output', nargs='?', help='Output DOCX file (required for single file input)')
    convert_parser.add_argument('--output-dir', help='Output directory for batch conversion')
    convert_parser.add_argument('--start-page', type=int, default=0, help='Start page (0-indexed)')
    convert_parser.add_argument('--end-page', type=int, help='End page (exclusive)')
    convert_parser.add_argument('--pages', type=int, nargs='+', help='Specific pages to convert (0-indexed)')
    convert_parser.add_argument('--password', help='Password for encrypted PDFs')
    convert_parser.add_argument('--force-ocr', action='store_true', help='Force OCR on all pages')
    convert_parser.add_argument('--no-ocr', action='store_true', help='Skip OCR even if needed')
    convert_parser.add_argument('--append-ocr-text', action='store_true', default=True,
                               help='Append OCR text as searchable supplement')
    convert_parser.add_argument('--verify', action='store_true', help='Enable fidelity check')
    convert_parser.add_argument('--verify-max-pages', type=int, default=3,
                               help='Maximum pages to check for fidelity (default: 3)')

    # Advanced pdf2docx options
    convert_parser.add_argument('--extract-stream-table', action='store_true',
                               help='Enable borderless table detection')
    convert_parser.add_argument('--extract-font', action='store_true',
                               help='Preserve font information')
    convert_parser.add_argument('--extract-margin', type=float, nargs=4,
                               metavar=('LEFT', 'TOP', 'RIGHT', 'BOTTOM'),
                               help='Crop margins during conversion')
    convert_parser.add_argument('--extract-pages', type=int, nargs='+',
                               help='Convert specific non-consecutive pages')
    convert_parser.add_argument('--img-dpi', type=int, default=140,
                               help='Control image extraction resolution (default: 140)')
    convert_parser.add_argument('--multi-processing', action='store_true',
                               help='Speed up conversion on multi-core systems')
    convert_parser.add_argument('--cpu-count', type=int,
                               help='Number of CPU cores to use for multiprocessing')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show system capabilities and dependencies')
    info_parser.add_argument('--verbose', '-v', action='store_true',
                            help='Enable verbose output')

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    pdf2docx_logger.setLevel(log_level)

    # Clear existing handlers and add new ones
    for handler in pdf2docx_logger.handlers[:]:
        pdf2docx_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    pdf2docx_logger.addHandler(console_handler)

    # File handler if specified
    if args.log_file:
        try:
            file_handler = logging.FileHandler(args.log_file)
            file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(file_formatter)
            pdf2docx_logger.addHandler(file_handler)
        except Exception as e:
            pdf2docx_logger.error(f"Could not open log file {args.log_file}: {e}")

    if args.command == 'info':
        show_info(args.verbose)
        return 0
    elif args.command == 'convert':
        return handle_convert(args)
    else:
        parser.print_help()
        return 1

def show_info(verbose: bool = False):
    """Show system capabilities and dependencies."""
    print("PDF to DOCX Converter - System Information")
    print("=" * 50)

    print("\nDependencies:")
    for name, available in CAPS.items():
        status = "[x]" if available else "[ ]"
        print(f"  {status} {name}")

    if verbose:
        print("\nOptional dependencies notes:")
        if not CAPS["tesseract"]:
            print("  -> No Tesseract: scanned PDFs will convert but won't be OCR'd.")
            print("     Install with: sudo apt-get install tesseract-ocr (Debian/Ubuntu) or brew install tesseract (macOS)")
        if not CAPS["libreoffice"]:
            print("  -> No LibreOffice ('soffice'): fidelity check will fall back to text-only comparison.")
            print("     Install with: sudo apt-get install libreoffice (Debian/Ubuntu) or brew install --cask libreoffice (macOS)")
        if not CAPS["unpaper"]:
            print("  -> No unpaper: optional image cleaning for OCR unavailable.")
            print("     Install with: sudo apt-get install unpaper (Debian/Ubuntu) or brew install unpaper (macOS)")
        if not CAPS["ghostscript"]:
            print("  -> No ghostscript: optional OCR quality improvement unavailable.")
            print("     Install with: sudo apt-get install ghostscript (Debian/Ubuntu) or brew install ghostscript (macOS)")

def handle_convert(args) -> int:
    """Handle the convert command."""
    input_path = Path(args.input)

    # Validate input
    if not input_path.exists():
        pdf2docx_logger.error(f"Input path does not exist: {input_path}")
        return 1

    # Determine if we're processing a single file or directory
    is_single_file = input_path.is_file() and input_path.suffix.lower() == ".pdf"
    is_directory = input_path.is_dir()

    if not (is_single_file or is_directory):
        pdf2docx_logger.error(f"Input must be a PDF file or directory containing PDFs: {input_path}")
        return 1

    # For single file, output file is required unless output-dir is specified
    if is_single_file and not args.output and not args.output_dir:
        pdf2docx_logger.error("Output file required for single file input (unless --output-dir is specified)")
        return 1

    # Prepare layout kwargs from command line arguments
    layout_kwargs = {}
    if args.extract_stream_table:
        layout_kwargs['extract_stream_table'] = True
    if args.extract_font:
        layout_kwargs['extract_font'] = True
    if args.extract_margin:
        layout_kwargs['extract_margin'] = args.extract_margin
    if args.extract_pages:
        layout_kwargs['extract_pages'] = args.extract_pages
    if args.img_dpi != 140:  # Only add if different from default
        layout_kwargs['img_dpi'] = args.img_dpi
    if args.multi_processing:
        layout_kwargs['multi_processing'] = True
    if args.cpu_count:
        layout_kwargs['cpu_count'] = args.cpu_count

    try:
        if is_single_file:
            # Single file conversion
            output_path = Path(args.output) if args.output else None
            output_dir = Path(args.output_dir) if args.output_dir else None

            if output_dir:
                output_dir.mkdir(parents=True, exist_ok=True)
                if not output_path:
                    output_path = output_dir / (input_path.stem + ".docx")
            elif not output_path:
                output_path = input_path.with_suffix(".docx")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            result = convert_pdf_to_docx(
                str(input_path),
                str(output_path),
                start_page=args.start_page,
                end_page=args.end_page,
                pages=args.pages,
                password=args.password,
                force_ocr=args.force_ocr,
                no_ocr=args.no_ocr,
                append_ocr_text=args.append_ocr_text,
                verify=args.verify,
                verify_max_pages=args.verify_max_pages,
                **layout_kwargs
            )

            print(result.summary())
            return 0 if result.success else 1

        else:
            # Directory batch conversion
            output_dir = Path(args.output_dir) if args.output_dir else None
            if output_dir:
                output_dir.mkdir(parents=True, exist_ok=True)

            results = convert_pdfs(
                str(input_path),
                str(output_dir) if output_dir else None,
                start_page=args.start_page,
                end_page=args.end_page,
                pages=args.pages,
                password=args.password,
                force_ocr=args.force_ocr,
                no_ocr=args.no_ocr,
                verify=args.verify,
                verify_max_pages=args.verify_max_pages,
                **layout_kwargs
            )

            # Print results
            for result in results:
                print(result.summary())

            # Return success if all conversions succeeded
            failed_count = sum(1 for r in results if not r.success)
            return 1 if failed_count > 0 else 0

    except Exception as e:
        pdf2docx_logger.error(f"Conversion failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())