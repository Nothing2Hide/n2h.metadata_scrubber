import unittest
import os
import tempfile
import zipfile
import shutil
from lxml import etree

from nothing2hide.metadata.core.scrubber.docx import DocxFile

here = os.path.abspath(os.path.dirname(__file__))


class TestPdfFile(unittest.TestCase):

    def setUp(self):
        test_docx_filename = os.path.join(here, "data", "docx", "test.docx")
        test_xlsx_filename = os.path.join(here, "data", "docx", "test.xlsx")
        self.test_bad_filename = os.path.join(here, "data", "pdf", "n2h.pdf")
        self.test_docx = DocxFile(test_docx_filename)
        self.test_xlsx = DocxFile(test_xlsx_filename)

    def test_init(self):
        self.assertIsNotNone(self.test_docx.xml_content)
        self.assertIsNotNone(self.test_xlsx.xml_content)
        self.assertRaises(ValueError, DocxFile, self.test_bad_filename)

    def test_remove_metadata(self):
        self.test_docx.remove_metadata()
        root = self.test_docx.xml_content.getroottree().getroot()
        for elt in root:
            self.assertEqual(len(elt.text), 0)

        self.test_xlsx.remove_metadata()
        root = self.test_xlsx.xml_content.getroottree().getroot()
        for elt in root:
            self.assertEqual(len(elt.text), 0)

    def test_save(self):
        self.test_docx.remove_metadata()
        tmp_dir = tempfile.mkdtemp()
        save_filename = os.path.join(tmp_dir, "test_save.docx")
        self.test_docx.save(save_filename)
        unziped = zipfile.ZipFile(save_filename)
        xml_content = etree.fromstring(unziped.read('docProps/core.xml'))
        root = xml_content.getroottree().getroot()
        for elt in root:
            self.assertIsNone(elt.text)
        shutil.rmtree(tmp_dir)

        self.test_xlsx.remove_metadata()
        tmp_dir = tempfile.mkdtemp()
        save_filename = os.path.join(tmp_dir, "test_save.xlsx")
        self.test_xlsx.save(save_filename)
        unziped = zipfile.ZipFile(save_filename)
        xml_content = etree.fromstring(unziped.read('docProps/core.xml'))
        root = xml_content.getroottree().getroot()
        for elt in root:
            self.assertIsNone(elt.text)
        shutil.rmtree(tmp_dir)
