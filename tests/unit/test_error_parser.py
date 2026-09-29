from agents.diagnosis.subagents.error_parser import ErrorParser


def test_error_parser():
    traceback = """
    Traceback (most recent call last):
      File "train.py", line 42, in train_model
        output = model(image)
    NameError: name 'model' is not defined
    """

    parser = ErrorParser()
    result = parser.parse(traceback)

    assert result["error_type"] == "NameError"
    assert result["error_message"] == "name 'model' is not defined"
    assert result["file"] == "train.py"
    assert result["line"] == "42"
    assert result["function"] == "train_model"