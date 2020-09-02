#------------------------------------------------------------------------------
# Copyright 2016 Esri
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
import arcpy
import glob
import csv
from functools import lru_cache

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class DataSourceType():
    Unknown = 0
    File = 1
    Folder = 2


class RasterTypeFactory():

    def getRasterTypesInfo(self):

        self.acquisitionDate_auxField = arcpy.Field()
        self.acquisitionDate_auxField.name = 'AcquisitionDate'
        self.acquisitionDate_auxField.aliasName = 'Acquisition Date'
        self.acquisitionDate_auxField.type = 'Date'
        self.acquisitionDate_auxField.length = 50

        self.instrument_auxField = arcpy.Field()
        self.instrument_auxField.name = 'Instrument'
        self.instrument_auxField.aliasName = 'Instrument'
        self.instrument_auxField.type = 'String'
        self.instrument_auxField.length = 50

        self.sensorName_auxField = arcpy.Field()
        self.sensorName_auxField.name = 'SensorName'
        self.sensorName_auxField.aliasName = 'Sensor Name'
        self.sensorName_auxField.type = 'String'
        self.sensorName_auxField.length = 50

        self.sunAzimuth_auxField = arcpy.Field()
        self.sunAzimuth_auxField.name = 'SunAzimuth'
        self.sunAzimuth_auxField.aliasName = 'Sun Azimuth'
        self.sunAzimuth_auxField.type = 'Double'
        self.sunAzimuth_auxField.precision = 5

        self.sunElevation_auxField = arcpy.Field()
        self.sunElevation_auxField.name = 'SunElevation'
        self.sunElevation_auxField.aliasName = 'Sun Elevation'
        self.sunElevation_auxField.type = 'Double'
        self.sunElevation_auxField.precision = 5

        return [
                {
                    'rasterTypeName': 'DEIMOS-2',
                    'builderName': 'DeimosBuilder',
                    'description': ("Supports reading of DEIMOS-2 "
                                    "Level 1B / 1C product metadata files"),
                    'supportsOrthorectification': True,
                    'enableClipToFootprint': True,
                    'isRasterProduct': True,
                    'dataSourceType': (DataSourceType.File | DataSourceType.Folder),
                    'dataSourceFilter': '*.dim',
                    'crawlerName': 'Deimos2Crawler',
                    'supportedUriFilters': [
                                            {
                                                'name': 'Level1',
                                                'allowedProducts': [
                                                                    'L1C',
                                                                    'L1B'
                                                                   ],
                                                'supportsOrthorectification': True,
                                                'supportedTemplates': [
                                                                       'Multispectral',
                                                                       'Panchromatic',
                                                                       'Pansharpen',
                                                                       'All Bands'
                                                                      ]
                                            }
                                           ],
                    'productDefinitionName': 'DEIMOS2_4BANDS',
                    'processingTemplates': [
                                            {
                                                'name': 'Multispectral',
                                                'enabled': True,
                                                'outputDatasetTag': 'MS',
                                                'primaryInputDatasetTag': 'MS',
                                                'isProductTemplate': True,
                                                'functionTemplate': 'D2_stretch_ms.rft.xml'
                                            },
                                            {
                                                'name': 'Panchromatic',
                                                'enabled': False,
                                                'outputDatasetTag': 'Pan',
                                                'primaryInputDatasetTag': 'Pan',
                                                'isProductTemplate': True,
                                                'functionTemplate': 'D2_stretch_pan.rft.xml'
                                            },
                                            {
                                                'name': 'Pansharpen',
                                                'enabled': False,
                                                'outputDatasetTag': 'Pansharpened',
                                                'primaryInputDatasetTag': 'MS',
                                                'isProductTemplate': True,
                                                'functionTemplate': 'D2_stretch_psh.rft.xml'
                                            },
                                            {
                                                'name': 'All Bands',
                                                'enabled': False,
                                                'isProductTemplate': False,
                                                'functionTemplate': 'D2_stretch_allbands.rft.xml'
                                            }
                                           ],
                    'bandProperties': [
                                        {
                                            'bandName': 'Blue',
                                            'bandIndex': 3,
                                            'wavelengthMin': 466.0,
                                            'wavelengthMax': 525.0,
                                            'datasetTag': 'MS'
                                        },
                                        {
                                            'bandName': 'Green',
                                            'bandIndex': 2,
                                            'wavelengthMin': 532.0,
                                            'wavelengthMax': 599.0,
                                            'datasetTag': 'MS'
                                        },
                                        {
                                            'bandName': 'Red',
                                            'bandIndex': 1,
                                            'wavelengthMin': 640.0,
                                            'wavelengthMax': 697.0,
                                            'datasetTag': 'MS'
                                        },
                                        {
                                            'bandName': 'NearInfrared',
                                            'bandIndex': 0,
                                            'wavelengthMin': 770.0,
                                            'wavelengthMax': 892.0,
                                            'datasetTag': 'MS'
                                        },
                                        {
                                            'bandName': 'Panchromatic',
                                            'bandIndex': 0,
                                            'wavelengthMin': 560.0,
                                            'wavelengthMax': 900.0,
                                            'datasetTag': 'Pan'
                                        }
                                      ],
                    'fields': [self.sensorName_auxField,
                               self.acquisitionDate_auxField,
                               self.instrument_auxField,
                               self.sunAzimuth_auxField,
                               self.sunElevation_auxField]
                }
               ]


# ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ##
# Utility functions used by the Builder and Crawler classes
# ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ##


class Utilities():

    def isDeimos2(self, path):

        isD2 = False
        tree = cacheElementTree(path)
        if tree is not None:
            element = tree.find('Dataset_Sources/Source_Information/Scene_Source/MISSION')
            if element is not None:
                if 'Deimos 2' in element.text:
                    isD2 = True
        return isD2

    def __getTagFromTree(self, tree):
        
        nBands = tree.find('Raster_Dimensions/NBANDS')
        if nBands is not None:
            try:
                numBands = int(nBands.text)    
            except ValueError as e:
                print ("Value error {0}:".format(e))
                return None

            if numBands == 1:
                return 'Pan'
            if numBands >= 3:
                return 'MS'
        
        return None

    def getTag(self, path):
        # Get tag by parsing the dim file
        tree = cacheElementTree(path)
        if tree is not None:
            return self.__getTagFromTree(tree)

        return None

    def getProductName(self, tree):

        productName = tree.find('Production/PRODUCT_TYPE')
        if productName is not None:
            return productName.text

        return None

    def getProductNameFromFile(self, path):
        # Get product type
        tree = cacheElementTree(path)
        if tree is not None:
            return self.getProductName(tree)

        return None


# ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ##
# DEIMOS builder class
# ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ##


class DeimosBuilder():

    def __init__(self, **kwargs):
        self.SensorName = 'DEIMOS-2'
        self.utilities = Utilities()

    def canOpen(self, datasetPath):
        # Open the datasetPath and check if the metadata file contains the string Deimos
        return self.utilities.isDeimos2(datasetPath)

    def build(self, itemURI):

        # Make sure that the itemURI dictionary contains items
        if len(itemURI) <= 0:
            return None

        try:

            # ItemURI dictionary passed from crawler containing
            # path, tag, display name, group name, product type
            path = None
            if 'path' in itemURI:
                path = itemURI['path']
            else:
                return None

            # The metadata file is a XML file
            tree = cacheElementTree(path)
            # Horizontal CS (can also be a arcpy.SpatialReference object,
            # ESPG code, path to a PRJ file or a WKT string)
            srsWKT = 0
            projectionNode = tree.find('Coordinate_Reference_System/PROJECTION')
            if projectionNode is None:
                projectionNode = tree.find('Dataset_Sources/Source_Information/Coordinate_Reference_System/Projection_OGCWKT')

            if projectionNode is not None:
                srsWKT = projectionNode.text

            # Dataset path
            fileName = None
            filePathNode = tree.find('Data_Access/Data_File/DATA_FILE_PATH')
            if filePathNode is not None:
                fileName = filePathNode.attrib['href']

            if fileName is None:
                print ("path not found")
                return None

            fullPath = os.path.join(os.path.dirname(path), fileName)

            # Dataset frame - footprint; this is a list of Vertex coordinates
            vertex_array = arcpy.Array()
            all_vertex = tree.find('Dataset_Frame')
            if all_vertex is not None:
                for vertex in all_vertex:
                    x_vertex = vertex.find('FRAME_X')
                    y_vertex = vertex.find('FRAME_Y')
                    if x_vertex is not None and y_vertex is not None:
                        frame_x = float(x_vertex.text)
                        frame_y = float(y_vertex.text)
                        vertex_array.add(arcpy.Point(frame_x, frame_y))

            # Get geometry object for the footprint; the SRS of the
            # footprint can also be passed if it is different to the
            # SRS read from the metadata; by default, the footprint
            # geometry is assumed to be in the SRS of the metadata
            footprint_geometry = arcpy.Polygon(vertex_array)

            # Read pixel depth from dim file
            pixelDepthNode = tree.find('Raster_Encoding/NBITS')
            if pixelDepthNode is not None:
                pixelDepth = int(pixelDepthNode.text)
                            
            if pixelDepth == 16:
                maxInput = 1023
            if pixelDepth == 8:
                maxInput = 255

            # Metadata Information
            bandProperties = list()

            # Band info(part of metadata) - gain, bias etc
            img_interpretation = tree.find('Image_Interpretation')
            if img_interpretation is not None:
                for band_info in img_interpretation:
                    bandProperty = {}

                    band_desc = band_info.find('BAND_DESCRIPTION')
                    if band_desc is not None:
                        if band_desc.text == 'NIR':
                            bandProperty['bandName'] = 'NearInfrared'
                        elif band_desc.text == 'PAN':
                            bandProperty['bandName'] = 'Panchromatic'
                        else:
                            bandProperty['bandName'] = band_desc.text

                    band_num = 0
                    band_index = band_info.find('BAND_INDEX')
                    if band_index is not None:
                        band_num = int(band_index.text)

                    gain = band_info.find('PHYSICAL_GAIN')
                    if gain is not None:
                        bandProperty['RadianceGain'] = float(gain.text)

                    bias = band_info.find('PHYSICAL_BIAS')
                    if bias is not None:
                        bandProperty['RadianceBias'] = float(bias.text)

                    unit = band_info.find('PHYSICAL_UNIT')
                    if unit is not None:
                        bandProperty['unit'] = unit.text

                    bandProperties.append(bandProperty)

            # Other metadata information (Sun elevation, azimuth etc)
            metadata = {}

            acquisitionDate = None
            acquisitionTime = None

            scene_source = 'Dataset_Sources/Source_Information/Scene_Source'
            img_metadata = tree.find(scene_source)
            if img_metadata is not None:
                # Get the Sun Elevation
                sunElevation = img_metadata.find('SUN_ELEVATION')
                if sunElevation is not None:
                    metadata['SunElevation'] = float(sunElevation.text)

                # Get the acquisition date of the scene
                acquisitionDate = img_metadata.find('STOP_TIME')
                if acquisitionDate is not None:
                    metadata['AcquisitionDate'] = acquisitionDate.text

                # retrieve the view angle; this is the angle off Nadir view
                viewingAngle = img_metadata.find('SENSOR_VIEWING')
                if viewingAngle is None:
                    viewingAngle = img_metadata.find('VIEWING_ANGLE')

                if viewingAngle is not None:
                    metadata['OffNadir'] = float(viewingAngle.text)

                instrument = img_metadata.find('INSTRUMENT')
                if instrument is not None:
                    metadata['Instrument'] = instrument.text

                # Get the Sun Azimuth
                sunAzimuth = img_metadata.find('SUN_AZIMUTH')
                if sunAzimuth is not None:
                    metadata['SunAzimuth'] = float(sunAzimuth.text)

                # Get the Sun Distance
                sunDistance = img_metadata.find('EARTH_SUN_DISTANCE')
                if sunDistance is not None:
                    metadata['SunDistance'] = float(sunDistance.text)

            metadata['SensorName'] = self.SensorName
            metadata['bandProperties'] = bandProperties
            metadata['ProductType'] = self.utilities.getProductName(tree)

            # define a dictionary of variables
            variables = {}
            variables['DefaultMaximumInput'] = maxInput
            variables['DefaultGamma'] = 1

            # Assemble everything into an outgoing dictionary
            builtItem = {}
            builtItem['spatialReference'] = srsWKT
            builtItem['raster'] = {'uri': fullPath}
            builtItem['footprint'] = footprint_geometry
            builtItem['keyProperties'] = metadata
            builtItem['variables'] = variables
            builtItem['itemUri'] = itemURI

            builtItemsList = list()
            builtItemsList.append(builtItem)
            return builtItemsList

        except:
            raise


# ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ##
# DEIMOS Crawlerclass
# ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ## ----- ##


class Deimos2Crawler():

    def __init__(self, **crawlerProperties):
        self.utils = Utilities()
        self.paths = crawlerProperties['paths']
        self.recurse = crawlerProperties['recurse']
        self.filter = crawlerProperties['filter']

        if self.filter is (None or ""):
            self.filter = '*.dim'

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
                            if file.endswith(".dim"):
                                filename = os.path.join(root, file)
                                yield filename
                else:
                    filter_to_scan = path + os.path.sep + self.filter
                    for filename in glob.glob(filter_to_scan):
                        yield filename

            elif path.endswith(".csv"):
                with open(path, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    rasterFieldIndex = -1   
                    firstRow = next(reader)

                    #Check for the 'raster' field in the csv file, if not present take the first field as input data
                    for attribute in firstRow:
                        if attribute.lower() == 'raster':
                            rasterFieldIndex = firstRow.index(attribute)
                            break

                    if rasterFieldIndex == -1:
                        csvfile.seek(0)
                        rasterFieldIndex = 0

                    for row in reader:
                        filename = row[rasterFieldIndex]
                        if filename.endswith(".dim") and os.path.exists(filename):
                            yield filename

            elif path.endswith(".dim"):
                yield path

    def __iter__(self):
        return self

    def next(self):
        ## Return URI dictionary to Builder
        return self.getNextUri()
       

    def getNextUri(self):
        
        try:
            self.curPath = next(self.pathGenerator)
            curTag = self.utils.getTag(self.curPath)
            productName = self.utils.getProductNameFromFile(self.curPath)
            
            #If the tag or productName was not found in the metadata file or there was some exception raised, we move on to the next item
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



@lru_cache(maxsize=128)
def cacheElementTree(path):
        try:
            tree = ET.parse(path)
        except ET.ParseError as e:
            print("Exception while parsing {0}\n{1}".format(path,e))
            return None
      
        return tree
