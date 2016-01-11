#!/usr/bin/env python
import argparse
import shutil
import operator

import icqsol_utils

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', help='Shape dataset selected from history')
parser.add_argument('--input_file_format_and_type', dest='input_file_format_and_type', help='Input file format and type')
parser.add_argument('--input_dataset_type', dest='input_dataset_type', help='Input dataset_type')
parser.add_argument('--rotation_degrees', dest='rotation_degrees', type=float, default=0.0, help='Rotation angle in degrees')
parser.add_argument('--rotation_axis_x', dest='rotation_axis_x', type=float, default=1.0, help='X coordinate of rotation axis')
parser.add_argument('--rotation_axis_y', dest='rotation_axis_y', type=float, default=0.0, help='Y coordinate of rotation axis')
parser.add_argument('--rotation_axis_z', dest='rotation_axis_z', type=float, default=0.0, help='Z coordinate of rotation axis')
parser.add_argument('--output', dest='output', help='Output file name')
parser.add_argument('--output_vtk_type', dest='output_vtk_type', default='ascii', help='Output VTK type')

args = parser.parse_args()

# Get the format of the input - either vtk or ply.
input_format, input_file_type = icqsol_utils.get_format_and_type(args.input_file_format_and_type)
tmp_dir = icqsol_utils.get_temp_dir()

# Instantiate a ShapeManager for loading the input.
shape_mgr = icqsol_utils.get_shape_manager(input_format, args.input_dataset_type)

# Get the vtk polydata from the input dataset.
vtk_poly_data = shape_mgr.loadAsVtkPolyData(args.input)

# Only rotate if the axis has some non-zero coordinates.
# FIXME: this should be handled in a Galaxy tool validator.
axis = (args.rotation_axis_x, args.rotation_axis_y, args.rotation_axis_z)
if reduce(operator.mul, axis) != 0.0:
    # Rotate (in place operation).
    shape_mgr.rotateVtkPolyData(vtk_poly_data, angleDeg=args.rotation_degrees, axis=axis)

output_format, output_file_type = icqsol_utils.get_format_and_type(args.output_vtk_type)

# Save the output.
tmp_dir = icqsol_utils.get_temp_dir()
tmp_output_path = icqsol_utils.get_temporary_file_path(tmp_dir, icqsol_utils.VTK)
shape_mgr.saveVtkPolyData(vtk_poly_data, file_name=tmp_output_path, file_type=output_file_type)
shutil.move(tmp_output_path, args.output)
