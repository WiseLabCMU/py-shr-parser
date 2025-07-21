import numpy as np
import matplotlib.pyplot as plt
from ..shr_parser import ShrSweep
from .units import si_scale
from ..enumerations import ShrScale


def _plot_spectrum(spectrum, f_min, f_max, bins):
    freq = np.linspace(f_min, f_max, bins)

    fig, ax = plt.subplots()
    ax.plot(freq, spectrum)

    return fig, ax

def plot_spectrum(sweep: ShrSweep):
    """
    Plot the frequency spectrum of a certain sweep.

    :param sweep: The frequency sweep to plot.
    :return: matplotlib figure object and matplotlib Axes object.
    """
    if not isinstance(sweep, ShrSweep):
        raise TypeError("`sweep` must be of type `ShrSweep`")

    prefix, scale = si_scale(sweep.f_min)

    pwr_scale = 'dBm' if sweep.file_header.ref_scale == ShrScale.DBM else 'mV'

    ref = sweep.file_header.ref_level
    div = sweep.file_header.div

    y_ticks = [ref - (i * div) for i in range(0, 11)]

    fig, ax = _plot_spectrum(sweep.sweep, sweep.f_min / scale, sweep.f_max / scale, sweep.sweep_bins)

    ax.set_xlabel(f"Frequency ({prefix}Hz)")
    ax.set_ylabel(f"Power ({pwr_scale})")

    ax.set_title(f"Frequency Spectrum at sweep {sweep.n}")
    ax.grid(True)
    ax.set_yticks(y_ticks)

    return fig, ax
