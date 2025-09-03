import json
import pandas as pd

from baseball_data_lab.data_converter import DataConverter


def test_csv_to_json_success(tmp_path):
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    csv_file = tmp_path / 'input.csv'
    df.to_csv(csv_file, index=False)
    converter = DataConverter(input_dir=str(tmp_path), output_dir=str(tmp_path))
    converter.csv_to_json('input.csv', 'output.json')
    output_file = tmp_path / 'output.json'
    assert output_file.exists()
    with open(output_file) as f:
        lines = [json.loads(line) for line in f]
    assert lines == [{'A': 1, 'B': 3}, {'A': 2, 'B': 4}]


def test_csv_to_json_missing_file(tmp_path, capsys):
    converter = DataConverter(input_dir=str(tmp_path), output_dir=str(tmp_path))
    converter.csv_to_json('missing.csv', 'out.json')
    captured = capsys.readouterr().out
    assert 'CSV file not found' in captured
    assert not (tmp_path / 'out.json').exists()


def test_csv_to_json_empty_file(tmp_path, capsys):
    empty = tmp_path / 'empty.csv'
    empty.write_text('')
    converter = DataConverter(input_dir=str(tmp_path), output_dir=str(tmp_path))
    converter.csv_to_json('empty.csv', 'out.json')
    captured = capsys.readouterr().out
    assert 'CSV file is empty' in captured


def test_create_current_teams_json(tmp_path):
    df = pd.DataFrame({
        'ID': [1, 2],
        'yearID': [2021, 2020],
        'lgID': ['AL', 'NL'],
        'teamID': ['T1', 'T2'],
        'franchID': ['F1', 'F2'],
        'teamIDfg': [111, 222],
        'teamIDBR': ['B1', 'B2'],
        'teamIDretro': ['R1', 'R2']
    })
    teams_csv = tmp_path / 'fangraphs_teams.csv'
    df.to_csv(teams_csv, index=False)
    converter = DataConverter(input_dir=str(tmp_path), output_dir=str(tmp_path))
    converter.create_current_teams_json()
    output_file = tmp_path / 'current_teams.json'
    assert output_file.exists()
    with open(output_file) as f:
        lines = [json.loads(line) for line in f]
    assert lines == [{
        'ID': 1,
        'yearID': 2021,
        'lgID': 'AL',
        'teamID': 'T1',
        'franchID': 'F1',
        'teamIDfg': 111,
        'teamIDBR': 'B1',
        'teamIDretro': 'R1'
    }]
