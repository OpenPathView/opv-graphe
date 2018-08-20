from copy import deepcopy

from atrevrix.graphe import Node, Point, Edge


def node_test(node, name, point, data, edges):
    assert(node.name == name)
    assert (node.point == point)
    print(node.data)
    assert (node.data == data)
    assert (node.edges == edges)


def test_basic():
    """Basic test"""
    point = 42
    node = Node("Test", point=point)

    node_test(node, "Test", point, {}, [])

    point = Point()

    node.point = point
    node.name = "Titi"
    toto = {
        "ici": "la"
    }
    node.data = toto
    print(node.data)
    node.edges = ["a", "b"]

    node_test(
        node, "Titi", point, toto, ["a", "b"]
    )

    assert(node.get("ici") == "la")
    assert(node.get("la") is None)
    assert(node.get("la", default=42) == 42)

    node.set("la", "This is a test")
    assert(node.get("la") == "This is a test")
    assert (node.get("la", default=42) == "This is a test")

    assert(node.to_dict() == {
        "name": "Titi",
        "point": point.to_dict(),
        "data": node.data
    })

    e1 = Edge("1", "2")
    e2 = Edge("2", "4")
    node.edges = [e1, e2]

    assert(node.format() == {
        "name": node.name,
        "data": node.data,
        "point": point.to_dict(),
        "edges": ["1-2", "2-4"]
    })


def test_deep_copy():
    """Test deepcopy"""
    node = Node(
        "Test",
        point=Point(1, 2, 3),
        data={
            "1": 2
        }
    )

    node.edges = ["a", "b"]
    node_copy = deepcopy(node)

    assert(node_copy.name == node.name)
    assert (node_copy.data == node.data)
    assert (node_copy.edges == node.edges)

    assert(node_copy.point.x == 1)
    assert (node_copy.point.y == 2)
    assert (node_copy.point.z == 3)


def test_merge():
    node = Node(
        "Test",
        point=Point(1, 2, 3),
        data={
            "1": 2
        }
    )

    e1 = Edge("1", "2")
    e2 = Edge("2", "4")
    node.edges = [e1, e2]

    node2 = deepcopy(node)
    e3 = Edge("2", "3")
    node2.add_edge(e3)

    node2.set("1", 3)
    node2.set("2", 4)

    node.merge(node2)

    assert(node.name == "Test")
    assert(node.point.x == 1)
    assert (node.point.y == 2)
    assert (node.point.z == 3)

    assert(node.get("1") == 3)
    assert (node.get("2") == 4)

    assert(node.edges == [
        e1, e2, e3
    ])


def test_succesors():
    node = Node(
        "1",
        point=Point(1, 2, 3),
        data={
            "1": 2
        }
    )

    e1 = Edge("1", "2", distance=15)
    e2 = Edge("1", "4", distance=25)
    node.edges = [e1, e2]

    assert(node.successors() == {
        "2": 15,
        "4": 25
    })

    # Check if edge not really good
    node = Node(
        "3",
        point=Point(1, 2, 3),
        data={
            "1": 2
        }
    )

    e1 = Edge("1", "2", distance=15)
    e2 = Edge("1", "4", distance=25)
    node.edges = [e1, e2]

    assert (node.successors() == {})

    # Check
    node = Node(
        "3",
        point=Point(1, 2, 3),
        data={
            "1": 2
        }
    )

    e1 = Edge("1", "3", distance=15)
    e2 = Edge("2", "3", distance=25)
    node.edges = [e1, e2]

    assert (node.successors() == {
        "1": 15,
        "2": 25
    })

    # Check edge between same node
    node = Node(
        "3",
        point=Point(1, 2, 3),
        data={
            "1": 2
        }
    )

    e1 = Edge("3", "3", distance=15)
    e2 = Edge("3", "3", distance=25)
    node.edges = [e1, e2]

    assert (node.successors() == {})