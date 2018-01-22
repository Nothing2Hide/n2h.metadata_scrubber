#!/bin/env python3
# -*- coding: UTF-8 -*-

import os
import zipfile
import tempfile
import shutil
import mimetypes

from xml.etree import ElementTree as etree
from PIL import Image
import pdfrw


class MimeTypeNotFoundError(Exception):
    pass


class XMLFile:

    def __init__(self, filename):
        self.filename = filename
        self.xml_contents = {}
        self.inner_files = []

    def open(self):
        try:
            self.unziped = zipfile.ZipFile(self.filename)
        except zipfile.BadZipFile:
            raise ValueError("{} is not a correct docx file."
                             .format(self.filename))

    def rescue_xml(self, filename):
        xml_content = etree.fromstring(
            self.unziped.read(filename)) \
            if filename in self.unziped.namelist() else None
        if xml_content is not None:
            self.xml_contents[filename] = xml_content

    def save(self, outfile=None):
        outfile = outfile or default_output_filename(self.filename)
        if self.xml_contents:
            tmp_dir = tempfile.mkdtemp()
            self.unziped.extractall(tmp_dir)
            for filename, xml_content in self.xml_contents.items():
                with open(os.path.join(tmp_dir, filename), 'w') as tmpf:
                    xmlstr = etree.tostring(xml_content).decode()
                    tmpf.write(xmlstr)
            filenames = self.unziped.namelist()
            with zipfile.ZipFile(outfile, "w") as xml_out:
                for filename in filenames:
                    xml_out.write(os.path.join(tmp_dir, filename), filename)
            shutil.rmtree(tmp_dir)

    def close(self):
        self.unziped.close()


class DocxFile:

    def __init__(self, docx_filename):
        self.filename = docx_filename
        self.xml = XMLFile(docx_filename)
        self.meta_file = "docProps/core.xml"

    def remove_metadata(self):
        self.xml.rescue_xml(self.meta_file)
        if self.xml.xml_contents:
            content = self.xml.xml_contents[self.meta_file]
            for elt in content.getchildren():
                content.remove(elt)

    def save(self, outfile=None):
        self.xml.save(outfile)

    def open(self):
        self.xml.open()

    def close(self):
        self.xml.close()


class OdtFile:

    def __init__(self, odt_filename):
        self.filename = odt_filename
        self.xml = XMLFile(odt_filename)
        self.meta_file = "meta.xml"

    def remove_metadata(self):
        self.xml.rescue_xml(self.meta_file)
        if self.xml.xml_contents:
            content = self.xml.xml_contents[self.meta_file]
            root = content.getchildren()[0]
            for elt in root.getchildren():
                root.remove(elt)

    def save(self, outfile=None):
        self.xml.save(outfile)

    def open(self):
        self.xml.open()

    def close(self):
        self.xml.close()


class ImageFile:

    def __init__(self, img_filename):
        self.img_filename = img_filename
        self.img = None

    def open(self):
        self.img = Image.open(self.img_filename)

    def close(self):
        self.img = Image.close()

    def remove_metadata(self):
        self.img_wo_metadata = Image.new(self.img.mode, self.img.size)
        self.img_wo_metadata.putdata(self.img.getdata())

    def save(self, outfile=None):
        outfile = outfile or default_output_filename(self.img_filename)
        self.img_wo_metadata.save(outfile)


class PdfFile:

    def __init__(self, pdf_filename):
        self.pdf_filename = pdf_filename
        self.pdf_file = pdfrw.PdfFileReader(self.pdf_filename)
        self.metadata = []

    def open(self):
        pass

    def close(self):
        pass

    def rescue_metadata(self):
        if '/Info' in self.pdf_file.keys():
            self.metadata = [
                metadata[1:] for metadata in self.pdf_file.get("/Info")
            ]
        return self.metadata

    def remove_metadata(self, exclude=None):
        self.rescue_metadata()
        exclude = exclude if exclude else []
        for metadata in self.metadata:
            if metadata not in exclude:
                self.pdf_file.Info.pop("/" + metadata)

    def save(self, outfile=None):
        outfile = outfile or default_output_filename(self.pdf_filename)
        pdfrw.PdfWriter().write(fname=outfile, trailer=self.pdf_file)
        return(outfile)


def guess_file_class(filename):
    mimetype = mimetypes.MimeTypes().guess_type(filename)[0]
    mimetypes_association = {
        "application/vnd.oasis.opendocument.text": OdtFile,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": DocxFile,  # NOQA
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocxFile,  # NOQA
        "application/pdf": PdfFile,
        "image/png": ImageFile,
        "image/jpeg": ImageFile
    }
    File = mimetypes_association.get(mimetype, None)
    if File is None:
        raise MimeTypeNotFoundError("Mimetype %s not found" % mimetype)
    return File


def remove_metadata(filename, outfile=None):
    try:
        File = guess_file_class(filename)
    except MimeTypeNotFoundError as error:
        raise error
    file_ = File(filename)
    file_.open()
    file_.remove_metadata()
    file_.save(outfile=outfile)


def default_output_filename(filename):
    path, file_ = os.path.split(filename)
    outfile = os.path.join(path, "scrubbed_%s" % file_)
    return outfile


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
