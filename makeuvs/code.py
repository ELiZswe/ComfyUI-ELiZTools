import trimesh
import xatlas
import torch
import torchvision.transforms as transforms
import copy
from PIL import Image
import numpy as np
from xatlas import PackOptions, ChartOptions

def mesh_uv_wrap(mesh, max_chart_area, max_cost, maxIterations, resolution, blockAlign, fix_winding, rotate_charts, rotate_charts_to_axis, padding, bruteForce, max_boundary_length, normal_deviation_weight, roundness_weight, straightness_weight, normal_seam_weight, texture_seam_weight, max_chart_size, texels_per_unit, bilinear, create_image, use_input_mesh_uvs):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump(concatenate=True)

    myAtlas = xatlas.Atlas()
    myAtlas.add_mesh(mesh.vertices, mesh.faces)

    #Using the names from here:
    #https://github.com/mworchel/xatlas-python/blob/main/src/options.cpp
    pack_options = xatlas.PackOptions()
    pack_options.create_image             = create_image
    pack_options.max_chart_size           = max_chart_size
    pack_options.padding                  = padding
    pack_options.texels_per_unit          = texels_per_unit
    pack_options.resolution               = resolution
    pack_options.bilinear                 = bilinear
    pack_options.blockAlign               = blockAlign
    pack_options.rotate_charts            = rotate_charts
    pack_options.rotate_charts_to_axis    = rotate_charts_to_axis
    pack_options.bruteForce               = bruteForce

    chart_options = xatlas.ChartOptions()
    chart_options.max_chart_area          = max_chart_area
    chart_options.max_cost                = max_cost
    chart_options.max_iterations          = maxIterations
    chart_options.fix_winding             = fix_winding
    chart_options.max_boundary_length     = max_boundary_length
    chart_options.normal_deviation_weight = normal_deviation_weight
    chart_options.roundness_weight        = roundness_weight
    chart_options.straightness_weight     = straightness_weight
    chart_options.normal_seam_weight      = normal_seam_weight
    chart_options.texture_seam_weight     = texture_seam_weight
    chart_options.use_input_mesh_uvs      = use_input_mesh_uvs

    myAtlas.generate(pack_options=pack_options, chart_options = chart_options)
    
    if create_image == True:
        #Create and nparray from the Chart
        np_myimage = myAtlas.get_chart_image(0)
        UVImage = Image.fromarray(np.uint8(np_myimage))
        UVImage = UVImage.transpose(Image.FLIP_TOP_BOTTOM)
        if resolution < 1:
            #From this point on, this is only used for Image output
            resolution = 1024

        transform_pipeline = transforms.Compose([
            transforms.Resize((resolution, resolution)),
            transforms.ToTensor(),
        ])
        image_transformed = transform_pipeline(UVImage)
        image_transformed = image_transformed.permute(1, 2, 0).unsqueeze(0)
    else:
        image_transformed = None

    Utilization = myAtlas.utilization  

    #the built in code4
    vmapping, indices, uvs = myAtlas[0]
    
    mesh.vertices = mesh.vertices[vmapping]
    mesh.faces = indices
    mesh.visual.uv = uvs

    texture_data = None
    material = trimesh.visual.texture.SimpleMaterial(image=texture_data, diffuse=(255, 255, 255))
    texture_visuals = trimesh.visual.TextureVisuals(uv=mesh.visual.uv, image=texture_data, material=material)
    mesh.visual = texture_visuals


    #material = trimesh.visual.texture.SimpleMaterial(image=UVImage)
    #color_visuals = trimesh.visual.TextureVisuals(uv=uvs, image=UVImage, material=material)
    #mesh.visual = color_visuals

    return mesh, image_transformed, Utilization
    
