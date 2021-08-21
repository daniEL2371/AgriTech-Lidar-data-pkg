from lidar_fetch_data import Lidar_Data_Fetch
from boundaries import Boundaries
from shapely.geometry import box, Point, Polygon
from elevation_extractor import ElevationExtractor
import geopandas as gpd
import matplotlib.pyplot as plt
import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import subsample


from boundaries import Boundaries


PUBLIC_DATA_URL = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
cache_folder = "./cache"
metadata_path = "./meta_data3.csv"
metric_epsg = 32643

try:
    meta_data = pd.read_csv(metadata_path)
    meta_data['year'] = meta_data['year'].fillna(0)
    meta_data['year'] = meta_data['year'].astype('int')
except:
    print("Could not read a metadata file")


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
        write_obj(str(file_name), obj)
    except:
        pass


class PythonLidarPackage:

    def __init__(self, crs_epsg: int) -> None:

        self.epsg = crs_epsg
        self.fetcher = Lidar_Data_Fetch(PUBLIC_DATA_URL, epsg=crs_epsg)
        self.ee = ElevationExtractor(crs_epgs=crs_epsg)
    
    def __get_region_from_boundary(self, bounds: Boundaries):
        filtered_df = meta_data.loc[
            (meta_data['xmin'] <= bounds.xmin)
            & (meta_data['xmax'] >= bounds.xmax)
            & (meta_data['ymin'] <= bounds.ymin)
            & (meta_data['ymax'] >= bounds.ymax)
        ]
        return filtered_df[["filename", "region", "year"]]

    def __get_regions(self, polygon: Polygon) -> dict():
        polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])

        polygon_df.set_crs(epsg=4326, inplace=True)
        polygon_df['geometry'] = polygon_df['geometry'].to_crs(
            epsg=3857)

        minx, miny, maxx, maxy = polygon_df['geometry'][0].bounds
        
        bounds = Boundaries(miny, minx, maxy, maxx)
        
        filtred_df = self.__get_region_from_boundary(bounds)
        filenames = filtred_df['filename'].to_list()
        years = filtred_df['year'].to_list()
        
        filename_year = dict()

        for filename, year in zip(filenames, years):
            filename_year[year] = filename

     
        return filename_year

    def get_elevation_df(self, polygon: Polygon, from_cache=True, enforce_cache=True):

        result = dict()

        cache_file_name = get_cache_name_from_polygon(polygon)

        if (from_cache and os.path.isfile(cache_file_name)):
            return read_obj(cache_file_name)

        regions_year_dict = self.__get_regions(polygon)
        
        ind = 0
    
        for year in regions_year_dict:
            
            
            file_name = regions_year_dict[year]
            if year == 0:
                year = "Unknown"
            
            try:
                print(f"trying to Fetch elevation data for year {year} from file_name {file_name}...")

                data, output_epsg = self.fetcher.runPipeline(file_name, polygon)
                df = self.ee.get_elevetion(data)
                result[year] = df
            except:
                pass
            ind += 1

        if enforce_cache:
            cache_fetched_data(cache_file_name, result)

        return result

    def save_elevation_geodata(self, df,  file_name: str, save_format="shp"):

#         polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])
#         polygon_df.set_crs(epsg=self.epsg, inplace=True)

        if save_format == "shp":
            df.to_file(f"{file_name}.shp")

        elif save_format == "geojson":
            df.to_file(f"{file_name}.geojson", driver='GeoJSON') 

        else:
            print("Unsupported format, geojson and shp are only supported formats")

    def get_heatmap_visulazation(self, df: gpd.GeoDataFrame, cmap="terrain") -> None:

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))

        df.plot(column='elevation', ax=ax, legend=True, cmap=cmap)
        plt.show()
    
    def get_3D_visualzation(self, df, s=0.01, color="blue"):
        
        x = df.geometry.x
        y = df.geometry.y
        z = df.elevation
        
        points = np.vstack((x, y, z)).transpose()
        
      
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        ax = plt.axes(projection='3d')
        ax.scatter(points[:,0], points[:,1], points[:,2],  s=0.01, color="blue")
        plt.show()
    
    def subsampling_interpolation(self, df: gpd.GeoDataFrame, resolution: int):
        df_meter = df.copy()
        df_meter['geometry'] = df_meter.geometry.to_crs(metric_epsg)
        df_meter = df_meter.set_crs(epsg=metric_epsg)
        
        subsample_df = subsample.grid_barycenter_sample(df_meter, resolution)
        print(f"subsampled number of points {subsample_df.shape[0]}")
        return subsample_df
        


    def covert_crs(self, df: gpd.GeoDataFrame, crs_epgs: int) -> gpd.GeoDataFrame:

        return self.ee.covert_crs(crs_epgs, df)
