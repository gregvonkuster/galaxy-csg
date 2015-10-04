#!/usr/bin/env python
import argparse
import shutil

import icqsol_utils
from icqsol.shapes.icqShapeManager import ShapeManager

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument( '--expression', dest='expression', help='Composition expression' )
parser.add_argument( '--shape_dataset', dest='shape_datasets', action='append', nargs=4, help='Shape datasets selected from history' )
parser.add_argument( '--output', dest='output', help='Output dataset' )
parser.add_argument( '--output_vtk_type', dest='output_vtk_type', help='Output file format and type' )

args = parser.parse_args()

tmp_dir = icqsol_utils.get_temp_dir()
shape_tuples = []
shape_mgr = ShapeManager()

# Load the shapes.
for ( expression_var, dataset_path, galaxy_ext, vtk_dataset_type ) in args.shape_datasets:
    # Define the file format and type.
    format, file_type = icqsol_utils.get_format_and_type( galaxy_ext )
    if format == 'vtk':
        shape_mgr.setReader( file_format=format, vtk_dataset_type=vtk_dataset_type )
    else:
        shape_mgr.setReader( file_format=format )
    icqsol_path = icqsol_utils.get_input_file_path( tmp_dir, dataset_path, format )
    shape_tuple = ( expression_var, shape_mgr.loadAsShape( icqsol_path ) )
    shape_tuples.append( shape_tuple )

# Define the output file format and type.
output_format, output_file_type = icqsol_utils.get_format_and_type( args.output_vtk_type )
tmp_output_path = icqsol_utils.get_temporary_file_path( tmp_dir, output_format )

shape_mgr.setWriter( file_format=output_format, vtk_dataset_type=icqsol_utils.POLYDATA )

# Compose the shapes.
composite_shape = shape_mgr.composeShapes( shape_tuples, args.expression )

# Save the output.
shape_mgr.saveShape( shape=composite_shape, file_name=tmp_output_path, file_type=output_file_type )
shutil.move( tmp_output_path, args.output )
