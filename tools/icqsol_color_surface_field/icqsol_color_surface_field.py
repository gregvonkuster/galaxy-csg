#!/usr/bin/env python
import argparse
import shutil

import icqsol_utils

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', help='Shape dataset selected from history')
parser.add_argument('--input_file_format_and_type', dest='input_file_format_and_type', help='Input file format and type')
parser.add_argument('--input_dataset_type', dest='input_dataset_type', help='Input dataset_type')
parser.add_argument('--field_name', dest='field_name', help='Field name')
parser.add_argument('--field_component_index', dest='field_component_index', type=int, help='Index of field component')
parser.add_argument('--color_map', dest='color_map', help='Color map')
parser.add_argument('--output', dest='output', help='Output dataset')
parser.add_argument('--output_vtk_type', dest='output_vtk_type', help='Output VTK type')

args = parser.parse_args()

tmp_dir = icqsol_utils.get_temp_dir()
input_format, input_file_type = icqsol_utils.get_format_and_type(args.input_file_format_and_type)

# Instantiate a ShapeManager for loading the input.
shape_mgr = icqsol_utils.get_shape_manager(icqsol_utils.VTK, args.input_dataset_type)

# Get the vtkPolyData from the input dataset.
vtk_poly_data = shape_mgr.loadAsVtkPolyData(args.input)
# Add color to the data.
colored_vtk_poly_data = shape_mgr.colorSurfaceField(vtk_poly_data=vtk_poly_data,
                                                    color_map=args.color_map,
                                                    field_name=args.field_name,
                                                    field_component=args.field_component_index)

# Write min/max field values.
minVal, maxVal = shape_mgr.getFieldRange(vtk_poly_data, args.field_name, args.field_component_index)
print 'component {2} min/max values of field {3}: {0}/{1}'.format(minVal, maxVal, args.field_component_index, args.field_name)

# Define the output file format and type.
output_format, output_file_type = icqsol_utils.get_format_and_type(args.output_vtk_type)
tmp_output_path = icqsol_utils.get_temporary_file_path(tmp_dir, output_format)

# Make sure the ShapeManager's writer is VTK POLYDATA.
shape_mgr.setWriter(file_format=icqsol_utils.VTK, vtk_dataset_type=icqsol_utils.POLYDATA)

# Save the output.
shape_mgr.saveVtkPolyData(vtk_poly_data=colored_vtk_poly_data, file_name=tmp_output_path, file_type=output_file_type)
shutil.move(tmp_output_path, args.output)
