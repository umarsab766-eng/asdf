from nicegui import ui, app
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class TileType(Enum):
    EMPTY = "empty"
    WALL = "wall"
    DOOR = "door"
    WINDOW = "window"
    FLOOR = "floor"
    ROOF = "roof"
    FURNITURE = "furniture"

class RoomType(Enum):
    LIVING_ROOM = "Living Room"
    BEDROOM = "Bedroom"
    KITCHEN = "Kitchen"
    BATHROOM = "Bathroom"
    GARAGE = "Garage"

class FurnitureType(Enum):
    SOFA = "sofa"
    BED = "bed"
    TABLE = "table"
    CHAIR = "chair"
    TV = "tv"
    FRIDGE = "fridge"
    TOILET = "toilet"
    SINK = "sink"

@dataclass
class Tile:
    type: TileType
    room_type: Optional[RoomType] = None
    furniture_type: Optional[FurnitureType] = None
    color: str = "#E0E0E0"
    rotation: int = 0

class HouseMakerGame:
    def __init__(self):
        self.grid_size = 20
        self.tile_size = 30
        self.grid: List[List[Tile]] = [[Tile(TileType.EMPTY) for _ in range(self.grid_size)] 
                                       for _ in range(self.grid_size)]
        self.selected_tool = TileType.WALL
        self.selected_room = RoomType.LIVING_ROOM
        self.selected_furniture = FurnitureType.SOFA
        self.selected_color = "#8B4513"
        self.is_placing = False
        self.saved_designs = []
        self.current_design_name = "My House"
        
        self.color_options = {
            "Wood": "#8B4513",
            "White": "#FFFFFF",
            "Gray": "#808080",
            "Blue": "#4169E1",
            "Red": "#DC143C",
            "Green": "#228B22",
            "Yellow": "#FFD700",
            "Purple": "#9370DB",
            "Black": "#2C2C2C"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        with ui.column().classes('w-full h-screen bg-gradient-to-br from-blue-50 to-purple-50'):
            
            with ui.row().classes('w-full p-4 bg-white shadow-md justify-between items-center'):
                ui.label('🏠 House Maker Game').classes('text-3xl font-bold text-purple-600')
                with ui.row().classes('gap-2'):
                    ui.button('📁 Load', on_click=self.load_design).classes('bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600')
                    ui.button('💾 Save', on_click=self.save_design).classes('bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600')
                    ui.button('🗑️ Clear', on_click=self.clear_grid).classes('bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600')
                    ui.button('🎲 Random', on_click=self.random_house).classes('bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600')
            
            with ui.row().classes('flex-1 gap-4 p-4'):
                # Left Panel - Tools
                with ui.card().classes('w-64 h-full bg-white shadow-lg rounded-xl p-4 overflow-y-auto'):
                    ui.label('🛠️ Building Tools').classes('text-xl font-bold mb-4 text-gray-700')
                    
                    # Tile Type Selection
                    ui.label('Select Tile Type:').classes('text-sm font-semibold text-gray-600 mb-2')
                    with ui.column().classes('gap-2 mb-4'):
                        for tile_type in TileType:
                            if tile_type != TileType.EMPTY:
                                ui.button(self.get_tile_emoji(tile_type) + f' {tile_type.value.title()}',
                                         on_click=lambda t=tile_type: self.select_tool(t),
                                         color='primary' if self.selected_tool == tile_type else 'secondary').classes('w-full justify-start')
                    
                    # Room Types
                    ui.label('Room Types:').classes('text-sm font-semibold text-gray-600 mb-2')
                    with ui.column().classes('gap-2 mb-4'):
                        for room in RoomType:
                            ui.button(self.get_room_emoji(room) + f' {room.value}',
                                     on_click=lambda r=room: self.select_room(r),
                                     color='primary' if self.selected_room == room else 'secondary').classes('w-full justify-start')
                    
                    # Furniture Types
                    ui.label('Furniture:').classes('text-sm font-semibold text-gray-600 mb-2')
                    with ui.column().classes('gap-2 mb-4'):
                        for furniture in FurnitureType:
                            ui.button(self.get_furniture_emoji(furniture) + f' {furniture.value.title()}',
                                     on_click=lambda f=furniture: self.select_furniture(f),
                                     color='primary' if self.selected_furniture == furniture else 'secondary').classes('w-full justify-start')
                    
                    # Color Selection
                    ui.label('Colors:').classes('text-sm font-semibold text-gray-600 mb-2')
                    with ui.grid(columns=3).classes('gap-2'):
                        for name, color in self.color_options.items():
                            ui.button('', on_click=lambda c=color: self.select_color(c)).classes(f'w-12 h-12 rounded-lg shadow-md hover:scale-110 transition-transform').style(f'background-color: {color}')
                
                # Center - Grid
                with ui.card().classes('flex-1 bg-white shadow-lg rounded-xl p-4 overflow-auto'):
                    with ui.column().classes('items-center'):
                        ui.label(f'🏡 {self.current_design_name}').classes('text-xl font-bold mb-4 text-gray-700')
                        self.grid_container = ui.column().classes('inline-block border-2 border-gray-300')
                        with self.grid_container:
                            self.grid_elements = []
                            for i in range(self.grid_size):
                                with ui.row().classes('gap-0'):
                                    row_elements = []
                                    for j in range(self.grid_size):
                                        tile_elem = ui.button('', on_click=lambda e, x=i, y=j: self.place_tile(x, y)).classes(
                                            f'border border-gray-200 hover:border-blue-400 transition-colors'
                                        ).style(f'width: {self.tile_size}px; height: {self.tile_size}px;')
                                        tile_elem.on('contextmenu', lambda e, x=i, y=j: self.remove_tile(x, y))
                                        row_elements.append(tile_elem)
                                    self.grid_elements.append(row_elements)
                        
                        # Instructions
                        ui.label('Left Click: Place | Right Click: Remove').classes('text-sm text-gray-500 mt-4')
                
                # Right Panel - Info & Stats
                with ui.card().classes('w-64 h-full bg-white shadow-lg rounded-xl p-4 overflow-y-auto'):
                    ui.label('📊 House Stats').classes('text-xl font-bold mb-4 text-gray-700')
                    
                    self.stats_labels = {}
                    with ui.column().classes('gap-2'):
                        self.stats_labels['walls'] = ui.label('Walls: 0').classes('text-gray-600')
                        self.stats_labels['doors'] = ui.label('Doors: 0').classes('text-gray-600')
                        self.stats_labels['windows'] = ui.label('Windows: 0').classes('text-gray-600')
                        self.stats_labels['rooms'] = ui.label('Rooms: 0').classes('text-gray-600')
                        self.stats_labels['furniture'] = ui.label('Furniture: 0').classes('text-gray-600')
                    
                    ui.separator().classes('my-4')
                    
                    ui.label('🎨 Current Selection').classes('text-lg font-bold mb-2 text-gray-700')
                    self.selection_label = ui.label('Wall').classes('text-gray-600')
                    self.color_preview = ui.element('div').classes('w-full h-12 rounded-lg shadow-md mt-2').style(f'background-color: {self.selected_color}')
                    
                    ui.separator().classes('my-4')
                    
                    # Templates
                    ui.label('📋 Quick Templates').classes('text-lg font-bold mb-2 text-gray-700')
                    ui.button('Small House', on_click=lambda: self.load_template('small')).classes('w-full bg-indigo-500 text-white hover:bg-indigo-600')
                    ui.button('Mansion', on_click=lambda: self.load_template('mansion')).classes('w-full bg-indigo-500 text-white hover:bg-indigo-600')
                    ui.button('Apartment', on_click=lambda: self.load_template('apartment')).classes('w-full bg-indigo-500 text-white hover:bg-indigo-600')
        
        self.update_grid_display()
        self.update_stats()
    
    def get_tile_emoji(self, tile_type: TileType) -> str:
        emojis = {
            TileType.WALL: "🧱",
            TileType.DOOR: "🚪",
            TileType.WINDOW: "🪟",
            TileType.FLOOR: "🟫",
            TileType.ROOF: "🔺",
            TileType.FURNITURE: "🪑"
        }
        return emojis.get(tile_type, "⬜")
    
    def get_room_emoji(self, room: RoomType) -> str:
        emojis = {
            RoomType.LIVING_ROOM: "🛋️",
            RoomType.BEDROOM: "🛏️",
            RoomType.KITCHEN: "🍳",
            RoomType.BATHROOM: "🚿",
            RoomType.GARAGE: "🚗"
        }
        return emojis.get(room, "🏠")
    
    def get_furniture_emoji(self, furniture: FurnitureType) -> str:
        emojis = {
            FurnitureType.SOFA: "🛋️",
            FurnitureType.BED: "🛏️",
            FurnitureType.TABLE: "🪑",
            FurnitureType.CHAIR: "💺",
            FurnitureType.TV: "📺",
            FurnitureType.FRIDGE: "🧊",
            FurnitureType.TOILET: "🚽",
            FurnitureType.SINK: "🚰"
        }
        return emojis.get(furniture, "📦")
    
    def select_tool(self, tool: TileType):
        self.selected_tool = tool
        self.selection_label.text = f"Tool: {tool.value.title()}"
        self.update_grid_display()
    
    def select_room(self, room: RoomType):
        self.selected_room = room
        self.selection_label.text = f"Room: {room.value}"
    
    def select_furniture(self, furniture: FurnitureType):
        self.selected_furniture = furniture
        self.selected_tool = TileType.FURNITURE
        self.selection_label.text = f"Furniture: {furniture.value.title()}"
        self.update_grid_display()
    
    def select_color(self, color: str):
        self.selected_color = color
        self.color_preview.style(f'background-color: {color}')
    
    def place_tile(self, x: int, y: int):
        if self.selected_tool == TileType.FURNITURE:
            self.grid[x][y] = Tile(TileType.FURNITURE, furniture_type=self.selected_furniture, color=self.selected_color)
        elif self.selected_tool == TileType.FLOOR:
            self.grid[x][y] = Tile(TileType.FLOOR, room_type=self.selected_room, color=self.selected_color)
        else:
            self.grid[x][y] = Tile(self.selected_tool, color=self.selected_color)
        
        self.update_grid_display()
        self.update_stats()
    
    def remove_tile(self, x: int, y: int):
        self.grid[x][y] = Tile(TileType.EMPTY)
        self.update_grid_display()
        self.update_stats()
    
    def update_grid_display(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                tile = self.grid[i][j]
                elem = self.grid_elements[i][j]
                
                if tile.type == TileType.EMPTY:
                    elem.text = ''
                    elem.style(f'background-color: #F5F5F5; width: {self.tile_size}px; height: {self.tile_size}px;')
                elif tile.type == TileType.FURNITURE:
                    elem.text = self.get_furniture_emoji(tile.furniture_type)
                    elem.style(f'background-color: {tile.color}; width: {self.tile_size}px; height: {self.tile_size}px;')
                elif tile.type == TileType.FLOOR:
                    elem.text = self.get_room_emoji(tile.room_type) if tile.room_type else ''
                    elem.style(f'background-color: {tile.color}; width: {self.tile_size}px; height: {self.tile_size}px;')
                else:
                    elem.text = self.get_tile_emoji(tile.type)
                    elem.style(f'background-color: {tile.color}; width: {self.tile_size}px; height: {self.tile_size}px;')
    
    def update_stats(self):
        stats = {
            'walls': 0,
            'doors': 0,
            'windows': 0,
            'rooms': set(),
            'furniture': 0
        }
        
        for row in self.grid:
            for tile in row:
                if tile.type == TileType.WALL:
                    stats['walls'] += 1
                elif tile.type == TileType.DOOR:
                    stats['doors'] += 1
                elif tile.type == TileType.WINDOW:
                    stats['windows'] += 1
                elif tile.type == TileType.FURNITURE:
                    stats['furniture'] += 1
                elif tile.type == TileType.FLOOR and tile.room_type:
                    stats['rooms'].add(tile.room_type.value)
        
        self.stats_labels['walls'].text = f"Walls: {stats['walls']}"
        self.stats_labels['doors'].text = f"Doors: {stats['doors']}"
        self.stats_labels['windows'].text = f"Windows: {stats['windows']}"
        self.stats_labels['rooms'].text = f"Rooms: {len(stats['rooms'])}"
        self.stats_labels['furniture'].text = f"Furniture: {stats['furniture']}"
    
    def clear_grid(self):
        self.grid = [[Tile(TileType.EMPTY) for _ in range(self.grid_size)] 
                    for _ in range(self.grid_size)]
        self.update_grid_display()
        self.update_stats()
        ui.notify('Grid cleared!', type='info')
    
    def random_house(self):
        self.clear_grid()
        
        # Create random house structure
        import random
        
        # Build outer walls
        for i in range(5, 15):
            self.grid[5][i] = Tile(TileType.WALL, color="#8B4513")
            self.grid[14][i] = Tile(TileType.WALL, color="#8B4513")
        for i in range(5, 15):
            self.grid[i][5] = Tile(TileType.WALL, color="#8B4513")
            self.grid[i][14] = Tile(TileType.WALL, color="#8B4513")
        
        # Add doors and windows
        self.grid[5][10] = Tile(TileType.DOOR, color="#654321")
        self.grid[10][5] = Tile(TileType.WINDOW, color="#87CEEB")
        self.grid[10][14] = Tile(TileType.WINDOW, color="#87CEEB")
        
        # Add floors
        for i in range(6, 14):
            for j in range(6, 14):
                if random.random() > 0.3:
                    room_type = random.choice(list(RoomType))
                    self.grid[i][j] = Tile(TileType.FLOOR, room_type=room_type, color="#DEB887")
        
        # Add random furniture
        for _ in range(10):
            x = random.randint(6, 13)
            y = random.randint(6, 13)
            furniture = random.choice(list(FurnitureType))
            self.grid[x][y] = Tile(TileType.FURNITURE, furniture_type=furniture, color="#8B4513")
        
        self.update_grid_display()
        self.update_stats()
        ui.notify('Random house generated!', type='success')
    
    def load_template(self, template_type: str):
        self.clear_grid()
        
        if template_type == 'small':
            # Small house template
            for i in range(7, 13):
                self.grid[7][i] = Tile(TileType.WALL, color="#8B4513")
                self.grid[12][i] = Tile(TileType.WALL, color="#8B4513")
            for i in range(7, 13):
                self.grid[i][7] = Tile(TileType.WALL, color="#8B4513")
                self.grid[i][12] = Tile(TileType.WALL, color="#8B4513")
            
            self.grid[7][10] = Tile(TileType.DOOR, color="#654321")
            self.grid[9][7] = Tile(TileType.WINDOW, color="#87CEEB")
            
            for i in range(8, 12):
                for j in range(8, 12):
                    self.grid[i][j] = Tile(TileType.FLOOR, room_type=RoomType.LIVING_ROOM, color="#DEB887")
            
            self.grid[9][9] = Tile(TileType.FURNITURE, furniture_type=FurnitureType.SOFA, color="#4682B4")
            self.grid[10][10] = Tile(TileType.FURNITURE, furniture_type=FurnitureType.TV, color="#2F4F4F")
            
        elif template_type == 'mansion':
           
            for i in range(3, 17):
                self.grid[3][i] = Tile(TileType.WALL, color="#8B4513")
                self.grid[16][i] = Tile(TileType.WALL, color="#8B4513")
            for i in range(3, 17):
                self.grid[i][3] = Tile(TileType.WALL, color="#8B4513")
                self.grid[i][16] = Tile(TileType.WALL, color="#8B4513")
            
            self.grid[3][10] = Tile(TileType.DOOR, color="#654321")
            self.grid[8][3] = Tile(TileType.WINDOW, color="#87CEEB")
            self.grid[8][16] = Tile(TileType.WINDOW, color="#87CEEB")
            self.grid[12][3] = Tile(TileType.WINDOW, color="#87CEEB")
            self.grid[12][16] = Tile(TileType.WINDOW, color="#87CEEB")
            
            
            for i in range(4, 10):
                for j in range(4, 10):
                    self.grid[i][j] = Tile(TileType.FLOOR, room_type=RoomType.LIVING_ROOM, color="#DEB887")
            
            for i in range(4, 10):
                for j in range(10, 16):
                    self.grid[i][j] = Tile(TileType.FLOOR, room_type=RoomType.KITCHEN, color="#F0E68C")
            
            for i in range(10, 16):
                for j in range(4, 10):
                    self.grid[i][j] = Tile(TileType.FLOOR, room_type=RoomType.BEDROOM, color="#E6E6FA")
            
            for i in range(10, 16):
                for j in range(10, 16):
                    self.grid[i][j] = Tile(TileType.FLOOR, room_type=RoomType.BATHROOM, color="#B0E0E6")
            
        elif template_type == 'apartment':
            
            for i in range(5, 15):
                self.grid[5][i] = Tile(TileType.WALL, color="#696969")
                self.grid[14][i] = Tile(TileType.WALL, color="#696969")
            for i in range(5, 15):
                self.grid[i][5] = Tile(TileType.WALL, color="#696969")
                self.grid[i][14] = Tile(TileType.WALL, color="#696969")
            
            self.grid[5][10] = Tile(TileType.DOOR, color="#4A4A4A")
            self.grid[9][5] = Tile(TileType.WINDOW, color="#87CEEB")
            self.grid[10][14] = Tile(TileType.WINDOW, color="#87CEEB")
            
            for i in range(6, 14):
                for j in range(6, 14):
                    if i < 10:
                        self.grid[i][j] = Tile(TileType.FLOOR, room_type=RoomType.LIVING_ROOM, color="#D3D3D3")
                    else:
                        self.grid[i][j] = Tile(TileType.FLOOR, room_type=RoomType.BEDROOM, color="#DDA0DD")
            
            self.grid[7][8] = Tile(TileType.FURNITURE, furniture_type=FurnitureType.SOFA, color="#708090")
            self.grid[11][11] = Tile(TileType.FURNITURE, furniture_type=FurnitureType.BED, color="#8B7355")
        
        self.update_grid_display()
        self.update_stats()
        ui.notify(f'{template_type.title()} template loaded!', type='success')
    
    def save_design(self):
        design_data = {
            'name': self.current_design_name,
            'grid': [[{
                'type': tile.type.value,
                'room_type': tile.room_type.value if tile.room_type else None,
                'furniture_type': tile.furniture_type.value if tile.furniture_type else None,
                'color': tile.color
            } for tile in row] for row in self.grid]
        }
        
        self.saved_designs.append(design_data)
        ui.notify(f'Design "{self.current_design_name}" saved!', type='success')
    
    def load_design(self):
        if not self.saved_designs:
            ui.notify('No saved designs available!', type='warning')
            return
        
        design = self.saved_designs[-1] 
        self.current_design_name = design['name']
        
        for i, row in enumerate(design['grid']):
            for j, tile_data in enumerate(row):
                self.grid[i][j] = Tile(
                    TileType(tile_data['type']),
                    RoomType(tile_data['room_type']) if tile_data['room_type'] else None,
                    FurnitureType(tile_data['furniture_type']) if tile_data['furniture_type'] else None,
                    tile_data['color']
                )
        
        self.update_grid_display()
        self.update_stats()
        ui.notify(f'Design "{self.current_design_name}" loaded!', type='success')


@ui.page('/')
def main():
    game = HouseMakerGame()

if __name__ in {'__main__', '__mp_main__'}:

     ui.run(title='House Maker Game', port=8080, dark=False, reload=False)
