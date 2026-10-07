from pathlib import Path


def test_fixture_directory_exists() -> None:
    fixture_dir = Path(__file__).parent / "fixtures"
    assert fixture_dir.is_dir()
