from typing import Union, List

from osgeo import gdal
import pandas as pd
import pyvista as pv
import numpy as np

from subsurface import UnstructuredData

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


def read_in_dat_files(path_to_file: str, columns_map: Union[dict, List[str]],  attribute_cols: dict = None,
                      vertex_map: Union[dict, List[str]] = None) -> UnstructuredData:
    """
    Reads in .dat files of gravity data with n table columns and returns UnstructuredData object. Default cells will be
    generated for creating an UnstructuredData object if delaunay is not false.

    Vertices will be read from columns named East_KKJ, North_KKJ and Elev_m by default. Use vertex_map to map the required
    column names to any other names.

    Args:
        attribute_cols (dict): Dictionary with format: {'columns_name1': column_1_index, 'columns_name2':
        column_2_index, ...}
        path_to_file (str): Filepath.
        columns_map (Union[dict, List[str]]): Dictionary with format: {'columns_name1': 'line', 'columns_name2':
        'station', ...} or List with format['columns_name1', 'columns-name2', ...]
        vertex_map (: Union[dict, List[str]]): Dictionary with format: {'columns_name1': 'x', 'columns_name2':
        'y', ...} or List with format['x', 'y', ...].
    Returns:
        (UnstructuredData) csv with n columns stored in pandas.DataFrame of vertices with
        3 columns (3d vertices), cells of m columns forming an m-sided polygon and pandas.DataFrame of attributes with n-(m+3) columns.

    """

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
    if vertex_map is None:
        try:
            vertex = df[['x', 'y', 'z']].values.astype('float')
        except KeyError:
            raise KeyError('Use vertex_map to map columns other than x, y, z')
    else:
        vertex = df[vertex_map].values.astype('float')

    a = pv.PolyData(vertex)
    b = a.delaunay_2d().faces
    cells = b.reshape(-1, 4)[:, 1:]

    ud = UnstructuredData(vertex, cells)

    if attribute_cols:
        attributes = [[x[v] for k, v in attribute_cols.items()] for x in df.values]
        # print(len(attributes))
        df2 = pd.DataFrame(attributes)
        df2.columns = [k for k, v in attribute_cols.items()]
        # Check if is point or cell data
        if df2.shape[0] == vertex.shape[0]:
            kwargs_ = {'points_attributes': df2}
        elif df2.shape[0] == cells.shape[0]:
            kwargs_ = {'attributes': df2}
        else:
            raise ValueError('Attribute cols must be either of the shape of vertex or'
                             'cells.')
        ud = UnstructuredData(vertex, cells, **kwargs_)
    return ud
