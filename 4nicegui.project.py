from nicegui import ui
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime
import asyncio
import json



portfolio = {'cash': 10000, 'BTC': 0.5, 'ETH': 5}

price_data = {
    'BTC': [],
    'ETH': []
}

MAX_POINTS = 100



async def price_feed():
    btc = 50000
    eth = 3000

    while True:
        btc *= 1 + random.uniform(-0.005, 0.005)
        eth *= 1 + random.uniform(-0.005, 0.005)

        now = datetime.now().strftime('%H:%M:%S')

        price_data['BTC'].append((now, btc))
        price_data['ETH'].append((now, eth))

        price_data['BTC'] = price_data['BTC'][-MAX_POINTS:]
        price_data['ETH'] = price_data['ETH'][-MAX_POINTS:]

        update_price_chart_js()
        update_surface_chart_js()
        update_portfolio_chart_js()
        update_portfolio_display()

        await asyncio.sleep(1)



def update_price_chart_js():
    x_btc, y_btc = zip(*price_data['BTC'])
    x_eth, y_eth = zip(*price_data['ETH'])

    ui.run_javascript(f"""
    Plotly.react(
        document.getElementById('price_chart'),
        [
            {{ x: {json.dumps(x_btc)}, y: {json.dumps(y_btc)}, mode: 'lines', name: 'BTC', line: {{color: 'orange'}} }},
            {{ x: {json.dumps(x_eth)}, y: {json.dumps(y_eth)}, mode: 'lines', name: 'ETH', line: {{color: 'blue'}} }}
        ],
        {{
            title: 'Cryptocurrency Prices',
            xaxis: {{title: 'Time'}},
            yaxis: {{title: 'Price (USD)'}},
            height: 400
        }}
    );
    """)

def update_surface_chart_js():
    if len(price_data['BTC']) < 5:
        return

    z = [
        [p[1] for p in price_data['BTC']],
        [p[1] for p in price_data['ETH']]
    ]

    ui.run_javascript(f"""
    Plotly.react(
        document.getElementById('surface_chart'),
        [{{
            type: 'surface',
            z: {json.dumps(z)},
            colorscale: 'Viridis'
        }}],
        {{
            title: '3D Price Surface',
            scene: {{
                xaxis: {{title: 'Time'}},
                yaxis: {{title: 'Asset (0=BTC, 1=ETH)'}},
                zaxis: {{title: 'Price'}}
            }},
            height: 400
        }}
    );
    """)

def update_portfolio_chart_js():
    btc_price = price_data['BTC'][-1][1]
    eth_price = price_data['ETH'][-1][1]

    values = [
        portfolio['cash'],
        portfolio['BTC'] * btc_price,
        portfolio['ETH'] * eth_price
    ]

    ui.run_javascript(f"""
    Plotly.react(
        document.getElementById('portfolio_chart'),
        [{{
            type: 'scatter3d',
            mode: 'markers',
            x: [0, 1, 0],
            y: [0, 0, 1],
            z: [0, 0, 0],
            marker: {{
                size: {json.dumps([v / sum(values) * 50 for v in values])},
                color: ['green', 'orange', 'blue'],
                opacity: 0.8
            }},
            text: ['Cash', 'BTC', 'ETH'],
            hoverinfo: 'text'
        }}],
        {{
            title: '3D Portfolio Allocation',
            scene: {{
                xaxis: {{title: 'Cash'}},
                yaxis: {{title: 'BTC'}},
                zaxis: {{title: 'ETH'}}
            }},
            height: 400
        }}
    );
    """)


portfolio_display = None

def update_portfolio_display():
    btc_price = price_data['BTC'][-1][1]
    eth_price = price_data['ETH'][-1][1]

    total = (
        portfolio['cash'] +
        portfolio['BTC'] * btc_price +
        portfolio['ETH'] * eth_price
    )

    portfolio_display.clear()
    with portfolio_display:
        ui.label(f"Cash: ${portfolio['cash']:.2f}")
        ui.label(f"BTC: {portfolio['BTC']:.4f} (${portfolio['BTC'] * btc_price:.2f})")
        ui.label(f"ETH: {portfolio['ETH']:.4f} (${portfolio['ETH'] * eth_price:.2f})")
        ui.label(f"Total Value: ${total:.2f}")

@ui.page('/')
def main():
    global portfolio_display

    with ui.header().classes('bg-blue-500 text-white'):
        ui.label('Crypto Trading Platform (JS Optimized)').classes('text-h6 q-pa-md')

    with ui.row().classes('w-full'):
        with ui.column().classes('w-2/3 p-4'):
            ui.html('<div id="price_chart"></div>')
            ui.html('<div id="surface_chart" class="mt-4"></div>')

        with ui.column().classes('w-1/3 p-4'):
            with ui.card():
                ui.label('Portfolio')
                portfolio_display = ui.column()

            ui.html('<div id="portfolio_chart" class="mt-4"></div>')

    asyncio.create_task(price_feed())



ui.run(title='Crypto Trading Platform (JS)', port=8080, reload=False)