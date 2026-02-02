from domain.position import Position
from domain.events import MoveProposal, Collision

# Interface Class for Collision Detection with its implementation
class CollisionDetector:
    def detect(
        self,
        step: int,
        proposals_by_position: dict[Position, list[MoveProposal]],
    ) -> list[Collision]:

        raise NotImplementedError


class SameTileCollisionDetector(CollisionDetector):
    def detect(
        self,
        step: int,
        proposals_by_position: dict[Position, list[MoveProposal]],
    ) -> list[Collision]:
        collisions: list[Collision] = []
        for pos, proposals in proposals_by_position.items():
            if len(proposals) > 1:
                collisions.append(
                    Collision(
                        position=pos,
                        step=step,
                        cars=[p.car for p in proposals],
                    )
                )
        return collisions

