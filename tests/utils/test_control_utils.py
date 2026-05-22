import io

from lerobot.utils.control_utils import _stdin_command_reader, apply_stdin_command


def _fresh_events():
    return {"exit_early": False, "rerecord_episode": False, "stop_recording": False}


def test_apply_stdin_command_save_sets_exit_early():
    events = _fresh_events()
    assert apply_stdin_command(events, "save\n") is True
    assert events == {"exit_early": True, "rerecord_episode": False, "stop_recording": False}


def test_apply_stdin_command_rerecord_sets_rerecord_and_exit_early():
    events = _fresh_events()
    assert apply_stdin_command(events, " rerecord ") is True
    assert events == {"exit_early": True, "rerecord_episode": True, "stop_recording": False}


def test_apply_stdin_command_stop_sets_stop_and_exit_early():
    events = _fresh_events()
    assert apply_stdin_command(events, "stop\n") is True
    assert events == {"exit_early": True, "rerecord_episode": False, "stop_recording": True}


def test_apply_stdin_command_unknown_returns_false_and_no_change():
    events = _fresh_events()
    assert apply_stdin_command(events, "garbage") is False
    assert events == _fresh_events()


def test_apply_stdin_command_blank_returns_false():
    events = _fresh_events()
    assert apply_stdin_command(events, "\n") is False
    assert events == _fresh_events()


def test_stdin_command_reader_applies_commands_until_eof():
    events = _fresh_events()
    stream = io.StringIO("save\nrerecord\n")
    _stdin_command_reader(events, stream)
    assert events["exit_early"] is True
    assert events["rerecord_episode"] is True


def test_stdin_command_reader_ignores_unknown_and_blank_lines():
    events = _fresh_events()
    stream = io.StringIO("\n\n\nhello\n")
    _stdin_command_reader(events, stream)
    assert events == _fresh_events()


def test_stdin_command_reader_handles_stream_error_gracefully():
    class _BrokenStream:
        def __iter__(self):
            yield "save\n"
            raise UnicodeDecodeError("utf-8", b"", 0, 1, "bad byte")

    events = _fresh_events()
    _stdin_command_reader(events, _BrokenStream())  # must not raise
    assert events["exit_early"] is True  # the good line before the error was applied
