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
                "max_chart_area": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 8.0, "tooltip": "Don\'t grow charts to be larger than this. 0 means no limit."}),
                "max_cost": ("FLOAT", {"default": 2.0, "min": 2.0, "max": 24.0, "tooltip": "If total of all metrics * weights > maxCost, don't grow chart. Lower values result in more charts."}),
                "maxIterations": ("INT", {"default": 1, "min": 1, "max": 32, "tooltip": "Number of iterations of the chart growing and seeding phases. Higher values result in better charts."}),
                "resolution": ("INT", {"default": 0, "min": 0, "max": 4096, "tooltip": "If 0, generate a single atlas with texelsPerUnit determining the final resolution. If not 0, and texelsPerUnit is not 0, generate one or more atlases with that exact resolution. If not 0, and texelsPerUnit is 0, texelsPerUnit is estimated to approximately match the resolution."}),
                "blockAlign": ("BOOLEAN", {"default": False, "tooltip": "Align charts to 4x4 blocks. Also improves packing speed, since there are fewer possible chart locations to consider."}),
            }            
        }

    RETURN_TYPES = ("TRIMESH", "IMAGE",)
    RETURN_NAMES = ("trimesh", "UVImage",)
    FUNCTION = "process"
    CATEGORY = "ELiZTools"

    def process(self, trimesh, max_chart_area, max_cost, maxIterations, resolution, blockAlign):
        from .makeuvs.code import mesh_uv_wrap
        trimesh, UVImage = mesh_uv_wrap(trimesh, max_chart_area, max_cost, maxIterations, resolution, blockAlign)
        return (trimesh, UVImage)

NODE_CLASS_MAPPINGS = {
    "ELiZMeshUVWrap": ELiZMeshUVWrap,
    }

NODE_DISPLAY_NAME_MAPPINGS = {
    "ELiZMeshUVWrap": "ELiZ Mesh UV Wrap",
    }
