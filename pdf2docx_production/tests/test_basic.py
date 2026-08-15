"""Basic tests for the PDF to DOCX converter."""

import unittest
import tempfile
import os
from pathlib import Path
from pdf2docx.converter import (
    sparse_page_indices,
    is_scanned,
    _open_pdf,
    CAPS,
    logger
)

class TestConverter(unittest.TestCase):
    """Test cases for the PDF to DOCX converter."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = Path(__file__).parent.parent
        self.sample_pdf = self.test_dir / "input_pdfs" / "AFM.pdf"

        # Skip tests if no sample PDF is available
        if not self.sample_pdf.exists():
            self.skipTest("No sample PDF available for testing")

    def test_open_pdf(self):
        """Test that we can open a PDF file."""
        doc = _open_pdf(str(self.sample_pdf))
        self.assertIsNotNone(doc)
        self.assertGreater(len(doc), 0)
        doc.close()

    def test_sparse_page_indices(self):
        """Test sparse page indices detection."""
        indices = sparse_page_indices(str(self.sample_pdf))
        self.assertIsInstance(indices, list)
        # All indices should be integers
        for i in indices:
            self.assertIsInstance(i, int)
            self.assertGreaterEqual(i, 0)

    def test_is_scanned(self):
        """Test scanned document detection."""
        result = is_scanned(str(self.sample_pdf))
        self.assertIsInstance(result, bool)
        logger.info(f"Document is_scanned: {result}")

    def test_dependencies(self):
        """Test that dependencies are properly checked."""
        self.assertIn('ocrmypdf_installed', CAPS)
        self.assertIn('tesseract', CAPS)
        self.assertIn('ghostscript', CAPS)
        self.assertIn('unpaper', CAPS)
        self.assertIn('libreoffice', CAPS)

if __name__ == '__main__':
    unittest.main()