class Boundaries:
    """A class represntation of a rectangular bound
    """

    def __init__(self, ymin: float, xmin: float, ymax: float, xmax: float) -> None:
        """Boundaries class is instantiated by providing x minmum, y minmum,  x maximum, y maximum coordinates defining a rectangular bounds

        Args:
            ymin (float)
            xmin (float)
            ymax (float)
            xmax (float)
        """
        self.ymin = ymin
        self.xmin = xmin
        self.ymax = ymax
        self.xmax = xmax
        pass

    def getBounds(self) -> tuple:
        """Returns the extreme points defining the rectangular bounds in a list in the order of xmin, ymin, ymax, xmax
        """
        return ([self.xmin, self.ymin], [self.ymax, self.xmax])

    def getBoundStr(self) -> str:
        """Return a string representation of the extreme points defining the rectangular bounds in a '({[minx, maxx]},{[miny,maxy]})' format (i.e the format our pdal pipeline's reader.ept (https://pdal.io/stages/readers.ept.html#readers-ept) expects
        """
        return f"({[self.xmin, self.xmax]},{[self.ymin, self.ymax]})"
