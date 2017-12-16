#!/bin/env python3
# -*- coding: UTF-8 -*-

"""
Remove all metadata from doc.
"""
import zipfile
import tempfile
import os
import shutil
from lxml import etree


class DocxFile:

    def __init__(self, docx_filename):
        self.filename = docx_filename
        try:
            self.unziped = zipfile.ZipFile(docx_filename)
        except zipfile.BadZipFile:
            raise ValueError("{} is not a correct docx file."
                             .format(docx_filename))
        self.xml_content = etree.fromstring(
            self.unziped.read('docProps/core.xml')) \
            if 'docProps/core.xml' in self.unziped.namelist() else None

    def remove_metadata(self):
        if self.xml_content is not None:
            root = self.xml_content.getroottree().getroot()
            for elt in root:
                elt.text = ""

    def save(self, outfile=None):
        outfile = outfile if outfile else "EDITED_" + self.filename
        if self.xml_content is not None:
            tmp_dir = tempfile.mkdtemp()
            self.unziped.extractall(tmp_dir)
            with open(os.path.join(tmp_dir, 'docProps/core.xml'), 'w') as tmpf:
                xmlstr = etree.tostring(self.xml_content).decode()
                tmpf.write(xmlstr)
            filenames = self.unziped.namelist()
            with zipfile.ZipFile(outfile, "w") as docx:
                for filename in filenames:
                    docx.write(os.path.join(tmp_dir, filename), filename)
            shutil.rmtree(tmp_dir)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
