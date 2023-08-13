from typing import Any


class USA:
    S_i: set

    def __init__(self) -> None:
        self.S_i = set()

    def delta(self, element) -> tuple[set, set]:
        return (set(), set())

    def step(self) -> None:
        A, B = set(), set()
        for element in self.S_i:
            a, b = self.delta(element)
            A |= a
            B |= b

        self.S_i = (self.S_i | A) - B


class DictUSA:
    """
    It may be more efficient to impelemnt S_i with dictionaries.
    We can still formalize this as a set of elements from $K \\times V$
    with the restriction that elements in S_i can only have one
    (k, v) pair for each $k \in K$.

    Caveats:
    - delta is now passed a (key, value) pair.
    - If the additive dictionary returned by two calls to delta,
      the update to S_i will depend on iteration order (try to avoid this).
    - Values in delta's subtractive dictionary should allow "!=" comparison
      to ensure correct updates to S_i.
    """
    S_i: dict

    def __init__(self) -> None:
        self.S_i = dict()

    def delta(self, element: tuple[Any, Any]) -> tuple[dict, dict]:
        return (dict(), dict())

    def step(self) -> None:
        # TODO: optionally enable error checking for the mentioned caveats, test performance
        A, B = dict(), dict()
        for element in self.S_i.items():
            a, b = self.delta(element)
            # Updates may conflict here
            A |= a
            B |= b

        # Values from A will overwrite any existing values with the same key
        self.S_i |= A
        # Only remove B elements if both key and value match
        self.S_i = {k: v for k, v in self.S_i.items() if k not in B or v != B[k]}
