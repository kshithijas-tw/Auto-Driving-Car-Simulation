from domain.field import Field
from domain.car import Car
from domain.position import Position
from domain.direction import Direction
from domain.events import MoveProposal, Collision
from simulation.collision import CollisionDetector, SameTileCollisionDetector


class Simulation:
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
            collision_detector or SameTileCollisionDetector()
        )
        self.collisions: list[dict] = []

    def _collect_move_proposals(self) -> dict[Position, list[MoveProposal]]:
        proposals_by_position: dict[Position, list[MoveProposal]] = {}

        for car in self.cars:
            if not car.has_commands_left():
                continue

            from_pos = car.position
            from_dir = car.direction
            to_pos, to_dir = car.peek_next_state(self.field)

            proposal = MoveProposal(
                car=car,
                from_position=from_pos,
                to_position=to_pos,
                from_direction=from_dir,
                to_direction=to_dir,
            )
            proposals_by_position.setdefault(to_pos, []).append(proposal)

        return proposals_by_position

    def _record_collisions(self, collisions: list[Collision]) -> None:
        for collision in collisions:
            self.collisions.append(
                {
                    "position": collision.position,
                    "step": collision.step,
                    "cars": [car.name for car in collision.cars],
                }
            )

    def run(self) -> dict:
        while True:
            self.step += 1

            proposals_by_position = self._collect_move_proposals()

            collisions = self.collision_detector.detect(self.step, proposals_by_position)
            if collisions:
                self._record_collisions(collisions)
                break

            moved = False
            for proposals in proposals_by_position.values():
                for proposal in proposals:
                    proposal.car.commit(
                        proposal.to_position,
                        proposal.to_direction,
                    )
                    moved = True

            if not moved:
                break

        return {"collisions": self.collisions}
