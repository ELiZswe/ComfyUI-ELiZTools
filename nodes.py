import os
#import torch
#import torch.nn.functional as F
#from pathlib import Path
#import numpy as np
#import json
import trimesh as Trimesh
   
class ELiZMeshUVWrap:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trimesh": ("TRIMESH",),
            },
        }

    RETURN_TYPES = ("TRIMESH", )
    RETURN_NAMES = ("trimesh", )
    FUNCTION = "process"
    CATEGORY = "ELiZTools"

    def process(self, trimesh):
        from .makeuvs.code import mesh_uv_wrap
        trimesh = mesh_uv_wrap(trimesh)
        return (trimesh,)

NODE_CLASS_MAPPINGS = {
    "ELiZMeshUVWrap": ELiZMeshUVWrap,
    }

NODE_DISPLAY_NAME_MAPPINGS = {
    "Hy3DMeshUVWrap": "ELiZ Mesh UV Wrap",
    }
