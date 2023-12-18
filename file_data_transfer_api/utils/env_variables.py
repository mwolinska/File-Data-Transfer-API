import os
from dataclasses import dataclass, asdict
from pathlib import Path

UPLOAD_PATH = \
    os.getenv(
        "UPLOAD_PATH",
        str(Path(__file__).parent.parent.parent / "uploads"),
    )

DATABASE_PATH = \
    os.getenv(
        "UPLOAD_PATH",
        str(Path(__file__).parent.parent.parent / "image_database.json"),
    )
