import laspy
import geopandas as gpd
from shapely.geometry import box, Point, Polygon
import numpy as np


class ElevationExtractor:
    """This class accapts a cloud datapoints and constructs a geopandas data frame having an elevation coulmn and a geometry column represnting points coordinate in a given coordinate reference system, CRS (https://epsg.io/)
    """

    def __init__(self, crs_epgs=26915) -> None:
        """This method is used to instantiate the class. It takes a CRS EPSG value (i.e refer to https://epsg.io/) to use

        Args:
            crs_epgs (int, optional): an integer EPSG value of coordinate reference system. Defaults to 26915.
        """

        self.crs_epgs = crs_epgs

    def __point_data_file(self, path: str) -> dict:
        try:
            las = laspy.read(path)
            return las

        except FileNotFoundError as e:
            print("File not found")

    def get_elevetion(self, array_data):
        """This method accapts cloud datapoints from the pdal pipeline output as a numpy array (i.e refer to https://pdal.io/python.html) and constructs a geopandas data frame having an elevation coulmn and a geometry column represnting point coordinates in a given coordinate reference system, CRS (https://epsg.io/)

        Args:
            array_data (Numpy): cloud datapoints results from pdal pipeline in Numpy format

        Returns:
            geopandas.GeoDataFrame: a geopandas data frame having an elevation coulmn and a geometry column represnting point coordinates in a given coordinate reference system

        """

        if array_data:

            for i in array_data:
                geometry_points = [Point(x, y) for x, y in zip(i["X"], i["Y"])]
                elevetions = i["Z"]
                df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
                df['elevation'] = elevetions
                df['geometry'] = geometry_points
                df = df.set_geometry("geometry")
                df.set_crs(epsg=self.crs_epgs, inplace=True)

            return df

        return None

    def get_elevetion_from_file(self, file_path: str):
        """This reads cloud data points file in LAS/LAZ format and constructs a geopandas data frame having an elevation coulmn and a geometry column represnting point coordinates in a given coordinate reference system, CRS (https://epsg.io/)

        Args:
            file_path (str): the path to LAS/LAZ file

        Returns:
            geopandas.GeoDataFrame: a geopandas data frame having an elevation coulmn and a geometry column represnting point coordinates in a given coordinate reference system
        """

        self.file_path = file_path
        self.las = self.__point_data_file(self.file_path)

        geometry_points = [Point(x, y) for x, y in zip(self.las.x, self.las.y)]
        elevetions = np.array(self.las.z)

        df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
        df['elevation'] = elevetions
        df['geometry'] = geometry_points
        df = df.set_geometry("geometry")
        df.set_crs(epsg=self.crs_epgs, inplace=True)

        return df

    def covert_crs(self, crs_epgs: int, df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """This method accepts a geopandas dataframe and a CRS and converts the dataframe to the provided coordinate reference system

        Args:
            df (gpd.GeoDataFrame): a geopandas data frame,  the dataframe must contain int sereis cloumn called elevation and and a geometry point series column called geometry.
            crs_epgs (int): [description]

        Returns:
            geopandas.GeoDataFrame: an integer EPSG value of coordinate reference system, (i.e refer to https://epsg.io/)
        """
        df_copy = df.copy()
        df_copy['geometry'] = df_copy['geometry'].to_crs(crs_epgs)
        df_copy = df_copy.set_crs(epsg=crs_epgs)
        return df_copy
