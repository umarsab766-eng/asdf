from nicegui import ui
import time


PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "price": 29.99},
    {"id": 2, "name": "Mechanical Keyboard", "category": "Electronics", "price": 89.99},
    {"id": 3, "name": "Coffee Mug", "category": "Kitchen", "price": 12.50},
    {"id": 4, "name": "Notebook", "category": "Stationery", "price": 5.99},
    {"id": 5, "name": "Desk Lamp", "category": "Furniture", "price": 45.00},
    {"id": 6, "name": "USB-C Cable", "category": "Electronics", "price": 9.99},
    {"id": 7, "name": "Water Bottle", "category": "Kitchen", "price": 18.75},
    {"id": 8, "name": "Pen Set", "category": "Stationery", "price": 15.30},
]


search_results = PRODUCTS.copy()
search_history = []
loading = False

def perform_search():
    global search_results, loading
    loading = True
    search_term = search_input.value.lower().strip()
    
  
    time.sleep(0.5)
    
    if not search_term:
        search_results = PRODUCTS.copy()
    else:
        search_results = [
            p for p in PRODUCTS 
            if search_term in p["name"].lower() 
            or search_term in p["category"].lower()
        ]
    
   
    if search_term and search_term not in search_history:
        search_history.append(search_term)
        history_refresh()
    
    loading = False
    results_refresh()

def results_refresh():
    results_container.clear()
    
    if loading:
        with results_container:
            ui.spinner('dots').classes('text-2xl')
            ui.label('Searching...').classes('text-gray-500')
        return
    
    if not search_results:
        with results_container:
            ui.icon('search_off').classes('text-4xl text-gray-400')
            ui.label('No results found').classes('text-gray-500')
        return
    
    with results_container:
        for product in search_results:
            with ui.card().classes('w-full p-4 mb-2'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label(product['name']).classes('text-lg font-semibold')
                    ui.label(f"${product['price']:.2f}").classes('text-green-600 font-bold')
                ui.label(product['category']).classes('text-gray-500 text-sm')

def history_refresh():
    history_container.clear()
    if search_history:
        with history_container:
            ui.label('Recent Searches:').classes('font-semibold mb-2')
            with ui.row().classes('gap-2'):
                for term in search_history[-5:]:  # Show last 5 searches
                    ui.button(term, on_click=lambda t=term: (
                        search_input.set_value(t),
                        perform_search()
                    )).props('flat dense').classes('text-sm')


with ui.header().classes('bg-blue-500 text-white'):
    ui.label('Product Search').classes('text-2xl font-bold')

with ui.column().classes('w-full max-w-3xl mx-auto p-4'):
   
    with ui.row().classes('w-full gap-2'):
        search_input = ui.input(
            placeholder='Search products...',
            on_change=lambda: perform_search()
        ).props('outlined clearable').classes('flex-grow')
        
        ui.button('Search', on_click=perform_search).props('color=primary')
    
 
    history_container = ui.column().classes('w-full mt-2')
    history_refresh()
    
    
    result_counter = ui.label().classes('text-gray-600 mt-4')
    
   
    results_container = ui.column().classes('w-full mt-2')
    results_refresh()


@ui.refreshable
def update_counter():
    result_counter.text = f"Showing {len(search_results)} of {len(PRODUCTS)} products"


def on_results_change():
    update_counter()
    results_refresh()


search_input.on('change', lambda: on_results_change())
search_input.on('keyup.enter', lambda: perform_search())


update_counter()

ui.run()