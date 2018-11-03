#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 NOUCHET Christophe
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

# Author: Christophe Nouchet
# Email: nouchet.christophe@gmail.com
# Date: 07/2018 08/2018

from setuptools import setup, find_packages

# Merci Sam & Max : http://sametmax.com/creer-un-setup-py-et-mettre-sa-bibliotheque-python-en-ligne-sur-pypi/

setup(
    name='opv-graphe',
    version='0.0.1',
    packages=find_packages(),
    namespace_packages=['opv'],
    author="Christophe NOUCHET",
    author_email="nouchet.christophe@gmail.com",
    description="OPV Graphe",
    long_description="The goal of this module is to create virtual tour from a campaign of panorama taken in a hiking\
     session.",
    include_package_data=True,
    url='https://github.com/OpenPathView/opv-graphe',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=[
        'Flask',
        "Flask-Cors",
        "gunicorn",
        "flasgger",
        "marshmallow",
        "apispec"
    ],
    license="GPL3",
)
