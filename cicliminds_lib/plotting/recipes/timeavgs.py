from matplotlib import cm
import xhistogram.xarray as xh

from cicliminds_lib.utils import patch_config

from cicliminds_lib.bindings import cdo_gridweights_from_data

from cicliminds_lib.plotting.recipes.means_of_hists import MeansOfHistsRecipe
from cicliminds_lib.plotting.recipes.means_of_hists import MeansOfHistsDiffRecipe
from cicliminds_lib.plotting._helpers import _standardize_data
from cicliminds_lib.plotting._helpers import _generate_timeslices
from cicliminds_lib.plotting._helpers import _get_histogram_params
from cicliminds_lib.plotting._helpers import _configure_axes
from cicliminds_lib.plotting._helpers import _get_year_label


class HistOfTimeavgsRecipe:
    @classmethod
    def plot(cls, ax, val, query):
        default_cfg = cls.get_default_config(val.name)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        weights = cdo_gridweights_from_data(val)
        timeslices = _generate_timeslices(val, query)
        _, timeslice = next(timeslices)
        mean = val.isel(time=timeslice).mean(dim=["time"])
        bins, x, widths = _get_histogram_params(mean, cfg.binsize)
        hist = xh.histogram(mean, bins=[bins], dim=["lat", "lon"], weights=weights)
        ax.bar(x, hist.values.ravel(), widths, label=_get_year_label(cfg, timeslice))
        cmap = cm.get_cmap(cfg.colormap)
        for intensity, timeslice in timeslices:
            mean = val.isel(time=timeslice).mean(dim=["time"])
            hist = xh.histogram(mean, bins=[bins], dim=["lat", "lon"], weights=weights)
            ax.stairs(hist, bins, label=_get_year_label(cfg, timeslice), color=cmap(intensity))
        _configure_axes(ax, cfg)

    @staticmethod
    def get_default_config(index_name):
        return MeansOfHistsRecipe.get_default_config(index_name)


class HistOfTimeavgsDiffRecipe:
    @classmethod
    def plot(cls, ax, val, query):
        default_cfg = cls.get_default_config(val.name)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        weights = cdo_gridweights_from_data(val)
        timeslices = _generate_timeslices(val, cfg)
        _, timeslice = next(timeslices)
        mean = val.isel(time=timeslice).mean(dim=["time"])
        bins, _, _ = _get_histogram_params(mean, cfg.binsize)
        ref_hist = xh.histogram(mean, bins=[bins], dim=["lat", "lon"], weights=weights)
        cmap = cm.get_cmap(cfg.colormap)
        for intensity, timeslice in timeslices:
            mean = val.isel(time=timeslice).mean(dim=["time"])
            hist = xh.histogram(mean, bins=[bins], dim=["lat", "lon"], weights=weights)
            ax.stairs(hist - ref_hist, bins, label=_get_year_label(cfg, timeslice), color=cmap(intensity))
        _configure_axes(ax, cfg)
        ax.set_yscale("linear")

    @staticmethod
    def get_default_config(index_name):
        return MeansOfHistsDiffRecipe.get_default_config(index_name)