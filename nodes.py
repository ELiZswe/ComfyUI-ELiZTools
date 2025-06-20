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
                "maxIterations": ("INT", {"default": 1, "min": 1, "max": 4}),
            }            
        }

    RETURN_TYPES = ("TRIMESH", "IMAGE",)
    RETURN_NAMES = ("trimesh", "UVImage",)
    FUNCTION = "process"
    CATEGORY = "ELiZTools"

    def process(self, trimesh, maxIterations):
        from .makeuvs.code import mesh_uv_wrap
        trimesh, UVImage = mesh_uv_wrap(trimesh, maxIterations)
        return (trimesh, UVImage)

NODE_CLASS_MAPPINGS = {
    "ELiZMeshUVWrap": ELiZMeshUVWrap,
    }

NODE_DISPLAY_NAME_MAPPINGS = {
    "ELiZMeshUVWrap": "ELiZ Mesh UV Wrap",
    }
