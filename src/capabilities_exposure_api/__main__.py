#!/usr/bin/env python3

from connexion import FlaskApp
from pathlib import Path

module_path = Path(__file__).resolve().parent
specification_file_path = module_path / "./specification/openapi.yaml"


def main():
    app = FlaskApp(__name__)
    app.add_api(
        specification_file_path,
        arguments={"title": "Capabilities Exposure API Server"},
        validate_responses=True,
    )
    app.run(
        host="127.0.0.1",
        port=8080,
        # debug=True,
    )


if __name__ == "__main__":
    main()
