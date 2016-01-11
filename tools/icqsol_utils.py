import os
import sys
import tempfile

from icqsol.shapes.icqShapeManager import ShapeManager
from icqsol.bem.icqLaplaceMatrices import LaplaceMatrices

PLY = 'ply'
POLYDATA = 'POLYDATA'
VTK = 'vtk'


def asbool(val):
    return str(val).lower() in ['yes', 'true']


def get_format_and_type(galaxy_ext):
    # Define the output file format and type.
    format = None
    datatype = None
    if galaxy_ext in ['vtkascii', 'vtkbinary']:
        format = VTK
    elif galaxy_ext in ['plyascii', 'plybinary']:
        format = PLY
    if galaxy_ext in ['vtkascii', 'plyascii']:
        datatype = 'ascii'
    elif galaxy_ext in ['vtkbinary', 'plybinary']:
        datatype = 'binary'
    return format, datatype


def get_input_file_path(tmp_dir, input_file, format):
    """
    iCqSol uses file extensions (e.g., .ply, .vtk) when reading and
    writing files, so the Galaxy dataset naming convention of
    setting all file extensions as .dat must be handled.
    """
    file_path = get_temporary_file_path(tmp_dir, format)
    # Remove the file so we can create a symlink.
    os.remove(file_path)
    os.symlink(input_file, file_path)
    return file_path


def get_laplace_solver(shape_data, max_edge_length=float('inf')):
    return LaplaceMatrices(shape_data, max_edge_length=max_edge_length)


def get_shape_manager(format, dataset_type):
    # Instantiate a ShapeManager.
    if format == VTK:
        return ShapeManager(file_format=format, vtk_dataset_type=dataset_type)
    else:
        return ShapeManager(file_format=format)


def get_temp_dir(prefix='tmp-vtk-', dir=None):
    """
    Return a temporary directory.
    """
    return tempfile.mkdtemp(prefix=prefix, dir=dir)


def get_tempfilename(dir=None, suffix=None):
    """
    Return a temporary file name.
    """
    if suffix is None:
        s = None
    elif suffix.startswith('.'):
        s = suffix
    else:
        s = '.%s' % suffix
    fd, name = tempfile.mkstemp(suffix=s, dir=dir)
    os.close(fd)
    return name


def get_temporary_file_path(tmp_dir, file_extension):
    """
    Return the path to a temporary file with a valid VTK format
    file extension.
    """
    return get_tempfilename(tmp_dir, file_extension)


def stop_err(msg):
    sys.stderr.write("%s\n" % msg)
    sys.exit()
