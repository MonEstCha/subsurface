from typing import Union, List

from osgeo import gdal
import pandas as pd
import numpy as np
try:
    import anuga_core.anuga.abstract_2d_finite_volumes.ermapper_grids
    ermapper_grids_imported = True
except ImportError:
    ermapper_grids_imported = False


def read_in_geophysical_data(path_to_file1: str, path_to_file2: str):
    header = gdal.Open(path_to_file1, gdal.GA_ReadOnly)
    dataset = []
    with open(path_to_file1, "rb") as f:
        byte = f.read(1)
        while byte != b"":
            # Do stuff with byte.
            byte = f.read(1)
            dataset.append(byte)
    # data = ermapper_grids(ifile1)
    return header, dataset


def read_in_dat_files(path_to_file: str, columns_map: Union[dict, List[str]] = None):
    if columns_map:
        f = open(path_to_file, encoding='utf-8')
        data = []
        for line in f.readlines():
            if columns_map[0] in line:
                pass
            else:
                s = line.strip("\n").split()
                data.append(s)
        f.close()
        df = pd.DataFrame(data, columns=columns_map)
        print(df)
    # print(type(columns_map))
    # if type(columns_map) == List[str]:

    # data = np.genfromtxt(path_to_file, delimiter='\t', usecols=columns_map)
    # print(data)
    # if columns_map is not None:
    #     data.columns = data.columns.map(columns_map)
    #     assert data.columns.isin(['x', 'y', 'z']).any(), 'At least x, y, z must be passed to `columns_map`'
    # with open(path_to_file, 'r') as d:
    #     lines = [ln.strip() for ln in d.readlines()]
    #     return lines
