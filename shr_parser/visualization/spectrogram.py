import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from ..shr_parser import ShrSweep
from .units import si_scale
from ..enumerations import ShrScale


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


def spectrogram(sweeps: list[ShrSweep], shading='auto', cmap='viridis'):
    if not isinstance(sweeps, list):
        raise TypeError("`sweeps` must be a list of type `ShrSweep`")
    if not sweeps:
        raise ValueError("Empty list")
    if not all(isinstance(sweep, ShrSweep) for sweep in sweeps):
        raise TypeError("`sweeps` must be a list of type `ShrSweep`")

    prefix, scale = si_scale(sweeps[0].f_min)

    pwr_scale = 'dBm' if sweeps[0].file_header.ref_scale == ShrScale.DBM else 'mV'

    pcm, fig, ax = _plot_spectrogram([sweep.sweep for sweep in sweeps], [sweep.timestamp for sweep in sweeps],
                                     sweeps[0].f_min / scale, sweeps[0].f_max / scale, sweeps[0].sweep_bins, shading, cmap)

    fig.colorbar(pcm, ax=ax, label=f'Power ({pwr_scale})')

    ax.set_xlabel(f'Frequency ({prefix}Hz)')
    ax.set_title('Spectrogram')

    plt.tight_layout()

    return fig, ax
