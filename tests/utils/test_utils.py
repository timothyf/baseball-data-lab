import json
import numpy as np
import pandas as pd
import pytest
from baseball_data_lab.utils import Utils


def test_format_stat_variants():
    assert Utils.format_stat(0.25, 'percent') == '25.0%'
    assert Utils.format_stat(3.14159, '.2f') == '3.14'
    assert Utils.format_stat(0.123, 'no_leading_zero') == '.123'
    assert Utils.format_stat(5, lambda x: f'value:{x}') == 'value:5'
    with pytest.raises(TypeError):
        Utils.format_stat(1.0, 123)


def test_numpy_encoder_dump_json():
    data = {'a': np.int64(5), 'b': np.float64(1.5), 'c': np.array([1, 2])}
    dumped = Utils.dump_json(data)
    parsed = json.loads(dumped)
    assert parsed == {'a': 5, 'b': 1.5, 'c': [1, 2]}


def test_ensure_directory_exists(tmp_path):
    file_path = tmp_path / 'a' / 'b' / 'file.txt'
    Utils.ensure_directory_exists(file_path)
    assert (tmp_path / 'a' / 'b').is_dir()


def test_validate_statcast_df():
    empty_df = pd.DataFrame()
    assert Utils.validate_statcast_df(empty_df) is False

    missing_cols_df = pd.DataFrame({'hc_x': [1]})
    assert Utils.validate_statcast_df(missing_cols_df) is False

    nan_df = pd.DataFrame({'hc_x': [None], 'hc_y': [None]})
    assert Utils.validate_statcast_df(nan_df) is False

    valid_df = pd.DataFrame({'hc_x': [10], 'hc_y': [20]})
    assert Utils.validate_statcast_df(valid_df) is True
