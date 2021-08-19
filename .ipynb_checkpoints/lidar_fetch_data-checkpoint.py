
import geopandas as gpd
import os
import pdal
import json
import ErrorMsgs

from boundaries import Boundaries
from shapely.geometry import Polygon, Point


err_msgs = ErrorMsgs.getErrorObj()


class Lidar_Data_Fetch:

    def __init__(self, public_data_url, epsg=26915, fetch_json_path="./fetch.json") -> None:
        self.public_data_url = public_data_url
        self.fetch_json_path = fetch_json_path

        self.__createDataFolderStruct()

        self.input_epsg = 3857
        self.output_epsg = epsg

        # todo if folder not exist create folder structure
        self.out_put_laz_path = "./data/laz/temp.laz"
        self.out_put_tif_path = "./data/tif/temp.tif"

    def __readFetchJson(self, path: str) -> dict:
        try:
            with open(path, 'r') as json_file:
                dict_obj = json.load(json_file)
            return dict_obj

        except FileNotFoundError as e:
            print(err_msgs['FETCH_JSON_FILE_NOT_FOUND'])

    def get_polygon_boundaries(self, polygon: Polygon):
        polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])

        polygon_df.set_crs(epsg=self.output_epsg, inplace=True)
        polygon_df['geometry'] = polygon_df['geometry'].to_crs(
            epsg=self.input_epsg)
        minx, miny, maxx, maxy = polygon_df['geometry'][0].bounds

        polygon_input = 'POLYGON(('

        xcord, ycord = polygon_df['geometry'][0].exterior.coords.xy
        for x, y in zip(list(xcord), list(ycord)):
            polygon_input += f'{x} {y}, '
        polygon_input = polygon_input[:-2]
        polygon_input += '))'
        

        return f"({[minx, maxx]},{[miny,maxy]})", polygon_input

    def getPipeline(self, region: str, polygon: Polygon):

        fetch_json = self.__readFetchJson(self.fetch_json_path)
        # BOUND = "([-10425171.94, -10423171.94], [5164494.71, 5166494.71])"

        boundaries, polygon_input = self.get_polygon_boundaries(polygon)

        full_dataset_path = f"{self.public_data_url}{region}/ept.json"

        fetch_json['pipeline'][0]['filename'] = full_dataset_path
        fetch_json['pipeline'][0]['bounds'] = boundaries

        fetch_json['pipeline'][1]['polygon'] = polygon_input

        fetch_json['pipeline'][4]['out_srs'] = f'EPSG:{self.output_epsg}'

        fetch_json['pipeline'][5]['filename'] = self.out_put_laz_path
        fetch_json['pipeline'][6]['filename'] = self.out_put_tif_path

        pipeline = pdal.Pipeline(json.dumps(fetch_json))

        return pipeline

    def runPipeline(self, region: str, polygon: Polygon):
        pipeline = self.getPipeline(region, polygon)

        try:
            pipeline.execute()
            metadata = pipeline.metadata
            log = pipeline.log
            return pipeline.arrays, self.output_epsg
        except RuntimeError as e:
            print(e)

    def __createDataFolderStruct(self):
        if (not os.path.isdir('./data')):
            os.mkdir("./data")
            os.mkdir("./data/laz/")
            os.mkdir("./data/tif/")
        if (not os.path.isdir('./data/laz')):
            os.mkdir("./data/laz/")
        if (not os.path.isdir('./data/tif')):
            os.mkdir("./data/tif/")
