import matplotlib.pyplot as plt
import pandas as pd
import pytest

from baseball_data_lab.data_viz.rolling_pitch_usage_plot import RollingPitchUsagePlot


@pytest.fixture
def sample_pitch_data():
    """Create a small sample DataFrame for testing."""
    data = {
        'game_pk': [1, 1, 2, 2],
        'game_date': pd.to_datetime(['2021-04-01', '2021-04-01', '2021-04-02', '2021-04-02']),
        'pitch_type': ['FF', 'SL', 'FF', 'CU'],
        'release_speed': [90, 88, 91, 92]
    }
    return pd.DataFrame(data)


@pytest.fixture
def plot_object():
    """Create an instance of RollingPitchUsagePlot."""
    return RollingPitchUsagePlot(player="Test Pitcher")


@pytest.mark.integration
def test_plot_integration(plot_object, sample_pitch_data):
    """Integration test for the top-level plot method."""
    fig, ax = plt.subplots()
    window = 1
    plot_object.plot(sample_pitch_data, ax, window)
    assert ax.get_xlabel() != ""
    assert ax.get_ylabel() != ""
    assert ax.get_title() != ""
    plt.close(fig)
