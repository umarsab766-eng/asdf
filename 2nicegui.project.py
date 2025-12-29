from nicegui import ui
import time
import random

class Laptop3DGame:
    def __init__(self):
        self.username = ""
        self.score = 0
        self.laptop_rotation_x = 0
        self.laptop_rotation_y = 0
        self.is_spinning = False
        self.game_active = False
        self.particles = []
        
    def create_login_screen(self):
        with ui.card().classes('w-96 h-96 bg-gradient-to-br from-purple-900 to-blue-900 rounded-3xl shadow-2xl'):
            with ui.column().classes('w-full h-full items-center justify-center gap-6 p-8'):
                # 3D Title
                ui.label('3D LAPTOP GAME').classes(
                    'text-4xl font-bold text-white mb-4 transform transition-all duration-500 hover:scale-110'
                    ' drop-shadow-[0_0_20px_rgba(255,255,255,0.8)]'
                )
                
                # 3D Username Input
                with ui.card().classes('w-full p-4 bg-white/10 backdrop-blur-md rounded-xl border border-white/20'):
                    ui.label('Username').classes('text-white text-sm mb-2')
                    self.username_input = ui.input(
                        placeholder='Enter your username'
                    ).classes(
                        'w-full bg-white/20 text-white placeholder-white/60 rounded-lg px-4 py-2 '
                        'border border-white/30 focus:border-white/60 focus:outline-none '
                        'transform transition-all duration-300 hover:scale-105'
                    ).props('dark')
                
                # 3D Password Input
                with ui.card().classes('w-full p-4 bg-white/10 backdrop-blur-md rounded-xl border border-white/20'):
                    ui.label('Password').classes('text-white text-sm mb-2')
                    self.password_input = ui.input(
                        placeholder='Enter password',
                        password=True
                    ).classes(
                        'w-full bg-white/20 text-white placeholder-white/60 rounded-lg px-4 py-2 '
                        'border border-white/30 focus:border-white/60 focus:outline-none '
                        'transform transition-all duration-300 hover:scale-105'
                    ).props('dark')
                
                # 3D Login Button
                ui.button(
                    'LOGIN',
                    on_click=self.login
                ).classes(
                    'w-full mt-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-bold py-3 px-6 '
                    'rounded-xl transform transition-all duration-300 hover:scale-105 hover:shadow-lg '
                    'hover:shadow-cyan-500/50 active:scale-95'
                )
                 
                # Demo credentials hint
                ui.label('Demo: user / password').classes('text-white/60 text-xs mt-2')

    def create_game_screen(self):
        with ui.card().classes('w-full max-w-6xl h-screen bg-gradient-to-br from-gray-900 to-black rounded-none shadow-2xl'):
            with ui.column().classes('w-full h-full p-6 gap-4'):
                # Header with user info and logout
                with ui.row().classes('w-full justify-between items-center'):
                    with ui.row().classes('items-center gap-4'):
                        ui.label(f'Welcome, {self.username}!').classes(
                            'text-2xl font-bold text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]'
                        )
                        ui.label(f'Score: {self.score}').classes(
                            'text-xl text-cyan-400 font-mono'
                        )
                    
                    ui.button(
                        'LOGOUT',
                        on_click=self.logout
                    ).classes(
                        'bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-lg '
                        'transform transition-all duration-300 hover:scale-105'
                    )
                
                # 3D Laptop Game Area
                with ui.card().classes('flex-1 bg-black/50 backdrop-blur-sm rounded-2xl border border-cyan-500/30'):
                    with ui.column().classes('w-full h-full items-center justify-center gap-6'):
                        # 3D Laptop Container
                        with ui.card().classes('relative w-96 h-64 perspective-1000'):
                            self.laptop_3d = ui.card().classes(
                                'w-full h-full relative transform-style-3d transition-transform duration-1000'
                            ).style(f'transform: rotateX({self.laptop_rotation_x}deg) rotateY({self.laptop_rotation_y}deg)')
                            
                            with self.laptop_3d:
                                # Laptop Screen
                                ui.card().classes(
                                    'absolute w-80 h-48 bg-gradient-to-b from-gray-800 to-gray-900 rounded-lg '
                                    'border-2 border-gray-600 shadow-2xl top-0 left-8'
                                ).style('transform: translateZ(20px)')
                                
                                # Screen Content
                                with ui.card().classes(
                                    'absolute w-72 h-40 bg-black rounded m-2 overflow-hidden'
                                ).style('transform: translateZ(21px)'):
                                    self.screen_content = ui.label('READY TO PLAY').classes(
                                        'w-full h-full flex items-center justify-center text-cyan-400 '
                                        'text-2xl font-mono font-bold'
                                    )
                                
                                # Laptop Base
                                ui.card().classes(
                                    'absolute w-96 h-16 bg-gradient-to-b from-gray-700 to-gray-800 rounded-b-lg '
                                    'border-t-2 border-gray-600 shadow-2xl bottom-0'
                                ).style('transform: rotateX(-90deg) translateZ(8px)')
                                
                                # Keyboard
                                ui.card().classes(
                                    'absolute w-88 h-12 bg-gray-900 rounded m-2 grid grid-cols-10 gap-1 p-1'
                                ).style('transform: translateZ(9px)')
                        
                        # Control Buttons
                        with ui.row().classes('gap-4'):
                            ui.button(
                                'SPIN LAPTOP',
                                on_click=self.spin_laptop
                            ).classes(
                                'bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-3 px-6 '
                                'rounded-xl transform transition-all duration-300 hover:scale-105 '
                                'hover:shadow-lg hover:shadow-purple-500/50'
                            )
                            
                            ui.button(
                                'PLAY GAME',
                                on_click=self.start_game
                            ).classes(
                                'bg-gradient-to-r from-green-600 to-teal-600 text-white font-bold py-3 px-6 '
                                'rounded-xl transform transition-all duration-300 hover:scale-105 '
                                'hover:shadow-lg hover:shadow-green-500/50'
                            )
                        
                        # Instructions
                        ui.label('Click and drag to rotate the laptop manually').classes(
                            'text-white/60 text-sm'
                        )

    def login(self):
        username = self.username_input.value
        password = self.password_input.value
        
        # Simple validation (demo purposes)
        if username and password:
            self.username = username
            ui.notify(f'Welcome, {username}!', color='positive')
            time.sleep(0.5)
            ui.navigate.to('/game')
        else:
            ui.notify('Please enter username and password', color='negative')

    def logout(self):
        self.username = ""
        self.score = 0
        self.game_active = False
        ui.notify('Logged out successfully', color='info')
        ui.navigate.to('/')

    def spin_laptop(self):
        if not self.is_spinning:
            self.is_spinning = True
            self.laptop_rotation_x = random.randint(-180, 180)
            self.laptop_rotation_y = random.randint(-180, 180)
            self.laptop_3d.style(f'transform: rotateX({self.laptop_rotation_x}deg) rotateY({self.laptop_rotation_y}deg)')
            
            # Add score for spinning
            self.score += 10
            ui.notify('+10 points!', color='positive')
            
            # Reset spinning state
            ui.timer(1.0, lambda: setattr(self, 'is_spinning', False))

    def start_game(self):
        if not self.game_active:
            self.game_active = True
            self.screen_content.classes('remove:text-cyan-400 add:text-green-400')
            self.screen_content.text = 'GAME ACTIVE!'
            
            # Simple game: random score generation
            def update_game():
                if self.game_active:
                    points = random.randint(1, 5)
                    self.score += points
                    self.screen_content.text = f'+{points} POINTS!'
                    ui.timer(1.0, update_game)
            
            update_game()
            
            # Stop game after 10 seconds
            ui.timer(10.0, self.stop_game)

    def stop_game(self):
        self.game_active = False
        self.screen_content.classes('remove:text-green-400 add:text-yellow-400')
        self.screen_content.text = f'FINAL SCORE: {self.score}'
        ui.notify(f'Game Over! Final Score: {self.score}', color='warning')

    def setup_routes(self):
        @ui.page('/')
        def login_page():
            self.create_login_screen()
            
            # Add CSS for 3D effects
            ui.add_head_html('''
                <style>
                    .perspective-1000 {
                        perspective: 1000px;
                    }
                    .transform-style-3d {
                        transform-style: preserve-3d;
                    }
                    body {
                        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                        min-height: 100vh;
                    }
                </style>
            ''')
        
        @ui.page('/game')
        def game_page():
            if not self.username:
                ui.navigate.to('/')
                return
            
            self.create_game_screen()
            
            # Add CSS for 3D effects and animations
            ui.add_head_html('''
                <style>
                    .perspective-1000 {
                        perspective: 1000px;
                    }
                    .transform-style-3d {
                        transform-style: preserve-3d;
                    }
                    body {
                        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
                        min-height: 100vh;
                        overflow: hidden;
                    }
                    .glow {
                        animation: glow 2s ease-in-out infinite alternate;
                    }
                    @keyframes glow {
                        from { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; }
                        to { text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff; }
                    }
                </style>
            ''')
            
            # Mouse drag functionality for laptop rotation
            def on_mouse_down(e):
                self.drag_start_x = e.args['clientX']
                self.drag_start_y = e.args['clientY']
                self.start_rotation_x = self.laptop_rotation_x
                self.start_rotation_y = self.laptop_rotation_y
                
                def on_mouse_move(e):
                    if hasattr(self, 'drag_start_x'):
                        dx = e.args['clientX'] - self.drag_start_x
                        dy = e.args['clientY'] - self.drag_start_y
                        self.laptop_rotation_y = self.start_rotation_y + dx * 0.5
                        self.laptop_rotation_x = self.start_rotation_x - dy * 0.5
                        self.laptop_3d.style(f'transform: rotateX({self.laptop_rotation_x}deg) rotateY({self.laptop_rotation_y}deg)')
                
                def on_mouse_up():
                    if hasattr(self, 'drag_start_x'):
                        del self.drag_start_x
                        del self.drag_start_y
                
                self.laptop_3d.on('mousemove', on_mouse_move)
                self.laptop_3d.on('mouseup', on_mouse_up)
                self.laptop_3d.on('mouseleave', on_mouse_up)
            
            self.laptop_3d.on('mousedown', on_mouse_down)


game = Laptop3DGame()
game.setup_routes()

ui.run(title='3D Laptop Game', port=8000)