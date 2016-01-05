#!/usr/bin/env python
import argparse
import shutil

import icqsol_utils
from icqsol.shapes.icqShapeManager import ShapeManager
from icqsol.bem.icqLaplaceMatrices import LaplaceMatrices

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', help='Shape dataset selected from history')
parser.add_argument('--input_file_format_and_type', dest='input_file_format_and_type', help='Input file format and type')
parser.add_argument('--input_dataset_type', dest='input_dataset_type', help='Input dataset_type')
parser.add_argument('--input_potential_name', dest='input_potential_field_name', default='', help='Input surface potential field name.')
parser.add_argument('--output_jump_electric_field_name', dest='output_jump_electric_field_name', default='jump_normal_electric_field', help='Set the name of the output field name.')
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

# Define the Laplace equation problem.
solver = LaplaceMatrices(vtk_poly_data, max_edge_length=float('inf'))

# Set the output field names.
solver.setNormalElectricFieldJumpName(args.output_jump_electric_field_name)

# In place operation, vtk_poly_data will be modified.
normalEJump = solver.computeNormalElectricFieldJump(potName=args.input_potential_name)

# Define the output file format and type (the output_format can only be 'vtk').
output_format, output_file_type = icqsol_utils.get_format_and_type(args.output_vtk_type)
tmp_output_path = icqsol_utils.get_temporary_file_path(tmp_dir, output_format)

# Make sure the ShapeManager's writer is vtk.
shape_mgr.setWriter(file_format=icqsol_utils.VTK, vtk_dataset_type=icqsol_utils.POLYDATA)

# Save the output.
shape_mgr.saveVtkPolyData(vtk_poly_data=solver.getVtkPolyData(), file_name=tmp_output_path, file_type=output_file_type)
shutil.move(tmp_output_path, args.output)
