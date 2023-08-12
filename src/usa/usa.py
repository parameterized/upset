class USA:
    S_i = set()

    def delta(self, element: tuple) -> tuple[set, set]:
        return (set(), set())

    def step(self) -> None:
        A, B = set(), set()
        for element in self.S_i:
            a, b = self.delta(element)
            A.update(a)
            B.update(b)

        self.S_i = (self.S_i | A) - B
