import numpy as np
import matplotlib.pyplot as plt
from ..shr_parser import ShrSweep
from .units import si_scale
from ..enumerations import ShrScale
import matplotlib.animation as animate


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
    ax.set_ylabel(f"Amplitude ({pwr_scale})")

    ax.set_title(f"Frequency Spectrum at sweep {sweep.n}")
    ax.grid(True)
    ax.set_yticks(y_ticks)

    return fig, ax


def animate_spectrum(sweeps: list[ShrSweep], title: str | None = None, interval: int = 200, repeat_delay: int = 0,
                     repeat: bool = True):
    """
    Animate the spectrum changes over time.

    :param sweeps: The frequency sweeps to animate.
    :param title: The title of the figure.
    :param interval: Delay between frames in milliseconds.
    :param repeat_delay: The delay in milliseconds between consecutive animation runs, if repeat is True.
    :param repeat: Whether the animation repeats when the sequence of frames is completed.
    :return: matplotlib FunAnimation object.
    """
    if not isinstance(sweeps, list):
        raise TypeError("`sweeps` must be a list of type `ShrSweep`")
    if not sweeps:
        raise ValueError("Empty list")
    if not all(isinstance(sweep, ShrSweep) for sweep in sweeps):
        raise TypeError("`sweeps` must be a list of type `ShrSweep`")

    prefix, scale = si_scale(sweeps[0].f_min)
    header = sweeps[0].file_header

    freq = np.linspace(sweeps[0].f_min / scale, sweeps[0].f_max / scale, sweeps[0].sweep_bins)

    pwr_scale = 'dBm' if header.ref_scale == ShrScale.DBM else 'mV'

    ref = header.ref_level
    div = header.div

    y_ticks = [ref - (i * div) for i in range(0, 11)]

    # Initial frame
    fig, ax = plt.subplots()
    lines, = ax.plot(freq, sweeps[0].sweep)

    ax.grid(True)
    ax.set_yticks(y_ticks)

    if title is None:
        title = "Frequency Spectrum"

    ax.set_title(title)

    ax.set_xlabel(f"Frequency ({prefix}Hz)")
    ax.set_ylabel(f"Amplitude ({pwr_scale})")

    def update(i_):
        lines.set_ydata(sweeps[i_].sweep)
        return [lines]

    return animate.FuncAnimation(fig, update, frames=len(sweeps), blit=False, interval=interval,
                                 repeat_delay=repeat_delay, repeat=repeat)
