from agents.diagnosis.subagents.log_analyzer import LogAnalyzer


def test_log_analyzer():

    logs = """
    Starting application...
    WARNING: Deprecated API usage
    Loading model...
    CUDA out of memory
    ERROR: Failed to load model
    """

    analyzer = LogAnalyzer()
    result = analyzer.analyze(logs)

    assert len(result["errors"]) == 1
    assert len(result["warnings"]) == 1
    assert len(result["patterns"]) == 1

    assert "Failed to load model" in result["errors"][0]
    assert "Deprecated API" in result["warnings"][0]
    assert "CUDA out of memory" in result["patterns"][0]