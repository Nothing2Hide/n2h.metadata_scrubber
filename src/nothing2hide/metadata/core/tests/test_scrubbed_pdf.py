import os
import unittest

from nothing2hide.metadata.core.scrubber.pdf import PdfFile

here = os.path.abspath(os.path.dirname(__file__))


class TestPdfFile(unittest.TestCase):

    def test_init(self):
        test_pdf_filename = os.path.join(here, "data", "pdf", "n2h.pdf")
        test_pdf = PdfFile(test_pdf_filename)
        self.assertEqual(test_pdf.pdf_filename, test_pdf_filename)
        self.assertEqual(test_pdf.metadata, [])

    def test_rescue_metadata(self):
        test_pdf_filename = os.path.join(here, "data", "pdf", "n2h.pdf")
        test_pdf = PdfFile(test_pdf_filename)
        metadata = test_pdf.rescue_metadata()
        self.assertListEqual(
            metadata,
            [
                'Author', 'Title', 'Subject', 'Creator',
                'Producer', 'Keywords', 'CreationDate', 'ModDate',
                'Trapped', 'PTEX.Fullbanner'
            ]
        )

    def test_remove_metadata(self):
        test_pdf_filename = os.path.join(here, "data", "pdf", "n2h.pdf")
        test_pdf = PdfFile(test_pdf_filename)
        test_pdf.rescue_metadata()
        test_pdf.remove_metadata()
        for metadata in test_pdf.metadata:
            self.assertEqual(test_pdf.pdf_file.Info[metadata], None)
