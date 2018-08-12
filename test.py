#!/usr/bin/env python3

# coding: utf-8

import sys
import json
import copy

from atrevrix.graphe import Point, Node, Graphe, GrapheHelper


if __name__ == "__main__":

    name = "test.json"
    if len(sys.argv) > 1:
        name = sys.argv[1]

    with open(name, "r") as fic:
        data = json.load(fic)

    graphe = Graphe("Test")
    for name, gps in data.items():
        point = Point(
            x=gps["latitude"],
            y=gps["longitude"],
            z=gps["altitude"]
        )

        graphe.create_node(
            name,
            point=point
        )

    graphe.generate_json("01_points.json")
    graphe.detect_nears_nodes()
    for_reporting = copy.deepcopy(graphe)
    for_reporting.create_edge_from_near_nodes()
    for_reporting.generate_json("02_detect_nears_panorama.json")
    graphes = graphe.get_sub_graphes()
    graphe_helper = GrapheHelper()
    graphe = graphe_helper.merge_subgraphe(graphes)
    graphe.hotpoints = [
        '634',
        '633',
        '660',
        '670',
        '86',
        '770',
        '777',
        '767'
    ]
    graphe.generate_json("03_merge_graphe.json")
    graphe.get_end_points()
    graphe.generate_json("04_get_endpoints.json")
    final_graphe = graphe_helper.reduce_path(graphe)
    final_graphe.generate_json("05_reduce_path.json")
    reduce_path = graphe_helper.reduce_nodes(final_graphe, 15)
    graphes = reduce_path.get_sub_graphes(near_node=False)
    final_graphe = graphe_helper.merge_subgraphe(graphes)
    a = final_graphe.get_sub_graphes(near_node=False)
    print("Number of reduce path: %s" % len(a))
    reduce_path.generate_json("06_reduce_nodes.json")