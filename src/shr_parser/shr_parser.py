from .enumerations import *
from .metadata import ShrFileHeader, ShrSweepHeader
from .exceptions import ShrFileParserException, FileNotOpenError, ShrFileParserWarning
import struct
from io import BufferedReader
import numpy as np
from pathlib import Path

SHR_FILE_SIGNATURE = 0xAA10
SHR_FILE_VERSION = 0x2

METADATA_PACK = "HHL"
DATA_OFFSET_PACK = "Q"
SWEEP_PARAMETERS_PACK = "LLdd"
TITLE_PACK = "256s"
DEV_CONFIG_PACK = "ddddfLfLlllld"
TIME_AVG_PACK = "llll"
FREQ_AVG_PACK = "lldd"
RESERVED1_PACK = f"{16 * 4}s"
FILE_HEADER_PACK = (f"<{METADATA_PACK}{DATA_OFFSET_PACK}{SWEEP_PARAMETERS_PACK}{TITLE_PACK}{DEV_CONFIG_PACK}"
                    f"{TIME_AVG_PACK}{FREQ_AVG_PACK}{RESERVED1_PACK}")
FILE_HEADER_SIZE = struct.calcsize(FILE_HEADER_PACK)

TIMESTAMP_PACK = 'Q'
LATITUDE_PACK = 'd'
LONGITUDE_PACK = 'd'
ALTITUDE_PACK = 'd'
ADC_OVERFLOW_PACK = 'B'
RESERVED2_PACK = '15s'
SWEEP_HEADER_PACK = (f"<{TIMESTAMP_PACK}{LATITUDE_PACK}{LONGITUDE_PACK}{ALTITUDE_PACK}{ADC_OVERFLOW_PACK}"
                     f"{RESERVED2_PACK}")
SWEEP_HEADER_SIZE = struct.calcsize(SWEEP_HEADER_PACK)


class ShrSweep:
    """
    Frequency sweep information.
    """

    def __init__(self, header: ShrSweepHeader, sweep: np.array, n: int, file_header: ShrFileHeader):
        """
        Initializer.
        :param header: Sweep header
        :param sweep: Sweep data
        :param n: Sweep index
        :param file_header: File header
        """
        self.__header: ShrSweepHeader = header
        self.__sweep: np.array = sweep
        self.__file_header = file_header
        self.__n = n

    @property
    def header(self):
        """Sweep header"""
        return self.__header

    @property
    def sweep(self):
        """Sweep data (np.array[np.float32])"""
        return self.__sweep

    @property
    def n(self):
        """The sweep id"""
        return self.__n

    @property
    def file_header(self):
        """The file header"""
        return self.__file_header

    @property
    def peak(self):
        """The maximum value from the sweep"""
        return self.__sweep.max()

    @property
    def timestamp(self):
        """The timestamp of the sweep in milliseconds since epoch"""
        return self.__header.timestamp

    @property
    def adc_overflow(self):
        """Flag indicating that the ADC overflowed."""
        return self.__header.adc_overflow

    @property
    def f_min(self):
        """Start frequency of the sweep (Hz)"""
        return self.__file_header.center_freq_hz - (self.__file_header.span_hz / 2.0)

    @property
    def f_max(self):
        """Stop frequency of the sweep (Hz)"""
        return self.__file_header.center_freq_hz + (self.__file_header.span_hz / 2.0)

    @property
    def sweep_bins(self):
        """Number of bins for each sweep"""
        return self.__file_header.sweep_length

    def __repr__(self):
        peak_idx = np.argmax(self.__sweep)
        peak_freq = self.__file_header.first_bin_freq_hz + (peak_idx * self.__file_header.bin_size_hz)
        peak_freq /= 1.0e6
        return (f"Sweep {self.__n}: Peak Freq {peak_freq:.6f} MHz, Peak Amplitude {float(self.__sweep[peak_idx]):.2f} "
                f"{'dBm' if self.__file_header.ref_scale == ShrScale.DBM else 'mV'}")


class ShrFileParser:
    """
    Class that parses Signal Hound Data Capture (SHR) files.

    :raises ShrFileParserException: If a problem occurred with parsing.
    :raises FileNotFoundError: If unable to open file for reading.
    :raises FileNotOpenError: If the file is not open.
    """

    def __init__(self, fname: str):
        """
        Initializer.
        :param fname: The name of the file to parse.
        """
        self.__fname = fname
        self.__f: BufferedReader | None = None
        self.__header = ShrFileHeader()

    def _open_file(self, fname: str):
        try:
            self.__f = open(fname, 'rb')
        except OSError:
            raise FileNotFoundError(fname)

        bytes_read = self.__f.read(FILE_HEADER_SIZE)
        if len(bytes_read) != FILE_HEADER_SIZE:
            self.__f.close()
            self.__f = None
            raise ShrFileParserException("Unable to read header")

        self.__header.from_tuple(struct.unpack(FILE_HEADER_PACK, bytes_read))

        if self.__header.signature != SHR_FILE_SIGNATURE:
            self.__f.close()
            self.__f = None
            raise ShrFileParserException("Invalid SHR file")

        if self.__header.version > SHR_FILE_VERSION:
            self.__f.close()
            self.__f = None
            raise ShrFileParserException(
                f"Tried parsing SHR file with version {self.__header.version}. Version {SHR_FILE_VERSION} "
                f"and lower is supported.")

        sweep_data_size = Path(fname).stat().st_size - FILE_HEADER_SIZE
        sz_per_sweep = (4 * self.__header.sweep_length) + SWEEP_HEADER_SIZE

        if sweep_data_size != (sz_per_sweep * self.__header.sweep_count):
            raise ShrFileParserWarning(f"{fname} reported {self.__header.sweep_count} sweeps in the file. "
                                       f"Found {sweep_data_size / sz_per_sweep} sweeps instead!")

    def __enter__(self):
        self._open_file(self.__fname)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        """
        Opens the SHR file for parsing.

        This does nothing if the file is already opened.

        :raises ShrFileParserException: If a problem occurred with parsing.
        :raises FileNotFoundError: If unable to open file for reading.
        """
        if self.__f is None:
            self._open_file(self.__fname)

    def close(self):
        """
        Closes the SHR file.

        This does nothing if the file is already closed.
        """
        if self.__f is not None:
            self.__f.close()
            self.__f = None

    @property
    def header(self) -> ShrFileHeader:
        """The SHR File Header Metadata"""
        if self.__f is None:
            raise FileNotOpenError()
        return self.__header

    def get_sweep_n(self, n: int) -> ShrSweep:
        """
        Retrieves a certain sweep from the SHR file.
        :param n: The ID of the sweep to retrieve.
        :return: The sweep information.

        :raises FileNotOpenError: If the SHR file is not open.
        :raises ValueError: If the sweep ID is out of range.
        :raises ShrFileParserException: If the sweep information was not read correctly.
        """
        if self.__f is None:
            raise FileNotOpenError()

        if n < 0 or n >= self.__header.sweep_count:
            raise ValueError("Invalid sweep number")

        sweep_size = (4 * self.__header.sweep_length)
        self.__f.seek(self.__header.data_offset + ((sweep_size + SWEEP_HEADER_SIZE) * n))

        header_bytes: bytes = self.__f.read(SWEEP_HEADER_SIZE)
        sweep_bytes: bytes = self.__f.read(4 * self.__header.sweep_length)

        if len(header_bytes) != SWEEP_HEADER_SIZE:
            raise ShrFileParserException("Invalid sweep header size")
        if len(sweep_bytes) != sweep_size:
            raise ShrFileParserException("Invalid sweep size")

        header = ShrSweepHeader()
        header.from_tuple(struct.unpack(SWEEP_HEADER_PACK, header_bytes))
        sweep = np.frombuffer(sweep_bytes, dtype=np.float32)

        return ShrSweep(header, sweep, n, self.__header)

    def get_all_sweeps(self) -> list[ShrSweep]:
        """
        Retrieve all the sweeps present in the file.
        :return: A list of sweeps.
        """
        return [self.get_sweep_n(n) for n in range(self.__header.sweep_count)]

    def __iter__(self):
        for n in range(self.__header.sweep_count):
            yield self.get_sweep_n(n)

    def __len__(self):
        if self.__f is not None:
            return self.__header.sweep_count
        return 0

    def __del__(self):
        self.close()
