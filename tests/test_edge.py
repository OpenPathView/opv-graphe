from opv.graphe import Edge


def edge_test(edge, source, dest, data, distance):
    assert(edge.source == source)
    assert (edge.dest == dest)
    assert (edge.data == data)
    assert (edge.distance == distance)


def test_basic():
    edge = Edge("1", "2")

    edge_test(edge, "1", "2", {}, None)

    assert (edge.get("distance") == None)
    assert (edge.get("distance", default=42) == None)

    edge.source = "3"
    edge.dest = "4"
    edge.data = {
        "a": 42
    }
    edge.distance = 42

    edge_test(edge, "3", "4", {"a": 42}, 42)

    assert(edge.get("distance") == 42)

    assert(edge.get("toto") == None)
    assert (edge.get("toto", default=42) == 42)
    edge.set("toto", "titi")

    assert (edge.get("toto") == "titi")

    edge.set("distance", 3)
    assert(edge.distance == 3)
