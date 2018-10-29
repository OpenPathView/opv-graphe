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

"""Defined the Node class"""
import json
import copy
import logging

from opv.graphe.point import Point


class Node(object):
    """The Bode point"""

    def __init__(self, name: str, point=None, data=None, logger=None):
        """
        :param name:
        :param data:
        """
        self.__name = name
        self.__point = point if point is not None else Point()
        self.__data = data if data is not None else {}
        self.__edges = []
        self.logger = logger if logger is not None else logging.getLogger(
            "%s:%s" % (__name__, self.__class__.__name__)
        )

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        result.__name = copy.deepcopy(self.name)
        result.__point = copy.deepcopy(self.__point)
        result.__data = copy.deepcopy(self.__data)
        temp = []
        for edge in self.edges:
            temp.append(copy.deepcopy(edge))
        result.__edges = temp
        result.logger = copy.copy(self.logger)
        return result

    @property
    def name(self) -> str:
        """
        :return:
        """
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        :param name:
        :return:
        """
        self.__name = str(name)

    @property
    def point(self) -> Point:
        """Get point"""
        return self.__point

    @point.setter
    def point(self, point: Point):
        """Set point"""
        self.__point = point

    @property
    def data(self) -> dict:
        """
        :return:
        """
        return self.__data

    @data.setter
    def data(self, data: dict):
        """
        :param data:
        :return:
        """
        self.__data = data

    @property
    def id(self):
        return self.name

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    @property
    def z(self):
        return self.point.z

    @property
    def edges(self) -> list:
        """Get edges"""
        return self.__edges

    @edges.setter
    def edges(self, edges: list):
        """Set edges"""
        self.__edges = edges

    def get(self, name: str, default=None):
        """
        :param name:
        :param default:
        :return:
        """
        return self.data[name] if name in self.data else default

    def set(self, name: str, value):
        """
        :param name:
        :param value:
        :return:
        """
        self.logger.debug("Node %s: Add data to node: %s=%s" % (
            self.name, name, value
        ))
        self.data[name] = value

    def to_dict(self) -> dict:
        """to dict"""
        return {
            "name": self.name,
            "point": self.point.to_dict(),
            "data": self.data
        }

    def format(self) -> dict:
        """
        :return:
        """
        return {
            "name": self.name,
            "data": self.data,
            "point": self.point.to_dict(),
            "edges": self.get_edges_name_list()
        }

    def get_edges_name_list(self):
        """Get edges name list"""
        return [edge.name for edge in self.edges]

    def merge(self, node):
        """Merge Node"""
        for edge in node.edges:
            if edge.name not in self.get_edges_name_list():
                self.edges.append(edge)

        for name, value in node.data.items():
            self.data[name] = value

    def add_edge(self, edge):
        """Add edge"""
        if edge.name not in self.get_edges_name_list():
            self.edges.append(edge)

    def __check_if_valid_edge(self, edge):
        """Check if is a valid edge (source or dest must be name)"""
        return edge.source == self.name or edge.dest == self.name

    def __successor(self, edge):
        """Get the successor for an edge"""
        if edge.source == self.name:
            return edge.dest
        return edge.source

    def successors(self) -> dict:
        """Get successors"""
        successors = {}
        for edge in self.edges:
            if not self.__check_if_valid_edge(edge):
                self.logger.warning("Node %s have a strange edge %s (not an edge link to node)" % (
                    self.name, edge.name
                ))
                continue
            name = self.__successor(edge)
            if name == self.name:
                continue
            successors[name] = edge.distance
        return successors