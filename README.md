# galaxy-csg

Galaxy tools for Constructive Solid Geometry
============================================

This repository contains tools and a CSG Viewer visualization plug-in that can be used within Galaxy for creating, assembling and to a limited extent, solving equations on 3-dimensional shapes. These tools are written in Python and based upon the following packages.

 * [Python version 2.7.x](https://www.python.org)
 * [Numpy version 1.9](http://www.numpy.org)
 * [VTK version 6.3.0](http://www.vtk.org)
 * [icqsol version 1.0](https://github.com/pletzer/icqsol)

All of these tools should soon be available in the [Galaxy Tool Shed](https://toolshed.g2.bx.psu.edu/), at which time they can be automatically installed into Galaxy.

Wrapping tools for use in Galaxy is easy!  If you want to start, see the [Galaxy wiki](https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial).

Tool Highlights
---------------
 * [Create 3D shape](./tools/icqsol_create_shape/icqsol_create_shape.xml) - Creates a selected primitive shape where shapes are Box, Cone, Cylinder and Sphere.
 * [Compose 3D shapes](./tools/icqsol_compose_shapes/icqsol_compose_shapes.xml) - Creates a shape composed of any number of selected shapes where the composition is based on a mathematical expression consisting of +, - and * operations.  The + results in a union of shapes, the - operator removes a shape and the * operator results in an intersection of shapes.
 * [Refine shape](./tools/icqsol_refine_shape/icqsol_refine_shape.xml) - Refines the discrete, triangulated surface representation of a shape using a maximum edge length criterion, breaking triangles into smaller ones where necessary.
  * [Coarsen shape](./tools/icqsol_coarsen_shape/icqsol_coarsen_shape.xml) - Coarsens the discrete, triangulated surface representation of a shape using a minimum cell area criterion, merging triangles into larger ones where necessary.
  * [Add texture](./tools/icqsol_add_texture/icqsol_add_texture.xml) - Adds a texture to a shape by projecting an image onto the surface of the shape.
 * [Add surface field](./tools/icqsol_add_surface_field_from_expression/icqsol_add_surface_field_from_expression.xml) - Adds a surface field to a selected shape based on a given mathematical expression consisting of variables x, y, z (shape point coordinates) and t (time).
 * [Color surface field](./tools/icqsol_color_surface_field/icqsol_color_surface_field.xml) - Colors a shape's surface field using a selected color map.

Other repositories with high quality tools
------------------------------------------

 * [IUC repo](https://github.com/galaxyproject/tools-iuc)
 * [Bjoern Gruening's repo](https://github.com/bgruening/galaxytools)
 * [DevTeam repo](https://github.com/galaxyproject/tools-devteam)
 * [Peter Cock's blast repo](https://github.com/peterjc/galaxy_blast)
 * [Peter Cock's pico_galaxy repo](https://github.com/peterjc/pico_galaxy)
 * [ENCODE tools repo](https://github.com/modENCODE-DCC/Galaxy)
 * [Biopython repo](https://github.com/biopython/galaxy_packages)
 * [Galaxy Proteomics repo](https://github.com/galaxyproteomics/tools-galaxyp)
 * [Colibread Galaxy Tools repo](https://github.com/genouest/tools-colibread)
