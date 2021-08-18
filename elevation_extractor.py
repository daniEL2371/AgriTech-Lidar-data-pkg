import laspy
import geopandas as gpd
from shapely.geometry import box, Point, Polygon
import numpy as np


class ElevationExtractor:

    def __init__(self, file_path: str, crs_epgs=26915) -> None:

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
        df.set_crs(epsg=self.crs_epgs, inplace=True)

        return df

    def covert_crs(self, crs_epgs: int, df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:

        df['geometry'] = df['geometry'].to_crs(crs_epgs)
        return df
