import geopandas as gpd
import numpy as np

def subsample(elevation_point_array_data, method="grid_barycenter"):
    
    data = elevation_point_array_data
    points = np.vstack((data[0]["X"], data[0]["Y"], data[0]["Z"])).transpose()
    voxel_size=1
    nb_vox=np.ceil((np.max(points, axis=0) - np.min(points, axis=0))/voxel_size)

    non_empty_voxel_keys, inverse, nb_pts_per_voxel = np.unique(((points - np.min(points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
    idx_pts_vox_sorted=np.argsort(inverse)

    voxel_grid={}
    grid_barycenter,grid_candidate_center=[],[]
    last_seen=0
    for idx,vox in enumerate(non_empty_voxel_keys):
        print(idx)
        voxel_grid[tuple(vox)]= points[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
        grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
        grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(voxel_grid[tuple(vox)] - np.mean(voxel_grid[tuple(vox)],axis=0),axis=1).argmin()])
        last_seen+=nb_pts_per_voxel[idx]
    
    if method == "grid_barycenter":
        return grid_barycenter
    elif method == "grid_center":
        grid_candidate_center
        
def grid_barycenter_sample(elevation_point_array_data):
    return subsample(elevation_point_array_data, method="grid_barycenter")

def grid_candidate_center_sample(elevation_point_array_data):
    return subsample(elevation_point_array_data, method="grid_center")

    
        