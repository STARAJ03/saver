# Copyright (c) 2025 devgagan : https://github.com/devgaganin.
# Licensed under the GNU General Public License v3.0.
# See LICENSE file in the repository root for full license text.

import asyncio
import importlib
import os
import sys
import threading
from flask import Flask
from shared_client import start_client

# --- Flask app for health checks ---
app = Flask(__name__)

@app.route("/health")
def health():
    return "OK", 200

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# --- Plugin loader ---
async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [
        f[:-3] for f in os.listdir(plugin_dir)
        if f.endswith(".py") and f != "__init__.py"
    ]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        func_name = f"run_{plugin}_plugin"
        if hasattr(module, func_name):
            print(f"Running {plugin} plugin...")
            await getattr(module, func_name)()

# --- Async main loop ---
async def main():
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)

# --- Entry point ---
if __name__ == "__main__":
    print("Starting clients and health server...")

    # Start Flask in a background thread
    threading.Thread(target=run_flask, daemon=True).start()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
