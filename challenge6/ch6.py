import socket


moves = ["2u1l", "2u1r", "2d1l", "2d1r", "1u2l", "1u2r", "1d2l", "1d2r"]
next_squares = [(2, -1), (2, 1), (-2, -1), (-2, 1), (1, -2), (1, 2), (-1, -2), (-1, 2)]
op_moves = dict(zip(moves, next_squares))



opposites = {
    "2u1l": "2d1r",
    "2u1r": "2d1l",
    "2d1l": "2u1r",
    "2d1r": "2u1l",
    "1u2l": "1d2r",
    "1u2r": "1d2l",
    "1d2l": "1u2r",
    "1d2r": "1u2l",
}
hostname = "52.49.91.111"
port = 2003
debug = False


def sum_coordinates(coord1, coord2):
    return tuple(c1 + c2 for c1, c2 in zip(coord1, coord2))


class State(object):
    def __init__(self, coord, move=None, parent=None):
        self.coord = coord
        self.move = move
        self.parent = parent

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return other.coord == self.coord

    def __hash__(self):
        return hash(self.coord)

    def __str__(self):
        return str(self.coord)


def subgrid_coords(subgrid, knight_pos):
    # Knight is always positioned at (2,2) on the relative grid
    local_coords = []
    for i in range(2, -3, -1):
        row = []
        for j in range(-2, 3):
            row.append((i, j))
        local_coords.append(row)

    global_coords = {}
    for coords, squares in zip(local_coords, subgrid):
        for coord, square in zip(coords, squares):
            coord = sum_coordinates(coord, knight_pos)
            global_coords[coord] = square
    return global_coords


def successors(subgrid, parent):
    successors = []
    global_coords = subgrid_coords(subgrid, parent.coord)
    for move in moves:
        coord = sum_coordinates(parent.coord, op_moves[move])
        if global_coords[coord] == "#":
            pass
        else:
            successors.append(State(coord, move, parent))
    return successors


def set_subgrid(prev, socket):
    reset_moves = []
    while prev.parent is not None:
        reset_moves.append(prev.move)
        prev = prev.parent
    for mv in reset_moves[::-1]:
        socket.send(mv.encode("utf-8"))
        data = socket.recv(1024).decode("utf-8")


def find_princess(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    while True:
        start = State((0, 0))
        visited = set()
        to_visit = list()
        open_nodes = set()
        to_visit.append(start)
        open_nodes.add(start)
        current = None
        while len(to_visit) > 0:
            prev = current
            current = to_visit.pop()
            if current != start:
                if prev != current.parent:
                    s.close()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((hostname, port))
                    s.recv(1024).decode("utf-8")
                    set_subgrid(current.parent, s)
                s.send(current.move.encode("utf-8"))
            data = s.recv(1024).decode("utf-8")
            if current.coord == (0, 1):  # GOAL
                return data

            subgrid = data[:30].split()
            for succ in successors(subgrid, current):
                if succ not in open_nodes and succ not in visited:
                    to_visit.append(succ)
                    open_nodes.add(succ)
            visited.add(current)


def main():
    print(find_princess(hostname, port))


if __name__ == "__main__":
    main()
