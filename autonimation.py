import sys
import subprocess
import os
import json
import math

def _install_dependency(package_name):
    """Dynamically install missing packages into Blender's isolated environment."""
    python_exe = sys.executable
    print(f"Installing {package_name} using {python_exe}...")
    subprocess.check_call([python_exe, "-m", "pip", "install", package_name])

# Auto-install essential dependencies
try:
    import numpy as np
except ImportError:
    _install_dependency("numpy")
    import numpy as np

try:
    import scipy
except ImportError:
    _install_dependency("scipy")

try:
    from dotenv import load_dotenv
except ImportError:
    _install_dependency("python-dotenv")
    from dotenv import load_dotenv

try:
    import bpy
except ImportError:
    print("Warning: bpy not found. This module must be run within Blender.")

import bmesh
from mathutils import Vector, Euler

class Autonimation:
    """
    Elite autonomous AI pipeline director and expert Python developer for the bpy API.
    """

    def __init__(self, style="Disney", is_headless=True):
        self.style = style
        self.is_headless = is_headless
        self.context_memory = {}

        # Load API Keys
        self._load_environment_variables()

        print(f"Autonimation Initialized. Style: {self.style}, Headless: {self.is_headless}")

    def _load_environment_variables(self):
        """Load API keys from .env into memory context."""
        load_dotenv()
        self.context_memory['HF_TOKEN'] = os.getenv('HF_TOKEN')
        self.context_memory['TRIPOSR_ENDPOINT'] = os.getenv('TRIPOSR_ENDPOINT')
        self.context_memory['CEREBRAS_API_KEY'] = os.getenv('CEREBRAS_API_KEY')
        self.context_memory['TOGETHER_API_KEY'] = os.getenv('TOGETHER_API_KEY')
        self.context_memory['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
        print("Environment variables loaded. Ready for cloud generation APIs.")

    # --------------------------------------------------------------------------
    # ERROR RECOVERY & CONTEXT OVERRIDES
    # --------------------------------------------------------------------------
    def get_3d_view_override(self):
        """Dynamically generate a context override dictionary for the 3D Viewport."""
        if not hasattr(bpy, 'context'): return {}
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                override['region'] = area.regions[-1]
                override['space_data'] = area.spaces.active
                return override
        return {}

    def safe_ops_execute(self, op_func, *args, **kwargs):
        """Execute a bpy.ops command safely with a 3D view override."""
        override = self.get_3d_view_override()
        try:
            with bpy.context.temp_override(**override):
                return op_func(*args, **kwargs)
        except Exception as e:
            print(f"Failed safe execution: {e}")
            return None

    # --------------------------------------------------------------------------
    # GITHUB REPOSITORY INTEGRATION (Wrappers)
    # --------------------------------------------------------------------------
    def clone_repo(self, url, dest_folder):
        """Clone a GitHub repository."""
        if not os.path.exists(dest_folder):
            print(f"Cloning {url} to {dest_folder}...")
            subprocess.check_call(["git", "clone", url, dest_folder])
        else:
            print(f"Repository {dest_folder} already exists.")

    def integrate_infinigen(self):
        """Clone princeton-vl/infinigen for infinite photorealistic worlds."""
        self.clone_repo("https://github.com/princeton-vl/infinigen.git", "infinigen_repo")
        print("Infinigen integrated. Use procedural node trees for generation.")

    def integrate_blenderproc(self):
        """Clone DLR-RM/BlenderProc for physics-based object scattering."""
        self.clone_repo("https://github.com/DLR-RM/BlenderProc.git", "blenderproc_repo")
        print("BlenderProc integrated. Use for physics-based assembly.")

    def integrate_asset_std(self):
        """Clone SunzeY/awesome-blender-script for asset standardization."""
        self.clone_repo("https://github.com/SunzeY/awesome-blender-script.git", "blender_scripts_repo")
        print("Asset standardization script ready to bake vertex colors.")

    def integrate_stablegen(self):
        """Clone sakalond/StableGen for PBR texture generation."""
        self.clone_repo("https://github.com/sakalond/StableGen.git", "stablegen_repo")
        print("StableGen integrated for PBR textures via TRELLIS.2 / ComfyUI.")

    def integrate_mocap(self):
        """Clone VIPER-Blender-Mocap or SOMA for optical point-cloud mocap solving."""
        self.clone_repo("https://github.com/Daniel-W-Blender-Python/VIPER-Blender-Mocap.git", "viper_mocap_repo")
        print("Mocap integration ready via VIPER.")

    # --------------------------------------------------------------------------
    # SCENE GENERATION & ASSET ASSEMBLY
    # --------------------------------------------------------------------------
    def clear_scene(self):
        """Safely clear the scene for procedural instantiation."""
        print("Clearing scene...")
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        for block in list(bpy.data.meshes):
            if block.users == 0: bpy.data.meshes.remove(block)
        for block in list(bpy.data.materials):
            if block.users == 0: bpy.data.materials.remove(block)
        for block in list(bpy.data.cameras):
            if block.users == 0: bpy.data.cameras.remove(block)
        for block in list(bpy.data.lights):
            if block.users == 0: bpy.data.lights.remove(block)

    def instantiate_mesh(self, name, vertices, faces):
        """Create a mesh using bmesh instead of bpy.ops to avoid context dependencies."""
        mesh = bpy.data.meshes.new(name)
        bm = bmesh.new()
        for v in vertices:
            bm.verts.new(v)
        bm.verts.ensure_lookup_table()
        for f in faces:
            try:
                bm.faces.new([bm.verts[i] for i in f])
            except ValueError:
                pass # Face already exists or invalid
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        self.context_memory[f"{name}_uuid"] = obj.name
        return obj

    def setup_character_rig(self, obj, armature):
        """Synchronize mesh data with armature and configure IK pole targets."""
        modifier = obj.modifiers.new(name="Armature", type='ARMATURE')
        modifier.object = armature
        # Setup IK programmatically
        for bone in armature.pose.bones:
            if "IK" in bone.name:
                constraint = bone.constraints.new('IK')
                # Assume pole target exists
                print(f"Configured IK for {bone.name}")

    # --------------------------------------------------------------------------
    # AESTHETIC DIRECTIVES
    # --------------------------------------------------------------------------
    def apply_style(self):
        if self.style == "Disney":
            self._apply_disney_style()
        elif self.style == "Anime":
            self._apply_anime_style()
        else:
            print("Unknown style. Defaulting to Disney.")
            self._apply_disney_style()

    def _apply_disney_style(self):
        """Apply Disney/Pixar Cinematic PBR rules."""
        print("Applying Disney Style...")
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.max_bounces = 4

        # Shader example for Disney
        mat = bpy.data.materials.new(name="DisneyMaterial")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            # Enable Subsurface Scattering
            if 'Subsurface Weight' in bsdf.inputs:
                bsdf.inputs['Subsurface Weight'].default_value = 0.25
            elif 'Subsurface' in bsdf.inputs: # Older blender versions
                bsdf.inputs['Subsurface'].default_value = 0.25
            if 'Subsurface Radius' in bsdf.inputs:
                bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)
            bsdf.inputs['Roughness'].default_value = 0.5

        # Lighting: Area Light (Key), Spot/Area (Rim)
        light_data = bpy.data.lights.new(name="KeyLight", type='AREA')
        light_data.energy = 1000
        light_data.size = 5.0
        light_obj = bpy.data.objects.new(name="KeyLight", object_data=light_data)
        bpy.context.collection.objects.link(light_obj)
        light_obj.location = (5, -5, 5)

        rim_data = bpy.data.lights.new(name="RimLight", type='SPOT')
        rim_data.energy = 5000
        rim_obj = bpy.data.objects.new(name="RimLight", object_data=rim_data)
        bpy.context.collection.objects.link(rim_obj)
        rim_obj.location = (0, 5, 5)
        rim_obj.rotation_euler = (math.radians(-45), 0, math.radians(180))

    def _apply_anime_style(self):
        """Apply Japanese Anime (Cel-Shaded) rules."""
        print("Applying Anime Style...")
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

        # Custom Toon Shader Node Tree
        mat = bpy.data.materials.new(name="AnimeToonMaterial")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type="ShaderNodeOutputMaterial")
        diffuse = nodes.new(type="ShaderNodeBsdfDiffuse")
        shader_to_rgb = nodes.new(type="ShaderNodeShaderToRGB")
        color_ramp = nodes.new(type="ShaderNodeValToRGB")

        color_ramp.color_ramp.interpolation = 'CONSTANT'
        color_ramp.color_ramp.elements[0].position = 0.4
        color_ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
        color_ramp.color_ramp.elements[1].position = 0.6
        color_ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.8, 1.0)

        links.new(diffuse.outputs['BSDF'], shader_to_rgb.inputs['Shader'])
        links.new(shader_to_rgb.outputs['Color'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], output.inputs['Surface'])

        # Stark Lighting: Single Sun Light
        sun_data = bpy.data.lights.new(name="MLight", type='SUN')
        sun_data.energy = 3.0
        sun_obj = bpy.data.objects.new(name="MLight", object_data=sun_data)
        bpy.context.collection.objects.link(sun_obj)
        sun_obj.rotation_euler = (math.radians(45), math.radians(45), 0)

        # Line Art (Grease Pencil)
        gp_data = bpy.data.grease_pencils.new("LineArt")
        gp_layer = gp_data.layers.new("Lines", set_active=True)

        # Solid Material for Grease Pencil
        mat_gp = bpy.data.materials.new("LineArtMat")
        bpy.data.materials.create_gpencil_data(mat_gp)
        mat_gp.grease_pencil.color = (0.01, 0.01, 0.01, 1.0)
        gp_data.materials.append(mat_gp)

        gp_obj = bpy.data.objects.new("LineArt", gp_data)
        bpy.context.collection.objects.link(gp_obj)
        mod = gp_obj.modifiers.new(name="LineArt", type='LINEART')
        mod.source_type = 'SCENE'

    # --------------------------------------------------------------------------
    # KINEMATICS, MOVEMENT & ANIMATION
    # --------------------------------------------------------------------------
    def apply_parametric_animation(self, obj, frames, trajectory_func):
        """Script F-Curves directly to animate object along a trajectory."""
        print(f"Animating {obj.name}...")
        obj.animation_data_create()
        action = bpy.data.actions.new(name=f"{obj.name}Action")
        obj.animation_data.action = action

        # 3 Location F-Curves
        fcurves = [action.fcurves.new(data_path="location", index=i) for i in range(3)]

        for frame in frames:
            loc = trajectory_func(frame)
            for i in range(3):
                fcurves[i].keyframe_points.insert(frame, loc[i])

        # Set interpolation to LINEAR
        for fc in fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'LINEAR'

    def retarget_mocap(self, rig, json_data_path):
        """Bake external mocap actions to armature via visual keying."""
        print(f"Retargeting mocap from {json_data_path} to {rig.name}...")
        # Implement logic to parse json and apply to rig.pose.bones
        # ...
        pass

    # --------------------------------------------------------------------------
    # HEADLESS EXECUTION & RENDER ORCHESTRATION
    # --------------------------------------------------------------------------
    def configure_render(self, output_filepath):
        """Configure GPU and FFmpeg output settings."""
        scene = bpy.context.scene
        print("Configuring render settings...")

        if scene.render.engine == 'CYCLES':
            scene.cycles.device = 'GPU'
            prefs = bpy.context.preferences.addons['cycles'].preferences
            prefs.compute_device_type = 'CUDA' # or OPTIX
            for device in prefs.get_devices():
                for d in device:
                    d.use = True

        scene.render.image_settings.file_format = "FFMPEG"
        scene.render.ffmpeg.format = "MPEG4"
        scene.render.ffmpeg.codec = "H264"
        scene.render.fps = 24
        scene.render.filepath = output_filepath

    def execute_render(self, blend_file_path):
        """Save and trigger headless render via command line."""
        bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
        print(f"Saved project to {blend_file_path}. Triggering render...")
        blender_exec = bpy.app.binary_path
        subprocess.Popen([blender_exec, "-b", blend_file_path, "-a"])

    # --------------------------------------------------------------------------
    # THREAD SAFETY (App Timers)
    # --------------------------------------------------------------------------
    def push_to_main_thread(self, func, *args, **kwargs):
        """Push execution to main thread using bpy.app.timers."""
        def wrapper():
            func(*args, **kwargs)
            return None
        bpy.app.timers.register(wrapper)

    # --------------------------------------------------------------------------
    # EXECUTION PIPELINE
    # --------------------------------------------------------------------------
    def build_scene(self):
        """Orchestrates the entire production end-to-end."""
        self.clear_scene()
        self.apply_style()
        # Add a simple camera
        cam_data = bpy.data.cameras.new("Camera")
        cam = bpy.data.objects.new("Camera", cam_data)
        bpy.context.collection.objects.link(cam)
        cam.location = (0, -10, 0)
        cam.rotation_euler = (math.radians(90), 0, 0)
        bpy.context.scene.camera = cam

        # Add a placeholder mesh
        cube = self.instantiate_mesh("Actor",
            vertices=[(-1,-1,-1), (-1,1,-1), (1,1,-1), (1,-1,-1),
                      (-1,-1,1), (-1,1,1), (1,1,1), (1,-1,1)],
            faces=[(0,1,2,3), (4,5,6,7), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)])

        def trajectory(f):
            return (math.sin(f/10.0)*2, 0, math.cos(f/10.0)*2)

        self.apply_parametric_animation(cube, range(1, 100), trajectory)
        self.configure_render("/tmp/autonimation_output.mp4")
        print("Pipeline built successfully.")

def run_pipeline(style="Disney"):
    director = Autonimation(style=style)
    # Ensure it's run on main thread
    if hasattr(bpy, 'app'):
        director.push_to_main_thread(director.build_scene)
    else:
        print("Running outside Blender. Simulation mode.")

if __name__ == "__main__":
    run_pipeline("Disney")
