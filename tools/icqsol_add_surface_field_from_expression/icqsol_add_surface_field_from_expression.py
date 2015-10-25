#!/usr/bin/env python
import argparse
import shutil

import icqsol_utils
from icqsol.shapes.icqShapeManager import ShapeManager

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument( '--input', dest='input', help='Shape dataset selected from history' )
parser.add_argument( '--input_file_format_and_type', dest='input_file_format_and_type', help='Input file format and type' )
parser.add_argument( '--input_dataset_type', dest='input_dataset_type', help='Input dataset_type' )
parser.add_argument( '--field_name', dest='field_name', help='Surface field name' )
parser.add_argument( '--location', dest='location', help='Location of field within cell, either point or cell' )
parser.add_argument( '--expression', dest='expression', help='Expression for applying surface field to shape' )
parser.add_argument( '--time_point', dest='time_points', type=float, action='append', nargs=1, help='Points in time' )
parser.add_argument( '--max_edge_length', dest='max_edge_length', type=float, default='0', help='Maximum edge length' )
parser.add_argument( '--output', dest='output', help='Output dataset' )
parser.add_argument( '--output_vtk_type', dest='output_vtk_type', help='Output VTK type' )

args = parser.parse_args()

input_format, input_file_type = icqsol_utils.get_format_and_type( args.input_file_format_and_type )
time_points = [ tp[0] for tp in args.time_points ]
tmp_dir = icqsol_utils.get_temp_dir()

# Instantiate a ShapeManager for loading the input.
if input_format == 'vtk':
    shape_mgr = ShapeManager( file_format=input_format, vtk_dataset_type=args.input_dataset_type )
else:
    shape_mgr = ShapeManager( file_format=input_format )

# Get the shape from the input dataset.
shp = shape_mgr.loadAsShape(args.input)

max_edge_length = float('inf')
if args.max_edge_length > 0:
    max_edge_length = args.max_edge_length

# Add surface field to shape data.
vtk_poly_data = shape_mgr.addSurfaceFieldFromExpressionToShape(shp,
                                                               args.field_name,
                                                               args.expression,
                                                               time_points,
                                                               max_edge_length,
                                                               args.location)

# Define the output file format and type (the outpur_format can only be 'vtk').
output_format, output_file_type = icqsol_utils.get_format_and_type( args.output_vtk_type )
tmp_output_path = icqsol_utils.get_temporary_file_path( tmp_dir, output_format )

# Make sure the ShapeManager's writer is vtk.
shape_mgr.setWriter( file_format='vtk', vtk_dataset_type=icqsol_utils.POLYDATA )

# Save the output.
shape_mgr.saveVtkPolyData( vtk_poly_data=vtk_poly_data, file_name=tmp_output_path, file_type=output_file_type)
shutil.move( tmp_output_path, args.output )
