import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from ..shr_parser import ShrSweep
from ..metadata import ShrSweepHeader
from .units import si_scale
from ..enumerations import ShrScale
from typing import Literal
from matplotlib.colors import Colormap
import matplotlib.animation as animate


def _plot_spectrogram(arrays, timestamps, f_min, f_max, bins, shading, cmap):
    dt_axis = [dt.datetime.fromtimestamp(ts / 1000.0, dt.timezone.utc) for ts in timestamps]

    pwr_mat = np.vstack(arrays)

    freq = np.linspace(f_min, f_max, bins)
    time = mdates.date2num(dt_axis)

    fig, ax = plt.subplots()

    pcm = ax.pcolormesh(
        freq,
        time,
        pwr_mat,
        shading=shading,
        cmap=cmap
    )

    return pcm, fig, ax


def spectrogram(sweeps: list[ShrSweep],
                shading: Literal["flat", "nearest", "gouraud", "auto"] | None = 'auto',
                cmap: str | Colormap = 'viridis'):
    """
    Plot a spectrogram from the given list of sweeps.

    :param sweeps: List of sweeps to plot on the spectrogram.
    :param shading: The fill style for the quadrilateral
    :param cmap: The Colormap instance or registered colormap name used to map scalar data to colors.
    :return: matplotlib figure object and matplotlib Axes object.
    """
    if not isinstance(sweeps, list):
        raise TypeError("`sweeps` must be a list of type `ShrSweep`")
    if not sweeps:
        raise ValueError("Empty list")
    if not all(isinstance(sweep, ShrSweep) for sweep in sweeps):
        raise TypeError("`sweeps` must be a list of type `ShrSweep`")

    prefix, scale = si_scale(sweeps[0].f_min)

    pwr_scale = 'dBm' if sweeps[0].file_header.ref_scale == ShrScale.DBM else 'mV'

    pcm, fig, ax = _plot_spectrogram([sweep.sweep for sweep in sweeps], [sweep.timestamp for sweep in sweeps],
                                     sweeps[0].f_min / scale, sweeps[0].f_max / scale, sweeps[0].sweep_bins, shading,
                                     cmap)

    fig.colorbar(pcm, ax=ax, label=f'Power ({pwr_scale})')

    ax.set_xlabel(f'Frequency ({prefix}Hz)')
    ax.set_title('Spectrogram')
    ax.invert_yaxis()
    ax.get_yaxis().set_visible(False)

    plt.tight_layout()

    return fig, ax


def animate_spectrogram(sweeps: list[ShrSweep],
                        n_display: int = 256,
                        step_size: int = 1,
                        shading: Literal["flat", "nearest", "gouraud", "auto"] | None = 'auto',
                        cmap: str | Colormap = 'viridis',
                        interval: int = 200,
                        repeat_delay: int = 0,
                        repeat: bool = True,
                        title: str | None = None):
    """
    Generates an animated spectrogram given the sweep data.

    :param sweeps: List of sweeps to plot on the spectrogram.
    :param n_display: Number of sweeps to display at any given time.
    :param step_size: Number of sweeps to remove and add for each frame.
    :param shading: The fill style for the quadrilateral.
    :param cmap: The Colormap instance or registered colormap name used to map scalar data to colors.
    :param interval: Delay between frames in milliseconds.
    :param repeat_delay: The delay in milliseconds between consecutive animation runs, if repeat is True.
    :param repeat: Whether the animation repeats when the sequence of frames is completed.
    :param title: The title of the animation.
    :return: matplotlib FunAnimation object.
    """
    if not isinstance(sweeps, list):
        raise TypeError("`sweeps` must be a list of type `ShrSweep`")
    if not sweeps:
        raise ValueError("Empty list")
    if not all(isinstance(sweep, ShrSweep) for sweep in sweeps):
        raise TypeError("`sweeps` must be a list of type `ShrSweep`")

    prefix, scale = si_scale(sweeps[0].f_min)
    freq = np.linspace(sweeps[0].f_min / scale, sweeps[0].f_max / scale, sweeps[0].sweep_bins)
    min_val = min(sweeps, key=lambda swp__: swp__.sweep.min()).sweep.min()
    shape = sweeps[0].sweep.shape
    header = sweeps[0].file_header

    def generate_data(amplitude: list[np.ndarray], timestamps: list[int]):
        dt_ax = [dt.datetime.fromtimestamp(ts / 1000.0, dt.timezone.utc) for ts in timestamps]
        dt_ax = mdates.date2num(dt_ax)
        amp = np.vstack(amplitude)
        return amp, dt_ax

    _sweeps: list[list[ShrSweep]] = []
    for i in range(0, len(sweeps), step_size):
        swp = sweeps[i:i + n_display]
        if len(swp) < n_display:
            swp += [ShrSweep(ShrSweepHeader(), np.full(shape, min_val, dtype=np.float32), 0, header) for _ in
                    range(n_display - len(swp))]
        _sweeps.append(swp)

    # Initial frame
    pwr_, time_ = generate_data([swp.sweep for swp in _sweeps[0]], [swp.timestamp for swp in _sweeps[0]])

    fig, ax = plt.subplots()
    pcm = ax.pcolormesh(freq, time_, pwr_, shading=shading, cmap=cmap, vmin=header.ref_level - (header.div * 10),
                        vmax=header.ref_level)

    ax.invert_yaxis()
    ax.get_yaxis().set_visible(False)

    fig.colorbar(pcm, ax=ax, label=f"Amplitude ({'dBm' if header.ref_scale == ShrScale.DBM else 'mV'})")

    if title is None:
        title = "Spectrogram"

    ax.set_title(title)
    ax.set_xlabel(f"Frequency ({prefix}Hz)")

    def update(i_):
        sweep = _sweeps[i_]
        pwr, _ = generate_data([swp_.sweep for swp_ in sweep], [swp_.timestamp for swp_ in sweep])
        pcm.set_array(pwr.ravel())
        return [pcm]

    ani = animate.FuncAnimation(fig, update, frames=len(_sweeps), blit=False, interval=interval,
                                repeat_delay=repeat_delay, repeat=repeat)
    return ani
