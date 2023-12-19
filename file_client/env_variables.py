import os
from pathlib import Path

UPLOAD_PATH = \
    Path(
        os.getenv(
            "UPLOAD_PATH",
            str(
                    (
                        Path(__file__).parent.parent / "uploads"
                    ).absolute()),
        )
    )
