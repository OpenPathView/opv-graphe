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

POINT_TYPE_GPS = "GPS"


class Point(object):
    """
    The Point class is the representation of a point

    With type == POINT_TYPE_GPS
        x => latitude
        y => longitude
        z => altitude
    """

    def __init__(self, x=0, y=0, z=0, type=POINT_TYPE_GPS):
        """
        :param x: The first coordinate
        :param y: The second coordinate
        :param z: The third coordinate
        :param type: The type of point (gps)
        """
        self.x = x
        self.y = y
        self.z = z
        self.type = type

    @property
    def latitude(self):
        """Get latitude"""
        return self.x

    @latitude.setter
    def latitude(self, latitude):
        """Set latitude"""
        self.x = latitude

    @property
    def longitude(self):
        """Get longitude"""
        return self.y

    @longitude.setter
    def longitude(self, longitude):
        """Set longitude"""
        self.y = longitude

    @property
    def altitude(self):
        """Get altitude"""
        return self.z

    @altitude.setter
    def altitude(self, altitude):
        """Set altitude"""
        self.z = altitude

    def is_gps(self) -> bool:
        """Check if the point use GPS coordinate"""
        return self.type == POINT_TYPE_GPS

    def to_dict(self) -> dict:
        """To dict"""
        if self.is_gps():
            return {
                "latitude": self.x,
                "longitude": self.y,
                "altitude": self.z,
                "type": self.type
            }
        else:
            return {
                "x": self.x,
                "y": self.y,
                "z": self.z,
                "type": self.type
            }


