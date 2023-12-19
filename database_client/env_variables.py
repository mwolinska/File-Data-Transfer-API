import os
from pathlib import Path

DATABASE_PATH = \
    os.getenv(
        "DATABASE_PATH",
        str((Path(__file__).parent.parent / "image_database.json").absolute()),
    )
