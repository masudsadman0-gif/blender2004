# Autonimation

An elite, autonomous AI pipeline director and expert Python developer package specifically designed for the `bpy` (Blender Python) API. Autonimation aims to autonomously orchestrate end-to-end 3D animation productions in a headless server environment.

## Features

- **Strict Thread Safety First**: Utilizes `bpy.app.timers` to execute logic on the main thread and prevent segmentation faults.
- **Context Dependency Evasion**: Bypasses `bpy.ops` reliance by utilizing mathematical API interactions with `bmesh` and `bpy.data`.
- **Headless Execution Native**: Specifically programmed for `blender -b -P` operations.

### Dual Aesthetic Directives

1. **Disney / Pixar (Cinematic PBR)**
   - Procedural Principled BSDF with Subsurface Scattering programmatic controls.
   - Cinematic Orchestration with multi-light setup (Key, Fill, Rim).
   - High GI cycles rendering support.
2. **Japanese Anime (Cel-Shaded)**
   - Programmatic Node Tree generation with Constant Color Ramp.
   - Stark Single Sun Lighting.
   - Procedural Grease Pencil line art generation.

### Parametric Animation & Kinematics

- Deep mathematical curve tracking utilizing F-Curves and Keyframe baking.
- Mocap retargeting integration parameters.

## Integration Protocols

Autonimation dynamically resolves missing tools by wrapping GitHub repository integrations:
- `infinigen`
- `BlenderProc`
- `awesome-blender-script`
- `StableGen`
- `SOMA` / `VIPER-Blender-Mocap`

## API Configuration
Autonimation relies on freely hosted cloud API endpoints to avoid restrictive paid APIs and to eliminate the need for heavy local PC hardware requirements.
It supports loading free-tier API parameters for Hugging Face Serverless, Cerebras Cloud, Together AI, and Groq for autonomous AI integrations.

1. Copy the `.env.example` file to `.env`:
   `cp .env.example .env`
2. Populate the `.env` file with your respective free cloud API keys.

## Installation
Run `python setup.py install` within Blender's bundled Python distribution.

## Execution
Run within blender directly using the command line:
`blender -b -P autonimation.py`
