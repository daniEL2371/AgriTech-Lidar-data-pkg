

import pdal
import json
import ErrorMsgs

from boundaries import Boundaries


err_msgs = ErrorMsgs.getErrorObj()


class Lidar_Data_Fetch:

    def __init__(self, public_data_url, fetch_json_path="./fetch.json") -> None:
        self.public_data_url = public_data_url
        self.fetch_json_path = fetch_json_path
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

    def getPipeline(self, region: str, bounds: Boundaries):
        fetch_json = self.__readFetchJson(self.fetch_json_path)
        BOUND = "([-10425171.94, -10423171.94], [5164494.71, 5166494.71])"

        boundaries = bounds.getBoundStr()

        full_dataset_path = f"{self.public_data_url}{region}/ept.json"

        fetch_json['pipeline'][0]['filename'] = full_dataset_path
        fetch_json['pipeline'][0]['bounds'] = BOUND

        fetch_json['pipeline'][3]['filename'] = self.out_put_laz_path
        fetch_json['pipeline'][4]['filename'] = self.out_put_tif_path

        pipeline = pdal.Pipeline(json.dumps(fetch_json))

        return pipeline

    def runPipeline(self, region: str, bounds: Boundaries):
        pipeline = self.getPipeline(region, bounds)

        try:
            pipeline.execute()
            metadata = pipeline.metadata
            log = pipeline.log
        except RuntimeError as e:
            print(e)

    def __createDataFolderStruct(self):
        # todo create folder structure for output folder
        pass
