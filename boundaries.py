class Boundaries:
    def __init__(self, ymin: float, xmin: float, ymax: float, xmax: float) -> None:
        self.ymin = ymin
        self.xmin = xmin
        self.ymax = ymax
        self.xmax = xmax
        pass

    def getBounds(self) -> tuple:
        return ([self.xmin, self.ymin], [self.ymax, self.xmax])

    def getBoundStr(self) -> str:
        return f"([{self.xmin}, {self.ymin}], [{self.ymax}, {self.xmax}])"
