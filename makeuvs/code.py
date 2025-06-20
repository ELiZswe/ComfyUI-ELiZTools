import trimesh
import xatlas
from PIL import Image
#import numpy as np
from xatlas import PackOptions, ChartOptions

def mesh_uv_wrap(mesh):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump(concatenate=True)

    #vmapping, indices, uvs = xatlas.parametrize(mesh.vertices, mesh.faces)

    myAtlas = xatlas.Atlas()

    myAtlas.add_mesh(mesh.vertices, mesh.faces)
    #myAtlas.generate()

    pack_options = xatlas.PackOptions()
    pack_options.create_image = True
    #pack_options.maxChartSize = 4096
    #pack_options.padding = 1
    #pack_options.resolution = 4096
    #pack_options.blockAlign = True
    #pack_options.bruteForce = True

    chart_options = xatlas.ChartOptions()
    #chart_options.maxChartArea = 0.0
    #chart_options.maxBoundaryLength = 0.0
    #chart_options.normalDeviationWeight = 2.0
    #chart_options.roundnessWeight = 0.01
    #chart_options.straightnessWeight = 6.0
    #chart_options.normalSeamWeight = 4.0
    #chart_options.textureSeamWeight = 0.5
    #chart_options.maxCost = 2.0
    #chart_options.maxIterations = 2  #org = 1
    #chart_options.useInputMeshUvs =  False
    #chart_options.fixWinding = False
    
    myAtlas.generate(pack_options=pack_options, chart_options = chart_options)

    #myImage = myAtlas.get_chart_image(0)        # Debug image of the first atlas
    UVImage = Image.new('RGB',(1024,1024),"rgb(255,0,255)")

    vmapping, indices, uvs = myAtlas[0]

    mesh.vertices = mesh.vertices[vmapping]
    mesh.faces = indices
    mesh.visual.uv = uvs
    
    return mesh, UVImage