from main import main
from counter import Counter


# UNIT TESTS ===================================================================
def test_initial_value():
    c = Counter(10)
    assert c.value == 10


def test_increment():
    c = Counter()
    c.increment()
    assert c.value == 1


def test_decrement():
    c = Counter(5)
    c.decrement()
    assert c.value == 4


def test_string_representation():
    c = Counter(11)
    assert str(c) == "11"


# INTEGRATION TESTS ============================================================
def test_counter_flow_capture_prompt(monkeypatch):
    captured_prompts = []
    inputs = iter(["i", "i", "d", "quit"])

    def mocked_input(prompt):
        captured_prompts.append(prompt)
        return next(inputs)

    monkeypatch.setattr("builtins.input", mocked_input)

    main()

    all_prompts = "".join(captured_prompts)

    assert "Current: 1" in all_prompts
    assert "Current: 2" in all_prompts
    assert "Current: 1" in all_prompts


def test_counter_cli_error_handling(monkeypatch, capsys):
    inputs = iter(["d", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()
    captured = capsys.readouterr().out

    assert "Error: Counter cannot be negative" in captured
