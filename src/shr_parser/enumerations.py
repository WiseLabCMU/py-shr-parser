from enum import IntEnum


class ShrScale(IntEnum):
    """
    Input reference scales

    Members
    -------
    DBM: MilliDecibels (dBm)
    MV: Millivolts (mV)
    """

    DBM = 0
    MV = 1


class ShrWindow(IntEnum):
    """
    Window functions

    Members
    -------
    NUTTALL: Nuttall window
    FLATTOP: Flat top window
    GUASSIAN: Gaussian window
    """
    NUTTALL = 0
    FLATTOP = 1
    GAUSSIAN = 2


class ShrDecimationType(IntEnum):
    """
    Downsampling types

    Members
    -------
    TIME: Downsampled with respect to time
    COUNT: Downsampled with respect to counts
    """
    TIME = 0
    COUNT = 1


class ShrDecimationDetector(IntEnum):
    """
    Decimation detector

    Members
    -------
    AVERAGE: Samples are averaged
    MAXIMUM: Maximum taken from samples
    """
    AVERAGE = 0
    MAXIMUM = 1


class ShrChannelizerOutputUnits(IntEnum):
    """
    Channel serializer units

    Members
    -------
    DBM: MilliDecibels (dBm)
    DBMHZ: Power spectral density (dB/MHz)
    """
    DBM = 0
    DBMHZ = 1


class ShrVideoDetector(IntEnum):
    """
    Video acquisition detector

    Members
    -------
    MIN_MAX: Minimum and/or Maximum captured
    AVERAGE: Average
    """
    MIN_MAX = 0
    AVERAGE = 1


class ShrVideoUnits(IntEnum):
    """
    Video acquisition units

    Members
    -------
    LOG: Log
    VOLTAGE: Voltage
    POWER: Power
    SAMPLE: Sample
    """
    LOG = 0
    VOLTAGE = 1
    POWER = 2
    SAMPLE = 3
