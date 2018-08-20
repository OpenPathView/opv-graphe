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
The graphe module defined the Graphe class
"""

import json
import math
import copy
import queue
import logging
import operator

from atrevrix.graphe.exception import AtrevrixExceptionGraphe
from atrevrix.graphe.node import Node
from atrevrix.graphe.edge import Edge
from atrevrix.graphe.math import get_angle, get_distance


class Graphe(object):
    """The graphe class

    A graphe have nodes, edges, endpoints, hot points and paths. You can use this class to get nears nodes,
    create edges, found subgraphe, found shortest path between nodes."""

    def __init__(self, name, logger=None):
        """
        :param name: The graphe name
        :param logger:
        """
        self.__name = name
        self.__nodes = {}
        self.__edges = {}
        self.__endpoints = []
        self.__hotpoints = []
        self.__path = []
        self.__paths = []
        self.__junctions_point = []
        self.logger = logger if logger is not None else logging.getLogger(
            "%s(%s)" % (self.__class__.__name__, self.name)
        )

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        memodict[id(self)] = result
        result.__name = copy.deepcopy(self.name)
        temp = {}
        for name, node in self.__nodes.items():
            temp[name] = copy.deepcopy(node)

        result.__nodes = temp
        temp = {}
        for name, edge in self.__edges.items():
            temp[name] = copy.deepcopy(edge)
        result.__edges = temp

        for name in ["endpoints", "hotpoints", "path", "paths", "junctions_point"]:
            for element in getattr(self, name):
                setattr(result, name, copy.deepcopy(element))
        result.logger = copy.copy(self.logger)
        return result

    @property
    def name(self) -> str:
        """Get name"""
        return self.__name

    @name.setter
    def name(self, name: str):
        """Set name"""
        self.__name = name

    @property
    def nodes(self) -> dict:
        """
        Get nodes
        :return:
        """
        return self.__nodes

    @nodes.setter
    def nodes(self, nodes: dict):
        """
        Set nodes
        :param nodes:
        :return:
        """
        self.__nodes = nodes

    @property
    def edges(self) -> dict:
        """
        Get edges
        :return:
        """
        return self.__edges

    @edges.setter
    def edges(self, edges: dict):
        """
        Set edges
        :param edges:
        :return:
        """
        self.__edges = edges

    @property
    def endpoints(self) -> list:
        """Get endoints"""
        return self.__endpoints

    @endpoints.setter
    def endpoints(self, endpoints: list):
        """Set endpoints"""
        self.__endpoints = endpoints

    @property
    def hotpoints(self) -> list:
        """Get hotpoints"""
        return self.__hotpoints

    @hotpoints.setter
    def hotpoints(self, hotpoints: list):
        """Set hotpoints"""
        self.__hotpoints = hotpoints

    @property
    def junctions_point(self) -> list:
        """Get junctions point"""
        return self.__junctions_point

    @junctions_point.setter
    def junctions_point(self, junctions_point: list):
        """Set jonctions point"""
        self.__junctions_point = junctions_point

    @property
    def path(self) -> list:
        """Get the main path"""
        return self.__path

    @path.setter
    def path(self, path: list):
        """
        Set the main path
        :param path:
        :return:
        """
        self.__path = path

    @property
    def paths(self) -> list:
        """Get all sub paths"""
        return self.__paths

    @paths.setter
    def paths(self, paths: list):
        """
        Set sub paths
        :param paths:
        :return:
        """
        self.__paths = paths

    def add_path(self, path: list):
        """Add a path to graphe"""
        self.paths.append(path)

    def node_exist(self, name: str) -> bool:
        """
        Check if a node exit
        :param name: The name of the node
        :return:
        """
        if name in self.nodes:
            return True
        return False

    def create_node(self, name: str, *args, **kwargs) -> [Node, None]:
        """Create a node"""
        real_name = str(name)

        if self.node_exist(real_name):
            self.logger.warning("Node %s already exist!" % real_name)
            return None

        self.logger.debug("Creating node %s" % real_name)

        node = Node(real_name, *args, **kwargs)
        self.add_node(node, make_copy=False)
        return node

    def add_node(self, node: Node, make_copy=True):
        """
        Add a node
        :param node:
        :return:
        """
        if self.node_exist(node.name):
            self.logger.debug("Node %s already exit!" % node.name)
            return
        self.logger.debug("Add node %s" % node.name)
        new_node = node
        if make_copy:
            new_node = copy.copy(node)
            new_node.edges = []
        self.__nodes[node.name] = new_node

    def get_node(self, name: str) -> Node:
        """
        Get a node by its name
        :param name:
        :return:
        """
        if self.node_exist(str(name)):
            return self.nodes[str(name)]
        return None

    def add_edge(self, name0: str, name1: str, distance=None) -> [bool, Edge]:
        """
        Add edge
        :param name0: The source node
        :param name1: The dest node
        :param distance: The distance between node
        :return:
        """

        if not self.node_exist(name0):
            raise AtrevrixExceptionGraphe("Node %s doesn't exist!" % name0)

        if not self.node_exist(name1):
            raise AtrevrixExceptionGraphe("Node %s doesn't exist!" % name1)

        if name0 == name1:
            self.logger.warning(
                "You are trying to create an edge between the same node (%s)!" % name0
            )
            return False

        name = Edge._compute_name(name0, name1)

        if name in self.edges:
            self.logger.debug("%s Already exist" % name)
            return False

        self.logger.debug("Add edge between %s with distance %s" % (
            name, distance
        ))

        edge = Edge(
            source=name0,
            dest=name1,
            distance=distance
        )

        self.edges[name] = edge

        # Add edges to Node
        self.logger.debug("Add edge %s to node %s" % (name, name0))
        self.get_node(name0).add_edge(edge)
        self.logger.debug("Add edge %s to node %s" % (name, name1))
        self.get_node(name1).add_edge(edge)

        return edge

    def merge(self, graphe):
        """Merge graphe"""
        for name, value in graphe.nodes.items():
            if name in self.nodes:
                self.nodes[name].merge(value)
            else:
                self.nodes[name] = value
        for name, value in graphe.edges.items():
            if name in self.edges:
                continue
            self.edges[name] = value

        for name in graphe.hotpoints:
            self.__add_hotpoint(name)

        for name in graphe.endpoints:
            self.__add_endpoints(name)

    def __add_endpoints(self, end_point: str):
        """
        Add endpoints
        :param end_point:
        :return:
        """
        if end_point not in self.endpoints:
            self.endpoints.append(end_point)

    def add_end_points(self, endpoints: [list, str]):
        """Add end_points"""
        if isinstance(endpoints, list):
            for endpoint in endpoints:
                self.__add_endpoints(endpoint)
        else:
            self.__add_endpoints(endpoints)

    def __add_hotpoint(self, hotpoint: str):
        """Add hotpoint"""
        if hotpoint not in self.hotpoints:
            self.hotpoints.append(hotpoint)

    def add_hotpoints(self, hotpoints: [list, str]):
        """Add hotpoints"""
        if isinstance(hotpoints, list):
            for hotpoint in hotpoints:
                self.__add_hotpoint(hotpoint)
        else:
            self.__add_hotpoint(hotpoints)

    def detect_nears_nodes(self, ref_angle=90.0, ref_radius=15.0):
        """
        Detect nears nodes for each node
        :param ref_angle: the minimum angle between 3 nodes to consider nears
        :param ref_radius: the maximum distance between nodes to consider as near
        :return:
        """
        self.logger.info("=============== %s ===============" % "Detect nears nodes")
        self.logger.debug(
            "find near node when distance is lesser than %s and angle between node is greater than %s" % (
                ref_radius, ref_angle
            ))

        for ref_node_name, ref_node in self.nodes.items():
            self.logger.debug("%s Start searching for near nodes" % ref_node_name)
            near_nodes = {}

            self.logger.debug("%s\tSearch near nodes by distance" % ref_node_name)
            # Compare the node with the other
            for node_name, data in self.nodes.items():

                # Don't test the same node ...
                if ref_node_name == node_name:
                    continue

                # Get the distances between nodes
                distance = get_distance(ref_node.point, data.point)

                if distance > ref_radius:
                    continue
                self.logger.debug("%s\t\tFound %s with distance %s" % (ref_node_name, node_name, round(distance, 3)))
                near_nodes[node_name] = distance

            referential_angle_id = None
            referential_angle = None
            referential_angle_data = None
            final_near_node = {}

            self.logger.debug("%s\tSearch nears node by angle" % ref_node_name)

            # Get the nearest node by a portion of X radian
            for node_name, distance in sorted(near_nodes.items(), key=operator.itemgetter(1)):
                # Get the node
                node = self.nodes[node_name]

                # Get a referential
                if referential_angle is None:
                    self.logger.debug("%s\t\tThe referential node is %s" % (ref_node_name, node_name))
                    referential_angle_id = node_name
                    referential_angle = node
                    referential_angle_data = {
                        "distance": distance,
                        "angle": 0.0
                    }
                    continue

                angle = math.degrees(get_angle(ref_node.point, referential_angle.point, node.point))

                self.logger.debug("%s\t\tCheck %s with angle %s" % (ref_node_name, node_name, round(angle, 3)))

                add_it_to_near = 0

                if angle >= 360 - ref_angle or angle <= ref_angle:
                    self.logger.debug("%s\t\t\tnode is near the referential! Skipped it" % (ref_node_name))
                    continue

                for node_name_to_test, data2 in final_near_node.items():
                    ref_angle2 = data2["angle"]

                    def normalise(angle):
                        toto = 360 + angle if angle < 0 else angle
                        return toto % 360

                    angle_to_test = normalise(angle - ref_angle2)
                    self.logger.debug("%s\t\t\tCompare it with %s angle=%s, diff=%s" % (
                        ref_node_name, node_name_to_test, round(ref_angle2, 3), round(angle_to_test, 3)
                    ))

                    if angle_to_test >= 360 - ref_angle or angle_to_test <= ref_angle:
                        self.logger.debug("%s\t\t\tnode is near %s! Skipped it" % (ref_node_name, node_name_to_test))
                        add_it_to_near = 1
                        continue

                if add_it_to_near == 0:
                    # print("\tpano_tested=%s, angle=%s, OK" % (node_name, angle))
                    self.logger.debug("%s\t\t\tnode %s added" % (
                        ref_node_name, node_name
                    ))
                    final_near_node[node_name] = {
                        "distance": distance,
                        "angle": angle
                    }

            if referential_angle_id is not None:
                final_near_node[referential_angle_id] = referential_angle_data

            self.logger.info("Node %s have %s nears nodes:" % (ref_node_name, len(final_near_node)))
            for name, obj in final_near_node.items():
                self.logger.info("\tNode %s with distance=%s and angle=%s" % (
                    name, obj["distance"], obj["angle"]
                ))
            ref_node.set("near_nodes", final_near_node)

    def create_edge_from_near_nodes(self):
        """Create edge from near nodes"""
        for node_name, node in self.nodes.items():
            for succ_id, distance in node.get("near_nodes").items():
                self.add_edge(node_name, succ_id, distance)

    def _bfs_setup(self):
        """Setup for BFS (Breadth First Search)"""
        for name, node in self.nodes.items():
            node.set("bfs", 0)

    def _bfs_get_subgraphe(self, graphe_name: str):
        """Get subgraphe with nears nodes"""
        self.logger.debug("Search subgraphe %s with BFS (Breadth First Search) algorithm" % graphe_name)

        first_node = None

        # Get the first node that largeur = False
        for _, data in self.nodes.items():
            if data.get("bfs") == 0:
                first_node = data
                break

        if first_node is None:
            self.logger.debug("BFS: No node to check left!")
            return None

        self.logger.debug("BFS: Found node %s, it will be used has referential point" % first_node.name)
        graphe = Graphe(graphe_name)

        node_to_check = queue.Queue()
        node_to_check.put(first_node)

        while not node_to_check.empty():
            node = node_to_check.get()
            self.logger.debug("BFS: Check node %s " % node.name)
            graphe.add_node(node, make_copy=False)
            for succ_id, distance in node.get("near_nodes").items():
                pano = self.nodes[succ_id]
                graphe.add_node(pano, make_copy=False)
                graphe.add_edge(node.name, succ_id, distance=distance["distance"])
                if pano.get("bfs") == 0:
                    self.logger.debug("\tNode %s have a successor node %s" % (
                        node.name,
                        succ_id
                    ))
                    node_to_check.put(pano)
                    pano.set("bfs", 1)
            node.set("bfs", 2)

        for hotpoint in self.hotpoints:
            if hotpoint in self.nodes:
                graphe.add_hotpoints(hotpoint)
        return graphe

    def _bfs_get_subgraphe2(self, graphe_name):
        """Get subgraphe with successors"""
        self.logger.debug("Search subgraphe2 %s with BFS (Breadth First Search) algorithm" % graphe_name)

        first_node = None

        # Get the first node that largeur = False
        for _, data in self.nodes.items():
            if data.get("bfs") == 0:
                first_node = data
                break

        if first_node is None:
            self.logger.debug("BFS: No node to check left!")
            return None

        self.logger.debug("BFS: Found node %s, it will be used has referential point" % first_node.name)
        graphe = Graphe(graphe_name)

        node_to_check = queue.Queue()
        node_to_check.put(first_node)

        while not node_to_check.empty():
            node = node_to_check.get()
            self.logger.debug("BFS: Check node %s " % node.name)
            graphe.add_node(node, make_copy=False)
            for succ_id in node.successors():
                pano = self.nodes[succ_id]
                graphe.add_node(pano, make_copy=False)
                graphe.add_edge(node.name, succ_id, distance=get_distance(node.point, pano.point))
                if pano.get("bfs") == 0:
                    self.logger.debug("\tNode %s have a successor node %s" % (
                        node.name,
                        succ_id
                    ))
                    node_to_check.put(pano)
                    pano.set("bfs", 1)
            node.set("bfs", 2)

        for hotpoint in self.hotpoints:
            if hotpoint in graphe.nodes:
                graphe.add_hotpoints(hotpoint)

        for endpoint in self.endpoints:
            if endpoint in graphe.nodes:
                graphe.add_end_points(endpoint)

        graphe.path = self.path
        graphe.paths = self.paths

        return graphe

    def get_sub_graphes(self, near_node=True):
        """
        Detect subgraphe with BFS (Breadth First Search) algorithm
        :param near_node: Flag to enable/disable search of near panorama
        :return: all subgraphe
        """
        self.logger.info("=============== %s ===============" % "Get all subgraphe")
        self.logger.info("Search all subgraphe")
        liste = []

        self._bfs_setup()
        graphe_name = 0

        while True:
            graphe_name += 1
            if near_node:
                graphe = self._bfs_get_subgraphe("%s-%s" % (self.name, graphe_name))
            else:
                graphe = self._bfs_get_subgraphe2("%s-%s" % (self.name, graphe_name))
            if graphe is None:
                break
            liste.append(graphe)
        self.logger.info("Found %s subgraphe" % len(liste))
        return liste

    def get_end_points(self):
        """
        Get all end points the simple way:
        With this implementation, an endpoint is a node with only one edge.
        :param graphe:
        :return:
        """
        self.logger.info("=============== %s ===============" % "Get all endpoints")
        self.logger.info("Launch a simple search for end points")
        endpoints = []

        # Simple search
        for node_name, node in self.nodes.items():
            # count = graphe.count_edges(node_name)
            if len(node.edges) == 0:
                self.logger.critical("Node %s has no edge" % node_name)
            if len(node.edges) == 1:
                self.logger.info("Node %s is an end points" % node_name)
                endpoints.append(node_name)

        self.logger.info("Found %s end points in graphe %s" % (
            len(endpoints), self.name
        ))

        self.endpoints = endpoints

        return endpoints

    def dijkstra(self, deb_node: str, end_nodes: list):
        """Dijkstra"""
        path = {}

        self.logger.info("Launch dijkstra with start_node=%s and end_nodes=%s" % (
            deb_node, end_nodes
        ))

        # Set the
        start_node = self.get_node(deb_node)

        visited = {}

        end_nodes_util = copy.copy(end_nodes)

        if deb_node in end_nodes_util:
            end_nodes_util.remove(deb_node)

        end_nodes_path = {}

        def setup():
            """Setup for dijkstra"""
            for name, _ in self.nodes.items():
                visited[name] = math.inf

            visited[deb_node] = 0

        def find_min_node():
            """Find min node"""
            mini = math.inf
            min_node = None
            for node_name in nodes:
                distance = visited[node_name]
                if distance < mini:
                    mini = distance
                    min_node = node_name
            return min_node

        def update_distance(node_a, node_b, distance):
            """Update distance of a node"""
            if visited[node_b] > visited[node_a] + distance:
                self.logger.debug("Update distance for %s = %s, predecesor is %s" % (
                    node_b, distance, node_a
                ))
                visited[node_b] = visited[node_a] + distance
                path[node_b] = node_a

        def get_path(end_node):
            """Get the path of an end node"""
            my_path = []

            def add_node(node_name, distance):
                """Add a node"""
                my_path.append({
                    "name": node_name,
                    "distance": distance
                })

            node_name = end_node
            while True:
                add_node(node_name, visited[node_name])
                node_name = path[node_name]
                if node_name == deb_node:
                    add_node(node_name, visited[node_name])
                    break

            return my_path

        nodes = set([name for name, _ in self.nodes.items()])
        # print(nodes)
        # Setup for dijkstra
        setup()

        while nodes:

            # Get the min node
            min_node = find_min_node()

            self.logger.debug("Found min node %s" % min_node)
            if min_node is None:
                self.logger.error("No node found!")
                break

            # Remove min node from nodes
            nodes.remove(min_node)

            # Get all successor of min node
            min_node_obj = self.get_node(min_node)

            self.logger.debug("Node %s have successors %s" % (
                min_node, json.dumps(min_node_obj.successors(), indent=4)
            ))
            for successor_name, distance in min_node_obj.successors().items():
                if successor_name not in nodes:
                    continue

                update_distance(min_node, successor_name, distance)

                # Check if it s an end_points
                if successor_name in end_nodes_util:
                    end_nodes_path[successor_name] = get_path(successor_name)

                    self.logger.debug("Found path for %s to %s: %s" % (
                        deb_node, successor_name, json.dumps([toto["name"] for toto in end_nodes_path[successor_name]])
                    ))
                    end_nodes_util.remove(successor_name)

            if not end_nodes_util:
                break

        return end_nodes_path

    def detect_junction_nodes(self):
        """Detect function point"""
        self.logger.info("=============== %s ===============" % "Get all junction nodes")
        for liste in self.paths:
            for node in liste:
                if node in self.path:
                    self.logger.info("Node %s is a junction point" % (
                        node
                    ))
                    if node not in self.endpoints:
                        self.junctions_point.append(node)

    def get_edge_node(self, node1: str, node2: str):
        """Get a edge between 2 nodes"""
        return self.get_edge(Edge._compute_name(node1, node2))

    def get_edge(self, name: str) -> [Edge, list]:
        """
        Get an edge
        :param name:
        :return:
        """
        if name in self.edges:
            return self.edges[name]
        return None

    def get_edge_distance(self, name):
        """Get the distance of a edge"""
        toto = self.get_edge(name)
        if toto is None:
            self.logger.error("Distance not found for %s!" % name)
            return 0
        return toto.distance

    def generate_json(self, filename):
        """
        :param filename:
        :return:
        """

        data = {
            "nodes": {name: node.format() for name, node in self.nodes.items()},
            "edges": [],
            "endpoints": self.endpoints,
            "hotpoints": self.hotpoints,
            "junctions_point": self.__junctions_point
        }

        for name, edge in self.edges.items():
            data["edges"].append(
                {
                    "name": name,
                    "source": edge.source,
                    "dest": edge.dest
                }
            )

        with open(filename, "w") as fic:
            fic.write(json.dumps(data))