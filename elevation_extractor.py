import laspy
import geopandas as gpd
from shapely.geometry import box, Point, Polygon


class ElevationExtractor:

    def __init__(self, file_path: str, crs_epgs) -> None:

        self.file_path = file_path
        self.las = self.__point_data_file(self.file_path)
        self.crs_epgs = crs_epgs

    def __point_data_file(self, path: str) -> dict:
        try:
            las = laspy.read(path)
            return las

        except FileNotFoundError as e:
            print("File not found")

    def get_elevetion(self):

        geometry_points = [Point(x, y) for x, y in zip(self.las.x, self.las.y)]
        elevetions = np.array(self.las.z)

        df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
        df['elevation'] = elevetions
        df['geometry'] = geometry_points
        df = df.set_geometry("geometry")

        return df
