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
