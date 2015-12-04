#!/usr/bin/env python
import argparse
import shutil
import operator

import icqsol_utils
from icqsol.shapes.icqShapeManager import ShapeManager

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', help='Shape dataset selected from history')
parser.add_argument('--input_file_format_and_type', dest='input_file_format_and_type', help='Input file format and type')
parser.add_argument('--input_dataset_type', dest='input_dataset_type', help='Input dataset_type')
parser.add_argument('--scale_x', dest='scale_x', type=float, default=1.0, help='X scaling factor')
parser.add_argument('--scale_y', dest='scale_y', type=float, default=1.0, help='Y scaling factor')
parser.add_argument('--scale_z', dest='scale_z', type=float, default=1.0, help='Z scaling factor')
parser.add_argument('--output', dest='output', help='Output file name')
parser.add_argument('--output_vtk_type', dest='output_vtk_type', default='ascii', help='Output VTK type')

args = parser.parse_args()

# Get the format of the input - either vtk or ply.
input_format, input_file_type = icqsol_utils.get_format_and_type(args.input_file_format_and_type)
tmp_dir = icqsol_utils.get_temp_dir()

# Instantiate a ShapeManager for loading the input.
if input_format == 'vtk':
    shape_mgr = ShapeManager(file_format=input_format, vtk_dataset_type=args.input_dataset_type)
else:
    shape_mgr = ShapeManager(file_format=input_format)

# Get the vtk polydata from the input dataset.
vtk_poly_data = shape_mgr.loadAsVtkPolyData(args.input)

# Scale (in place operation).
factors = (args.scale_x, args.scale_y, args.scale_z)
if reduce(operator.and_, [f > 0 for f in factors]):
    # All factors must be > 0 
    shape_mgr.scaleVtkPolyData(vtk_poly_data, factors=factors)

# Save the output.
output_format, output_file_type = icqsol_utils.get_format_and_type(args.output_vtk_type)
tmp_dir = icqsol_utils.get_temp_dir()
tmp_output_path = icqsol_utils.get_temporary_file_path(tmp_dir, 'vtk')
shape_mgr.saveVtkPolyData(vtk_poly_data, file_name=tmp_output_path, file_type=output_file_type)
shutil.move(tmp_output_path, args.output)
