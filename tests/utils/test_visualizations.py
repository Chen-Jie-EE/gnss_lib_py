"""Tests for visualizations.

"""

__authors__ = "D. Knowles"
__date__ = "22 Jun 2022"

import os
import random

import pytest
import numpy as np
from pytest_lazyfixture import lazy_fixture

import gnss_lib_py.utils.visualizations as viz
from gnss_lib_py.algorithms.snapshot import solve_wls
from gnss_lib_py.parsers.android import AndroidDerived2021
from gnss_lib_py.parsers.android import AndroidDerived2022
from gnss_lib_py.algorithms.residuals import solve_residuals

# pylint: disable=protected-access

@pytest.fixture(name="root_path")
def fixture_root_path():
    """Location of measurements for unit test

    Returns
    -------
    root_path : string
        Folder location containing measurements
    """
    root_path = os.path.dirname(
                os.path.dirname(
                os.path.dirname(
                os.path.realpath(__file__))))
    root_path = os.path.join(root_path, 'data/unit_test/android_2021/')
    return root_path

@pytest.fixture(name="derived_path")
def fixture_derived_path(root_path):
    """Filepath of Android Derived measurements

    Returns
    -------
    derived_path : string
        Location for the unit_test Android derived measurements

    Notes
    -----
    Test data is a subset of the Android Raw Measurement Dataset [1]_,
    particularly the train/2020-05-14-US-MTV-1/Pixel4 trace. The dataset
    was retrieved from
    https://www.kaggle.com/c/google-smartphone-decimeter-challenge/data

    References
    ----------
    .. [1] Fu, Guoyu Michael, Mohammed Khider, and Frank van Diggelen.
        "Android Raw GNSS Measurement Datasets for Precise Positioning."
        Proceedings of the 33rd International Technical Meeting of the
        Satellite Division of The Institute of Navigation (ION GNSS+
        2020). 2020.
    """
    derived_path = os.path.join(root_path, 'Pixel4_derived.csv')
    return derived_path

@pytest.fixture(name="derived_path_xl")
def fixture_derived_path_xl(root_path):
    """Filepath of Android Derived measurements

    Parameters
    ----------
    root_path : string
        Path of testing dataset root path

    Returns
    -------
    derived_path : string
        Location for the unit_test Android derived measurements

    Notes
    -----
    Test data is a subset of the Android Raw Measurement Dataset [6]_,
    particularly the train/2020-05-14-US-MTV-1/Pixel4XL trace. The
    dataset was retrieved from
    https://www.kaggle.com/c/google-smartphone-decimeter-challenge/data

    References
    ----------
    .. [6] Fu, Guoyu Michael, Mohammed Khider, and Frank van Diggelen.
        "Android Raw GNSS Measurement Datasets for Precise Positioning."
        Proceedings of the 33rd International Technical Meeting of the
        Satellite Division of The Institute of Navigation (ION GNSS+
        2020). 2020.
    """
    derived_path = os.path.join(root_path, 'Pixel4XL_derived.csv')
    return derived_path

@pytest.fixture(name="root_path_2022")
def fixture_root_path_2022():
    """Location of measurements for unit test

    Returns
    -------
    root_path : string
        Folder location containing measurements
    """
    root_path = os.path.dirname(
                os.path.dirname(
                os.path.dirname(
                os.path.realpath(__file__))))
    root_path = os.path.join(root_path, 'data/unit_test/android_2022')
    return root_path


@pytest.fixture(name="derived_2022_path")
def fixture_derived_2022_path(root_path_2022):
    """Filepath of Android Derived measurements

    Returns
    -------
    derived_path : string
        Location for the unit_test Android derived 2022 measurements

    Notes
    -----
    Test data is a subset of the Android Raw Measurement Dataset [4]_,
    from the 2022 Decimeter Challenge. Particularly, the
    train/2021-04-29-MTV-2/SamsungGalaxyS20Ultra trace. The dataset
    was retrieved from
    https://www.kaggle.com/competitions/smartphone-decimeter-2022/data

    References
    ----------
    .. [4] Fu, Guoyu Michael, Mohammed Khider, and Frank van Diggelen.
        "Android Raw GNSS Measurement Datasets for Precise Positioning."
        Proceedings of the 33rd International Technical Meeting of the
        Satellite Division of The Institute of Navigation (ION GNSS+
        2020). 2020.
    """
    derived_path = os.path.join(root_path_2022, 'device_gnss.csv')
    return derived_path

@pytest.fixture(name="derived")
def fixture_load_derived(derived_path):
    """Load instance of AndroidDerived2021

    Parameters
    ----------
    derived_path : pytest.fixture
        String with location of Android derived measurement file

    Returns
    -------
    derived : AndroidDerived2021
        Instance of AndroidDerived2021 for testing
    """
    derived = AndroidDerived2021(derived_path)
    return derived

@pytest.fixture(name="derived_xl")
def fixture_load_derived_xl(derived_path_xl):
    """Load instance of AndroidDerived2021

    Parameters
    ----------
    derived_path : pytest.fixture
        String with location of Android derived measurement file

    Returns
    -------
    derived : AndroidDerived2021
        Instance of AndroidDerived2021 for testing
    """
    derived = AndroidDerived2021(derived_path_xl,
                                 remove_timing_outliers=False)
    return derived

@pytest.fixture(name="derived_2022")
def fixture_load_derived_2022(derived_2022_path):
    """Load instance of AndroidDerived2021

    Parameters
    ----------
    derived_path : pytest.fixture
    String with location of Android derived measurement file

    Returns
    -------
    derived : AndroidDerived2022
    Instance of AndroidDerived2022 for testing
    """
    derived = AndroidDerived2022(derived_2022_path)
    return derived

@pytest.fixture(name="state_estimate")
def fixture_solve_wls(derived):
    """Fixture of WLS state estimate.

    Parameters
    ----------
    derived : AndroidDerived2021
        Instance of AndroidDerived2021 for testing.

    Returns
    -------
    state_estimate : gnss_lib_py.parsers.navdata.NavData
        Estimated receiver position in ECEF frame in meters and the
        estimated receiver clock bias also in meters as an instance of
        the NavData class with shape (4 x # unique timesteps) and
        the following rows: x_rx_m, y_rx_m, z_rx_m, b_rx_m.

    """
    state_estimate = solve_wls(derived)
    return state_estimate

@pytest.fixture(name="state_estimate_xl")
def fixture_solve_wls_xl(derived_xl):
    """Fixture of WLS state estimate.

    Parameters
    ----------
    derived : AndroidDerived2021
        Instance of AndroidDerived2021 for testing.

    Returns
    -------
    state_estimate : gnss_lib_py.parsers.navdata.NavData
        Estimated receiver position in ECEF frame in meters and the
        estimated receiver clock bias also in meters as an instance of
        the NavData class with shape (4 x # unique timesteps) and
        the following rows: x_rx_m, y_rx_m, z_rx_m, b_rx_m.

    """
    state_estimate = solve_wls(derived_xl)
    return state_estimate

def test_plot_metrics(derived):
    """Test for plotting metrics.

    Parameters
    ----------
    derived : AndroidDerived2021
        Instance of AndroidDerived2021 for testing.

    """

    test_rows = [
                 "raw_pr_m",
                 "raw_pr_sigma_m",
                 "tropo_delay_m",
                 ]

    for row in derived.rows:
        if not derived.is_str(row):
            if row in test_rows:
                fig = viz.plot_metric(derived, row, save=False)
                viz.close_figures(fig)
        else:
            # string rows should cause a KeyError
            with pytest.raises(KeyError) as excinfo:
                fig = viz.plot_metric(derived, row, save=False)
                viz.close_figures(fig)
            assert "non-numeric row" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        viz.plot_metric(derived, "raw_pr_m", save=True, prefix=1)
    assert "Prefix" in str(excinfo.value)

    for row in derived.rows:
        if not derived.is_str(row):
            if row in test_rows:
                fig = viz.plot_metric(derived, "raw_pr_m", row, save=False)
                viz.close_figures(fig)
        else:
            # string rows should cause a KeyError
            with pytest.raises(KeyError) as excinfo:
                fig = viz.plot_metric(derived, "raw_pr_m", row, save=False)
                viz.close_figures(fig)
            with pytest.raises(KeyError) as excinfo:
                fig = viz.plot_metric(derived, row, "raw_pr_m", save=False)
                viz.close_figures(fig)
            assert "non-numeric row" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        viz.plot_metric(derived, "raw_pr_m", save=True, prefix=1)
    assert "Prefix" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        viz.plot_metric(derived, 'raw_pr_m', row, row, save=False)

def test_plot_metrics_by_constellation(derived):
    """Test for plotting metrics.

    Parameters
    ----------
    derived : AndroidDerived2021
        Instance of AndroidDerived2021 for testing.

    """

    test_rows = [
                 "raw_pr_m",
                 "raw_pr_sigma_m",
                 "tropo_delay_m",
                 ]

    for row in derived.rows:
        if not derived.is_str(row):
            if row in test_rows:
                fig = viz.plot_metric_by_constellation(derived, row, save=False)
                viz.close_figures(fig)
        else:
            # string rows should cause a KeyError
            with pytest.raises(KeyError) as excinfo:
                fig = viz.plot_metric_by_constellation(derived, row, save=False)
                viz.close_figures(fig)
            assert "non-numeric row" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        viz.plot_metric_by_constellation(derived, "raw_pr_m", save=True,
                                         prefix=1)
    assert "Prefix" in str(excinfo.value)

    derived_no_gnss_id = derived.remove(rows="gnss_id")
    with pytest.raises(KeyError) as excinfo:
        viz.plot_metric_by_constellation(derived_no_gnss_id, "raw_pr_m",
                                         save=False)
    assert "gnss_id" in str(excinfo.value)

    derived_no_sv_id = derived.remove(rows="signal_type")
    viz.plot_metric_by_constellation(derived_no_sv_id,
                                     "raw_pr_m", save=False)

    derived_no_signal_type = derived.remove(rows="signal_type")
    viz.plot_metric_by_constellation(derived_no_signal_type,
                                     "raw_pr_m", save=False)

@pytest.mark.parametrize('navdata',[
                                    # lazy_fixture('derived_2022'),
                                    # lazy_fixture('derived'),
                                    lazy_fixture('derived_xl'),
                                    ])
def test_plot_skyplot(navdata, state_estimate_xl):
    """Test for plotting skyplot.

    Parameters
    ----------
    navdata : AndroidDerived
        Instance of AndroidDerived for testing.
    state_estimate : gnss_lib_py.parsers.navdata.NavData
        Estimated receiver position in ECEF frame in meters and the
        estimated receiver clock bias also in meters as an instance of
        the NavData class with shape (4 x # unique timesteps) and
        the following rows: x_rx_m, y_rx_m, z_rx_m, b_rx_m.

    """

    if isinstance(navdata, AndroidDerived2022):
        row_map = {
                   "WlsPositionXEcefMeters" : "x_rx_m",
                   "WlsPositionYEcefMeters" : "y_rx_m",
                   "WlsPositionZEcefMeters" : "z_rx_m",
                    }
        navdata.rename(row_map,inplace=True)
        state_estimate = navdata.copy(rows=["gps_millis","x_rx_m","y_rx_m","z_rx_m"])
    else:
        state_estimate = state_estimate_xl

    # don't save figures
    fig = viz.plot_skyplot(navdata, state_estimate, save=False)
    viz.close_figures(fig)

    with pytest.raises(TypeError) as excinfo:
        viz.plot_skyplot(navdata, state_estimate, save=True, prefix=1)
    assert "Prefix" in str(excinfo.value)

    for row in ["x_sv_m","y_sv_m","z_sv_m","gps_millis"]:
        derived_removed = navdata.remove(rows=row)
        with pytest.raises(KeyError) as excinfo:
            viz.plot_skyplot(derived_removed, state_estimate, save=False)
        assert row in str(excinfo.value)

def test_plot_residuals(derived_xl, state_estimate_xl):
    """Test for plotting residuals.

    Parameters
    ----------
    derived : AndroidDerived2021
        Instance of AndroidDerived2021 for testing.
    state_estimate : gnss_lib_py.parsers.navdata.NavData
        Estimated receiver position in ECEF frame in meters and the
        estimated receiver clock bias also in meters as an instance of
        the NavData class with shape (4 x # unique timesteps) and
        the following rows: x_rx_m, y_rx_m, z_rx_m, b_rx_m.

    """

    solve_residuals(derived_xl, state_estimate_xl, inplace=True)

    # don't save figures
    figs = viz.plot_metric_by_constellation(derived_xl, "gps_millis",
                                            "residuals", save=False)
    viz.close_figures(figs)

def test_get_label():
    """Test for getting nice labels.

    """

    assert viz._get_label({"signal_type" : "GPS_L1"}) == "GPS L1"
    assert viz._get_label({"signal_type" : "GLO_G1"}) == "GLO G1"
    assert viz._get_label({"signal_type" : "BDS_B1I"}) == "BDS B1i"
    # shouldn't do lowercase 'i' trick if not signal_type
    assert viz._get_label({"random" : "BDS_B1I"}) == "BDS B1I"

def test_sort_gnss_ids():
    """Test sorting GNSS IDs.

    """

    unsorted_ids = ["galileo","beta","beidou","irnss","gps","unkown","glonass",
                "alpha","qzss","sbas"]
    sorted_ids = ["gps","glonass","galileo","beidou","qzss","irnss","sbas",
                  "unkown", "alpha", "beta"]

    assert viz._sort_gnss_ids(unsorted_ids) == sorted_ids
    assert viz._sort_gnss_ids(np.array(unsorted_ids)) == sorted_ids
    assert viz._sort_gnss_ids(set(unsorted_ids)) == sorted_ids
    assert viz._sort_gnss_ids(tuple(unsorted_ids)) == sorted_ids

    for _ in range(100):
        random.shuffle(unsorted_ids)
        assert viz._sort_gnss_ids(unsorted_ids) == sorted_ids
        assert viz._sort_gnss_ids(np.array(unsorted_ids)) == sorted_ids
        assert viz._sort_gnss_ids(set(unsorted_ids)) == sorted_ids
        assert viz._sort_gnss_ids(tuple(unsorted_ids)) == sorted_ids
