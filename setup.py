# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os


version = '0.1.dev0'

here = os.path.abspath(os.path.dirname(__file__))


def read_file(*pathes):
    path = os.path.join(here, *pathes)
    if os.path.isfile(path):
        with open(path, 'r') as desc_file:
            return desc_file.read()
    else:
        return ''


desc_files = (('README.rst',), ('docs', 'CHANGES.rst'),
              ('docs', 'CONTRIBUTORS.rst'))

long_description = '\n\n'.join([read_file(*pathes) for pathes in desc_files])

install_requires = ['pdfrw', 'pillow']

extras_require = {'test': ['setuptools',
                           'pytest',
                           'pytest-cov',
                           'flake8',
                           ],
                  'development': ['pyinstaller']
                  }

# setup(name='nothing2hide.metadata.core',
setup(name='n2h.metadata_scrubber',
      version=version,
      description="Metadata scrubber library.",
      long_description=long_description,
      platforms=["any"],
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: BSD License",
      ],
      keywords="",
      author="nothing2hide",
      author_email="contact__at__nothing2hide.org",
      url="github",
      license="BSD",
      packages=find_packages("src"),
      package_dir={"": "src"},
      namespace_packages=["n2h"],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      scrubbertk = n2h.metadata_scrubber.gui:main
      """,
      )

# vim:set et sts=4 ts=4 tw=80:
