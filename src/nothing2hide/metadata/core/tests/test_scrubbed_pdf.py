import os
import tempfile
import unittest

from nothing2hide.metadata.core.scrubber.pdf import PdfFile

here = os.path.abspath(os.path.dirname(__file__))


class TestPdfFile(unittest.TestCase):
    def setUp(self):
        self.test_pdf_filename = os.path.join(here, "data", "pdf", "n2h.pdf")
        self.test_pdf = PdfFile(self.test_pdf_filename)

    def test_init(self):
        self.assertEqual(self.test_pdf.pdf_filename, self.test_pdf_filename)
        self.assertEqual(self.test_pdf.metadata, [])

    def test_rescue_metadata(self):
        metadata = self.test_pdf.rescue_metadata()
        self.assertListEqual(
            metadata,
            [
                'Author', 'Title', 'Subject', 'Creator',
                'Producer', 'Keywords', 'CreationDate', 'ModDate',
                'Trapped', 'PTEX.Fullbanner'
            ]
        )

    def test_remove_metadata(self):
        self.test_pdf.rescue_metadata()
        self.test_pdf.remove_metadata()
        for metadata in self.test_pdf.metadata:
            self.assertIsNone(self.test_pdf.pdf_file.Info[metadata])

    def test_save_newfile(self):
        test_tmp_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_pdf.rescue_metadata()
        self.test_pdf.remove_metadata()
        self.test_pdf.save(outfile=test_tmp_file.name)
        tmp_file_metadata = PdfFile(test_tmp_file.name).rescue_metadata()
        self.assertListEqual(tmp_file_metadata, [])
        os.remove(test_tmp_file.name)

    def test_save_erase(self):
        self.test_pdf.rescue_metadata()
        self.test_pdf.remove_metadata()
        new_pdf_file_name = self.test_pdf.save()
        tmp_file_metadata = PdfFile(new_pdf_file_name).rescue_metadata()
        self.assertListEqual(tmp_file_metadata, [])
        os.remove(new_pdf_file_name)
