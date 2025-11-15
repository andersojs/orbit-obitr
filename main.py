from __future__ import annotations

from orbitr import create_app


def main():
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
