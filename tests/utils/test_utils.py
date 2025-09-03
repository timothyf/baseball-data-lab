import json
import numpy as np
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
