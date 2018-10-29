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

"""Defined the GrapheHelper"""

import json
import copy
import logging

from opv.graphe.math import get_angle, get_distance
from opv.graphe.edge import Edge
from opv.graphe.graphe import Graphe


class GrapheHelper(object):
    """The GrapheHelper class"""

    def __init__(self, logger=None):
        """
        :param logger:
        """
        self.logger = logger if logger is not None else logging.getLogger(
            "%s" % self.__class__.__name__
        )

    def get_nearest_node_between_graphe(self, ref_graphe: Graphe, graphe: Graphe) -> dict:
        """
        :param ref_graphe:
        :param graphe:
        :return:
        """
        self.logger.debug("Search near panorama between graphe %s and graphe %s" % (
            ref_graphe.name, graphe.name
        ))
        temp = {
            "distance": None,
            "ref_node_id": 0,
            "node_id": 0
        }

        for ref_node_id, ref_pano in ref_graphe.nodes.items():
            for node_id, pano in graphe.nodes.items():
                distance = get_distance(ref_pano.point, pano.point)

                if temp["distance"] is None or temp["distance"] > distance:
                    ref_distance = distance
                    temp = {
                        "distance": distance,
                        "ref_node_id": ref_node_id,
                        "node_id": node_id
                    }

        self.logger.debug("\tFound panorama %s with %s with distance=%s" % (
            temp["ref_node_id"], temp["node_id"], temp["distance"]
        ))
        return temp

    def merge_subgraphe(self, graphes: list) -> Graphe:
        """
        :param graphes:
        :return: a new merge graphe
        """
        self.logger.info("=============== %s ===============" % "Merge subgraphe")
        if len(graphes) == 0:
            self.logger.error("No graphe to test!")
            return None
        if len(graphes) == 1:
            self.logger.info("No graphe to merge, you only have one graphe")
            return graphes[0]

        ref_graphe = graphes[0]
        graphes_to_test = graphes[1:]

        self.logger.debug("I take graphe %s has referential" % ref_graphe.name)

        while True:
            merge_dict = []
            self.logger.debug("Search graphe to merge")
            for graphe in graphes_to_test:
                temp = self.get_nearest_node_between_graphe(ref_graphe, graphe)
                merge_dict.append({
                    "node": temp,
                    "graphe": graphe
                })

            self.logger.debug("Search the nearest graphe to merge")
            graphe_to_merge = sorted(merge_dict, key=lambda k: k["node"]['distance'])[0]

            self.logger.debug("Nearest graphe of %s is %s" % (ref_graphe.name, graphe_to_merge["graphe"].name))
            ref_graphe.merge(graphe_to_merge["graphe"])
            ref_graphe.add_edge(
                graphe_to_merge["node"]["ref_node_id"], graphe_to_merge["node"]["node_id"],
                distance=graphe_to_merge["node"]["distance"]
            )
            graphes_to_test.remove(graphe_to_merge["graphe"])

            if len(graphes_to_test) == 0:
                break

        return ref_graphe

    def _get_longest_path(self, paths: dict) -> dict:
        """
        Get the longest path in the paths dict
        :param paths: paths to test
        :return:
        """
        result = {
            "max":0,
            "source": None,
            "dest": None,
            "longest_path": None
        }

        for source, toto in paths.items():
            for dest, obj in toto.items():
                distance = obj[0]["distance"]
                if distance > result["max"]:
                    result = {
                        "max": distance,
                        "source": source,
                        "dest": dest,
                        "longest_path": obj
                    }
        self.logger.info("The longest path (%s m) is %s to %s: %s" % (
            result["max"], result["source"], result["dest"],
            "=>".join([o["name"] for o in result["longest_path"]])
        ))
        return result

    def __create_path_to_check(self, graphe: Graphe) -> dict:
        """
        Create the dict that can be used to test path between nodes
        :param graphe: The graphe
        :return:
        """
        to_test_check, to_test = [], {}

        def add_point(a: str, b: str):
            name = "%s-%s" % (a, b)

            if name in to_test_check:
                return
            to_test_check.append(name)

            if a not in to_test:
                to_test[a] = []

            if b not in to_test[a]:
                to_test[a].append(b)

        hot_end = graphe.endpoints + graphe.hotpoints
        for endpoint in hot_end:
            for endpoint_to_test in hot_end:
                if endpoint == endpoint_to_test:
                    continue
                add_point(endpoint, endpoint_to_test)
                add_point(endpoint_to_test, endpoint)

        self.logger.debug("Path to test %s" % json.dumps(to_test_check))

        return to_test

    def merge_path(self, source_graphe: Graphe, graphe: Graphe, path: dict, reduce=0) -> list:
        """
        Merge path
        :param graphe: The graphe to add the path
        :param path: The path to add
        :param reduce: if node numbers of the new path is lesser than reduce, it will not be merged.
        :return:
        """
        # Node to add
        new_path = []
        break_condition = False
        for node in path:
            name = node["name"]
            new_path.append(name)
            if graphe.node_exist(name):
                break
            # if graphe.node_exist(name) and ((name not in graphe.endpoints or name not in graphe.hotpoints) or break_condition):
            #     break
            # elif graphe.node_exist(name):
            #     break_condition = True

        # if break_condition:
        #     return
        if len(new_path) == 1:
            return

        if reduce > 0 and len(new_path) <= reduce:
            return

        # Add node
        for name in new_path:
            graphe.add_node(source_graphe.get_node(name))

        # Add edge
        for i in range(1, len(new_path)):
            graphe.add_edge(
                new_path[i - 1], new_path[i],
                source_graphe.get_edge_distance(Edge._compute_name(new_path[i - 1], new_path[i]))
            )

        # Add end_points
        for i in [0, -1]:
            name = path[i]["name"]
            if name in source_graphe.hotpoints:
                graphe.add_hotpoints(name)
            else:
                graphe.add_end_points(name)
        # graphe.add_end_points(path[0]["name"])
        # graphe.add_end_points(path[-1]["name"])

        return new_path

    def reduce_path(self, graphe: Graphe, reduce=0) -> Graphe:
        """
        Reduce the edge of the graphe with only shortest path between endpoints
        :param graphe: The graphe to reduce
        :param reduce: The reduce factor for the merge_path function
        :return:
        """

        self.logger.info("============================== %s ==============================" % (
            "Search the longest path"
        ))

        # Get list of path to test
        to_test = self.__create_path_to_check(graphe)
        path, path_simplified = {}, {}

        # Get distance of each path
        for name, endpoints in to_test.items():
            path[name] = graphe.dijkstra(name, endpoints)
            path_simplified[name] = {}

            for suc, distance in path[name].items():
                path_simplified[name][str(suc)] = distance[0]["distance"]

        # Get the longest path
        longest_path = self._get_longest_path(path)

        # Create the final graphe
        final_graphe = Graphe("Path.%s" % graphe.name)

        # Get new endpoints without start and stop node of the longest graphe
        to_test = [longest_path["source"], longest_path["dest"]]
        endpoints = copy.copy(graphe.endpoints)
        try:
            endpoints.remove(to_test[0])
        except ValueError:
            pass
        try:
            endpoints.remove(to_test[1])
        except ValueError:
            pass
        endpoints += copy.copy(graphe.hotpoints)

        for i in range(0, 2):
            if to_test[i] in endpoints:
                endpoints.remove(to_test[i])

        # New path, is the path between the longest path and all others endpoints
        new_path = {}

        # Merge longest path to final graphe
        self.merge_path(graphe, final_graphe, longest_path["longest_path"])

        # Set the longest path
        final_graphe.path = [o["name"] for o in longest_path["longest_path"]]

        for start_node in to_test:
            for endpoint in endpoints:
                if start_node not in new_path:
                    new_path[start_node] = {}

                path_to_add = self.merge_path(
                    graphe, final_graphe, path[start_node][endpoint], reduce=reduce
                )

                if path_to_add is not None:
                    new_path[start_node][endpoint] = path_to_add
                    final_graphe.add_path(path_to_add)

        for hotpoint in graphe.hotpoints:
            if hotpoint in final_graphe.endpoints:
                final_graphe.endpoints.remove(hotpoint)
            final_graphe.add_hotpoints(hotpoint)

        self.logger.info("New path is: %s" % json.dumps(new_path, indent=4))
        self.logger.info("Endpoints: %s" % json.dumps(final_graphe.endpoints, indent=4))
        self.logger.info("Hotpoints: %s" % json.dumps(final_graphe.hotpoints, indent=4))

        return final_graphe

    @staticmethod
    def __node_in_path(path: list, node_name: str) -> bool:
        """
        Check if a node is in path
        :param path: The path
        :param node_name: The node name to test
        :return: Boolean
        """
        for path_element in path:
            if node_name == path_element["name"]:
                return True
        return False

    def reduce_nodes(self, graphe: Graphe, reduce: int) -> Graphe:
        """
        Reduce graphe node number's
        :param graphe: The graphe to reduce
        :param longest_path: The longest path
        :param paths: Additionnal paths
        :param reduce: The minimum distance between nodes
        :return:
        """

        # Node_to_heep is a list of nodes that can't be reduce
        node_to_keep = copy.copy(graphe.endpoints)

        graphe.detect_junction_nodes()

        node_to_keep += copy.copy(graphe.junctions_point) + copy.copy(graphe.hotpoints)

        def reduce_graphe(graphe, path, node_to_keep, reduce):
            nodes = []
            new_path = {}
            previous, test = -1, 0

            if len(path) == 2:
                nodes.append(path[0])
                nodes.append(path[1])
                new_path[path[1]] = graphe.get_edge_distance(Edge._compute_name(path[previous], path[test]))
                return nodes, new_path

            distance = 0

            while True:
                if test == len(path) - 1:
                    if previous >= 0:
                        distance += graphe.get_edge_distance(Edge._compute_name(path[previous], path[test]))
                    nodes.append(path[test])
                    new_path[path[test]] = distance
                    break
                if test >= len(path):
                    break

                if path[test] in node_to_keep:
                    nodes.append(path[test])
                    new_path[path[test]] = distance
                    distance = 0
                    previous = test
                    test += 1

                if previous >= 0:
                    distance += graphe.get_edge_distance(Edge._compute_name(path[previous], path[test]))

                if distance >= reduce:
                    nodes.append(path[test])
                    new_path[path[test]] = distance
                    distance = 0
                previous = test
                test += 1

            return nodes, new_path

        reduced_graphe = Graphe("ReducedGraphe.%s" % graphe.name)
        reduced_graphe.endpoints = graphe.endpoints
        reduced_graphe.hotpoints = graphe.hotpoints
        reduced_graphe.junctions_point = graphe.junctions_point

        for nodes in [graphe.endpoints, graphe.junctions_point]:
            for node in nodes:
                # print(node)
                reduced_graphe.add_node(graphe.get_node(node))
        reduce_node, reduce_path = reduce_graphe(graphe, graphe.path, node_to_keep, reduce)

        def add_node_path(ref_graphe, graphe, nodes, paths, is_path=False):

            for node in nodes:
                # print(node)
                toto = ref_graphe.get_node(node)
                if toto is not None:
                    graphe.add_node(toto)

            if len(nodes) < 2:
                self.logger.error("Impossible to add path %s" % nodes)
                return

            for i in range(1, len(nodes)):
                graphe.add_edge(nodes[i-1], nodes[i], paths[nodes[i]])

            if is_path:
                graphe.path = nodes
            else:
                graphe.add_path(nodes)

        add_node_path(graphe, reduced_graphe, reduce_node, reduce_path, is_path=True)

        for path in graphe.paths:
            reduce_node, reduce_path = reduce_graphe(graphe, path, node_to_keep, reduce)
            add_node_path(graphe, reduced_graphe, reduce_node, reduce_path, is_path=False)

        # print(json.dumps(node_to_keep, indent=4))
        return reduced_graphe
