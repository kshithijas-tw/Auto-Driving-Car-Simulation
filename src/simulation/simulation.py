from domain.field import Field
from domain.car import Car
from domain.events import MoveProposal
from simulation.collision import CollisionDetector


class SimulationBase:
    def __init__(
        self,
        field: Field,
        cars: list[Car],
        collision_detector: CollisionDetector | None = None,
    ):
        self.field = field
        self.cars = cars
        self.step = 0
        self.collision_detector: CollisionDetector = (
            collision_detector or CollisionDetector()
        )

    def _collect_move_proposals(self) -> dict[Car, list[MoveProposal]]:
        paths: dict[Car, list[MoveProposal]] = {}

        for car in self.cars:
            if not car.has_commands_left():
                continue

            from_pos = car.position
            from_dir = car.direction
            to_pos, to_dir = car.peek_next_state(self.field)

            proposal = MoveProposal(
                from_position=from_pos,
                to_position=to_pos,
                from_direction=from_dir,
                to_direction=to_dir,
            )
            paths.setdefault(car, []).append(proposal)

        return paths

    def run(self) -> dict:
        raise NotImplementedError


class StepByStepSimulation(SimulationBase):
    def run(self) -> dict:
        while True:
            self.step += 1

            paths = self._collect_move_proposals()

            collisions = self.collision_detector.detect(self.step, paths)
            for collision in collisions:
                for car in collision.cars:
                    car.set_collided()

            moved = False
            for car, proposals in paths.items():
                for proposal in proposals:
                    if car.has_collided():
                        continue
                    car.commit(
                        proposal.to_position,
                        proposal.to_direction,
                    )
                    moved = True

            if not moved:
                break

        return {"collisions": collisions}
