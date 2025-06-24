import os
#import torch
#import torch.nn.functional as F
#from pathlib import Path
#import numpy as np
#import json
from PIL import Image
import trimesh as Trimesh
   
class ELiZMeshUVWrap:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trimesh": ("TRIMESH",),
            },
            "optional": {
                "max_chart_area":          ("FLOAT", {"default": 0.0, "min": 0.0, "max": 2000.0,  "tooltip": "Chart Option: Don\'t grow charts to be larger than this. 0 means no limit."}),
                "max_boundary_length":     ("FLOAT", {"default": 0.0, "min": 0.0, "max": 2000.0,  "tooltip": "Chart Option: Don't grow charts to have a longer boundary than this. 0 means no limit."}),

                "normal_deviation_weight": ("FLOAT", {"default": 2.0, "min": 0.0, "max": 2000.0,  "tooltip": "Chart Option: Angle between face and average chart normal. Default = 2.0"}),
                "roundness_weight":        ("FLOAT", {"default": 0.01, "min": 0.0, "max": 2000.0, "tooltip": "Chart Option:  Default = 0.01"}),
                "straightness_weight":     ("FLOAT", {"default": 6.0, "min": 0.0, "max": 2000.0,  "tooltip": "Chart Option:  Default = 6.0"}),
                "normal_seam_weight":      ("FLOAT", {"default": 4.0, "min": 0.0, "max": 2000.0,  "tooltip": "Chart Option: If > 1000, normal seams are fully respected.  Default = 4.0"}),
                "texture_seam_weight":     ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2000.0,  "tooltip": "Chart Option: Default = 0.5"}),

                "max_cost":                ("FLOAT", {"default": 2.0, "min": 0.0, "max": 2000.0,  "tooltip": "Chart Option: If total of all metrics * weights > maxCost, don't grow chart. Lower values result in more charts.  Default = 2.0"}),
                "maxIterations":           ("INT", {"default": 1, "min": 1, "max": 100,           "tooltip": "Chart Option: Number of iterations of the chart growing and seeding phases. Higher values result in better charts.  Default = 1"}),
                "use_input_mesh_uvs":      ("BOOLEAN", {"default": False,                         "tooltip": "Chart Option: Default = False"}),
                "fix_winding":             ("BOOLEAN", {"default": False,                         "tooltip": "Chart Option: Enforce consistent texture coordinate winding.  Default = False"}),

                "max_chart_size":          ("INT", {"default": 0, "min": 0, "max": 2000,          "tooltip": "Pack Option: Charts larger than this will be scaled down. 0 means no limit. Default = 0"}),
                "padding":                 ("INT", {"default": 0, "min": 0, "max": 2000,          "tooltip": "Pack Option: Number of pixels to pad charts with. Default = 0"}),
                "texels_per_unit":         ("FLOAT", {"default": 0.0, "min": 0.0, "max": 8.0,     "tooltip": "Pack Option: \n// Unit to texel scale. e.g. a 1x1 quad with texelsPerUnit of 32 will take up approximately 32x32 texels in the atlas.\n// If 0, an estimated value will be calculated to approximately match the given resolution.\n// If resolution is also 0, the estimated value will approximately match a 1024x1024 atlas. Default = 0.0"}),
                "resolution":              ("INT", {"default": 0, "min": 0, "max": 4096,          "tooltip": "Pack Option: If 0, generate a single atlas with texelsPerUnit determining the final resolution. If not 0, and texelsPerUnit is not 0, generate one or more atlases with that exact resolution. If not 0, and texelsPerUnit is 0, texelsPerUnit is estimated to approximately match the resolution. Default = 0"}),
                "bilinear":                ("BOOLEAN", {"default": True,                          "tooltip": "Pack Option: Leave space around charts for texels that would be sampled by bilinear filtering. Default = True"}),
                "blockAlign":              ("BOOLEAN", {"default": False,                         "tooltip": "Pack Option: Align charts to 4x4 blocks. Also improves packing speed, since there are fewer possible chart locations to consider. Default = False"}),
                "bruteForce":              ("BOOLEAN", {"default": False,                         "tooltip": "Pack Option: Slower, but gives the best result. If false, use random chart placement.  Default = False"}),
                "create_image":            ("BOOLEAN", {"default": True,                          "tooltip": "Pack Option: Default = True"}),
                "rotate_charts":           ("BOOLEAN", {"default": True,                          "tooltip": "Pack Option: Rotate charts to improve packing. Default = True"}),
                "rotate_charts_to_axis":   ("BOOLEAN", {"default": True,                          "tooltip": "Pack Option: Rotate charts to the axis of their convex hull. Default = True"}),
            }            
        }

    RETURN_TYPES = ("TRIMESH", "IMAGE","STRING")
    RETURN_NAMES = ("trimesh", "UVImage","Utilization")
    FUNCTION = "process"
    CATEGORY = "ELiZTools"

    def process(self, trimesh, max_chart_area, max_cost, maxIterations, resolution, blockAlign, fix_winding, rotate_charts, rotate_charts_to_axis, padding, bruteForce, max_boundary_length, normal_deviation_weight, roundness_weight, straightness_weight, normal_seam_weight, texture_seam_weight, max_chart_size, texels_per_unit, bilinear, create_image, use_input_mesh_uvs):
        from .makeuvs.code import mesh_uv_wrap
        trimesh, UVImage, Utilization = mesh_uv_wrap(trimesh, max_chart_area, max_cost, maxIterations, resolution, blockAlign, fix_winding, rotate_charts, rotate_charts_to_axis, padding, bruteForce, max_boundary_length, normal_deviation_weight, roundness_weight, straightness_weight, normal_seam_weight, texture_seam_weight, max_chart_size, texels_per_unit, bilinear, create_image, use_input_mesh_uvs)
        return (trimesh, UVImage, Utilization)

NODE_CLASS_MAPPINGS = {
    "ELiZMeshUVWrap": ELiZMeshUVWrap,
    }

NODE_DISPLAY_NAME_MAPPINGS = {
    "ELiZMeshUVWrap": "ELiZ Mesh UV Wrap",
    }
