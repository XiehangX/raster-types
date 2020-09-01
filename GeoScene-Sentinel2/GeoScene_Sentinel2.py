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

import arcpy


class DataSourceType():
    File = 1
    Folder = 2
    
class RasterTypeFactory():

    def getRasterTypesInfo(self):

        self.datastrip_id_auxField = arcpy.Field()
        self.datastrip_id_auxField.name = 'DatastripId'
        self.datastrip_id_auxField.aliasName = 'Datastrip_Id'
        self.datastrip_id_auxField.type = 'string'
        self.datastrip_id_auxField.length = 200

        self.clcoverp_auxField = arcpy.Field()
        self.clcoverp_auxField.name = 'CloudCoverPercentage'
        self.clcoverp_auxField.aliasName = 'Cloud Cover Percentage'
        self.clcoverp_auxField.type = 'double'
        self.clcoverp_auxField.precision = 5

##        self.datatake_identifier_auxField = arcpy.Field()
##        self.datatake_identifier_auxField.name = 'DataTakeIdentifier'
##        self.datatake_identifier_auxField.aliasName = 'Data Take Identifier'
##        self.datatake_identifier_auxField.type = 'string'
##        self.datatake_identifier_auxField.precision = 200

        self.dacq_auxField = arcpy.Field()
        self.dacq_auxField.name = 'AcquisitionDate'
        self.dacq_auxField.aliasName = 'Acquisition Date'
        self.dacq_auxField.type = 'date'

##        self.ancdp_auxField = arcpy.Field()
##        self.ancdp_auxField.name = 'DegradedANC_DataPercentage'
##        self.ancdp_auxField.aliasName = 'Degraded anc Data Percentage'
##        self.ancdp_auxField.type = 'double'
##        self.ancdp_auxField.length = 5

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

        self.reflconv_auxField = arcpy.Field()
        self.reflconv_auxField.name = 'ReflectanceConversion'
        self.reflconv_auxField.aliasName = 'Reflectance Conversion'
        self.reflconv_auxField.type = 'double'
        self.reflconv_auxField.precision = 50

        #self.tile_ref_auxField = arcpy.Field()################################
        #self.tile_ref_auxField.name = 'TileReference'
        #self.tile_ref_auxField.aliasName = 'Tile Reference'
        #self.tile_ref_auxField.type = 'String'
        #self.tile_ref_auxField.length = 50

##        self.Orbit_auxField = arcpy.Field()
##        self.Orbit_auxField.name = 'Orbit'
##        self.Orbit_auxField.aliasName = 'Orbit'
##        self.Orbit_auxField.type = 'float'
##        self.Orbit_auxField.precision = 10

##        self.Orbit_direction_auxField = arcpy.Field()
##        self.Orbit_direction_auxField.name = 'OrbitDirection'
##        self.Orbit_direction_auxField.aliasName = 'Orbit Direction'
##        self.Orbit_direction_auxField.type = 'string'
##        self.Orbit_direction_auxField.precision = 200

        #self.platform_code_auxField = arcpy.Field()###################################
        #self.platform_code_auxField.name = 'PlatformCode'
        #self.platform_code_auxField.aliasName = 'Platform Code'
        #self.platform_code_auxField.type = 'String'
        #self.platform_code_auxField.length = 200

        self.processingLevel_auxField = arcpy.Field()
        self.processingLevel_auxField.name = 'ProcessingLevel'
        self.processingLevel_auxField.aliasName = 'Processing Level'
        self.processingLevel_auxField.type = 'String'
        self.processingLevel_auxField.length = 200

        self.prod_format_auxField = arcpy.Field()
        self.prod_format_auxField.name = 'ProductFormat'
        self.prod_format_auxField.aliasName = 'Product Format'
        self.prod_format_auxField.type = 'String'
        self.prod_format_auxField.length = 200


##        self.prod_uri_auxField = arcpy.Field()
##        self.prod_uri_auxField.name = 'ProductURI'
##        self.prod_uri_auxField.aliasName = 'Product URI'
##        self.prod_uri_auxField.type = 'String'
##        self.prod_uri_auxField.length = 200

        self.tile_id_auxField = arcpy.Field()
        self.tile_id_auxField.name = 'TileID'
        self.tile_id_auxField.aliasName = 'Tile ID'
        self.tile_id_auxField.type = 'String'
        self.tile_id_auxField.length = 200

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
                # 'crawlerName': 'GeosceneSentinelCrawler',
                # 'productDefinitionName': 'Geoscene-Sentinel',
                # 'supportedUriFilters': [
                #     {
                #         'name': 'Level2',
                #         'allowedProducts': [
                #                 'S2MSIARD',
                #                 'ard'
                #         ],
                #         'supportsOrthorectification': True,
                #         'enableClipToFootprint': True,
                #         'supportedTemplates': [
                #             'Geoscience_MS_ALL',
                #             'Geoscience_MS_Supplementary',
                #             'Geoscience_MS_QA',
                #             'Geoscience_MS_Lambertian',
                #             'Geoscience_MS_NBAR',
                #             'Geoscience_MS_NBART'
                #         ]
                #     },

                #     {
                #         'name': 'Level1',
                #         'allowedProducts': [
                #                 'S2MSIARD',
                #                 'ard'
                #         ],
                #         'supportsOrthorectification': True,
                #         'supportedTemplates': [
                #             'Geoscience_MS_Lambertian'
                #         ]
                #     }
                # ],
                'processingTemplates': [
                    {
                        'name': 'GeoScene_ALL_Composite',
                        'enabled': True,
                        'outputDatasetTag': 'MS',
                        'primaryInputDatasetTag': 'MS',
                        'isProductTemplate': True,
                        'functionTemplate': 'GeoScene_ALL_Composite.rft.xml'
                    }
                ],
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

                'fields': [self.datastrip_id_auxField,
                           self.clcoverp_auxField,
                           # self.datatake_identifier_auxField,
                           self.dacq_auxField,
                           # self.ancdp_auxField,
                           self.sunAzimuth_auxField,
                           self.sunElevation_auxField,
                           # self.msidp_auxField,
                           self.reflconv_auxField,
                           # self.saturated_auxField,
                           self.tile_ref_auxField,
                           # self.Orbit_auxField,
                           # self.Orbit_direction_auxField,
                           self.platform_code_auxField,
                           # self.proc_baseline_auxField,
                           self.processingLevel_auxField,
                           self.prod_format_auxField,
                           # self.prod_uri_auxField,
                           self.tile_id_auxField]
            }
        ]


class GeoSceneSentinelBuilder():

    def __init__(self, **kwargs):
        self.RasterTypeName = 'GeoScene Sentinel2'
        print('init')

    def build(self, itemURI):
        
        print('build')
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



#class GeosceneSentinelCrawler():

#    def __init__(self, **crawlerProperties):
#        self.utils = Utilities()
#        try:
#            self.paths = crawlerProperties['paths']
#            self.recurse = crawlerProperties['recurse']
#            self.filter = crawlerProperties['filter']
#        except BaseException:
#            ##            print ('Error in crawler properties')
#            return None
#        self.run = 1
#        if (self.filter is (None or "")):
#            self.filter = 'L2*METADATA.yaml'
#        try:
#            self.pathGenerator = self.createGenerator()
#        except StopIteration:
#            return None

#        try:
#            self.tagGenerator = self.createTagGenerator()  # reinitialize tag generator
#        except StopIteration:
#            return None

#    def createTagGenerator(self):
#        for tag in [
#            "MS",
#            "Supplementary",
#            "Lambertian",
#            "QA",
#            "NBART",
#                "NBAR"]:  # Landsat8 L2 product have 5 types of sub-products
#            yield tag

#    def createGenerator(self):
#        for path in self.paths:
#            if (path.startswith("http") or (path.startswith("s3"))):
#                yield path

#            elif (not os.path.exists(path)):
#                continue

#            elif (os.path.isdir(path)):
#                if (self.recurse):
#                    for root, dirs, files in (os.walk(path)):
#                        for file in (files):
#                            if (file.endswith(".yaml")):
#                                filename = os.path.join(root, file)
#                                yield filename
#                else:
#                    filter_to_scan = path + os.path.sep + self.filter
#                    for filename in glob.glob(filter_to_scan):
#                        yield filename

#            elif (path.endswith(".csv")):
#                with open(path, 'r') as csvfile:
#                    reader = csv.reader(csvfile)
#                    rasterFieldIndex = -1
#                    firstRow = next(reader)
#                    # Check for the 'raster' field in the csv file, if not
#                    # present take the first field as input data
#                    for attribute in firstRow:
#                        if (attribute.lower() == 'raster'):
#                            rasterFieldIndex = firstRow.index(attribute)
#                            break
#                    if (rasterFieldIndex == -1):
#                        csvfile.seek(0)
#                        rasterFieldIndex = 0
#                    for row in reader:
#                        filename = row[rasterFieldIndex]
#                        if (filename.startswith("http")or (filename.startswith(
#                                "s3"))):  # if the csv list contains a list of s3 urls
#                            yield filename
#                        elif (filename.endswith(".yaml") and os.path.exists(filename)):
#                            yield filename
#            elif (path.endswith(".yaml")):
#                yield path

#    def __iter__(self):
#        return self

#    def next(self):
#        # Return URI dictionary to Builder
#        return self.getNextUri()

#    def getNextUri(self):
#        try:
#            if (self.run == 1):
#                try:
#                    self.curPath = next(self.pathGenerator)
#                    self.run = 10
#                except BaseException:
#                    return None
#            if ((self.curPath).startswith("http:")):
#                doc = self.utils.readYamlS3(self.curPath)
#            elif ((self.curPath).startswith("s3:")):
#                _yamlpath = self.curPath
#                # giving a start index of 5 will ensure that the / from s3://
#                # is not returned.
#                index = _yamlpath.find("/", 5)
#                # First 5 letters will always be s3://
#                bucketname = _yamlpath[5:index]
#                key = _yamlpath[index + 1:]
#                doc = self.utils.readYamlS3_boto3(bucketname, key)
#            else:
#                doc = self.utils.readYaml(self.curPath)
#            productName = self.utils.getProductName(doc)
#            processingLevel = self.utils.getProcessingLevel(doc)
#            if (processingLevel == "Level-2"):
#                try:
#                    curTag = next(self.tagGenerator)
#                except StopIteration:
#                    try:
#                        self.tagGenerator = self.createTagGenerator()  # reinitialize tag generator
#                    except StopIteration:
#                        return None
#                    try:
#                        self.curPath = next(self.pathGenerator)
#                    except BaseException:
#                        return None
#                    curTag = next(self.tagGenerator)
#                    if ((self.curPath).startswith(
#                            "http:")):  # this is needed to get the product name from the new path
#                        doc = self.utils.readYamlS3(self.curPath)
#                    else:
#                        doc = self.utils.readYaml(self.curPath)
#                    productName = self.utils.getProductName(doc)

#            else:
#                self.curPath = next(self.pathGenerator)
#                curTag = "MS"
#        except StopIteration:
#            return None
#        uri = {
#            'path': self.curPath,
#            'displayName': os.path.split(os.path.dirname(self.curPath))[1],
#            'tag': curTag,
#            'groupName': os.path.split(os.path.dirname(self.curPath))[1],
#            'productName': productName
#        }
#        return uri
