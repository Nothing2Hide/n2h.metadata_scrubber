#!/bin/env python3
# -*- coding: UTF-8 -*-

"""
Remove all metadata from PDF.
By default, create a new file with named prefixed by « CLEAN_ ».
"""
import pdfrw


class PdfFile:
    """
    """

    def __init__(self, pdf_filename):
        self.pdf_filename = pdf_filename
        self.pdf_file = pdfrw.PdfFileReader(self.pdf_filename)
        self.metadata = []

    def rescue_metadata(self):
        if '/Info' in self.pdf_file.keys():
            self.metadata = \
                    [metadata[1:] for metadata in self.pdf_file.get("/Info")]
        return self.metadata

    def remove_metadata(self, exclude=None):
        """
        """
        exclude = exclude if exclude else []
        for metadata in self.metadata:
            if metadata not in exclude:
                self.pdf_file.Info.pop("/" + metadata)

    def save(self, outfile=None):  # pragma: no cover
        outfile = outfile if outfile else f"scubbed_{self.pdf_filename}"
        pdfrw.PdfWriter().write(fname=outfile, trailer=self.pdf_file)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
