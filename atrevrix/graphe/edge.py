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

"""
The edge class
"""


import logging


class Edge(object):
    """
    The Edge class
    """
    def __init__(self, source: str, dest: str, data=None, distance=None, logger=None):
        """
        :param source:
        :param dest:
        """
        self.__name = self._compute_name(source, dest)
        self.__source = source
        self.__dest = dest
        self.__data = data if data is not None else {}
        self.__distance = distance
        self.logger = logger if logger is not None else logging.getLogger(
            "%s:%s" % (__name__, self.__class__.__name__)
        )

    @property
    def name(self):
        """Get name"""
        return self.__name

    @property
    def source(self):
        """Get source"""
        return self.__source

    @source.setter
    def source(self, source: str):
        """Set source"""
        self.__source = source
        self.__update_name()

    @property
    def dest(self):
        """Get dest"""
        return self.__dest

    @dest.setter
    def dest(self, dest: str):
        """Set dest"""
        self.__dest = dest
        self.__update_name()

    @property
    def data(self) -> dict:
        """Get data"""
        return self.__data

    @data.setter
    def data(self, data: dict):
        """Set data"""
        self.__data = data

    @property
    def distance(self) -> float:
        """Get distance"""
        return self.__distance

    @distance.setter
    def distance(self, distance: float):
        """Set distance"""
        self.__distance = distance

    @staticmethod
    def _compute_name(name1: str, name2: str) -> str:
        """Compute the edge name"""
        return "%s-%s" % tuple(sorted([name1, name2]))

    def __update_name(self):
        """Update the name"""
        self.__name = self._compute_name(self.source, self.dest)

    def get(self, name: str, default=None):
        if name == "distance":
            return self.distance
        if name in self.data:
            return self.data[name]
        return default

    def set(self, name: str, value):
        if name == "distance":
            self.distance = value
        else:
            self.data[name] = value
