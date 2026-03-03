from domain.position import Position
from domain.car import Car
from domain.events import MoveProposal, Collision


class CollisionDetector():
    def __init__(self):
        self.collisions: list[Collision] = []

    def detect(self, step: int, paths: dict[Car, list[MoveProposal]]) -> list[Collision]:
        step_positions: dict[(Position, int), list[Car]] = {}
        position_graph = {}

        collided_positions = [
            collision.position
            for collision in self.collisions
        ]

        for car, proposals in paths.items():
            for proposal in proposals:

                if proposal.from_position != proposal.to_position:
                    position_graph[proposal.from_position] = proposal.to_position

                    if proposal.to_position in collided_positions:
                        existing_cars = next(
                            c.cars for c in self.collisions if c.position ==
                                proposal.to_position
                        )
                        self.collisions.append(
                            Collision(position=proposal.to_position,
                                      step=step, cars=existing_cars + [car])
                        )
                        continue

                step_positions.setdefault(
                    (proposal.to_position, step), []).append(car)

        for (position, step), cars in step_positions.items():
            if len(cars) > 1:
                self.collisions.append(
                    Collision(position=position, step=step, cars=cars)
                )

        cycles = self._find_cycles(position_graph)
        for cycle in cycles:
            if len(cycle) > 1:
                cars_in_cycle = []
                for car, proposals in paths.items():
                    for proposal in proposals:
                        if proposal.from_position in cycle and car not in cars_in_cycle:
                            cars_in_cycle.append(car)

                    self.collisions.append(
                        Collision(
                            position=cycle[0], step=step, cars=cars_in_cycle, type="cycle")
                    )

        return self.collisions

    def _find_cycles(self, graph):
        visited = set()
        cycles = []

        def dfs(node, path, path_set):
            if node in path_set:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:])
                return
            if node in visited:
                return
            visited.add(node)
            path.append(node)
            path_set.add(node)
            if node in graph:
                dfs(graph[node], path, path_set)
            path.pop()
            path_set.remove(node)

        for node in graph:
            if node not in visited:
                dfs(node, [], set())

        return cycles
