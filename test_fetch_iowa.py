from lidar_fetch_data import Lidar_Data_Fetch
from boundaries import Boundaries


REGION = "IA_FullState"
PUBLIC_DATA_URL = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
if __name__ == "__main__":
    fetcher = Lidar_Data_Fetch(PUBLIC_DATA_URL)

    xmin, ymin = -10425171.940, -10423171.940
    xmax, ymax = 5164494.710, 5166494.710
    bounds = Boundaries(ymin, xmin, ymax, xmax)

    fetcher.runPipeline(REGION, bounds)
