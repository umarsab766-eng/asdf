from nicegui import ui, app
import json
import random
from datetime import datetime
from typing import Dict, List, Optional

class CarDesignGame:
    def __init__(self):
        self.current_design = {
            'body_color': '#FF4444',
            'roof_color': '#333333',
            'wheel_color': '#888888',
            'window_tint': '#4A90E2',
            'body_style': 'sports',
            'wheel_style': 'sport',
            'decal': 'none',
            'spoiler': 'none',
            'name': 'My Car Design'
        }
        
        self.saved_designs = []
        self.price = 0
        self.budget = 50000
        
        # Car parts catalog
        self.body_styles = {
            'sports': {'name': 'Sports Car', 'price': 25000, 'emoji': '🏎️'},
            'sedan': {'name': 'Sedan', 'price': 20000, 'emoji': '🚗'},
            'suv': {'name': 'SUV', 'price': 30000, 'emoji': '🚙'},
            'truck': {'name': 'Truck', 'price': 35000, 'emoji': '🚚'},
            'convertible': {'name': 'Convertible', 'price': 28000, 'emoji': '🚘'}
        }
        
        self.wheel_styles = {
            'sport': {'name': 'Sport Wheels', 'price': 2000, 'emoji': '⭕'},
            'luxury': {'name': 'Luxury Rims', 'price': 3500, 'emoji': '💎'},
            'offroad': {'name': 'Off-Road', 'price': 2500, 'emoji': '🛞'},
            'classic': {'name': 'Classic', 'price': 1500, 'emoji': '🎯'}
        }
        
        self.decals = {
            'none': {'name': 'None', 'price': 0, 'emoji': ''},
            'flames': {'name': 'Flames', 'price': 500, 'emoji': '🔥'},
            'stripes': {'name': 'Racing Stripes', 'price': 800, 'emoji': '🏁'},
            'lightning': {'name': 'Lightning', 'price': 600, 'emoji': '⚡'},
            'stars': {'name': 'Stars', 'price': 400, 'emoji': '⭐'}
        }
        
        self.spoilers = {
            'none': {'name': 'None', 'price': 0, 'emoji': ''},
            'small': {'name': 'Small Spoiler', 'price': 1200, 'emoji': '▶'},
            'medium': {'name': 'Medium Spoiler', 'price': 1800, 'emoji': '▷'},
            'large': {'name': 'Large Wing', 'price': 2500, 'emoji': '►'}
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the main UI"""
        with ui.header().classes('bg-gradient-to-r from-purple-600 to-blue-600 text-white'):
            with ui.row().classes('w-full justify-between items-center px-4'):
                ui.label('🏁 Car Design Studio').classes('text-2xl font-bold')
                with ui.row().classes('gap-4 items-center'):
                    ui.label(f'💰 Budget: ${self.budget:,}').classes('text-lg')
                    ui.label(f'🛒 Total: $0').classes('text-lg').bind_text_from(self, 'price', 
                        lambda x: f'🛒 Total: ${x:,}')
        
        with ui.tabs().classes('w-full') as tabs:
            design_tab = ui.tab('🎨 Design')
            saved_tab = ui.tab('💾 My Designs')
            gallery_tab = ui.tab('🏆 Gallery')
        
        with ui.tab_panels(tabs, value=design_tab):
            # Design Tab
            with ui.tab_panel(design_tab):
                with ui.row().classes('w-full gap-4 p-4'):
                    # Left Panel - Customization Options
                    with ui.column().classes('w-1/3 gap-4'):
                        self.create_customization_panel()
                    
                    # Center Panel - Car Preview
                    with ui.column().classes('w-1/3 gap-4'):
                        self.create_preview_panel()
                    
                    # Right Panel - Stats & Actions
                    with ui.column().classes('w-1/3 gap-4'):
                        self.create_stats_panel()
            
            # Saved Designs Tab
            with ui.tab_panel(saved_tab):
                self.create_saved_designs_panel()
            
            # Gallery Tab
            with ui.tab_panel(gallery_tab):
                self.create_gallery_panel()
    
    def create_customization_panel(self):
        """Create the customization options panel"""
        with ui.card().classes('w-full p-4 shadow-lg'):
            ui.label('🎨 Customization').classes('text-xl font-bold mb-4')
            
            # Car Name
            with ui.row().classes('w-full gap-2 mb-4'):
                ui.label('Car Name:').classes('font-semibold')
                ui.input(value=self.current_design['name']).classes('flex-grow').bind_value(
                    self.current_design, 'name')
            
            # Body Style
            with ui.expansion('🚗 Body Style', value=True).classes('w-full'):
                with ui.row().classes('w-full gap-2 flex-wrap'):
                    for style_id, style_info in self.body_styles.items():
                        with ui.card().classes('p-2 cursor-pointer hover:shadow-lg transition-shadow'):
                            ui.button(
                                f"{style_info['emoji']} {style_info['name']}\n${style_info['price']:,}",
                                on_click=lambda s=style_id: self.update_body_style(s)
                            ).classes('w-full').props('flat')
            
            # Colors
            with ui.expansion('🎨 Colors', value=True).classes('w-full'):
                with ui.column().classes('w-full gap-2'):
                    ui.label('Body Color:').classes('font-semibold')
                    ui.color_picker(value=self.current_design['body_color'], on_pick=lambda: self.update_price()).bind_value(
                        self.current_design, 'body_color')
                    
                    ui.label('Roof Color:').classes('font-semibold')
                    ui.color_picker(value=self.current_design['roof_color'], on_pick=lambda: self.update_price()).bind_value(
                        self.current_design, 'roof_color')
                    
                    ui.label('Wheel Color:').classes('font-semibold')
                    ui.color_picker(value=self.current_design['wheel_color'], on_pick=lambda: self.update_price()).bind_value(
                        self.current_design, 'wheel_color')
            
            # Wheels
            with ui.expansion('⭕ Wheels', value=True).classes('w-full'):
                with ui.row().classes('w-full gap-2 flex-wrap'):
                    for wheel_id, wheel_info in self.wheel_styles.items():
                        with ui.card().classes('p-2 cursor-pointer hover:shadow-lg transition-shadow'):
                            ui.button(
                                f"{wheel_info['emoji']} {wheel_info['name']}\n${wheel_info['price']:,}",
                                on_click=lambda w=wheel_id: self.update_wheel_style(w)
                            ).classes('w-full').props('flat')
            
            # Decals
            with ui.expansion('🔥 Decals', value=False).classes('w-full'):
                with ui.row().classes('w-full gap-2 flex-wrap'):
                    for decal_id, decal_info in self.decals.items():
                        with ui.card().classes('p-2 cursor-pointer hover:shadow-lg transition-shadow'):
                            ui.button(
                                f"{decal_info['emoji']} {decal_info['name']}\n${decal_info['price']:,}",
                                on_click=lambda d=decal_id: self.update_decal(d)
                            ).classes('w-full').props('flat')
            
            # Spoilers
            with ui.expansion('✈️ Spoilers', value=False).classes('w-full'):
                with ui.row().classes('w-full gap-2 flex-wrap'):
                    for spoiler_id, spoiler_info in self.spoilers.items():
                        with ui.card().classes('p-2 cursor-pointer hover:shadow-lg transition-shadow'):
                            ui.button(
                                f"{spoiler_info['emoji']} {spoiler_info['name']}\n${spoiler_info['price']:,}",
                                on_click=lambda s=spoiler_id: self.update_spoiler(s)
                            ).classes('w-full').props('flat')
    
    def create_preview_panel(self):
        """Create the car preview panel"""
        with ui.card().classes('w-full p-4 shadow-lg'):
            ui.label('👁️ Preview').classes('text-xl font-bold mb-4')
            
            # Car Visual Representation
            with ui.column().classes('w-full items-center'):
                ui.add_css('''                        .car-container {
                            width: 100%;
                            height: 300px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            position: relative;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            border-radius: 10px;
                            overflow: hidden;
                        }
                        .car-body {
                            font-size: 120px;
                            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));
                            transition: all 0.3s ease;
                            animation: float 3s ease-in-out infinite;
                        }
                        @keyframes float {
                            0%, 100% { transform: translateY(0px); }
                            50% { transform: translateY(-10px); }
                        }
                        .car-decoration {
                            position: absolute;
                            font-size: 40px;
                            animation: pulse 2s ease-in-out infinite;
                        }
                        @keyframes pulse {
                            0%, 100% { opacity: 0.8; }
                            50% { opacity: 1; }
                        }
''')
                
                with ui.column().classes('car-container'):
                    ui.label(self.body_styles[self.current_design['body_style']]['emoji']).classes(
                        'car-body')
                    
                    # Add decal if selected
                    if self.current_design['decal'] != 'none':
                        ui.label(self.decals[self.current_design['decal']]['emoji']).classes(
                            'car-decoration').style('top: 50%; left: 50%; transform: translate(-50%, -50%);')
                    
                    # Add spoiler if selected
                    if self.current_design['spoiler'] != 'none':
                        ui.label(self.spoilers[self.current_design['spoiler']]['emoji']).classes(
                            'car-decoration').style('top: 20%; right: 20%;')
            
            # Quick Stats
            with ui.row().classes('w-full justify-around mt-4 p-2 bg-gray-100 rounded'):
                ui.label(f"Style: {self.body_styles[self.current_design['body_style']]['name']}").classes('text-sm')
                ui.label(f"Wheels: {self.wheel_styles[self.current_design['wheel_style']]['name']}").classes('text-sm')
                ui.label(f"Decal: {self.decals[self.current_design['decal']]['name']}").classes('text-sm')
    
    def create_stats_panel(self):
        """Create the stats and actions panel"""
        with ui.card().classes('w-full p-4 shadow-lg'):
            ui.label('📊 Car Stats').classes('text-xl font-bold mb-4')
            
            # Performance Stats (simulated)
            with ui.column().classes('w-full gap-2'):
                self.speed_stat = ui.linear_progress(value=0.7).classes('w-full')
                ui.label('Speed').classes('text-sm')
                
                self.style_stat = ui.linear_progress(value=0.8).classes('w-full')
                ui.label('Style').classes('text-sm')
                
                self.value_stat = ui.linear_progress(value=0.6).classes('w-full')
                ui.label('Value').classes('text-sm')
            
            # Price Breakdown
            with ui.expansion('💰 Price Breakdown', value=True).classes('w-full mt-4'):
                with ui.column().classes('w-full gap-1 text-sm'):
                    self.breakdown_labels = {}
            
            # Action Buttons
            with ui.column().classes('w-full gap-2 mt-4'):
                ui.button('💾 Save Design', on_click=self.save_design).classes(
                    'w-full bg-green-500 text-white').props('icon=save')
                
                ui.button('🎲 Random Design', on_click=self.randomize_design).classes(
                    'w-full bg-purple-500 text-white').props('icon=shuffle')
                
                ui.button('🔄 Reset', on_click=self.reset_design).classes(
                    'w-full bg-gray-500 text-white').props('icon=refresh')
                
                ui.button('📸 Screenshot', on_click=self.take_screenshot).classes(
                    'w-full bg-blue-500 text-white').props('icon=photo_camera')
            
            # Budget Warning
            self.budget_warning = ui.label('').classes('text-red-500 font-bold mt-2')
    
    def create_saved_designs_panel(self):
        """Create the saved designs panel"""
        with ui.column().classes('w-full p-4 gap-4'):
            ui.label('💾 My Saved Designs').classes('text-2xl font-bold')
            
            with ui.row().classes('w-full gap-2 mb-4'):
                ui.button('📥 Load from File', on_click=self.load_from_file).classes('bg-blue-500 text-white')
                ui.button('📤 Export All', on_click=self.export_designs).classes('bg-green-500 text-white')
            
            self.saved_designs_container = ui.column().classes('w-full gap-4')
            self.update_saved_designs_display()
    
    def create_gallery_panel(self):
        """Create the gallery panel with preset designs"""
        with ui.column().classes('w-full p-4 gap-4'):
            ui.label('🏆 Design Gallery').classes('text-2xl font-bold')
            ui.label('Choose from these amazing preset designs!').classes('text-gray-600')
            
            # Preset designs
            presets = [
                {
                    'name': 'Speed Demon',
                    'body_style': 'sports',
                    'body_color': '#FF0000',
                    'wheel_style': 'sport',
                    'decal': 'flames',
                    'spoiler': 'large'
                },
                {
                    'name': 'Luxury Cruiser',
                    'body_style': 'sedan',
                    'body_color': '#1E1E1E',
                    'wheel_style': 'luxury',
                    'decal': 'none',
                    'spoiler': 'none'
                },
                {
                    'name': 'Adventure Seeker',
                    'body_style': 'suv',
                    'body_color': '#228B22',
                    'wheel_style': 'offroad',
                    'decal': 'lightning',
                    'spoiler': 'medium'
                },
                {
                    'name': 'Racing Champion',
                    'body_style': 'sports',
                    'body_color': '#0000FF',
                    'wheel_style': 'sport',
                    'decal': 'stripes',
                    'spoiler': 'large'
                }
            ]
            
            with ui.row().classes('w-full gap-4 flex-wrap'):
                for preset in presets:
                    with ui.card().classes('p-4 cursor-pointer hover:shadow-xl transition-shadow'):
                        ui.label(preset['name']).classes('font-bold text-lg mb-2')
                        ui.label(self.body_styles[preset['body_style']]['emoji']).classes('text-4xl mb-2')
                        ui.button('Load Design', on_click=lambda p=preset: self.load_preset(p)).classes(
                            'w-full bg-blue-500 text-white')
    
    def update_body_style(self, style):
        """Update the car body style"""
        self.current_design['body_style'] = style
        self.update_price()
        self.update_stats()
        ui.notify(f'Changed to {self.body_styles[style]["name"]}', type='positive')
    
    def update_wheel_style(self, style):
        """Update the wheel style"""
        self.current_design['wheel_style'] = style
        self.update_price()
        self.update_stats()
        ui.notify(f'Changed to {self.wheel_styles[style]["name"]}', type='positive')
    
    def update_decal(self, decal):
        """Update the car decal"""
        self.current_design['decal'] = decal
        self.update_price()
        self.update_stats()
        ui.notify(f'Added {self.decals[decal]["name"]}', type='positive')
    
    def update_spoiler(self, spoiler):
        """Update the car spoiler"""
        self.current_design['spoiler'] = spoiler
        self.update_price()
        self.update_stats()
        ui.notify(f'Added {self.spoilers[spoiler]["name"]}', type='positive')
    
    def update_price(self):
        """Calculate and update the total price"""
        self.price = (
            self.body_styles[self.current_design['body_style']]['price'] +
            self.wheel_styles[self.current_design['wheel_style']]['price'] +
            self.decals[self.current_design['decal']]['price'] +
            self.spoilers[self.current_design['spoiler']]['price']
        )
        
        # Update budget warning
        if self.price > self.budget:
            self.budget_warning.text = f'⚠️ Over budget by ${self.price - self.budget:,}!'
        else:
            self.budget_warning.text = ''
        
        # Update price breakdown
        self.update_price_breakdown()
    
    def update_price_breakdown(self):
        """Update the price breakdown display"""
        breakdown = [
            f"Body: ${self.body_styles[self.current_design['body_style']]['price']:,}",
            f"Wheels: ${self.wheel_styles[self.current_design['wheel_style']]['price']:,}",
            f"Decal: ${self.decals[self.current_design['decal']]['price']:,}",
            f"Spoiler: ${self.spoilers[self.current_design['spoiler']]['price']:,}",
            f"Total: ${self.price:,}"
        ]
        
        # Update the breakdown labels if they exist
        for i, text in enumerate(breakdown):
            if i not in self.breakdown_labels:
                self.breakdown_labels[i] = ui.label(text).classes('w-full')
            else:
                self.breakdown_labels[i].text = text
    
    def update_stats(self):
        """Update the car stats based on current design"""
        # Simulate stats based on choices
        speed = 0.5
        style = 0.5
        value = 0.5
        
        # Body style affects stats
        if self.current_design['body_style'] == 'sports':
            speed += 0.3
            style += 0.2
        elif self.current_design['body_style'] == 'sedan':
            value += 0.3
        elif self.current_design['body_style'] == 'suv':
            value += 0.2
        
        # Wheels affect stats
        if self.current_design['wheel_style'] == 'sport':
            speed += 0.2
            style += 0.1
        elif self.current_design['wheel_style'] == 'luxury':
            style += 0.3
        
        # Decals and spoilers affect style
        if self.current_design['decal'] != 'none':
            style += 0.1
        if self.current_design['spoiler'] != 'none':
            speed += 0.1
            style += 0.1
        
        # Update progress bars
        self.speed_stat.value = min(speed, 1.0)
        self.style_stat.value = min(style, 1.0)
        self.value_stat.value = min(value, 1.0)
    
    def save_design(self):
        """Save the current design"""
        if self.price > self.budget:
            ui.notify('Cannot save: Over budget!', type='negative')
            return
        
        design = {
            'id': datetime.now().isoformat(),
            'name': self.current_design['name'],
            'design': self.current_design.copy(),
            'price': self.price,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        self.saved_designs.append(design)
        self.update_saved_designs_display()
        ui.notify(f'Saved "{design["name"]}" successfully!', type='positive')
    
    def update_saved_designs_display(self):
        """Update the saved designs display"""
        self.saved_designs_container.clear()
        
        if not self.saved_designs:
            with self.saved_designs_container: (ui.label('No saved designs yet. Create your first design!').classes('text-gray-500'))
            return
        
        for design in self.saved_designs:
            with self.saved_designs_container:
                with ui.card().classes('w-full p-4 mb-2'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label(design['name']).classes('font-bold text-lg')
                        ui.label(f"${design['price']:,}").classes('text-green-600 font-bold')
                    
                    with ui.row().classes('w-full justify-between items-center mt-2'):
                        ui.label(f"Date: {design['date']}").classes('text-sm text-gray-600')
                        with ui.row().classes('gap-2'):
                            ui.button('Load', on_click=lambda d=design: self.load_design(d)).props('flat')
                            ui.button('Delete', on_click=lambda d=design: self.delete_design(d)).props('flat', color='red')
    
    def load_design(self, design):
        """Load a saved design"""
        self.current_design = design['design'].copy()
        self.update_price()
        self.update_stats()
        ui.notify(f'Loaded "{design["name"]}"', type='positive')
    
    def delete_design(self, design):
        """Delete a saved design"""
        self.saved_designs.remove(design)
        self.update_saved_designs_display()
        ui.notify(f'Deleted "{design["name"]}"', type='info')
    
    def load_preset(self, preset):
        """Load a preset design"""
        self.current_design.update(preset)
        self.update_price()
        self.update_stats()
        ui.notify(f'Loaded preset "{preset["name"]}"', type='positive')
    
    def randomize_design(self):
        """Generate a random design"""
        self.current_design.update({
            'body_color': f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}',
            'roof_color': f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}',
            'wheel_color': f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}',
            'body_style': random.choice(list(self.body_styles.keys())),
            'wheel_style': random.choice(list(self.wheel_styles.keys())),
            'decal': random.choice(list(self.decals.keys())),
            'spoiler': random.choice(list(self.spoilers.keys())),
            'name': f'Random Design #{random.randint(1000, 9999)}'
        })
        self.update_price()
        self.update_stats()
        ui.notify('Generated random design!', type='positive')
    
    def reset_design(self):
        """Reset to default design"""
        self.current_design = {
            'body_color': '#FF4444',
            'roof_color': '#333333',
            'wheel_color': '#888888',
            'window_tint': '#4A90E2',
            'body_style': 'sports',
            'wheel_style': 'sport',
            'decal': 'none',
            'spoiler': 'none',
            'name': 'My Car Design'
        }
        self.update_price()
        self.update_stats()
        ui.notify('Design reset to default', type='info')
    
    def take_screenshot(self):
        """Simulate taking a screenshot"""
        ui.notify('📸 Screenshot saved!', type='positive')
    
    def load_from_file(self):
        """Load designs from file (simulated)"""
        ui.notify('File loading feature coming soon!', type='info')
    
    def export_designs(self):
        """Export designs to file (simulated)"""
        if not self.saved_designs:
            ui.notify('No designs to export!', type='warning')
            return
        
        # In a real app, this would save to a file
        export_data = json.dumps(self.saved_designs, indent=2)
        ui.notify(f'Exported {len(self.saved_designs)} designs!', type='positive')
    
    def adjust_color(self, hex_color, amount):
        """Adjust a hex color by a certain amount"""
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Adjust
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'

# Main Application
@ui.page('/')
def main():
    """Main page of the Car Design Game"""
    game = CarDesignGame()
    
    # Add some footer info
    with ui.footer().classes('bg-gray-800 text-white p-2'):
        ui.label('🏁 Car Design Studio - Create Your Dream Car!').classes('text-center w-full')
    
    return game

# Run the application
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='Car Design Studio',
        port=8080,
        reload=True,
        dark=None,
          viewport='width=device-width, initial-scale=1'
    )