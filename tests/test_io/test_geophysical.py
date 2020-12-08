import pytest
from osgeo import gdal
import numpy as np
from subsurface.io.geophysical import read_in_geophysical_data, read_in_dat_files
import os

input_path = os.path.dirname(__file__) + '/../data/geophysical/'


@pytest.fixture(scope='module')
def get_data():
    header, data = read_in_geophysical_data(input_path + 'grav.ers', input_path + 'grav')
    columns_map = ['Line', 'Station', 'East_KKJ', 'North_KKJ', 'Lon_Intl24', 'Lat_Intl24', 'Elev_m', 'Orig_Boug267', 'Terr_corr', 'Curv_corr', 'Boug310',  'TC_Boug310', 'TC+Curv310']
    lines = read_in_dat_files(input_path + 'grav.dat', columns_map=columns_map)
    return header, data, lines


def test_data_retrieved(get_data):
    header, dataset, lines = get_data
    print(header)
    # print(dataset)
    # print(lines[0:2])
    # print("Driver: {}/{}".format(dataset.GetDriver().ShortName,
    #                              dataset.GetDriver().LongName))
    # print("Size is {} x {} x {}".format(dataset.RasterXSize,
    #                                     dataset.RasterYSize,
    #                                     dataset.RasterCount))
    # print("Projection is {}".format(dataset.GetProjection()))
    # geotransform = dataset.GetGeoTransform()
    #
    # if geotransform:
    #     print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
    #     print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
    #
    # band = dataset.GetRasterBand(1)
    # print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))
    #
    # min = band.GetMinimum()
    # max = band.GetMaximum()
    # if not min or not max:
    #     (min, max) = band.ComputeRasterMinMax(True)
    # print("Min={:.3f}, Max={:.3f}".format(min, max))
    #
    # if band.GetOverviewCount() > 0:
    #     print("Band has {} overviews".format(band.GetOverviewCount()))
    #
    # if band.GetRasterColorTable():
    #     print("Band has a color table with {} entries".format(band.GetRasterColorTable().GetCount()))
    #
    # scanline = band.ReadRaster(xoff=0, yoff=0,
    #                            xsize=band.XSize, ysize=1,
    #                            buf_xsize=band.XSize, buf_ysize=1,
    #                            buf_type=gdal.GDT_Float32)
    #
    # import struct
    # tuple_of_floats = struct.unpack('f' * b2.XSize, scanline)
    # scanline = band.ReadAsArray()
    # print(scanline[0][0])

