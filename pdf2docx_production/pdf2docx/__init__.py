"""PDF to DOCX Converter - Production Ready Module"""

from .converter import (
    convert_pdf_to_docx,
    convert_pdfs,
    ConversionResult,
    FidelityReport,
    check_fidelity,
    debug_layout,
    _append_ocr_supplement,
    ocr_pdf,
    sparse_page_indices,
    is_scanned,
    CAPS,
    logger
)

__all__ = [
    "convert_pdf_to_docx",
    "convert_pdfs",
    "ConversionResult",
    "FidelityReport",
    "check_fidelity",
    "debug_layout",
    "_append_ocr_supplement",
    "ocr_pdf",
    "sparse_page_indices",
    "is_scanned",
    "CAPS",
    "logger"
]