================
pySHRParser API
================

.. module:: shr_parser

Classes
=======
.. class:: ShrFileParser

    .. method:: __init__(fname: str)

        :param fname:
            File path or file name

        Initializes the parser parameters. This does not automatically
        open the file.

    .. method:: open()

        :exception ShrFileParserException:
            Will be raised if a problem occurred when parsing the header.

        :exception FileNotFoundError:
            Will be raised if the file was not found.

        Opens the SHR file for parsing. This will automatically parse the
        header from the file upon opening.

        .. note::

            This does nothing if the file is already open.

    .. method:: close()

        Closes the SHR file.

        .. note::

            This does nothing if the file is already closed.

    .. method:: get_sweep_n(n: int) -> ShrSweep

        :param n:
            The sweep index to fetch from the file.

        :return:
            The sweep information.

        :rtype:
            ShrSweep

        :exception FileNotOpenError:
            If the SHR file is not open.

        :exception ValueError:
            If the sweep index is out of range.

        :exception ShrFileParserException:
            If the sweep information could not be read and parsed.

        Loads a certain sweep from the SHR file.

    .. method:: get_all_sweeps() -> list[ShrSweep]

        :return:
            All the sweeps in the SHR file.

        :rtype:
            list[ShrSweep]

        :exception FileNotOpenError:
            If the SHR file is not open.

        :exception ValueError:
            If the sweep index is out of range.

        :exception ShrFileParserException:
            If the sweep information could not be read and parsed.

    .. attribute:: header

        :getter: SHR file header metadata.
        :type: ShrFileHeader
        :exception FileNotOpenError: If the file is not open.

        Return the parsed SHR file header metadata.

    .. method:: __iter__()

        :return:
            The current sweep

        :rtype:
            ShrSweep

        Fetches all the sweeps in the file in order.

    .. method:: __len__()

        :return:
            The number of sweeps stored in the file

        :rtype:
            int

        The number of sweeps in the SHR file.

    .. method:: __del__()

        Destructor, closes the SHR file when the instance is freed

    .. method:: __enter__()

        :returns: ShrFileParser instance

        Returns the instance that was used in the ``with`` statement. This will
        open the file automatically.

        Example:

        >>> with ShrFileParser("foo.shr") as f:
        ...     x = f.read_all_sweeps()

    .. method:: __exit__(exc_type, exc_val, exc_tb)

        Closes the file (exceptions are not handled by ``__exit__``).

.. class:: ShrSweep

    .. method:: __init__(header: ShrSweepHeader, sweep: numpy.ndarray, n: int, file_header: ShrFileHeader)

        :param header:
            The sweep header.

        :param sweep:
            The sweep data.

        :param n:
            The sweep index.

        :param file_header:
            Copy of the file header.

        Initializes the data class for the sweep information.

    .. attribute:: header

        :getter: The sweep metadata.
        :type: ShrSweepHeader

        Return the sweep header for this specific sweep.

    .. attribute:: sweep

        :getter: The sweep data.
        :type: numpy.ndarray[numpy.single]

        Return the sweep data for this specific sweep.

    .. attribute:: n

        :getter: The sweep index.
        :type: int

        Return the index that this sweep is associated with.

    .. attribute:: file_header

        :getter: The file header.
        :type: ShrFileHeader

        Return the file header associated with this sweep.

    .. attribute:: peak

        :getter: The sweep data maximum.
        :type: numpy.single

        Return the sweep data maximum value.

    .. attribute:: timestamp

        :getter: The sweep timestamp.
        :type: int

        Return the timestamp of the sweep in milliseconds since last epoch.

    .. attribute:: adc_overflow

        :getter: Flag indicating that the ADC overflowed during the sweep.
        :type: bool

        Return the flag indicating that the ADC overflowed during the sweep.

    .. attribute:: f_min

        :getter: The starting frequency of the sweep.
        :type: float

        Return the start frequency of the sweep (Hz).

    .. attribute:: f_max

        :getter: The stop frequency of the sweep.
        :type: float

        Return the stop frequency of the sweep (Hz).

    .. attribute:: sweep_bins

        :getter: The number of frequency bins for each sweep.
        :type: int

        Return the number of frequency bins for each sweep.

Header Metadata Classes
=======================

.. class:: ShrFileHeader

    .. attribute:: signature

        :type: int

        The file signature.

    .. attribute:: version

        :type: int

        The SHR format version.

    .. attribute:: data_offset

        :type: int

        Byte offset where the sweep data starts.

    .. attribute:: title

        :type: bytes

        Title of the file.

    Sweep Parameters:

    .. attribute:: sweep_count

        :type: int

        The number of sweeps performed.

    .. attribute:: sweep_length

        :type: int

        Number of entries in each sweep.

    .. attribute:: first_bin_freq_hz

        :type: float

        Sweep start frequency (Hz).

    .. attribute:: bin_size_hz

        :type: float

        Bandwidth of each bin (Hz).

    Device configuration at time of capture:

    .. attribute:: center_freq_hz

        :type: float

        The center frequency of the captured data (Hz).

    .. attribute:: span_hz

        :type: float

        Span of frequency being evaluated (Hz).

    .. attribute:: rbw_hz

        :type: float

        Resolution bandwidth (Hz).

    .. attribute::  vbw_hz

        :type: float

        Video bandwidth (Hz).

    .. attribute:: ref_level

        :type: float

        The ADC reference level (dBm/mV depending on scale).

    .. attribute:: ref_scale

        :type: ShrScale

        The ADC reference scale.

    .. attribute:: div

        :type: float

        The division scale for the spectrum graph (dB). This is used by Spike to show the grid on the
        horizontal scale. For example, if the reference level is set to -20dB and has a div of 10dB, then grid lines
        will be shown at -30dB, -40dB, and so on.

    .. attribute:: window

        :type: ShrWindow

        The RBW shape.

    .. attribute:: attenuation

        :type: int

        Amplitude attenuation.

    .. attribute:: gain

        :type: int

        Amplitude gain.

    .. attribute:: detector

        :type: ShrVideoDetector

        Video acquisition detector.

    .. attribute:: processing_units

        :type: ShrVideoUnits

        Video processing units.

    .. attribute:: window_bandwidth

        :type: float

        The window bandwidth in bins.

    Time averaging configuration:

    .. attribute:: decimation_type

        :type: ShrDecimationType

        The downsampling type.

    .. attribute:: decimation_detector

        :type: ShrDecimationDetector

        Downsampling detection.

    .. attribute:: decimation_count

        :type: int

        Amount of downsamples taken.

    .. attribute:: decimation_time_ms

        :type: int

        Downsampling time (ms).

    Frequency averaging configuration:

    .. attribute:: channelize_enable

        :type: bool

        Channelizer enable.

    .. attribute:: channel_output_units

        :type: ShrChannelizerOutputUnits

        Channelizer units.

    .. attribute:: channel_center_hz

        :type: float

        Center frequency of a channel (Hz).

    .. attribute:: channel_width_hz

        :type: float

        Channel spacing (Hz).

.. class:: ShrSweepHeader

    .. attribute:: timestamp

        :type: int

        The timestamp of the sweep in milliseconds since epoch.

    .. attribute:: latitude

        :type: float

        Latitude.

    .. attribute:: longitude

        :type: float

        Longitude.

    .. attribute:: altitude

        :type: float

        Altitude in meters.

    .. attribute:: adc_overflow

        :type: bool

        Flag indicating that the ADC overflowed.

Exceptions
==========

.. class:: ShrFileParserException

    Base exception class for ShrFileParser errors

.. class:: FileNotOpenError

    File not open error

Enumerations
============

.. class:: ShrScale

    Input reference scales

    Members
    ^^^^^^^
    DBM: MilliDecibels (dBm)

    MV: Millivolts (mV)

.. class:: ShrWindow

    Window functions

    Members
    ^^^^^^^
    NUTTALL: Nuttall window

    FLATTOP: Flat top window

    GUASSIAN: Gaussian window

.. class:: ShrDecimationType

    Downsampling types

    Members
    ^^^^^^^
    TIME: Downsampled with respect to time

    COUNT: Downsampled with respect to counts

.. class:: ShrDecimationDetector

    Decimation detector

    Members
    ^^^^^^^
    AVERAGE: Samples are averaged

    MAXIMUM: Maximum taken from samples

.. class:: ShrChannelizerOutputUnits

    Channel serializer units

    Members
    ^^^^^^^
    DBM: MilliDecibels (dBm)

    DBMHZ: Power spectral density (dB/MHz)

.. class:: ShrVideoDetector

    Video acquisition detector

    Members
    ^^^^^^^
    MIN_MAX: Minimum and/or Maximum captured

    AVERAGE: Average

.. class:: ShrVideoUnits

    Video acquisition units

    Members
    ^^^^^^^
    LOG: Log

    VOLTAGE: Voltage

    POWER: Power

    SAMPLE: Sample

Functions
=========

.. module:: shr_parser.visualization

.. function:: spectrogram(sweeps: list[ShrSweep], shading: Literal["flat", "nearest", "gouraud", "auto"] | None = 'auto', cmap: str | matplotlib.colors.Colormap = 'viridis') -> tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]

    Plot a spectrogram from the given list of sweeps.

    :param sweeps: List of sweeps to plot on the spectrogram.
    :param shading: The fill style for the quadrilateral.
    :param cmap: The Colormap instance or registered colormap name used to map scalar data to colors.

    :rtype: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]

.. function:: plot_spectrum(sweep: ShrSweep) -> tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]

    Plot the frequency spectrum of a certain sweep.

    :param sweep: The frequency sweep to plot.

    :rtype: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]
