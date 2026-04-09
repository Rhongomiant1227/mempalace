from mempalace.general_extractor import extract_memories


def test_extracts_chinese_decision_memory():
    text = (
        "我们决定改用新的剧情大纲格式，因为旧格式在长篇项目里很难回收伏笔。"
        "后续统一用卷目标、章节目标和回响目标三段式。"
    )

    memories = extract_memories(text, min_confidence=0.2)

    assert memories
    assert memories[0]["memory_type"] == "decision"


def test_extracts_chinese_resolved_problem_as_milestone():
    text = (
        "昨天一直报错，章节汇总脚本卡住了。今天终于跑通了，根因是文件编码不统一，"
        "现在已经修好了。"
    )

    memories = extract_memories(text, min_confidence=0.2)

    assert memories
    assert memories[0]["memory_type"] == "milestone"


def test_extracts_chinese_emotional_memory():
    text = "我其实有点害怕这本小说写崩，但也真的很喜欢这个主角，还是想把她写好。"

    memories = extract_memories(text, min_confidence=0.2)

    assert memories
    assert memories[0]["memory_type"] == "emotional"
