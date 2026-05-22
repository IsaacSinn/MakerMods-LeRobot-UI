import io

from lerobot.utils.control_utils import apply_stdin_command


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
