from Leaderboard import Leaderboard
import pytest

def test_add_player(tmp_path, monkeypatch):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))

    monkeypatch.setattr("builtins.input", lambda _: "100")

    leaderboard.writing_score("Ali")

    assert leaderboard.load_scores() == [["Ali", 100.0]]

@pytest.mark.parametrize(
    "players, expected",
    [
        (
            "Gamer,Score\nIkrom,100\nIsmoil,200\nBrad,50\n",
            [["Ismoil", 200.0], ["Ikrom", 100.0], ["Brad", 50.0]],
        ),
        (
            "Gamer,Score\nAli,10\nBob,90\n",
            [["Bob", 90.0], ["Ali", 10.0]],
        ),
        (
            "Gamer,Score\nSara,0\n",
            [["Sara", 0.0]],
        ),
    ],
)  


def test_sorting(tmp_path, players, expected):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text(players, encoding="utf-8")

    assert leaderboard.load_scores() == expected

def test_copy_player(tmp_path, monkeypatch):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    responses = iter(["100", "no"])

    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    leaderboard.writing_score("Ali")
    leaderboard.writing_score("Ali")

    scores = leaderboard.load_scores()

    assert scores == [["Ali", 100.0]]


def test_update_score(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,100\n", encoding = "utf-8")
    responses = iter(["Ikrom", "1000"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.update_score()
    assert "Score updated for gamer 'Ikrom'" in capsys.readouterr().out

def test_update_score_invalid_then_valid(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,100\n", encoding = "utf-8")
    responses = iter(["Ikrom", "abc", "-100", "150"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.update_score()
    output = capsys.readouterr().out    
    assert "Score cannot be negative. Please try again." in output
    assert "Invalid input. Please enter a valid score." in output
    assert leaderboard.load_scores() == [["Ikrom", 150]]

def test_gamer_search(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,100\nIsmoil,200\nBrad,50\n", encoding="utf-8")
    responses = iter(["Ikrom", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.gamer_search()
    assert "Match Found!" in capsys.readouterr().out

def test_update_score_missing_player_no(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,100\n", encoding="utf-8")
    responses = iter(["Unknown", "yessss", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.update_score()
    output = capsys.readouterr().out
    assert "Invalid input. Please enter 'yes' or 'no'" in output
    assert "No changes made." in output
    assert leaderboard.load_scores() == [["Ikrom", 100.0]]

def test_update_score_missing_player_yes(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,150\n", encoding="utf-8")
    responses = iter(["Ali", "yes", "-100", "abcsd", "110"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.update_score()
    output = capsys.readouterr().out
    assert "Score cannot be negative. Please try again." in output
    assert "Invalid input. Please enter a valid score." in output
    assert leaderboard.load_scores() == [["Ikrom", 150], ["Ali", 110]]

def test_case_insensitive_search(tmp_path, monkeypatch):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,150\n", encoding="utf-8")
    responses = iter(["ikrom", "200"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.update_score()
    assert leaderboard.load_scores() == [["Ikrom", 200.0]]

def test_gamer_search_various_yes(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,150\n", encoding="utf-8")
    responses = iter(["Ikrom", "yessss", "yes", "200"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.gamer_search()
    output = capsys.readouterr().out
    assert "Invalid input. Please enter 'yes' or 'no'." in output
    assert leaderboard.load_scores() == [["Ikrom", 200]]

def test_gamer_wrong_name_yes(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,200\n", encoding="utf-8")
    responses = iter(["Ali", "yessss", "yes", "190"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.gamer_search()
    output = capsys.readouterr().out
    assert "Invalid input. Please enter 'yes' or 'no'." in output
    assert leaderboard.load_scores() == [["Ikrom", 200], ["Ali", 190]]

def test_gamer_wrong_name_no(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,200\n", encoding="utf-8")
    responses = iter(["Ali", "yessss", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.gamer_search()
    output = capsys.readouterr().out
    assert "No changes made." in output
    assert leaderboard.load_scores() == [["Ikrom", 200]]

def test_writing_score_game_exists_no(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,200\n", encoding="utf-8")
    responses = iter(["Ikrom", "yessss", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.writing_score()
    output = capsys.readouterr().out
    assert "Invalid input. Please enter 'yes' or 'no'." in output
    assert leaderboard.load_scores() == [["Ikrom", 200]]

def test_writing_score_game_exists_yes(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,200\n", encoding="utf-8")
    responses = iter(["Ikrom", "yes", "-100", "hsahdnwj!!", "100"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.writing_score()
    output = capsys.readouterr().out
    assert "Score cannot be negative. Please try again." in output
    assert "Invalid input. Please enter a valid score." in output
    assert leaderboard.load_scores() == [["Ikrom", 100]]

def test_menu_with_invalid(tmp_path, monkeypatch, capsys):
    filename = tmp_path / "test_players.csv"
    leaderboard = Leaderboard(str(filename))
    filename.write_text("Gamer,Score\nIkrom,100\nIsmoil,200\nBrad,50\n", encoding="utf-8")
    responses = iter(["2", "1", "Ali", "150", "3", "Ikrom", "no", "4", "Ikrom", "250", "10", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    leaderboard.menu()
    output = capsys.readouterr().out
    assert leaderboard.load_scores() == [
        ["Ikrom", 250.0],
        ["Ismoil", 200.0],
        ["Ali", 150.0],
        ["Brad", 50.0]]
    assert "Invalid choice. Please enter a number between 1 and 5." in output
    assert "Exiting the program." in output




