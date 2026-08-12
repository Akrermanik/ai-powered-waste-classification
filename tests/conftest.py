import io
import os
from pathlib import Path

import pytest
from PIL import Image

# Test environment defaults
os.environ.setdefault("WASIFY_AUTH_SECRET", "test-secret-key-for-pytest-only")
os.environ.setdefault("DATABASE_URL", "test_wasify.db")


@pytest.fixture(autouse=True)
def clean_test_db():
    db_path = Path("test_wasify.db")
    if db_path.exists():
        db_path.unlink()
    yield
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def sample_image() -> Image.Image:
    return Image.new("RGB", (64, 64), color=(120, 180, 90))


@pytest.fixture
def sample_image_bytes(sample_image: Image.Image) -> bytes:
    buffer = io.BytesIO()
    sample_image.save(buffer, format="PNG")
    return buffer.getvalue()
