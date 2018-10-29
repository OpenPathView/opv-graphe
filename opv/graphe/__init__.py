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
The atrevrix.graphe module can be used to create and reduce graphe from a list of GPS point
"""

import opv.graphe.utils
from opv.graphe.exception import AtrevrixExceptionGraphe
from opv.graphe.point import Point
from opv.graphe.math import EARTH_RADIUS, get_distance, get_angle
from opv.graphe.node import Node
from opv.graphe.edge import Edge
from opv.graphe.graphe import Graphe
from opv.graphe.graphe_helper import GrapheHelper
from opv.graphe.api import graphe_api
