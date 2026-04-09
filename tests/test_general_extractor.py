"""Tests for mempalace.general_extractor."""

from mempalace.general_extractor import (
    ALL_MARKERS,
    NEGATIVE_WORDS,
    POSITIVE_WORDS,
    _extract_prose,
    _get_sentiment,
    _has_resolution,
    _is_code_line,
    _score_markers,
    _split_into_segments,
    extract_memories,
)


# ── extract_memories — empty / no markers ───────────────────────────────


def test_extract_memories_empty_text():
    result = extract_memories("")
    assert result == []


def test_extract_memories_no_markers():
    result = extract_memories("The quick brown fox jumped over the lazy dog.")
    assert result == []


def test_extract_memories_short_text_skipped():
    # Paragraphs shorter than 20 chars are skipped
    result = extract_memories("ok sure")
    assert result == []


# ── extract_memories — decision markers ─────────────────────────────────


def test_extract_memories_decision():
    text = (
        "We decided to go with PostgreSQL instead of MySQL "
        "because the performance was better for our use case. "
        "The trade-off was more complexity in setup."
    )
    result = extract_memories(text)
    assert len(result) >= 1
    assert any(m["memory_type"] == "decision" for m in result)


def test_extracts_chinese_decision_memory():
    text = (
        "我们决定改用新的剧情大纲格式，因为旧格式在长篇项目里很难回收伏笔。"
        "后续统一用卷目标、章节目标和回响目标三段式。"
    )

    memories = extract_memories(text, min_confidence=0.2)

    assert memories
    assert memories[0]["memory_type"] == "decision"


# ── extract_memories — preference markers ───────────────────────────────


def test_extract_memories_preference():
    text = (
        "I prefer using snake_case in Python code. "
        "Please always use type hints. "
        "Never use wildcard imports."
    )
    result = extract_memories(text)
    assert len(result) >= 1
    assert any(m["memory_type"] == "preference" for m in result)


# ── extract_memories — milestone markers ────────────────────────────────


def test_extract_memories_milestone():
    text = (
        "It finally works! After three days of debugging, "
        "I figured out the issue. The breakthrough was realizing "
        "the config file was cached. Got it working at 2am."
    )
    result = extract_memories(text)
    assert len(result) >= 1
    assert any(m["memory_type"] == "milestone" for m in result)


def test_extracts_chinese_resolved_problem_as_milestone():
    text = (
        "昨天一直报错，章节汇总脚本卡住了。今天终于跑通了，根因是文件编码不统一。"
        "现在已经修好了。"
    )

    memories = extract_memories(text, min_confidence=0.2)

    assert memories
    assert memories[0]["memory_type"] == "milestone"


# ── extract_memories — problem markers ──────────────────────────────────


def test_extract_memories_problem():
    text = (
        "There's a critical bug in the auth module. "
        "The error keeps crashing the server. "
        "The root cause was a missing null check. "
        "The problem is that tokens expire silently."
    )
    result = extract_memories(text)
    assert len(result) >= 1
    types = {m["memory_type"] for m in result}
    assert "problem" in types or "milestone" in types  # resolved problems become milestones


# ── extract_memories — emotional markers ────────────────────────────────


def test_extract_memories_emotional():
    text = (
        "I feel so proud of what we built together. "
        "I love working on this project, it makes me happy. "
        "I'm grateful for the team and the beautiful code we wrote."
    )
    result = extract_memories(text)
    assert len(result) >= 1
    assert any(m["memory_type"] == "emotional" for m in result)


def test_extracts_chinese_emotional_memory():
    text = "我其实有点害怕这本小说写崩，但也真的很喜欢这个主角，还是想把她写好。"

    memories = extract_memories(text, min_confidence=0.2)

    assert memories
    assert memories[0]["memory_type"] == "emotional"


# ── extract_memories — chunk_index ──────────────────────────────────────


def test_extract_memories_chunk_index_increments():
    text = (
        "We decided to use React because it fits our team.\n\n"
        "I prefer functional components always.\n\n"
        "It works! We finally shipped the v1.0 release."
    )
    result = extract_memories(text)
    if len(result) >= 2:
        indices = [m["chunk_index"] for m in result]
        assert indices == list(range(len(result)))


# ── _score_markers ──────────────────────────────────────────────────────


def test_score_markers_with_matches():
    score, keywords = _score_markers(
        "we decided to go with postgres because it is faster",
        ALL_MARKERS["decision"],
    )
    assert score > 0
    assert len(keywords) > 0


def test_score_markers_no_matches():
    score, keywords = _score_markers("nothing relevant here", ALL_MARKERS["decision"])
    assert score == 0.0


# ── _get_sentiment ──────────────────────────────────────────────────────


def test_get_sentiment_positive():
    assert _get_sentiment("I am so happy and proud of this breakthrough") == "positive"


def test_get_sentiment_negative():
    assert _get_sentiment("This bug caused a crash and total failure") == "negative"


def test_get_sentiment_neutral():
    assert _get_sentiment("The meeting is at three") == "neutral"


# ── _has_resolution ─────────────────────────────────────────────────────


def test_has_resolution_true():
    assert _has_resolution("I fixed the auth bug and it works now") is True


def test_has_resolution_false():
    assert _has_resolution("The server keeps crashing") is False


# ── _is_code_line ───────────────────────────────────────────────────────


def test_is_code_line_detects_code():
    assert _is_code_line("  import os") is True
    assert _is_code_line("  $ pip install flask") is True
    assert _is_code_line("  ```python") is True


def test_is_code_line_allows_prose():
    assert _is_code_line("This is a regular sentence about coding.") is False
    assert _is_code_line("") is False


# ── _extract_prose ──────────────────────────────────────────────────────


def test_extract_prose_strips_code_blocks():
    text = "Hello world\n```\nimport os\nprint('hi')\n```\nGoodbye"
    result = _extract_prose(text)
    assert "import os" not in result
    assert "Hello world" in result
    assert "Goodbye" in result


def test_extract_prose_returns_original_if_all_code():
    text = "import os\nfrom sys import argv"
    result = _extract_prose(text)
    # Falls back to original text if nothing left
    assert len(result) > 0


# ── _split_into_segments ───────────────────────────────────────────────


def test_split_into_segments_by_paragraph():
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    result = _split_into_segments(text)
    assert len(result) == 3


def test_split_into_segments_by_turns():
    lines = []
    for i in range(5):
        lines.append(f"Human: Question {i}")
        lines.append(f"Assistant: Answer {i}")
    text = "\n".join(lines)
    result = _split_into_segments(text)
    assert len(result) >= 3  # turn-based splitting should fire


def test_split_into_segments_single_block():
    # Many lines without double-newline produces chunked segments
    lines = [f"Line {i} of the document" for i in range(30)]
    text = "\n".join(lines)
    result = _split_into_segments(text)
    assert len(result) >= 1


# ── ALL_MARKERS constant ───────────────────────────────────────────────


def test_all_markers_has_five_types():
    assert set(ALL_MARKERS.keys()) == {
        "decision",
        "preference",
        "milestone",
        "problem",
        "emotional",
    }


# ── POSITIVE_WORDS / NEGATIVE_WORDS ────────────────────────────────────


def test_positive_words():
    assert "happy" in POSITIVE_WORDS
    assert "proud" in POSITIVE_WORDS


def test_negative_words():
    assert "bug" in NEGATIVE_WORDS
    assert "crash" in NEGATIVE_WORDS
