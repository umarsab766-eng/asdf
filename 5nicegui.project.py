import os
import tempfile
from pathlib import Path
from typing import Optional

import trimesh
from nicegui import ui, events


current_scene: Optional[ui.scene] = None

def convert_fbx_to_glb(fbx_path: str) -> str:
    """Convert FBX file to GLB format using trimesh."""
    try:
    
        mesh = trimesh.load(fbx_path)
        
        
        glb_path = fbx_path.replace('.fbx', '.glb')
        
       
        mesh.export(glb_path)
        
        return glb_path
    except Exception as e:
        ui.notify(f"Error converting FBX to GLB: {str(e)}", color="negative")
        raise

def handle_upload(e: events.UploadEventArguments):
    """Handle file upload event."""
    global current_scene
    
    
    if not e.files:
        return
    
   
    file_info = e.files[0]
    file_name = file_info.name.lower()
    

    if not (file_name.endswith('.fbx') or file_name.endswith('.glb')):
        ui.notify("Please upload an FBX or GLB file", color="warning")
        return
    
    try:
        
        with tempfile.TemporaryDirectory() as temp_dir:
            
            file_path = os.path.join(temp_dir, file_info.name)
            with open(file_path, 'wb') as f:
                f.write(file_info.content.read())
            

            if file_name.endswith('.fbx'):
                
                glb_path = convert_fbx_to_glb(file_path)
                model_path = glb_path
                ui.notify("FBX file converted to GLB format", color="info")
            else:
                
                model_path = file_path
                ui.notify("GLB file loaded directly", color="info")
            
            
            if current_scene:
                current_scene.clear()
            
            
            with current_scene:
                model = current_scene.gltf(model_path)
                
               
                model.scale(0.1)  
                model.move(0, 0, 0)  
                
               
                current_scene.spot_light(
                    x=2, y=3, z=4,
                    intensity=0.7,
                    angle=0.3,
                    penumbra=0.2
                )
                current_scene.ambient_light(intensity=0.3)
                
                
                current_scene.axes_helper()
            
            ui.notify(f"Successfully loaded {file_info.name}", color="positive")
    
    except Exception as e:
        ui.notify(f"Error processing file: {str(e)}", color="negative")

@ui.page('/')
def main_page():
    global current_scene
    
    
    ui.label('3D Model Viewer').classes('text-2xl font-bold mb-4')
    
    
    with ui.card().classes('w-full max-w-md mx-auto mb-6'):
        ui.label('Upload 3D Model').classes('text-lg font-semibold mb-2')
        ui.upload(
            label='Choose FBX or GLB file',
            auto_upload=True,
            on_upload=handle_upload,
            multiple=False,
        ).classes('w-full')
    
   
    with ui.card().classes('w-full'):
        ui.label('3D Visualization').classes('text-lg font-semibold mb-2')
        
      
        with ui.scene(
            width='100%',
            height='500px',
            grid=True,
            background_color='#f0f0f0'
        ) as scene:
            current_scene = scene
            
            
            scene.text('Upload an FBX or GLB file to visualize it here', 
                      style='color: #666; font-size: 16px;').move(0, 0, 0)
            
            
            scene.spot_light(
                intensity=0.7,
                angle=0.3,
                penumbra=0.2
            )
            
       
            scene.axes_helper()
    
   
    with ui.card().classes('w-full max-w-2xl mx-auto mt-6'):
        ui.label('Instructions').classes('text-lg font-semibold mb-2')
        ui.markdown("""
        1. Click the "Choose FBX or GLB file" button to upload a 3D model
        2. **GLB files** will be loaded directly
        3. **FBX files** will be converted to GLB format first
        4. Use your mouse to navigate the 3D scene:
           - Left click + drag: Rotate
           - Right click + drag: Pan
           - Scroll: Zoom in/out
        """)
    
   
    with ui.card().classes('w-full max-w-2xl mx-auto mt-4'):
        ui.label('Supported Formats').classes('text-lg font-semibold mb-2')
        with ui.row().classes('gap-4'):
            with ui.column().classes('items-center'):
                ui.label('GLB').classes('font-bold text-blue-600')
                ui.icon('check_circle', color='green')
                ui.label('Direct loading').classes('text-sm')
            with ui.column().classes('items-center'):
                ui.label('FBX').classes('font-bold text-blue-600')
                ui.icon('autorenew', color='orange')
                ui.label('Auto-converted').classes('text-sm')

ui.run()