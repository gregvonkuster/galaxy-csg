#!/usr/bin/env python
import argparse
import shutil

from icqsol.shapes.icqShapeManager import ShapeManager
from icqsol import util
import icqsol_utils

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input',
                    help='Shape dataset selected from history')
parser.add_argument('--displacement_x', dest='displacement_x', type=float,
                    default=1.0, help='X coordinate of displacement')
parser.add_argument('--displacement_y', dest='displacement_y', type=float,
                    default=0.0, help='Y coordinate of displacement')
parser.add_argument('--displacement_z', dest='displacement_z', type=float,
                    default=0.0, help='Z coordinate of displacement')
parser.add_argument('--output', dest='output', help='Output file name')
parser.add_argument('--output_vtk_type', dest='output_vtk_type',
                    default='ascii',
                    help='Output VTK type')

args = parser.parse_args()

# Get the format of the input - either vtk or ply.
input_format = util.getFileFormat(args.input)

tmp_dir = icqsol_utils.get_temp_dir()

# Get the format of the input - either vtk or ply.
file_format = util.getFileFormat(args.input)

# Instantiate a ShapeManager for loading the input.
if file_format == util.VTK_FORMAT:
    # We have a VTK file, so get the dataset type.
    vtk_dataset_type = util.getVtkDatasetType(args.input)
    shape_mgr = ShapeManager(file_format=file_format,
                             vtk_dataset_type=vtk_dataset_type)
else:
    shape_mgr = ShapeManager(file_format=file_format)

# Get the vtk polydata from the input dataset.
vtk_poly_data = shape_mgr.loadAsVtkPolyData(args.input)

displ = (args.displacement_x,
         args.displacement_y,
         args.displacement_z)

# Translate (in place operation).
shape_mgr.translateVtkPolyData(vtk_poly_data,
                               displ=displ)

if args.output_vtk_type.lower() == 'binary':
    file_type = util.BINARY
else:
    file_type = util.ASCII

tmp_dir = icqsol_utils.get_temp_dir()
tmp_output_path = icqsol_utils.get_temporary_file_path(tmp_dir, 'vtk')

shape_mgr.saveVtkPolyData(vtk_poly_data, file_name=tmp_output_path,
                          file_type=file_type)

shutil.move(tmp_output_path, args.output)
