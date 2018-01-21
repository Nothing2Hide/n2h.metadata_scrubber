import unittest
import os
import tempfile
import zipfile
import shutil
from xml.etree import ElementTree as etree

from n2h.metadata_scrubber.scrubber import OdtFile

here = os.path.abspath(os.path.dirname(__file__))


class TestDocxFile(unittest.TestCase):

    def setUp(self):
        test_odt_filename = os.path.join(here, "data", "odt", "ffc.odt")
        self.test_bad_filename = os.path.join(here, "data", "pdf", "n2h.pdf")
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
