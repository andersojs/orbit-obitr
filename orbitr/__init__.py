from __future__ import annotations

from pathlib import Path

from flask import Flask, redirect, send_from_directory

from .api import api_bp
from .catalog import load_catalog
from .storage import RsoStore


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(
        FRONTEND_PATH=Path(app.root_path).parent / "app",
        RSO_DATA_PATH=Path(app.instance_path) / "rso_store.json",
    )

    if test_config:
        app.config.update(test_config)

    _init_instance_path(app)

    store = RsoStore(Path(app.config["RSO_DATA_PATH"]))
    store.seed(load_catalog())
    app.config["RSO_STORE"] = store

    app.register_blueprint(api_bp)

    @app.route("/")
    def _root() -> str:
        return redirect("/app")

    @app.route("/app")
    def _frontend_index():
        return send_from_directory(app.config["FRONTEND_PATH"], "index.html")

    @app.route("/app/<path:asset_path>")
    def _frontend_assets(asset_path: str):
        return send_from_directory(app.config["FRONTEND_PATH"], asset_path)

    return app


def _init_instance_path(app: Flask) -> None:
    (Path(app.instance_path)).mkdir(parents=True, exist_ok=True)
