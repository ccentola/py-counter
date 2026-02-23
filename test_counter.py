from main import main


def test_counter_flow(monkeypatch, capsys):
    inputs = iter(["i", "d", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # run the function
    main()

    # capture the output
    captured = capsys.readouterr().out

    # assertions
    assert "1" in captured
    assert "0" in captured
    assert "Goodbye" in captured


def test_counter_is_not_negative(monkeypatch, capsys):
    inputs = iter(["d", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # run the function
    main()

    # capture the output
    captured = capsys.readouterr().out

    assert "0" in captured
    assert "Counter cannot be less than 0" in captured
