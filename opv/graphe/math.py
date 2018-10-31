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

"""Defined the math functions"""


import math

from opv.graphe.point import Point

EARTH_RADIUS = 6378000


def get_distance(gps_cord1: Point, gps_cord2: Point):
    """
    Return the distance between 2 point in meter
    :param gps_cord1:
    :param gps_cord2:
    :return:

    To verify if I am not too dumb:
    # Wikipedia saids that Paris and Network are 5 852 km away
    # - https://fr.wikipedia.org/wiki/Orthodromie.
    >>> a = Point(x=48.850000, y=2.350000) # Paris
    >>> b = Point(x=40.716667, y=-74.000000) # NewYork
    >>> get_distance(a,b)
    5843114.788446997
    """
    # we must convert gps cord who are in degrees to radians
    gps_cord1 = [math.radians(gps_cord1.x), math.radians(gps_cord1.y)]
    gps_cord2 = [math.radians(gps_cord2.x), math.radians(gps_cord2.y)]

    # Les liens utilisés:
    # - https://fr.wikipedia.org/wiki/Orthodromie
    # - http://ressources.univ-lemans.fr/AccesLibre/UM/Pedago/physique/02/divers/ortholoxo.html
    # - https://fr.wikipedia.org/wiki/Identit%C3%A9_trigonom%C3%A9trique
    #         O
    #        | |
    #     R |   | R
    #      |     |
    #     |       |
    #     A        B
    # cos(AOB) = OA / AB = OA . OB
    # Produit scalaire OA . OB
    # OA.x = cos(long1)*cos(lat1)
    # OA.y = sin(long1)*cos(lat1)
    # OA.z = sin(lat1)
    # OB.x = cos(long2)*cos(lat2)
    # OB.y = sin(long2)*cos(lat2)
    # OB.z = sin(lat2)
    # OA . OB = (OA.x * OB.x + OA.y * OB.y + OA.z * OB.z)
    # = cos(long1)*cos(lat1) *cos(long2)*cos(lat2) + sin(long1)*cos(lat1) * sin(long2)*cos(lat2) + sin(lat1) * sin(lat2)
    # = cos(lat1)*cos(lat2) * (cos(long1)*cos(long2) + sin(long1)*sin(long2)) + sin(lat1)*sin(lat2)
    # Identité remarquable cos(b - a) = cos(a)*cos(b) + sin(a)*sin(b)
    # = cos(lat1)*cos(lat2) * (cos(long2 - long1) + sin(lat1)*sin(lat2)
    # Donc
    # cos(AOB) = (cos(lat1)*cos(lat2) * (cos(long2 - long1) + sin(lat1)*sin(lat2))
    # distance = AOB*R
    # Avec R = 6378000 mètres
    # d = R*acos((cos(lat1)*cos(lat2) * (cos(long2 - long1) + sin(lat1)*sin(lat2)))


    temp = math.cos(gps_cord1[0]) * math.cos(gps_cord2[0]) * math.cos(gps_cord2[1] - gps_cord1[1]) + \
           math.sin(gps_cord1[0]) * math.sin(gps_cord2[0])

    temp = 1.0 if temp > 1.0 else temp
    temp = -1.0 if temp < -1.0 else temp

    return EARTH_RADIUS * (
        math.acos(
            temp
        )
    )


def get_angle(pano1: Point, pano2: Point, pano3: Point):
    """
    Get Angle between pano1, pano2, pano3
    :param pano1:
    :param pano2:
    :param pano3:
    :return:
    >>> a = Point(x=48.850000, y=2.350000) # Paris
    >>> b = Point(x=40.716667, y=-74.000000) # NewYork
    >>> c = Point(x=9.08196, y=7.402968) # Abuja (Nigeria)
    >>> get_angle(a, b, c)
    1.9788164423528525
    """

    d_ab = get_distance(pano1, pano2)
    d_ac = get_distance(pano1, pano3)
    d_bc = get_distance(pano2, pano3)

    # On va utiliser le théorème d'Al-Kashi pour calculer CAB:
    # - https://fr.wikipedia.org/wiki/Loi_des_cosinus
    #         C
    #        | |
    #       |   |
    #      |     |
    #     |       |
    #     A________B
    # Donc:
    # - a = AB
    # - b = AC
    # - c = BC
    # c *c = a * a + b * b - 2 * a * b * cos(CAB)
    # - 2 * a * b * cos(OAB) = c * c - a * a - b * b
    # cos(OAB) = (1 / (-2 * a * b)) * (c * c - a * a - b * b)
    # OAB = acos((1 / (-2 * a * b)) * (c * c - a * a - b * b)
    try:
        calcul = (-1.0 / (2.0 * d_ab * d_ac)) * (
            d_bc * d_bc -
            d_ab * d_ab -
            d_ac * d_ac
        )
        calcul = 1.00 if calcul > 1.0 else calcul
        calcul = -1.00 if calcul < -1.0 else calcul
        return math.acos(calcul)
    except ZeroDivisionError:
        return 0.0
