#!/usr/bin/env python
import argparse
import shutil
from pkg_resources import resource_filename

import icqsol_utils
from icqsol.shapes.icqShapeManager import ShapeManager

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', help='Shape dataset selected from history')
parser.add_argument('--input_file_format_and_type', dest='input_file_format_and_type', help='Input file format and type')
parser.add_argument('--input_dataset_type', dest='input_dataset_type', help='Input dataset_type')
parser.add_argument('--max_edge_length', dest='max_edge_length', type=float, default='0', help='Maximum edge length')
parser.add_argument('--texture', dest='texture', default='stone', help='Select texture (stone, wood, or checkerboard')
parser.add_argument('--output', dest='output', help='Output dataset')
parser.add_argument('--output_vtk_type', dest='output_vtk_type', help='Output VTK type')

args = parser.parse_args()

input_format, input_file_type = icqsol_utils.get_format_and_type(args.input_file_format_and_type)
tmp_dir = icqsol_utils.get_temp_dir()

# Instantiate a ShapeManager for loading the input.
if input_format == icqsol_utils.VTK:
    shape_mgr = ShapeManager(file_format=input_format, vtk_dataset_type=args.input_dataset_type)
else:
    shape_mgr = ShapeManager(file_format=input_format)

# Get the vtk polydata from the input dataset.
vtk_poly_data = shape_mgr.loadAsVtkPolyData(args.input)

# Add texture.
texture_name_to_filename = {
    'stone': resource_file('icqsol', 'textures/220px-COnglomerate-sandstone_layers_Nerriga.jpg'),
    'wood': resource_file('icqsol', 'textures/Swietenia_macrophylla_wood.jpg'),
    'checkerboard': resource_file('icqsol', 'textures/checkerboard.png'),
}
texture_file = texture_name_to_filename.get(args.texture, 'stone')
vtk_poly_data = shape_mgr.addTextureToVtkPolyData(vtk_poly_data, texture=texture_file, max_edge_length=args.max_edge_length)

# Define the output file format and type (the output_format can only be 'vtk').
output_format, output_file_type = icqsol_utils.get_format_and_type(args.output_vtk_type)
tmp_output_path = icqsol_utils.get_temporary_file_path(tmp_dir, output_format)

# Make sure the ShapeManager's writer is vtk.
shape_mgr.setWriter(file_format=icqsol_utils.VTK, vtk_dataset_type=icqsol_utils.POLYDATA)

# Save the output.
shape_mgr.saveVtkPolyData(vtk_poly_data=vtk_poly_data, file_name=tmp_output_path, file_type=output_file_type)
shutil.move(tmp_output_path, args.output)
