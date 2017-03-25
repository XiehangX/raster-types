# ArcGIS Raster Types in Python

This repository houses ArcGIS compatible Raster Types implemented in Python. This repository also contains developer-centric documentation on how to implement a custom raster type that ArcGIS can understand using Python.

A **Python raster type** is a [raster type](http://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/what-is-a-raster-type.htm) implemented in python. We can think of a raster type as a set of functions that understand the format of the metadata structure associated with any data; and it can parse the metadata to retrieve information such as 

- Paths to pixel data files
- Spatial reference information
- Metadata such as
  - Sensor name
  - Sun elevation, Sun azimuth, Sun distance
  - Acquisition date
  - Radiance/Reflectance parameters

In addition to parsing and reading metadata information from the metadata file, a raster type also defines the processing templates that are applicable to the type of data being read. The processing templates can combine different pieces of information from the source data to generate an output that is much more meaningful and convenient for further analysis. Most of the raster types based on sensor data define Multispectral as one of its processing templates. Many other templates can be defined based on the type of data available for a product. For example, Landsat 8 raster type defines various templates such as Multispectral, Panchromatic, Pansharpened, Vegetation, Cirrus, Snow/Ice etc.

## Getting Started 

Python Raster type framework is part of ArcGIS starting at version 10.5.1. To get started, install [ArcGIS Desktop 10.5.1](http://desktop.arcgis.com/en/#apps) or [ArcGIS Enterprise 10.5.1](http://server.arcgis.com/en/). 

## Resources

- Fundamentals
  - [ArcGIS Desktop Help](http://desktop.arcgis.com/en/documentation/)
  - [ArcGIS Enterprise Help](http://server.arcgis.com/en/documentation/)
  - [What is Python](http://desktop.arcgis.com/en/desktop/latest/analyze/python/what-is-python-.htm)

- Raster Types in ArcGIS
  - [What is a Raster Type](http://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/what-is-a-raster-type.htm)
  - [Raster Type properties](http://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/raster-type-properties.htm)
  - [What is a Raster Product](http://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/what-is-a-raster-product.htm)
  
## Issues

Find a bug or want to request a new feature? Please let us know by [submitting an issue](https://github.com/amitjain27/raster-types/issues).

## Licensing

Copyright 2017 Esri

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

A copy of the license is available in the repository's License.txt file.
