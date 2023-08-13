import random
import dataclasses
from dataclasses import dataclass, field

from usa.usa import DictUSA


@dataclass(frozen=True)
class Branch:
    parent_id: str = None
    child_ids: frozenset[str] = field(default_factory=frozenset)
    branch_level: int = 0

    steps_to_split: int = 0
    x: float = 0
    y: float = 0


class Trees(DictUSA):
    # Should be read-only within this class (after initialization)
    S_i: dict[str, Branch]

    def __init__(self) -> None:
        super().__init__()
        # Initialize default root node
        self.S_i["0"] = Branch()

    def delta(
        self,
        e_kv: tuple[str, Branch],
    ) -> tuple[dict[str, Branch], dict[str, Branch]]:
        e_id, e = e_kv
        add_dict, sub_dict = dict(), dict()
        # If steps to split > 0, update this and position
        if e.steps_to_split > 0:
            add_dict[e_id] = dataclasses.replace(
                e,
                steps_to_split=e.steps_to_split - 1,
                x=e.x + (random.random() - 0.5) * 0.5 / e.branch_level**2,
                y=e.y + (random.random() - 0.5) * 0.5 / e.branch_level**2,
            )
            sub_dict[e_id] = e
        # If branch steps 0, level < 5, and no children yet: add children
        elif e.branch_level < 5 and len(e.child_ids) == 0:
            new_children = []
            for i, dir in enumerate([-1, 1]):
                child_id = e_id + str(i)
                new_children.append(child_id)
                add_dict[child_id] = Branch(
                    parent_id=e_id,
                    branch_level=e.branch_level + 1,
                    x=e.x + 2 * dir / 2**e.branch_level,
                    y=e.y + 4 / 3**e.branch_level,
                    steps_to_split=random.randint(10, 40),
                )
                print(add_dict[child_id].steps_to_split)

            # Update current element to have new children
            add_dict[e_id] = dataclasses.replace(
                e,
                child_ids=frozenset(new_children),
            )
            sub_dict[e_id] = e

        return (add_dict, sub_dict)
