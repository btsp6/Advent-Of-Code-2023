from abc import ABCMeta, abstractmethod
from heapq import heappop, heappush
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Tuple

with open("clumsy_crucible.in", "r") as f:
    data = [line.rstrip() for line in f]

data = [list(map(int, line)) for line in data]

def add(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def opposite_dir(dir):
    if dir == 'S':
        raise ValueError("Direction 'S' has no opposite direction!")
    if dir == 'U':
        return 'D'
    if dir == 'D':
        return 'U'
    if dir == 'L':
        return 'R'
    if dir == 'R':
        return 'L'


class Graph(metaclass=ABCMeta):
    @dataclass(frozen=True)
    class Node:
        dir: Literal['S', 'U', 'D', 'L', 'R']
        layer: int
        coord: Tuple[int, int]

    def __init__(self, data):
        self.data = data

    def get_move_cost(self, src: Node, dest: Node):
        """Cost of move from src to dest"""
        return self.data[dest.coord[0]][dest.coord[1]]

    def get_move_heuristic(self, src_coord: Tuple[int, int], dest_coord: Tuple[int, int]):
        """Heuristical (estimated) cost from src to dest coords"""
        return abs(dest_coord[0] - src_coord[0]) + abs(dest_coord[1] - src_coord[1])


    def _is_coord(self, coord: Tuple[int, int]):
        if coord[0] < 0 or coord[0] >= len(self.data):
            return False
        if coord[1] < 0 or coord[1] >= len(self.data[0]):
            return False
        return True

    def _get_adj_coords(self, coord: Tuple[int, int]):
        moves = {"D": (1, 0), "R": (0, 1), "U": (-1, 0), "L": (0, -1)}
        return {
            move_type: adj_coord for move_type, move in moves.items() if self._is_coord(adj_coord := add(coord, move))
        }

    @abstractmethod
    def get_adj_costs(self, node_rep: Node):
        ...


class ThreeMoveGraph(Graph):
    def get_adj_costs(self, node_rep: Graph.Node):
        adj_coords = self._get_adj_coords(node_rep.coord)
        if node_rep.dir != 'S':
            adj_coords.pop(opposite_dir(node_rep.dir), None)
            if node_rep.layer == 2:
                adj_coords.pop(node_rep.dir, None)
        adjs = {}
        for direction, adj_coord in adj_coords.items():
            adj_node = Graph.Node(
                dir=direction,
                layer=node_rep.layer + 1 if direction == node_rep.dir else 0,
                coord=adj_coord,
            )
            adjs[adj_node] = self.get_move_cost(node_rep, adj_node)
        return adjs

class FourToTenMoveGraph(Graph):
    def get_adj_costs(self, node_rep: Graph.Node):
        adj_coords = self._get_adj_coords(node_rep.coord)
        if node_rep.dir != 'S':
            adj_coords.pop(opposite_dir(node_rep.dir), None)
            if node_rep.layer < 3:
                for direction in "UDLR":
                    if direction == node_rep.dir:
                        continue
                    adj_coords.pop(direction, None)
            elif node_rep.layer == 9:
                adj_coords.pop(node_rep.dir, None)
        adjs = {}
        for direction, adj_coord in adj_coords.items():
            adj_node = Graph.Node(
                dir=direction,
                layer=node_rep.layer + 1 if direction == node_rep.dir else 0,
                coord=adj_coord,
            )
            adjs[adj_node] = self.get_move_cost(node_rep, adj_node)
        return adjs


def extract_path(
    start: Graph.Node,
    end: Graph.Node,
    paths: Dict[Graph.Node, Graph.Node]
):
    """Extracts path from start to end"""
    final_path = []
    curr = end
    final_path.append(curr)
    while curr != start:
        curr = paths[curr]
        final_path.append(curr)
    return reversed(final_path)

@dataclass(order=True)
class PriorityItem:
    priority: int
    item: Any = field(compare=False)

def pathfind(start: Graph.Node, end: Tuple[int, int], graph: ThreeMoveGraph):
    """Performs A* pathfinding algorithm with the given set of nodes, an adjacency function, and A* heuristic.

    Args:
        start: node_rep of the starting node
        end: coord of ending node
        graph: Graph type graph storing
    """
    costs: Dict[Graph.Node, int] = {}
    paths: Dict[Graph.Node, Graph.Node] = {}

    active_nodes: List[Tuple[int, Graph.Node]] = []
    start_score = graph.get_move_heuristic(start.coord, end)
    heappush(active_nodes, PriorityItem(start_score, start))
    costs[start] = 0
    final_node = None
    while len(active_nodes) > 0:
        node = heappop(active_nodes).item
        node_cost = costs[node]
        if node.coord == end and node.layer >= 3:
            final_node = node
            break
        adjs = graph.get_adj_costs(node)
        for other_node, cost in adjs.items():
            other_node_cost = node_cost + cost
            if other_node in costs:
                if costs[other_node] <= other_node_cost:
                    continue
                else:
                    raise RuntimeError("I feel like this shouldn't happen")
            costs[other_node] = other_node_cost
            paths[other_node] = node
            score = graph.get_move_heuristic(other_node.coord, end) + other_node_cost
            heappush(active_nodes, PriorityItem(score, other_node))

    assert final_node is not None
    final_path = extract_path(start, final_node, paths)
    return final_path, costs[final_node]

def display_path(path):
    board = []
    for line in data:
        board.append(["."] * len(line))
    for node in path:
        board[node.coord[0]][node.coord[1]] = "#"
    board_print = ""
    for line in board:
        board_print += "".join(line) + "\n"
    print(board_print)


def part1():
    """The movement on the board is modeled by a graph containing 13 total copies of the board.
    This consists of four groups of 3 copies which represents the most recently made move, as well as
    a single layer starting node group.
    For example, the group representing 'down' has a stack of 3 copies of the board with directional edges pointing
    to the left, right, or down (but not up).
    On an additional 'down' move, we go one board deeper in the stack. On the final board in the stack, we also do
    not permit any down moves.
    On a 'left' or 'right' move, we instead move to the stack corresponding to that move instead.

        Start ______  Up ______  Down ______  Left __2'__  Right ______
                         __1___       ______       ______        ______
                         __2___       ______       ______        ______

    For example, if we're currently at a node (1) in the second board copy in the 'Up' stack, and we move up again, we
    end up on the third board copy in the 'Up' stack (2). However, if we move 'Left' instead, we end up on the first
    board copy in the 'Left' stack (2').

    We denote the start node, as well as the stack groups as 'S', 'U', 'D', 'L', and 'R' respectively.
    """
    start = Graph.Node('S', 0, (0, 0))
    end = (len(data)-1, len(data[0])-1)
    graph = ThreeMoveGraph(data)

    path, total_cost = pathfind(start, end, graph)
    print(total_cost)
    display_path(path)

def part2():
    start = Graph.Node('S', 0, (0, 0))
    end = (len(data)-1, len(data[0])-1)
    graph = FourToTenMoveGraph(data)

    path, total_cost = pathfind(start, end, graph)
    print(total_cost)
    display_path(path)

part1()
part2()