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
# Date: 29/10/2018

"""
This is shit, but it's working!
"""

import json
from flask import Flask, jsonify, request, Blueprint, render_template
from marshmallow import post_load, pre_dump, post_dump
from flasgger import Swagger, SwaggerView, Schema, fields


from opv.graphe import Edge, Node, Graphe, Point, GrapheHelper


class DummyGraphe:

    def __init__(self, nodes, edges, end_points, hotpoints):
        self.nodes = nodes
        self.edges = edges
        self.end_points = end_points
        self.hotpoints = hotpoints


class EdgeSchema(Schema):
    """
    An edge
    """
    # Source
    source = fields.Str(required=True, default="140-42", description="The source node id")
    # Dest
    dest = fields.Str(required=True, default="141-42", description="The dest node id")
    # Data
    data = fields.Dict(description="Some information about the edge")

    @post_load
    def make_edge(self, data):
        edge = Edge(**data)
        if "distance" in data["data"]:
            edge.distance = data["data"]["distance"]
        return edge

    @pre_dump
    def edge_helper2(self, data):
        class ALACON:
            def __init__(self, source, dest, data):
                self.source = source
                self.dest = dest
                self.data = data
        temp = data.data
        temp["distance"] = data.distance
        return ALACON(data.source, data.dest, temp)

    @post_dump
    def edge_helper(self, data):
        if "data" not in data:
            data["data"] = {}
        return data


class NodeSchema(Schema):
    """
    A node
    """
    id = fields.Str(required=True, default="140-42", description="The id of the node")
    x = fields.Float(required=True, default=48.399626, description="latitude in meter")
    y = fields.Float(required=True, default=-4.472394, description="longitude in meter")
    z = fields.Float(required=True, default=1.2, description="altitude in meter")
    data = fields.Dict(description="Some information about the node")

    @post_load
    def make_node(self, data):
        return Node(data["id"], point=Point(data["x"], data["y"], data["z"]), data=data["data"])

    @pre_dump
    def node_helper2(self, data):
        class ALACON:
            def __init__(self, id, x, y,z, data):
                self.id = id
                self.x = x
                self.y = y
                self.z = z
                self.data = data
        return ALACON(data.name, data.x, data.y, data.z, data.data)

    @post_dump
    def node_helper(self, data):
        if "data" not in data:
            data["data"] = {}
        return data


class GrapheSchema(Schema):
    """
    A graphe is composed of nodes and edges
    """
    end_points = fields.List(fields.Str(), required=True, description="End points of the graphe")
    hotpoints = fields.List(fields.Str(), required=True, description="The hotpoint of the graphe")
    nodes = fields.Nested(NodeSchema, many=True, required=True)
    edges = fields.Nested(EdgeSchema, many=True, required=True)

    @post_load
    def make_graphe(self, data):
        graphe = Graphe("GrapheFromApiRest")
        graphe.endpoints = data["end_points"]
        graphe.hotpoints = data["hotpoints"]
        graphe.nodes = {d.name: d for d in data["nodes"]}
        graphe.edges = {Edge._compute_name(d.source, d.dest): d for d in data["edges"]}

        for node_name, node in graphe.nodes.items():
            for name, edge in graphe.edges.items():
                if node_name == edge.source or node_name == edge.dest:
                    node.edges.append(edge)

        return graphe

    @pre_dump
    def graphe_helper(self, data):
        return DummyGraphe([d for d in data.nodes.values()], [e for e in data.edges.values()], data.end_points, data.hotpoints)


def load_graphe(data):
    """
    Load Graphe from data
    :param data:
    :return:
    """
    graphe = GrapheSchema()
    graphe = graphe.load(data)
    return graphe.data


def dump_graphe(graphe):
    """
    Dump graphe from data
    :param data:
    :return:
    """
    schema = GrapheSchema()
    return schema.dump(graphe, many=False).data


class CreateEdges(SwaggerView):

    description = "Create edges API"
    tags = ["graphe"]
    # parameters = [Graphe]
    parameters = [
        {
            "name": "perimeter",
            "in": "path",
            "type": "float",
            "default": 40.1,
            "description": "The perimeter to search with a node as center. This is a radius in meter."
        },
        {
            "name": "radial_spacing",
            "in": "path",
            "type": "float",
            "default": 90.2,
            "description": "The radial spacing bewteen to node."
        },
        {
            "name": "body",
            "in": "body",
            "schema": GrapheSchema,
            "required": True
        }
    ]
    responses = {
        200: {
            "description": "The graphe with new edges between nears nodes",
            "schema": GrapheSchema
        }
    }

    def post(self, perimeter: float, radial_spacing: float):
        """
        Create edges between nears node
        """
        graphe = load_graphe(request.json)
        graphe.detect_nears_nodes(ref_angle=radial_spacing, ref_radius=perimeter)
        graphe.create_edge_from_near_nodes()
        graphes = graphe.get_sub_graphes()
        graphe_helper = GrapheHelper()
        graphe = graphe_helper.merge_subgraphe(graphes)
        return jsonify(dump_graphe(graphe))


class SearchEndPoints(SwaggerView):

    description = "Search endpoints API"
    tags = ["graphe"]
    # parameters = [Graphe]
    parameters = [
        {
            "name": "body",
            "in": "body",
            "schema": GrapheSchema,
            "required": True
        }
    ]
    responses = {
        200: {
            "description": "The graphe with the endpoints",
            "schema": GrapheSchema
        }
    }

    def post(self):
        """
        Detect the endpoint of the graphe
        """
        graphe = load_graphe(request.json)
        graphe.get_end_points()
        return jsonify(dump_graphe(graphe))


class ReduceGraphe(SwaggerView):
    description = "Graphe API"
    tags = ["graphe"]
    # parameters = [Graphe]
    parameters = [
        {
            "name": "reduce",
            "in": "path",
            "type": "int",
            "default": 15,
            "description": "The number of edge to reduce in meter"
        },
        {
            "name": "min_path",
            "in": "path",
            "type": "int",
            "default": 0,
            "description": "Min node number to consider the path. If 0 consider all path"
        },
        {
            "name": "body",
            "in": "body",
            "schema": GrapheSchema,
            "required": True
        }
    ]
    responses = {
        200: {
            "description": "The graphe with the endpoints",
            "schema": GrapheSchema
        }
    }

    def post(self, reduce: int, min_path=0):
        """
        Reduce graphe, reduce the number of node and edge
        """
        graphe = load_graphe(request.json)
        graphe_helper = GrapheHelper()
        final_graphe = graphe_helper.reduce_path(graphe, reduce=min_path)
        reduce_path = graphe_helper.reduce_nodes(final_graphe, reduce)
        graphes = reduce_path.get_sub_graphes(near_node=False)
        final_graphe = graphe_helper.merge_subgraphe(graphes)
        return jsonify(dump_graphe(final_graphe))


class All(SwaggerView):
    description = "Graphe API"
    tags = ["graphe"]
    # parameters = [Graphe]
    parameters = [
        {
            "name": "perimeter",
            "in": "path",
            "type": "float",
            "default": 40.1,
            "description": "The perimeter to search with a node as center. This is a radius in meter.",
        },
        {
            "name": "radial_spacing",
            "in": "path",
            "type": "float",
            "default": 90.2,
            "description": "The radial spacing bewteen to node."
        },
        {
            "name": "reduce",
            "in": "path",
            "type": "int",
            "default": 15,
            "description": "The minimum distance between two node"
        },
        {
            "name": "min_path",
            "in": "path",
            "type": "int",
            "default": 0,
            "description": "Min node number to consider the path. If 0 consider all path",
            "required": False
        },
        {
            "name": "body",
            "in": "body",
            "schema": GrapheSchema,
            "required": True
        }
    ]
    responses = {
        200: {
            "description": "The graphe reduced",
            "schema": GrapheSchema
        }
    }

    def post(self, perimeter: float, radial_spacing: float, reduce: int, min_path=0):
        """
        Reduce graphe, reduce the number of node and edge
        """
        graphe = load_graphe(request.json)
        number_end_points = len(graphe.endpoints)
        graphe_helper = GrapheHelper()
        graphe.detect_nears_nodes(ref_angle=radial_spacing, ref_radius=perimeter)
        graphe.create_edge_from_near_nodes()
        graphes = graphe.get_sub_graphes()
        graphe = graphe_helper.merge_subgraphe(graphes)
        if number_end_points == 0:
            graphe.get_end_points()
        final_graphe = graphe_helper.reduce_path(graphe, reduce=min_path)
        reduce_path = graphe_helper.reduce_nodes(final_graphe, reduce)
        graphes = reduce_path.get_sub_graphes(near_node=False)
        final_graphe = graphe_helper.merge_subgraphe(graphes)
        return jsonify(dump_graphe(final_graphe))


class GrapheLeafletOpti(SwaggerView):
    description = "Graphe API"
    tags = ["graphe"]
    # parameters = [Graphe]
    parameters = [
        {
            "name": "body",
            "in": "body",
            "schema": GrapheSchema,
            "required": True
        }
    ]
    responses = {
        200: {
            "description": "The graphe reduced",
            "type": "dict"
        }
    }

    def post(self):
        """
        Tranform GrapheSchme to GrapheLeafletSchema
        """
        data = request.json
        nodes = []
        endpoints = []
        hotpoints = []
        nodes_dict = {}
        edges = []

        for node in data["nodes"]:
            line = [node["id"], node["x"], node["y"]]
            if node["id"] in data["end_points"]:
                endpoints.append(line)
            if node["id"] in data["hotpoints"]:
                hotpoints.append(line)
            nodes.append(line)
            nodes_dict[node["id"]] = node

        for edge in data["edges"]:
            source = nodes_dict[edge["source"]]
            dest = nodes_dict[edge["dest"]]
            edges.append([
                [source["x"], source["y"]],
                [dest["x"], dest["y"]]
            ])
        return jsonify({
            "nodes": nodes,
            "end_points": endpoints,
            "hotpoints": hotpoints,
            "edges": edges
        })


graphe_api = Blueprint('graphe', __name__, template_folder="templates")


graphe_api.add_url_rule(
    '/all/<float:perimeter>/<float:radial_spacing>/<int:reduce>/<int:min_path>',
    view_func=All.as_view('Graphe4'),
    methods=['POST']
)

graphe_api.add_url_rule(
    '/create_edges/<float:perimeter>/<float:radial_spacing>',
    view_func=CreateEdges.as_view('Graphe'),
    methods=['POST']
)

graphe_api.add_url_rule(
    '/detect_endpoints',
    view_func=SearchEndPoints.as_view('Graphe2'),
    methods=['POST']
)

graphe_api.add_url_rule(
    '/reduce/<int:reduce>/<int:min_path>',
    view_func=ReduceGraphe.as_view('Graphe3'),
    methods=['POST']
)

graphe_api.add_url_rule(
    '/to_leaflet',
    view_func=GrapheLeafletOpti.as_view('Graphe5'),
    methods=['POST']
)

@graphe_api.route("/map")
def get_map():
    """Use a Leaflet map to show graphe
        You can use this endpoint to have a map to show the graphe on
        ---
        responses:
          200:
            description: The map page
        """
    return render_template("show_graphe.html")