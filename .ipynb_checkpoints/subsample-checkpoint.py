import geopandas as gpd
import numpy as np
from shapely.geometry import box, Point, Polygon



def get_points_from_df(df: gpd.GeoDataFrame):
    x = df.geometry.x
    y = df.geometry.y
    z = df.elevation
    points = np.vstack((x, y, z)).transpose()
    return points

def subsample(df: gpd.GeoDataFrame, method="grid_barycenter", resolution: int=3):
    
    points = get_points_from_df(df)
    
    voxel_size=resolution
    nb_vox=np.ceil((np.max(points, axis=0) - np.min(points, axis=0))/voxel_size)

    non_empty_voxel_keys, inverse, nb_pts_per_voxel = np.unique(((points - np.min(points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
    idx_pts_vox_sorted=np.argsort(inverse)

    voxel_grid={}
    grid_barycenter,grid_candidate_center=[],[]
    last_seen=0
    for idx,vox in enumerate(non_empty_voxel_keys):
        voxel_grid[tuple(vox)]= points[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
        grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
        grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(voxel_grid[tuple(vox)] - np.mean(voxel_grid[tuple(vox)],axis=0),axis=1).argmin()])
        last_seen+=nb_pts_per_voxel[idx]
    
    if method == "grid_barycenter":
        
        sub_sampled =  np.array(grid_barycenter)
    elif method == "grid_center":
        sub_sampled = np.array(grid_candidate_center)
    
    df_sampled = gpd.GeoDataFrame(columns=["elevation", "geometry"])
    geometry_points = [Point(x, y) for x, y in zip( sub_sampled[:, 0],  sub_sampled[:, 1])]

    df_sampled['elevation'] = sub_sampled[:,2]
    df_sampled['geometry'] = geometry_points
    
    return df_sampled
        
def grid_barycenter_sample(df: gpd.GeoDataFrame, resolution: int):
    return subsample(df, method="grid_barycenter", resolution=resolution)

def grid_candidate_center_sample(df: gpd.GeoDataFrame, resolution: int):
    return subsample(df, method="grid_center", resolution=resolution)

    
        