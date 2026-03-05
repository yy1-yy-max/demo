# td-3d-to-pointcloud

A TouchDesigner component template and supporting scripts to convert 3D geometry (SOP) into a point cloud with instancing and export support. Built for TouchDesigner 2023.12120.

Features
- Convert mesh or scattered points into GPU-instanced point clouds
- Supports extracting position, color (Cd), normals, scale
- Option to render with sprite shader or instanced low-res geometry
- Includes a Text DAT Python exporter to write ASCII PLY

Usage
1. Follow the build instructions in build_instructions.md to assemble the component in TouchDesigner.
2. Optionally copy `example_shader.glsl` into a GLSL MAT or use the Sprite MAT.
3. Use the `export_ply.py` script (as a Text DAT) to export the current point cloud to a PLY file.

Attribution
Author: yy1-yy-max
