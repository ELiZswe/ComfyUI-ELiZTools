import trimesh
import xatlas
from xatlas import PackOptions, ChartOptions

def mesh_uv_wrap(mesh):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump(concatenate=True)

    atlas = xatlas.atlas()
    atlas.parametrize(mesh.vertices, mesh.faces)

    packOptions = PackOptions()
    packOptions.maxChartSize = 4096
    packOptions.padding = 1
    packOptions.resolution = 4096
    packOptions.blockAlign = True
    packOptions.bruteForce = True

    chartOptions = ChartOptions()
    #chartOptions.maxChartArea = 0.0
    #chartOptions.maxBoundaryLength = 0.0
    #chartOptions.normalDeviationWeight = 2.0
    #chartOptions.roundnessWeight = 0.01
    #chartOptions.straightnessWeight = 6.0
    #chartOptions.normalSeamWeight = 4.0
    #chartOptions.textureSeamWeight = 0.5
    #chartOptions.maxCost = 2.0
    chartOptions.maxIterations = 2  #org = 
    #chartOptions.useInputMeshUvs =  False
    #chartOptions.fixWinding = False

    atlas.Generate(atlas, chartOptions, packOptions);
    vmapping, indices, uvs = atlas[0]

    mesh.vertices = mesh.vertices[vmapping]
    mesh.faces = indices
    mesh.visual.uv = uvs

    return mesh