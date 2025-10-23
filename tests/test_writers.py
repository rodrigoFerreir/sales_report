import os
import pytest
from unittest.mock import patch, mock_open
from output.writers.json_writer import JsonWriter
from output.writers.text_writer import TextWriter


@pytest.fixture
def temp_dir(tmpdir):
    return str(tmpdir)


def test_json_writer_execute(temp_dir: str):
    """
    Testa se o JsonWriter.execute cria o arquivo corretamente.
    """
    writer = JsonWriter()
    writer.path_result = temp_dir
    data = """{"key": "value"}"""
    result = writer.execute(data)

    assert "Resultado salvo no path" in result
    file_name = result.split(" ")[-1]
    file_name = os.path.basename(file_name)

    created_files = os.listdir(temp_dir)
    assert len(created_files) == 1
    created_file = created_files[0]

    with open(os.path.join(temp_dir, created_file), "r") as f:
        content = f.read()
        assert content == data


def test_text_writer_execute(temp_dir: str):
    """
    Testa se o TextWriter.execute cria o arquivo corretamente.
    """
    writer = TextWriter()
    writer.path_result = temp_dir
    data = "line1\nline2"
    result = writer.execute(data)

    assert "Resultado salvo no path" in result
    file_name = result.split(" ")[-1]
    file_name = os.path.basename(file_name)

    created_files = os.listdir(temp_dir)
    assert len(created_files) == 1
    created_file = created_files[0]

    with open(os.path.join(temp_dir, created_file), "r") as f:
        content = f.read()
        assert content == data


@patch("builtins.open", new_callable=mock_open)
def test_json_writer_execute_exception(mock_open_file):
    """
    Testa se o JsonWriter.execute trata exceções corretamente.
    """
    mock_open_file.side_effect = Exception("Test error")
    writer = JsonWriter()
    result = writer.execute("""{"key": "value"}""")
    assert result == ""


@patch("builtins.open", new_callable=mock_open)
def test_text_writer_execute_exception(mock_open_file):
    """
    Testa se o TextWriter.execute trata exceções corretamente.
    """
    mock_open_file.side_effect = Exception("Test error")
    writer = TextWriter()
    result = writer.execute("line1\nline2")
    assert result == ""
