from lidar_fetch_data import Lidar_Data_Fetch
from boundaries import Boundaries
from shapely.geometry import box, Point, Polygon
from elevation_extractor import ElevationExtractor
import geopandas as gpd
import matplotlib.pyplot as plt
import pickle



PUBLIC_DATA_URL = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
cache_folder = "./cache"



def read_obj(file_name):
        with open(f"{cache_folder}/{file_name}.pkl", "rb") as f:
            return pickle.load(f)

def write_obj(file_name, obj):
    if (not os.path.isdir('./cache')):
        os.mkdir("./cache/")
    
    with open(f"{cache_folder}/{file_name}.pkl", "wb") as f:
        pickle.dump(obj, f)

def get_cache_name_from_polygon(polygon: Polygon):
    x, y = polygon.exterior.coords.xy

    temp = ""
    for i, j in zip(list(x), list(y)):
        temp += f"{i}_{j}"

    hashed_name = hash(temp)
    
    if hashed_name < 0:
        hashed_name = "a" + str(hashed_name)[1:]
    
    return hashed_name
        
def cache_fetched_data(file_name: str, obj):

    try:
        write_model(str(file_name), obj)
    except:
        pass
        

class PythonLidarPackage:

    def __init__(self, crs_epsg : int) -> None:
        
        self.epsg = crs_epsg
        self.fetcher = Lidar_Data_Fetch(PUBLIC_DATA_URL, epsg=epsg)
        self.ee = ElevationExtractor(crs_epgs=crs_epsg)
    
    def __get_regions(self, polygon: Polygon) -> list:
        pass
    
    def get_elevation_df(self, polygon: Polygon, from_cache=True, enforce_cache = True):
        
        result = dict()
        
        cache = get_cache_name_from_polygon(polygon)
        
        if (from_cache and os.path.isfile(cahce_file_name)):
            return read_obj(cahce_file_name)
            
        
        regions_year_tuple = self.__get_regions()
        
        for region, year in regions_year_tuple:
            
            if year == 0:
                year = "Unknown"
            
            data, output_epsg = self.fetcher.runPipeline(region, polygon)
            df = self.ee.get_elevetion(data)
            result[region] = (year, df)
        
        if enforce_cache:
            cache_fetched_data(file_name, result)
        
        return result
    
    def save_elevation_geodata(self, df, polygon: Polygon,  file_name: str, save_format="shp"):
        
        polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])
        polygon_df.set_crs(epsg=self.epsg, inplace=True)
        
        if save_format == "shp":
            df.to_file(f"{file_name}_elevation.shp")
            polygon_df.to_file(f"{file_name}_boundaries.shp")
        
        elif save_format == "geojson":
            countries_gdf.to_file(f"{file_name}_elevation.geojson", driver='GeoJSON')
            polygon_df.to_file(f"{file_name}_boundaries.geojson", driver='GeoJSON')
        
        else:
            print("Unsupported format, geojson and shp are only supported formats")

    
    def get_heatmap_visulazation(self, df: gpd.GeoDataFrame, cmap="terrain") -> None :

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))

        df.plot(column='elevation', ax=ax, legend=True, cmap=cmap)
        plt.show()
    
    def covert_crs(self, df: gpd.GeoDataFrame, crs_epgs: int) -> gpd.GeoDataFrame:
        
        return self.ee.covert_crs(crs_epgs, df)



            
            

