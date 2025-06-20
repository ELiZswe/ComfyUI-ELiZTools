import trimesh
import xatlas
import torch
import copy
from PIL import Image
import numpy as np

from xatlas import PackOptions, ChartOptions

def mesh_uv_wrap(mesh, maxIterations):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump(concatenate=True)

    #vmapping, indices, uvs = xatlas.parametrize(mesh.vertices, mesh.faces)

    myAtlas = xatlas.Atlas()
    myAtlas.add_mesh(mesh.vertices, mesh.faces)
    
    #These Can be used
    #    .def_readwrite("max_chart_size", &xatlas::PackOptions::maxChartSize, "Charts larger than this will be scaled down. 0 means no limit.")
    #    .def_readwrite("padding", &xatlas::PackOptions::padding, "Number of pixels to pad charts with.")
    #    .def_readwrite("texels_per_unit", &xatlas::PackOptions::texelsPerUnit, R"doc(Unit to texel scale. e.g. a 1x1 quad with texelsPerUnit of 32 will take up approximately 32x32 texels in the atlas.
    #If 0, an estimated value will be calculated to approximately match the given resolution.
    #If resolution is also 0, the estimated value will approximately match a 1024x1024 atlas.
	#    )doc")
    #    .def_readwrite("resolution", &xatlas::PackOptions::resolution, R"doc(If 0, generate a single atlas with texelsPerUnit determining the final resolution. 
    #If not 0, and texelsPerUnit is not 0, generate one or more atlases with that exact resolution. 
    #If not 0, and texelsPerUnit is 0, texelsPerUnit is estimated to approximately match the resolution.)doc")
    #    .def_readwrite("bilinear", &xatlas::PackOptions::bilinear, "Leave space around charts for texels that would be sampled by bilinear filtering.")
    #    .def_readwrite("blockAlign", &xatlas::PackOptions::blockAlign, "Align charts to 4x4 blocks. Also improves packing speed, since there are fewer possible chart locations to consider.")
    #    .def_readwrite("bruteForce", &xatlas::PackOptions::bruteForce, "Slower, but gives the best result. If false, use random chart placement.")
    #    .def_readwrite("create_image", &xatlas::PackOptions::createImage, "Create Atlas::image.")
    #    .def_readwrite("rotate_charts_to_axis", &xatlas::PackOptions::rotateChartsToAxis, "Rotate charts to the axis of their convex hull.")
    #    .def_readwrite("rotate_charts", &xatlas::PackOptions::rotateCharts, "Rotate charts to improve packing.");



    pack_options = xatlas.PackOptions()
    pack_options.create_image = True
    #pack_options.maxChartSize = 4096
    #pack_options.padding = 1
    pack_options.resolution = 4096
    #pack_options.blockAlign = True
    #pack_options.bruteForce = True



    chart_options = xatlas.ChartOptions()

        #These can be used
        #.def_readwrite("max_chart_area", &xatlas::ChartOptions::maxChartArea)
        #.def_readwrite("max_boundary_length", &xatlas::ChartOptions::maxBoundaryLength)
        #.def_readwrite("normal_deviation_weight", &xatlas::ChartOptions::normalDeviationWeight)
        #.def_readwrite("roundness_weight", &xatlas::ChartOptions::roundnessWeight)
        #.def_readwrite("straightness_weight", &xatlas::ChartOptions::straightnessWeight)
        #.def_readwrite("normal_seam_weight", &xatlas::ChartOptions::normalSeamWeight)
        #.def_readwrite("texture_seam_weight", &xatlas::ChartOptions::textureSeamWeight)
        #.def_readwrite("max_cost", &xatlas::ChartOptions::maxCost)
        #.def_readwrite("max_iterations", &xatlas::ChartOptions::maxIterations)
        #.def_readwrite("use_input_mesh_uvs", &xatlas::ChartOptions::useInputMeshUvs)
        #.def_readwrite("fix_winding", &xatlas::ChartOptions::fixWinding);


    #chart_options.maxChartArea = 0.0
    #chart_options.maxBoundaryLength = 0.0
    #chart_options.normalDeviationWeight = 2.0
    #chart_options.roundnessWeight = 0.01
    #chart_options.straightnessWeight = 6.0
    #chart_options.normalSeamWeight = 4.0
    #chart_options.textureSeamWeight = 0.5
    #chart_options.maxCost = 2.0

    chart_options.max_iterations = maxIterations  #org = 1
    
    
    #chart_options.useInputMeshUvs =  False
    #chart_options.fixWinding = False
    
    myAtlas.generate(pack_options=pack_options, chart_options = chart_options)

    
    myWidth = myAtlas.width       # Width of the atlas 
    myHeight = myAtlas.height      # Height of the atlas
    print ("maxIterations: " + str(maxIterations))
    print ("Width: " + str(myWidth))
    print ("Height: " + str(myHeight))
    myImage = myAtlas.get_chart_image(0)        # Debug image of the first atlas
    UVImages = Image.fromarray(np.uint8(myImage)).convert('RGB')
    
    #UVImages.append(Image.new('RGB',(1024,1024),"rgb(255,0,255)"))

    vmapping, indices, uvs = myAtlas[0]

    mesh.vertices = mesh.vertices[vmapping]
    mesh.faces = indices
    mesh.visual.uv = uvs
       
    return mesh, UVImages