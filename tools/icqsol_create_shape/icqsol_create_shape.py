#!/usr/bin/env python
import argparse
import shutil

import icqsol_utils
from icqsol.shapes.icqShapeManager import ShapeManager

# Parse Command Line.
parser = argparse.ArgumentParser()
parser.add_argument('--create_process', dest='create_process', help='Shape creation process (create or clone)')
parser.add_argument('--shape_input', dest='shape_input', default=None, help='Shape file if create_process is clone')
parser.add_argument('--shape', dest='shape', default=None, help='Shape if create_process is create')
parser.add_argument('--origin_x', dest='origin_x', type=float, default=None, help='X coordinate of origin')
parser.add_argument('--origin_y', dest='origin_y', type=float, default=None, help='Y coordinate of origin')
parser.add_argument('--origin_z', dest='origin_z', type=float, default=None, help='Z coordinate of origin')
parser.add_argument('--length_x', dest='length_x', type=float, default=None, help='X coordinate of end')
parser.add_argument('--length_y', dest='length_y', type=float, default=None, help='Y coordinate of end')
parser.add_argument('--length_z', dest='length_z', type=float, default=None, help='Z coordinate of end')
parser.add_argument('--angle', dest='angle', type=float, default=None, help='Angle')
parser.add_argument('--radius', dest='radius', type=float, default=None, help='Radius')
parser.add_argument('--n_theta', dest='n_theta', type=int, default=0, help='Number of slices')
parser.add_argument('--n_phi', dest='n_phi', type=int, default=0, help='Number of stacks')
parser.add_argument('--rotate', dest='rotate', help='Rotate cloned shape')
parser.add_argument('--rotation_axis_x', dest='rotation_axis_x', type=float, default=None, help='X component of rotation axis')
parser.add_argument('--rotation_axis_y', dest='rotation_axis_y', type=float, default=None, help='Y component of rotation axis')
parser.add_argument('--rotation_axis_z', dest='rotation_axis_z', type=float, default=None, help='Z component of rotation axis')
parser.add_argument('--rotation_degree', dest='rotation_degree', type=float, default=None, help='Degree of rotation around axis')
parser.add_argument('--translate', dest='translate', help='Translate cloned shape')
parser.add_argument('--output', dest='output', default=None, help='Output dataset')
parser.add_argument('--output_vtk_type', dest='output_vtk_type', help='Output file format and type')

args = parser.parse_args()

if args.origin_x is not None and args.origin_y is not None and args.origin_z is not None:
    origin = [args.origin_x, args.origin_y, args.origin_z]
if args.length_x is not None and args.length_y is not None and args.length_z is not None:
    lengths = [args.length_x, args.length_y, args.length_z]
if args.rotation_axis_x is not None and args.rotation_axis_y is not None and args.rotation_axis_z is not None:
    rotation_axis = [args.rotation_axis_x, args.rotation_axis_y, args.rotation_axis_z]

# Define the output file format and type.
format, file_type = icqsol_utils.get_format_and_type(args.output_vtk_type)
tmp_dir = icqsol_utils.get_temp_dir()
cloning = True if args.create_process == 'clone' else False

# TODO: fix this to handle inputPLY files for cloning, but producing VTK POLYDATA.
shape_mgr = ShapeManager(file_format=format, vtk_dataset_type=icqsol_utils.POLYDATA)

if cloning:
    # We're cloning an existing shape selected from the history.
    tmp_input_path = icqsol_utils.get_input_file_path(tmp_dir, args.shape_input, '.%s' % format)
    shape_to_clone = shape_mgr.loadAsShape(tmp_input_path)
    new_shape = shape_mgr.cloneShape(shape_to_clone)
    if icqsol_utils.asbool(args.rotate):
        shape_mgr.rotateShape(new_shape, axis=rotation_axis, angleDeg=args.rotation_degree)
    if icqsol_utils.asbool(args.translate):
        shape_mgr.translateShape(new_shape, disp=origin)
else:
    # Create the primitive shape.
    if args.shape == 'box':
        new_shape = shape_mgr.createShape('box',
                                          origin=origin,
                                          lengths=lengths)
    elif args.shape == 'cone':
        new_shape = shape_mgr.createShape('cone',
                                          radius=args.radius,
                                          origin=origin,
                                          lengths=lengths,
                                          n_theta=args.n_theta)
    elif args.shape == 'cylinder':
        new_shape = shape_mgr.createShape('cylinder',
                                          radius=args.radius,
                                          origin=origin,
                                          lengths=lengths,
                                          n_theta=args.n_theta)
    elif args.shape == 'sphere':
        new_shape = shape_mgr.createShape('sphere',
                                          radius=args.radius,
                                          origin=origin,
                                          n_theta=args.n_theta,
                                          n_phi=args.n_phi)

# Save the output.
tmp_output_path = icqsol_utils.get_temporary_file_path(tmp_dir, '.%s' % format)
shape_mgr.saveShape(shape=new_shape, file_name=tmp_output_path, file_type=file_type)
shutil.move(tmp_output_path, args.output)
