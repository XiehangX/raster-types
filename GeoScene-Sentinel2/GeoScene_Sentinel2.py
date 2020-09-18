#------------------------------------------------------------------------------
# Copyright 2017 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#------------------------------------------------------------------------------

import os
import glob
import arcpy
from functools import lru_cache

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class DataSourceType():
    File = 1
    Folder = 2
    
class RasterTypeFactory():

    def getRasterTypesInfo(self):

        # thumbnail
        # Sensor Name
        # Acquistion Date
        # Sensing Orbit
        # Cloud Cover
        #sys_acquisitiondate	成像时间	Date	True			
        #sys_sensorname	传感器名称	Text	True			255
        #sys_productname	产品名称	Text	True			255
        #sys_resolution	分辨率	Text	True			255
        #sys_resolution_max	最大分辨率	Long	True			
        #sys_resolution_min	最小分辨率	Long	True			
        #sys_cloudcover	云量(%)	Double	True
        
        self.sensorName_auxField = arcpy.Field()
        self.sensorName_auxField.name = 'SensorName'
        self.sensorName_auxField.aliasName = 'Sensor Name'
        self.sensorName_auxField.type = 'String'
        self.sensorName_auxField.length = 50

        self.acquisitiondate_auxField = arcpy.Field()
        self.acquisitiondate_auxField.name = 'AcquisitionDate'
        self.acquisitiondate_auxField.aliasName = 'Acquisition Date'
        self.acquisitiondate_auxField.type = 'date'

        self.cloudcover_auxField = arcpy.Field()
        self.cloudcover_auxField.name = 'CloudCoverPercentage'
        self.cloudcover_auxField.aliasName = 'Cloud Cover Percentage'
        self.cloudcover_auxField.type = 'double'
        self.cloudcover_auxField.precision = 5

        self.resolution_auxField = arcpy.Field()
        self.resolution_auxField.name = 'Resolution'
        self.resolution_auxField.aliasName = 'Resolution'
        self.resolution_auxField.type = 'String'
        self.resolution_auxField.precision = 50
        
        self.resolutionmax_auxField = arcpy.Field()
        self.resolutionmax_auxField.name = 'ResolutionMax'
        self.resolutionmax_auxField.aliasName = 'Max Resolution'
        self.resolutionmax_auxField.type = 'double'
        self.resolutionmax_auxField.precision = 8

        self.resolutionmin_auxField = arcpy.Field()
        self.resolutionmin_auxField.name = 'ResolutionMin'
        self.resolutionmin_auxField.aliasName = 'Min Resolution'
        self.resolutionmin_auxField.type = 'double'
        self.resolutionmin_auxField.precision = 8

        return [
                {
                    'rasterTypeName': 'GeoScene-Sentinel2',
                    'builderName': 'GeoSceneSentinelBuilder',
                    'description': ("Supports reading of GeoScene Sentinel2 Level1 and Level2"),
                    'supportsOrthorectification': True,
                    'enableClipToFootprint': True,
                    'isRasterProduct': False,
                    'dataSourceType': (DataSourceType.File | DataSourceType.Folder),
                    'dataSourceFilter': 'MTD_MSI*.xml',
                    'crawlerName': 'GeoSceneSentinelCrawler',
                    # 'productDefinitionName': 'Geoscene-Sentinel',
                    #'supportedUriFilters': [
                    #    {
                    #        'name': 'LEVEL1C',
                    #        'allowedProducts': ['L1C'],
                    #        'supportsOrthorectification': True,
                    #        'enableClipToFootprint': True,
                    #        'supportedTemplates': ['GeoScene_ALL_Composite']
                    #    },
                    #    {
                    #        'name': 'LEVEL2A',
                    #        'allowedProducts': ['L2A'],
                    #        'supportsOrthorectification': True,
                    #        'supportedTemplates': ['GeoScene_ALL_Composite']
                    #    }
                    #],
                    #'processingTemplates': [
                    #    {
                    #        'name': 'GeoScene_ALL_Composite',
                    #        'enabled': True,
                    #        'outputDatasetTag': 'ALLBANDS',
                    #        'primaryInputDatasetTag': 'ALLBANDS',
                    #        'isProductTemplate': True,
                    #        'functionTemplate': 'GeoScene_ALL_Composite.rft.xml'
                    #    }
                    #],
                    # GET THE CORRECT BAND INDEX , MIN MAX WAVELENGTH
                    'bandProperties': [
                        {
                            'bandName': 'azimuthal_exiting',
                            'bandIndex': 1,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'azimuthal_incident',
                            'bandIndex': 2,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'exiting',
                            'bandIndex': 3,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'fmask',
                            'bandIndex': 4,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'incident',
                            'bandIndex': 5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_blue',
                            'bandIndex': 6,
                            'wavelengthMin': 447.6,
                            'wavelengthMax': 545.6,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_coastal_aerosol',
                            'bandIndex': 7,
                            'wavelengthMin': 430.4,
                            'wavelengthMax': 457.4,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_contiguity',
                            'bandIndex': 8,
                            'wavelengthMin': 1550.0,
                            'wavelengthMax': 1590.0,
                            'datasetTag': 'CG'
                        },
                        {
                            'bandName': 'lambertian_green',
                            'bandIndex': 9,
                            'wavelengthMin': 537.5,
                            'wavelengthMax': 582.5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_nir_1',
                            'bandIndex': 10,
                            'wavelengthMin': 762.6,
                            'wavelengthMax': 907.6,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_nir_2',
                            'bandIndex': 11,
                            'wavelengthMin': 848.3,
                            'wavelengthMax': 881.3,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_red',
                            'bandIndex': 12,
                            'wavelengthMin': 645.5,
                            'wavelengthMax': 683.5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_red_edge_1',
                            'bandIndex': 13,
                            'wavelengthMin': 694.4,
                            'wavelengthMax': 713.4,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_red_edge_2',
                            'bandIndex': 14,
                            'wavelengthMin': 731.2,
                            'wavelengthMax': 749.2,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_red_edge_3',
                            'bandIndex': 15,
                            'wavelengthMin': 768.5,
                            'wavelengthMax': 796.5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'lambertian_swir_2',
                            'bandIndex': 16,
                            'wavelengthMin': 1542.2,
                            'wavelengthMax': 1685.2,
                            'datasetTag': 'SWIR'
                        },
                        {
                            'bandName': 'lambertian_swir_3',
                            'bandIndex': 17,
                            'wavelengthMin': 2081.4,
                            'wavelengthMax': 2323.4,
                            'datasetTag': 'SWIR'
                        },
                        {
                            'bandName': 'nbar_blue',
                            'bandIndex': 18,
                            'wavelengthMin': 447.6,
                            'wavelengthMax': 545.6,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbar_coastal_aerosol',
                            'bandIndex': 19,
                            'wavelengthMin': 430.4,
                            'wavelengthMax': 457.4,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbar_contiguity',
                            'bandIndex': 20,
                            'datasetTag': 'CG'
                        },
                        {
                            'bandName': 'nbar_green',
                            'bandIndex': 21,
                            'wavelengthMin': 537.5,
                            'wavelengthMax': 582.5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbar_nir_1',
                            'bandIndex': 22,
                            'wavelengthMin': 762.6,
                            'wavelengthMax': 907.6,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbar_nir_2',
                            'bandIndex': 23,
                            'wavelengthMin': 848.3,
                            'wavelengthMax': 881.3,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbar_red',
                            'bandIndex': 24,
                            'wavelengthMin': 645.5,
                            'wavelengthMax': 683.5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbar_red_edge_1',
                            'bandIndex': 25,
                            'wavelengthMin': 694.4,
                            'wavelengthMax': 713.4,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbar_red_edge_2',
                            'bandIndex': 26,
                            'wavelengthMin': 731.2,
                            'wavelengthMax': 749.2,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbar_red_edge_3',
                            'bandIndex': 27,
                            'wavelengthMin': 768.5,
                            'wavelengthMax': 796.5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbar_swir_2',
                            'bandIndex': 28,
                            'wavelengthMin': 1542.2,
                            'wavelengthMax': 1685.2,
                            'datasetTag': 'SWIR'
                        },
                        {
                            'bandName': 'nbar_swir_3',
                            'bandIndex': 29,
                            'wavelengthMin': 2081.4,
                            'wavelengthMax': 2323.4,
                            'datasetTag': 'SWIR'
                        },
                        {
                            'bandName': 'nbart_blue',
                            'bandIndex': 30,
                            'wavelengthMin': 447.6,
                            'wavelengthMax': 545.6,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbart_coastal_aerosol',
                            'bandIndex': 31,
                            'wavelengthMin': 430.4,
                            'wavelengthMax': 457.4,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbart_contiguity',
                            'bandIndex': 32,
                            'datasetTag': 'CG'
                        },
                        {
                            'bandName': 'nbart_green',
                            'bandIndex': 33,
                            'wavelengthMin': 537.5,
                            'wavelengthMax': 582.5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbart_nir_1',
                            'bandIndex': 34,
                            'wavelengthMin': 762.6,
                            'wavelengthMax': 907.6,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbart_nir_2',
                            'bandIndex': 35,
                            'wavelengthMin': 848.3,
                            'wavelengthMax': 881.3,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbart_red',
                            'bandIndex': 36,
                            'wavelengthMin': 645.5,
                            'wavelengthMax': 683.5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbart_red_edge_1',
                            'bandIndex': 37,
                            'wavelengthMin': 694.4,
                            'wavelengthMax': 713.4,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbart_red_edge_2',
                            'bandIndex': 38,
                            'wavelengthMin': 731.2,
                            'wavelengthMax': 749.2,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbart_red_edge_3',
                            'bandIndex': 39,
                            'wavelengthMin': 768.5,
                            'wavelengthMax': 796.5,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'nbart_swir_2',
                            'bandIndex': 40,
                            'wavelengthMin': 1542.2,
                            'wavelengthMax': 1685.2,
                            'datasetTag': 'SWIR'
                        },
                        {
                            'bandName': 'nbart_swir_3',
                            'bandIndex': 41,
                            'wavelengthMin': 2081.4,
                            'wavelengthMax': 2323.4,
                            'datasetTag': 'SWIR'
                        },
                        {
                            'bandName': 'relative_azimuth',
                            'bandIndex': 42,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'relative_slope',
                            'bandIndex': 43,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'satellite_azimuth',
                            'bandIndex': 44,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'satellite_view',
                            'bandIndex': 45,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'solar_azimuth',
                            'bandIndex': 46,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'solar_zenith',
                            'bandIndex': 47,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'terrain_shadow',
                            'bandIndex': 48,
                            'datasetTag': 'MS'
                        },
                        {
                            'bandName': 'timedelta',
                            'bandIndex': 49,
                            'datasetTag': 'MS'
                        }
                    ]
                    ,
                    # GET THE CORRECT BAND INDEX , MIN MAX WAVELENGTH

                    'fields': [self.sensorName_auxField,
                               self.acquisitiondate_auxField,
                               self.cloudcover_auxField,
                               self.resolution_auxField,
                               self.resolutionmax_auxField,
                               self.resolutionmin_auxField]
                }
               ]


class GeoSceneSentinelBuilder():

    def __init__(self, **kwargs):
        self.RasterTypeName = 'GeoScene-Sentinel2'
        self.utilities = Utilities()
        
    def canOpen(self, datasetPath):
        # Open the datasetPath and check if the metadata file contains the string TELEOS
        return self.utilities.isTarget(datasetPath)

    def build(self, itemURI):
        
        if len(itemURI) <= 0:
            return None

        try:
            path = None
            if 'path' in itemURI:
                path = itemURI['path']
            else:
                return None

            builtItem = {}
            builtItem['raster'] = {'uri': path}
            builtItem['itemUri'] = itemURI

            builtItemsList = list()
            builtItemsList.append(builtItem)
            return builtItemsList

        except:
            return None

class GeoSceneSentinelCrawler():

    def __init__(self, **crawlerProperties):
        self.utils = Utilities()
        try:
            self.paths = crawlerProperties['paths']
            self.recurse = crawlerProperties['recurse']
            self.filter = crawlerProperties['filter']
        except BaseException:
            return None
        self.run = 1
        if (self.filter is (None or "")):
            self.filter = 'MTD_MSI*.xml'
        try:
            self.pathGenerator = self.createGenerator()
        except StopIteration:
            return None

    def createGenerator(self):
        for path in self.paths:
            if not os.path.exists(path):
                continue
            
            if os.path.isdir(path):
                if self.recurse:
                    for root, dirs, files in (os.walk(path)):
                        for file in (files):
                            if file.endswith(".xml") and file.startswith("MTD_MSIL"):
                                filename = os.path.join(root, file)
                                yield filename
                else:
                    filter_to_scan = path + os.path.sep + self.filter
                    for filename in glob.glob(filter_to_scan):
                        yield filename
            # Todo PATH is like this and always false
            # \\192.168.1.223\ImageData\Test\Sentinel-2\L2A\S2A_MSIL2A_20200608T025551_N0214_R032_T49QFF_20200608T071537.SAFE\MTD_MSIL2A.xml
            #elif path.endswith(".xml") and "MTD_MSIL" in path:
            #    yield path

    def __iter__(self):
        return self

    def next(self):
        # Return URI dictionary to Builder
        return self.getNextUri()

    def getNextUri(self):
        
        try:
            self.curPath = next(self.pathGenerator)
            curTag = self.utils.getTag(self.curPath)
            productName = self.utils.getProductName(self.curPath)
            
            if curTag is None or productName is None:
                return self.getNextUri()

        except StopIteration:
            return None

        uri = {
                'path': self.curPath,
                'displayName': os.path.basename(self.curPath),
                'tag': curTag,
                'groupName': os.path.split(os.path.dirname(self.curPath))[1],
                'productName': productName
              }

        return uri

class Utilities():
    
    def isTarget(self, path):

        result = False
        tree = cacheElementTree(path)
        if tree is not None:
            generalInfo = self.__getGeneralInfoElement(tree)
            if generalInfo is not None:
                element = generalInfo.find('Product_Info/PRODUCT_TYPE')
                if element is not None and  'S2MSI' in element.text:
                    result = True
        return result

    def getTag(self, path):

        if self.isTarget(path):
            return 'ALLBANDS'
        return None

    def __getGeneralInfoElement(self,tree):
        
        if tree is not None:
            root = tree.getroot()
            if root is None:
                return result
            for child in root:
                if 'General_Info' in child.tag:
                    return child
        return None
    
    def getProductName(self, path):
        """        
        get Product Type
        :param path: MTD_MSI*.xml
        :return:
        """
        tree = cacheElementTree(path)
        if tree is not None:
            generalInfo = self.__getGeneralInfoElement(tree)
            if generalInfo is not None:
                product = generalInfo.find('Product_Info/PRODUCT_TYPE')
                if product is not None:
                    return product.text
        return None


    #def getProcessingLevel(self, doc):
    #    try:
    #        processingLevel = doc['processing_level']
    #        if (processingLevel is not None):
    #            return processingLevel
    #    except BaseException:
    #        return None
    #    return None
    
@lru_cache(maxsize=128)
def cacheElementTree(path):
        try:
            tree = ET.parse(path)
        except ET.ParseError as e:
            print("Exception while parsing {0}\n{1}".format(path,e))
            return None

        return tree