from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class KDTreeNode:
    point: tuple[float, float, float]
    payload: dict
    left: KDTreeNode | None = None
    right: KDTreeNode | None = None
    axis: int = 0


def build_kd_tree(points: list[tuple[tuple[float, float, float], dict]], depth: int = 0) -> KDTreeNode | None:
    if not points:
        return None

    axis = depth % 3
    points.sort(key=lambda item: item[0][axis])
    median_index = len(points) // 2

    node = KDTreeNode(
        point=points[median_index][0],
        payload=points[median_index][1],
        axis=axis
    )
    node.left = build_kd_tree(points[:median_index], depth + 1)
    node.right = build_kd_tree(points[median_index + 1 :], depth + 1)

    return node


def _distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.dist(a, b)


def radius_search(node: KDTreeNode | None, target: tuple[float, float, float], radius: float) -> list[tuple[dict, float]]:
    results: list[tuple[dict, float]] = []

    def search_recursive(current: KDTreeNode | None) -> None:
        if current is None:
            return

        point = current.point
        distance = _distance(point, target)

        if distance <= radius:
            results.append((current.payload, distance))

        axis = current.axis
        diff = target[axis] - point[axis]
        next_branch = current.left if diff <= 0 else current.right
        opposite_branch = current.right if diff <= 0 else current.left

        search_recursive(next_branch)

        if abs(diff) <= radius:
            search_recursive(opposite_branch)

    search_recursive(node)
    return results
