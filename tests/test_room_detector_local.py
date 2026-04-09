from pathlib import Path

from mempalace.room_detector_local import detect_rooms_from_folders


def test_detects_chinese_creative_rooms(tmp_path: Path):
    for dirname in ("人物", "世界观", "正文", "章节"):
        (tmp_path / dirname).mkdir()

    rooms = detect_rooms_from_folders(str(tmp_path))
    room_names = {room["name"] for room in rooms}

    assert "characters" in room_names
    assert "worldbuilding" in room_names
    assert "manuscript" in room_names
    assert "chapters" in room_names
    assert "general" in room_names


def test_detects_english_creative_rooms_without_regressing(tmp_path: Path):
    for dirname in ("outline", "plot", "novel"):
        (tmp_path / dirname).mkdir()

    rooms = detect_rooms_from_folders(str(tmp_path))
    room_names = {room["name"] for room in rooms}

    assert "outline" in room_names
    assert "plot" in room_names
    assert "story" in room_names
