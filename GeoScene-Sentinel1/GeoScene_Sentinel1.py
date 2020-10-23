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
        self.sensorName_auxField = arcpy.Field()
        self.sensorName_auxField.name = 'SensorName'
        self.sensorName_auxField.aliasName = 'Sensor Name'
        self.sensorName_auxField.type = 'String'
        self.sensorName_auxField.length = 50

        self.acquisitionDate_auxField = arcpy.Field()
        self.acquisitionDate_auxField.name = 'AcquisitionDate'
        self.acquisitionDate_auxField.aliasName = 'Acquisition Date'
        self.acquisitionDate_auxField.type = 'date'
        
        self.dirName_auxField = arcpy.Field()
        self.dirName_auxField.name = 'DirName'
        self.dirName_auxField.aliasName = 'Dir Name'
        self.dirName_auxField.type = 'String'
        self.dirName_auxField.length = 2048
        
        #self.previewImage_auxField = arcpy.Field()
        #self.previewImage_auxField.name = 'PreviewImage'
        #self.previewImage_auxField.aliasName = 'Preview Image'
        #self.previewImage_auxField.type = 'Blob'
        

        return [
                {
                    'rasterTypeName': 'GeoScene-Sentinel1',
                    'builderName': 'GeoSceneSentinelBuilder',
                    'description': ("Supports reading of GeoScene Sentinel1 data"),
                    'enableClipToFootprint': True,
                    'isRasterProduct': False,
                    'dataSourceType': (DataSourceType.File | DataSourceType.Folder),
                    'dataSourceFilter': 'manifest.safe',
                    'crawlerName': 'GeoSceneSentinelCrawler',
                    # 'productDefinitionName': 'Geoscene-Sentinel',
                    #'supportedUriFilters': [
                    #    {
                    #        'name': 'Level2',
                    #        'allowedProducts': [
                    #                'gamma_0',
                    #        ],
                    #        'supportsOrthorectification': True,
                    #        'enableClipToFootprint': True,
                    #        'supportedTemplates': [
                    #            'DataCube_S1_SAR',
                    #        ]
                    #    }

                    #],
                    #'processingTemplates': [
                    #    {
                    #        'name': 'DataCube_S1_SAR',
                    #        'enabled': True,
                    #        'outputDatasetTag': 'DataCube_S1_SAR',
                    #        'primaryInputDatasetTag': 'DataCube_S1_SAR',
                    #        'isProductTemplate': True,
                    #        'functionTemplate': 'DataCube_S1_SAR.rft.xml'
                    #    }
                    #],
                    ## GET THE CORRECT BAND INDEX , MIN MAX WAVELENGTH
                    #'bandProperties': [
                    #    {
                    #        'bandName': 'vh',
                    #        'bandIndex': 1,
                    #        'wavelengthMin': 180000000.0,  # C band with central frequency of 5.405 GHz
                    #        'wavelengthMax': 180000000.0,
                    #        'datasetTag': 'SAR'
                    #    }
                    #    ,
                    #    {
                    #        'bandName': 'vv',
                    #        'bandIndex': 2,
                    #        'wavelengthMin': 180000000.0,  # C band with central frequency of 5.405 GHz
                    #        'wavelengthMax': 180000000.0,
                    #        'datasetTag': 'SAR'
                    #    }
                    #],
                    # GET THE CORRECT BAND INDEX , MIN MAX WAVELENGTH

                    'fields': [self.sensorName_auxField,
                               self.acquisitionDate_auxField,
                               self.dirName_auxField]
                                #,self.previewImage_auxField
                }
               ]


class GeoSceneSentinelBuilder():

    def __init__(self, **kwargs):
        self.RasterTypeName = 'GeoScene-Sentinel1'
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

            tree = cacheElementTree(path)
            builtItem = {}

            #rasterInfo = {}
            ##rasterInfo['pixelType'] = pixelType
            ##rasterInfo['nCols'] = nCols
            ##rasterInfo['nRows'] = nRows
            ##rasterInfo['nBands'] = noBands
            #rasterInfo['spatialReference'] = int('4326')
            #rasterInfo['XMin'] = 111.711006
            #rasterInfo['YMin'] = 23.911518
            #rasterInfo['XMax'] = 114.473335
            #rasterInfo['YMax'] = 24.327019
            #builtItem['raster'] = {'uri': self.utilities.getQuickLook(path), 'rasterInfo': rasterInfo}

            builtItem['raster'] = {'uri': self.utilities.getQuickLook(path)}
            builtItem['itemUri'] = itemURI

            vertex_array = arcpy.Array()
            footprintCoords = self.utilities.getFootPrintCoords(path)
            if footprintCoords is not None:
                all_vertex = footprintCoords.split(" ")
                for vertex in all_vertex:
                    point = vertex.split(',')
                    vertex_array.add(arcpy.Point(float(point[1]), float(point[0])))
            footprint_geometry = arcpy.Polygon(vertex_array)
            builtItem['footprint'] = footprint_geometry
            
            sr = self.utilities.getFootPrintSR(path)
            builtItem['spatialReference'] = int(sr)
            
            metadata = {}
            metadata['SensorName'] = self.utilities.getSensorName(path)
            metadata['AcquisitionDate'] = self.utilities.getAcquistionDate(path)
            metadata['DirName'] = os.path.dirname(path)
            
            #quicklookpath = self.utilities.getQuickLook(path)
            #f = open(os.path.abspath(quicklookpath), "rb")
            #img = f.read()
            #f.close()
            #metadata['previewImage'] = str(img)

            # str.encode("UTF-8")
            # img.decode('UTF-8','strict'))
            # metadata['previewImage'] = img.decode('UTF-8','strict')
            # mdb.escape_string(img)

            builtItem['keyProperties'] = metadata

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
            self.filter = 'manifest.safe'
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
                            if file.endswith(".safe") and file.startswith("manifest"):
                                filename = os.path.join(root, file)
                                yield filename
                else:
                    filter_to_scan = path + os.path.sep + self.filter
                    for filename in glob.glob(filter_to_scan):
                        yield filename

            elif path.endswith(".safe") and "manifest.safe" in path:
                yield path

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

    #__namespace : None
    #__tree: None

    def __init__(self):
        self.__tree = None
        self.__namespace = None
    
    def isTarget(self, path):

        result = False
        sensorName = self.getSensorName(path)
        if sensorName is not None and sensorName[0:10] == 'SENTINEL-1':
            result = True
        return result

    def getTag(self, path):

        if self.isTarget(path):
            return 'SAR'
        return None
    
    def getTree(self,path):
        if self.__tree is None:
            self.__tree = cacheElementTree(path)
        return self.__tree

    def __getMetadataObjectByID(self,tree,id):
        
        if tree is not None:
            root = tree.getroot()
            metadataSectionNode = root.find('metadataSection')
            if metadataSectionNode is not None:
                for child in metadataSectionNode:
                    if child.tag == 'metadataObject' and child.get('ID') == id:
                        return child
        return None

    def getDataObjectByID(self,tree,id):
        
        if tree is not None:
            root = tree.getroot()
            metadataObjs = root.findall('dataObjectSection/dataObject')
            for metadataObj in metadataObjs:
                if metadataObj.get('ID') == id:
                    return metadataObj
        return None

    def getQuickLook(self,path):
        
        tree = self.getTree(path)
        if tree is not None:
            quicklookNode = self.getDataObjectByID(tree,'quicklook')
            if quicklookNode is not None:
                href = quicklookNode.find('byteStream/fileLocation').get('href')                
                #os.chdir(path)
                #quicklookPath = os.path.abspath(href)
                quicklookPath = os.path.dirname(path) if len(os.path.dirname(path)) != 0 else '.'
                return quicklookPath + '/' + href
        return None
    
    def getNamespace(self,path):
        if self.__namespace is None:
            self.__namespace = dict([node for _, node in ET.iterparse(path, events=['start-ns'])])
        return self.__namespace
    
    def getFootPrintCoords(self, path):
        tree = self.getTree(path)
        if tree is not None:
            metadataObjectNode = self.__getMetadataObjectByID(tree,'measurementFrameSet')
            namespaces = self.getNamespace(path)
            if metadataObjectNode is not None:
                xmlData = metadataObjectNode.find('metadataWrap/xmlData')
                coords = xmlData.find('safe:frameSet/safe:frame/safe:footPrint/gml:coordinates',namespaces)
                if coords is not None:
                    return coords.text
        return None

    def getFootPrintSR(self, path):
        tree = self.getTree(path)
        if tree is not None:
            metadataObjectNode = self.__getMetadataObjectByID(tree,'measurementFrameSet')
            namespaces = self.getNamespace(path)
            if metadataObjectNode is not None:
                xmlData = metadataObjectNode.find('metadataWrap/xmlData')
                footprint = xmlData.find('safe:frameSet/safe:frame/safe:footPrint',namespaces)
                if footprint is not None:
                    return footprint.get('srsName').split('#')[1]
        return None
    
    def getSensorName(self, path):
        tree = self.getTree(path)
        if tree is not None:
            metadataObjectNode = self.__getMetadataObjectByID(tree,'platform')
            namespaces = self.getNamespace(path)
            if metadataObjectNode is not None:
                xmlData = metadataObjectNode.find('metadataWrap/xmlData')
                familyName = xmlData.find('safe:platform/safe:familyName',namespaces)
                number = xmlData.find('safe:platform/safe:number',namespaces)
                if familyName is not None and number is not None:
                    sensorName = familyName.text + number.text
                    return sensorName
        return None

    def getAcquistionDate(self, path):
        tree = self.getTree(path)
        if tree is not None:
            metadataObjectNode = self.__getMetadataObjectByID(tree,'acquisitionPeriod')
            namespaces = self.getNamespace(path)
            if metadataObjectNode is not None:
                xmlData = metadataObjectNode.find('metadataWrap/xmlData')
                acquisitionPeriod = xmlData.find('safe:acquisitionPeriod/safe:startTime',namespaces)
                if acquisitionPeriod is not None:
                    return acquisitionPeriod.text[0:19].replace("T", " ")
        return None

    def getProductName(self, path):
        """        
        get Product Type
        :param path: manifest.safe
        :return:
        """
        tree = self.getTree(path)
        if tree is not None:
            metadataObjectNode = self.__getMetadataObjectByID(tree,'generalProductInformation')
            namespaces = self.getNamespace(path)
            if metadataObjectNode is not None:
                xmlData = metadataObjectNode.find('metadataWrap/xmlData')
                productType = xmlData.find('s1sarl1:standAloneProductInformation/s1sarl1:productType',namespaces).text
                return productType
        return None

    def getInfoElement(self,tree,metadataObjectId):
        if tree is not None:
            root = tree.getroot()
            if root is None:
                return result
            for child in root:
                if infoTag in child.tag:
                    return child
        return None
    
@lru_cache(maxsize=128)
def cacheElementTree(path):
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print("Exception while parsing {0}\n{1}".format(path,e))
        return None

    return tree