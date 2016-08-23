# galaxy-csg

Galaxy tools for Constructive Solid Geometry
============================================

This repository contains tools that can be used within Galaxy for creating, assembling and solving equations on 3-dimensional shapes.
Galaxy includes a CSG Viewer [Visualization plug-in](https://wiki.galaxyproject.org/Develop/Visualizations) for viewing the shapes
produced by these tools.  Here is the [CSG Viewer plug-in](https://github.com/galaxyproject/galaxy/tree/dev/config/plugins/visualizations/csg).

These tools are written in Python and based upon the following packages.

 * [Python version 2.7.x](https://www.python.org)
 * [VTK version 6.3.0](http://www.vtk.org)
 * [icqsol version 0.3.26](https://github.com/pletzer/icqsol)

All of these tools are available in the [Galaxy Tool Shed](https://toolshed.g2.bx.psu.edu/), so they can be automatically installed into Galaxy.

Wrapping tools for use in Galaxy is easy!  If you want to start, see the [Galaxy wiki](https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial).

Tool Highlights
---------------
 * [Create 3D shape](./tools/icqsol_create_shape/icqsol_create_shape.xml) - Creates a selected primitive shape where shapes are Box, Cone, Cylinder and Sphere.
 * [Compose 3D shapes](./tools/icqsol_compose_shapes/icqsol_compose_shapes.xml) - Creates a shape composed of any number of selected shapes where the composition is based on a mathematical expression consisting of +, - and * operations.  The + results in a union of shapes, the - operator removes a shape and the * operator results in an intersection of shapes.
 * [Scale shape](./tools/icqsol_scale_shape/icqsol_scale_shape.xml) - Magnifies the dimensions of a shape along some specified axes.
 * [Translate shape](./tools/icqsol_translate_shape/icqsol_translate_shape.xml) - Applies translation operations to a shape by adding a displacement to each coordinate.
 * [Rotate shape](./tools/icqsol_rotate_shape/icqsol_rotate_shape.xml) - Applies a rotation to a shape by a given angle about an arbitrary axis.
 * [Refine shape](./tools/icqsol_refine_shape/icqsol_refine_shape.xml) - Refines the discrete, triangulated surface representation of a shape using a maximum edge length criterion, breaking triangles into smaller ones where necessary.
 * [Coarsen shape](./tools/icqsol_coarsen_shape/icqsol_coarsen_shape.xml) - Coarsens the discrete, triangulated surface representation of a shape using a minimum cell area criterion, merging triangles into larger ones where necessary.
 * [Add texture](./tools/icqsol_add_texture/icqsol_add_texture.xml) - Adds a texture to a shape by projecting an image onto the surface of the shape.
 * [Add surface field](./tools/icqsol_add_surface_field_from_expression/icqsol_add_surface_field_from_expression.xml) - Adds a surface field to a selected shape based on a given mathematical expression consisting of variables x, y, z (shape point coordinates) and t (time).
 * [Color surface field](./tools/icqsol_color_surface_field/icqsol_color_surface_field.xml) - Colors a shape's surface field using a selected color map.
 * [Solve Laplace equation](./tools/icqsol_solve_laplace/icqsol_solve_laplace.xml) - Solve the Laplace equation given prescribed Dirichlet boundary conditions applied as a surface field.  The resulting field corresponds to the electric field in an electrostatic problem.

Creating shapes
---------------
This is the Create 3D shape tool.  It allows you to create 4 primitive shapes, boxes, cones, cylinders and spheres.  Here we're creating a cylinder.
![Create 3D shape](images/create_cylinder.png?raw=true)

We can view and manipulate the cylinder using the Galaxy CSG Viewer plug-in.
![CSG Viewer plug-in](images/csg_viewer.png?raw=true)

The plug-in renders the 3D image in Galaxy.
![View shape](images/cylinder.png?raw=true)

We can create a cone...
![Create 3D shape](images/create_cone.png?raw=true)
...and a box.
![Create 3D shape](images/create_box.png?raw=true)

The Create 3D shape tool allows you to create a shape by cloning another shape.  Options include rotating or translating the cloned shape.  Here we clone the box we just created, rotating it 90 degrees around the X axis.
![Create 3D shape](images/clone_box.png?raw=true)

Composing shapes
----------------
This is the Compose shapes tool.  This tool creates a shape composed of any number of selected shapes where the composition is based on a mathematical expression consisting of +, - and * operations.  The + operator results in a union of shapes, the - operator removes a shape and the * operator results in an intersection of shapes.
Here we are composing the four primitive shapes we just created, adding the cone to the cylinder and subtracting both boxes.
![Compose 3D shapes](images/compose_shapes.png?raw=true)

Our composed shapes produce a bolt.
![Composed 3D shapes](images/bolt.png?raw=true)

Texture
-------
This is the Add texture to shape tool.  It allows you to select an image dataset from your history and project it onto the shape's surface.
![Add texture](images/add_texture.png?raw=true)

Here is our shiny bolt.
![Shiny bolt](images/shiny_bolt.png?raw=true)

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
