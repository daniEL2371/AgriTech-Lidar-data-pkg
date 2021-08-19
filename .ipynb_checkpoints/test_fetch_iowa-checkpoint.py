from lidar_fetch_data import Lidar_Data_Fetch
from boundaries import Boundaries
from elevation_extractor import ElevationExtractor
from shapely.geometry import box, Point, Polygon


REGION = "IA_FullState"
PUBLIC_DATA_URL = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
epsg = 4326

if __name__ == "__main__":
    fetcher = Lidar_Data_Fetch(PUBLIC_DATA_URL, epsg=epsg)

    MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.747334, 41.921429]

    polygon = Polygon(((MINX, MINY), (MINX, MAXY),
                       (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))
    xmin, ymin = -10425171.940, -10423171.940
    xmax, ymax = 5164494.710, 5166494.710
    bounds = Boundaries(ymin, xmin, ymax, xmax)

    data, output_epsg = fetcher.runPipeline(REGION, polygon)

    ee = ElevationExtractor(crs_epgs=epsg)
    df = ee.get_elevetion(data)

    print(df.info())
    print(df)
