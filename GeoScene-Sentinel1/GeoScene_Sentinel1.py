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
        
        self.quicklookPath_auxField = arcpy.Field()
        self.quicklookPath_auxField.name = 'QuickLookPath'
        self.quicklookPath_auxField.aliasName = 'Quick Look Path'
        self.quicklookPath_auxField.type = 'String'
        self.quicklookPath_auxField.length = 2048
        
        self.quicklookFlag_auxField = arcpy.Field()
        self.quicklookFlag_auxField.name = 'QuicklookFlag'
        self.quicklookFlag_auxField.aliasName = 'Quick Look Flag'
        self.quicklookFlag_auxField.type = 'double'
        self.quicklookFlag_auxField.precision = 8
        
        #self.quicklook_auxField = arcpy.Field()
        #self.quicklook_auxField.name = 'QuickLook'
        #self.quicklook_auxField.aliasName = 'Quick Look'
        #self.quicklook_auxField.type = 'Blob'

        return [
                {
                    'rasterTypeName': 'GeoScene-Sentinel1',
                    'builderName': 'GeoSceneSentinelBuilder',
                    'description': ("Supports reading of GeoScene Sentinel1 data"),
                    'enableClipToFootprint': True,
                    'isRasterProduct': False,
                    'dataSourceType': (DataSourceType.Folder),  # DataSourceType.File | 
                    'dataSourceFilter': 'manifest.safe',
                    'crawlerName': 'GeoSceneSentinelCrawler',

                    'fields': [self.sensorName_auxField,
                               self.acquisitionDate_auxField,
                               self.quicklookPath_auxField,
                               self.quicklookFlag_auxField]
                    # ,self.quicklook_auxField
                }
               ]


class GeoSceneSentinelBuilder():

    def __init__(self, **kwargs):
        # self.RasterTypeName = 'GeoScene-Sentinel1'
        self.utilities = Utilities()
        
    def canOpen(self, datasetPath):
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
            if tree is None:
                return None


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
            
            quicklookPath = None
            quicklookFlag = None
            quicklookNode = self.utilities.getDataObjectByID(tree,'quicklook')
            if quicklookNode is not None:
                href = quicklookNode.find('byteStream/fileLocation').get('href')
                quicklookPath = os.path.abspath((os.path.dirname(path) if len(os.path.dirname(path)) != 0 else '.') + '/' + href)
                quicklookFlag = 1
            else:
                solutionLib_path = os.path.dirname(os.path.abspath(__file__)) 
                quicklookPath = os.path.join(solutionLib_path, 'noquicklook.png')
                quicklookFlag = 0
                
            footprintCoords = None
            spatialReference = None
            namespaces = self.utilities.getNamespace(path)
            metadataObjectNode = self.utilities.getMetadataObjectByID(tree,'measurementFrameSet')
            if metadataObjectNode is not None:
                footprintNode = metadataObjectNode.find('metadataWrap/xmlData/safe:frameSet/safe:frame/safe:footPrint',namespaces)
                spatialReference = int(footprintNode.get('srsName').split('#')[1]) if footprintNode is not None else None
                #coordsNode = metadataObjectNode.find('metadataWrap/xmlData/safe:frameSet/safe:frame/safe:footPrint/gml:coordinates',namespaces)
                #footprintCoords = self.utilities.getGeometryFromCoords(coordsNode.text) if coordsNode is not None else None
                
                dataObjs = metadataObjectNode.findall('metadataWrap/xmlData/safe:frameSet/safe:frame/safe:footPrint/gml:coordinates',namespaces)
                footprint_geometry = None
                polygon_array = arcpy.Array()
                #geo_final = None
                for dataObj in dataObjs:
                    coords = dataObj.text
                    vertex_array = arcpy.Array()
                    all_vertex = coords.split(" ")
                    for vertex in all_vertex:
                        point = vertex.split(',')
                        vertex_array.add(arcpy.Point(float(point[1]), float(point[0])))
                    polygon_array.add(vertex_array)
                    #if geo_final is None:
                    #    geo_final = arcpy.Polygon(vertex_array)
                    #else:
                    #    geo_final = geo_final.join(arcpy.Polygon(vertex_array))
                footprintCoords = arcpy.Polygon(polygon_array)
                footprintCoords = footprintCoords.convexHull()
                # footprintCoords = footprintCoords.extent
            
            sensorName = None
            platformNode = self.utilities.getMetadataObjectByID(tree,'platform')
            if platformNode is not None:
                familyName = platformNode.find('metadataWrap/xmlData/safe:platform/safe:familyName',namespaces)
                number = platformNode.find('metadataWrap/xmlData/safe:platform/safe:number',namespaces)
                sensorName = familyName.text + number.text if familyName is not None and number is not None else None

            acquistionDate = None
            acquisitionPeriodNode = self.utilities.getMetadataObjectByID(tree,'acquisitionPeriod')
            if acquisitionPeriodNode is not None:
                acquisitionPeriod = acquisitionPeriodNode.find('metadataWrap/xmlData/safe:acquisitionPeriod/safe:startTime',namespaces)
                acquistionDate = acquisitionPeriod.text[0:19].replace("T", " ") if acquisitionPeriod is not None else None
                

            metadata = {}
            metadata['SensorName'] = sensorName
            metadata['AcquisitionDate'] = acquistionDate
            metadata['QuickLookPath'] = quicklookPath
            metadata['QuicklookFlag'] = quicklookFlag
            # metadata['Quicklook'] = open(quicklookPath, "rb").read()
            
            # str.encode("UTF-8")
            # img.decode('UTF-8','strict'))
            # metadata['previewImage'] = img.decode('UTF-8','strict')
            # mdb.escape_string(img)
            
            builtItem = {}
            builtItem['itemUri'] = itemURI
            builtItem['raster'] = {'uri': quicklookPath}
            builtItem['footprint'] = footprintCoords
            builtItem['spatialReference'] = spatialReference
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
                # TODO ADD XML 
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

    #def __init__(self):
    #    self.__tree = None
    #    self.__namespace = None
    
    def isTarget(self, path):

        result = False
        sensorName = self.getSensorName(path)
        if sensorName is not None and sensorName[0:10] == 'SENTINEL-1':
            result = True
        return result

    def getTag(self, path):

        if self.isTarget(path):
            return 'SAR-Preview'
        return None
    
    def getTree(self,path):
        #if self.__tree is None:
        #    self.__tree = cacheElementTree(path)
        #return self.__tree
        return cacheElementTree(path)
    
    def getNamespace(self,path):
        #if self.__namespace is None:
        #    self.__namespace = dict([node for _, node in ET.iterparse(path, events=['start-ns'])])
        #return self.__namespace

        try:
            return dict([node for _, node in ET.iterparse(path, events=['start-ns'])])
        
        except StopIteration:
            return None

    def getMetadataObjectByID(self,tree,id):
        
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
            dataObjs = root.findall('dataObjectSection/dataObject')
            for dataObj in dataObjs:
                if dataObj.get('ID') == id:
                    return dataObj
        return None

    def getGeometryFromCoords(self, coords):

        vertex_array = arcpy.Array()
        all_vertex = coords.split(" ")
        for vertex in all_vertex:
            point = vertex.split(',')
            vertex_array.add(arcpy.Point(float(point[1]), float(point[0])))
        footprint_geometry = arcpy.Polygon(vertex_array)
        return footprint_geometry
        
    def getSensorName(self, path):
        tree = self.getTree(path)
        if tree is not None:
            metadataObjectNode = self.getMetadataObjectByID(tree,'platform')
            namespaces = self.getNamespace(path)
            if metadataObjectNode is not None:
                xmlData = metadataObjectNode.find('metadataWrap/xmlData')
                familyName = xmlData.find('safe:platform/safe:familyName',namespaces)
                number = xmlData.find('safe:platform/safe:number',namespaces)
                if familyName is not None and number is not None:
                    sensorName = familyName.text + number.text
                    return sensorName
        return None

    def getProductName(self, path):
        """        
        get Product Type
        :param path: manifest.safe
        :return:
        """
        tree = self.getTree(path)
        if tree is not None:
            metadataObjectNode = self.getMetadataObjectByID(tree,'generalProductInformation')
            namespaces = self.getNamespace(path)
            if metadataObjectNode is not None:
                productType = metadataObjectNode.find('metadataWrap/xmlData/s1sarl1:standAloneProductInformation/s1sarl1:productType',namespaces).text
                return productType
        return None
    
@lru_cache(maxsize=128)
def cacheElementTree(path):
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print("Exception while parsing {0}\n{1}".format(path,e))
        return None

    return tree