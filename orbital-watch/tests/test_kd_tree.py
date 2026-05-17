from src.kd_tree import build_kd_tree, radius_search


def test_kd_tree_radius_search_returns_neighbors_within_radius():
    points = [
        ((0.0, 0.0, 0.0), {"id": 1}),
        ((0.5, 0.0, 0.0), {"id": 2}),
        ((1.5, 0.0, 0.0), {"id": 3}),
        ((0.0, 1.0, 0.0), {"id": 4}),
    ]
    tree = build_kd_tree(points)
    neighbors = radius_search(tree, (0.0, 0.0, 0.0), 1.0)

    found_ids = {payload["id"] for payload, _ in neighbors}

    assert found_ids == {1, 2, 4}


def test_kd_tree_radius_search_excludes_outside_radius():
    points = [
        ((2.0, 0.0, 0.0), {"id": 1}),
        ((0.0, 2.0, 0.0), {"id": 2}),
    ]
    tree = build_kd_tree(points)
    neighbors = radius_search(tree, (0.0, 0.0, 0.0), 1.0)

    assert neighbors == []
