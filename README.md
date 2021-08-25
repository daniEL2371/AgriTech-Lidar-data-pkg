# AgriTech-Lidar-data-pkg
# Twitter-Data-Analysis

**Table of content**

- [Overview](##abstract)
- [Requirements](#setup)
- [Install](#install)
- [Data](#data)
- [Scripts](#scripts)
- [Usage](#usage)

## Overview
PythonLidar is an open-source python package for retrieving, transforming, and visualizing point cloud data obtained through an aerial LiDAR survey.
The package will accept boundary polygons in shapely.geometry.Polygon, and a coordinate reference system (CRS) and return a python dictionary with all years of data available and a geopandas grid point file with elevations encoded in the requested CRS. The package will also provide an option to graphically display the returned elevation files as a 3D plot and 2D heatmap.

## Requirements
- Python 3.5 and above, Pip
- Pdal
- Geopandas
- pandas
- laspy

## Install
```
git clone https://github.com/daniEL2371/AgriTech-Lidar-data-pkg.git
cd AgriTech-Lidar-data-pkg
pip install -r requirements.txt
```
## Data
- The USGS 3D Elevation Program (3DEP) provides access to lidar point cloud data from the 3DEP repository. The adoption of cloud storage and computing by 3DEP allows users to work with massive datasets of lidar point cloud data without having to download them to local machines.
- The point cloud data is freely accessible from AWS in EPT format. Entwine Point Tile (EPT) is a simple and flexible octree-based storage format for point cloud data. The organization of an EPT dataset contains JSON metadata portions as well as binary point data. The JSON file is core metadata required to interpret the contents of an EPT datase

## Usage
- A simple notebook on how to use the package is presented inside pkg_demonstration.ipynb
- For more please checkout the documentation here https://agri-tech-lidar-pkg.herokuapp.com/

