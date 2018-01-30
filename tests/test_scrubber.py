import os
import tempfile
import unittest
import zipfile
import shutil
from xml.etree import ElementTree as etree

from n2h.metadata_scrubber.scrubber import (
    OdtFile, PdfFile, DocxFile, remove_metadata, default_output_filename,
    directory_scrubber
)

here = os.path.abspath(os.path.dirname(__file__))


class TestPdfFile(unittest.TestCase):

    def setUp(self):
        self.test_pdf_filename = os.path.join(here, "data", "dirty",
                                              "dirty_1.pdf")
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
        try:
            os.remove(test_tmp_file.name)
        except PermissionError:
            pass

    def test_save_erase(self):
        self.test_pdf.rescue_metadata()
        self.test_pdf.remove_metadata()
        new_pdf_file_name = self.test_pdf.save()
        tmp_file_metadata = PdfFile(new_pdf_file_name).rescue_metadata()
        self.assertListEqual(tmp_file_metadata, [])
        try:
            os.remove(new_pdf_file_name)
        except PermissionError:
            pass


class TestOdtFile(unittest.TestCase):

    def setUp(self):
        test_odt_filename = os.path.join(here, "data", "dirty", "dirty_1.odt")
        self.test_bad_filename = os.path.join(here, "data", "dirty",
                                              "dirty_0.pdf")
        self.test_bad_file = OdtFile(self.test_bad_filename)
        self.test_odt = OdtFile(test_odt_filename)
        self.test_odt.open()

    def tearDown(self):
        self.test_odt.close()

    def test_init(self):
        self.assertRaises(ValueError, self.test_bad_file.open)

    def test_remove_metadata(self):
        self.test_odt.remove_metadata()
        root = self.test_odt.xml.xml_contents['meta.xml'] \
            .getchildren()[0]
        self.assertTrue(len(root.getchildren()) == 0)

    def test_save(self):
        self.test_odt.remove_metadata()
        tmp_dir = tempfile.mkdtemp()
        save_filename = os.path.join(tmp_dir, "test_save.odt")
        self.test_odt.save(save_filename)
        unziped = zipfile.ZipFile(save_filename)
        xml_content = etree.fromstring(unziped.read('meta.xml'))
        root = xml_content.getchildren()[0]
        self.assertTrue(len(root.getchildren()) == 0)
        try:
            shutil.rmtree(tmp_dir)
        except PermissionError:
            pass


class TestDocxFile(unittest.TestCase):

    def setUp(self):
        test_docx_filename = os.path.join(here, "data", "dirty",
                                          "dirty_1.docx")
        test_xlsx_filename = os.path.join(here, "data", "dirty",
                                          "dirty_0.xlsx")
        self.test_bad_filename = os.path.join(here, "data", "dirty",
                                              "dirty_0.pdf")
        self.test_bad_file = DocxFile(self.test_bad_filename)
        self.test_docx = DocxFile(test_docx_filename)
        self.test_xlsx = DocxFile(test_xlsx_filename)
        self.test_docx.open()
        self.test_xlsx.open()

    def tearDown(self):
        self.test_docx.close()
        self.test_xlsx.close()

    def test_init(self):
        self.assertRaises(ValueError, self.test_bad_file.open)

    def test_remove_metadata(self):
        self.test_docx.remove_metadata()
        root = self.test_docx.xml.xml_contents['docProps/core.xml'] \
            .getchildren()
        self.assertTrue(len(root) == 0)

        self.test_xlsx.remove_metadata()
        root = self.test_xlsx.xml.xml_contents['docProps/core.xml'] \
            .getchildren()
        self.assertTrue(len(root) == 0)

    def test_save(self):
        self.test_docx.remove_metadata()
        tmp_dir = tempfile.mkdtemp()
        save_filename = os.path.join(tmp_dir, "test_save.docx")
        self.test_docx.save(save_filename)
        unziped = zipfile.ZipFile(save_filename)
        xml_content = etree.fromstring(unziped.read('docProps/core.xml'))
        root = xml_content.getchildren()
        for elt in root:
            self.assertIsNone(elt.text)
        try:
            shutil.rmtree(tmp_dir)
        except PermissionError:
            pass

        self.test_xlsx.remove_metadata()
        tmp_dir = tempfile.mkdtemp()
        save_filename = os.path.join(tmp_dir, "test_save.xlsx")
        self.test_xlsx.save(save_filename)
        unziped = zipfile.ZipFile(save_filename)
        xml_content = etree.fromstring(unziped.read('docProps/core.xml'))
        root = xml_content.getchildren()
        for elt in root:
            self.assertIsNone(elt.text)
        try:
            shutil.rmtree(tmp_dir)
        except PermissionError:
            pass


class TestAllType(unittest.TestCase):

    def setUp(self):
        self.data_path = os.path.join(here, 'data')
        self.dirty_data_path = os.path.join(self.data_path, 'dirty')
        self.clean_data_path = os.path.join(self.data_path, 'scrubbed')
        self.dirty_filenames = os.listdir(self.dirty_data_path)
        self.clean_filenames = os.listdir(self.clean_data_path)

    def test_all(self):
        for filename in self.dirty_filenames:
            tmp_dir = tempfile.mkdtemp()
            tmp_filename = os.path.join(tmp_dir, filename)
            remove_metadata(os.path.join(self.dirty_data_path, filename),
                            tmp_filename)
            self.assertTrue(
                os.path.getsize(default_output_filename(
                    os.path.join(self.clean_data_path, filename)
                )), os.path.getsize(tmp_filename)
            )
        try:
            shutil.rmtree(tmp_dir)
        except PermissionError:
            pass

    def test_directory(self):
        tmp_dir = tempfile.mkdtemp()
        directory_scrubber(self.dirty_data_path, tmp_dir)
        self.assertSetEqual(
            set(self.dirty_filenames),
            set(os.listdir(tmp_dir))
        )
        try:
            shutil.rmtree(tmp_dir)
        except PermissionError:
            pass
