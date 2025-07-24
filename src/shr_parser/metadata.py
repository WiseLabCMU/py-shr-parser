import dataclasses
from .enumerations import *


@dataclasses.dataclass
class ShrFileHeader:
    """
    SHR file header metadata.

    Attributes:
        signature (int): The file signature.
        version (int): The SHR format version.
        data_offset (int): Byte offset where the sweep data starts.
        sweep_count (int): The number of sweeps performed.
        sweep_length (int): Number of entries in each sweep.
        first_bin_freq_hz (float): Sweep start frequency (Hz).
        bin_size_hz (float): Bandwidth of each bin (Hz).
        title (bytes): Title of the file.
        center_freq_hz (float): The center frequency of the captured data (Hz).
        span_hz (float): Span of frequency being evaluated (Hz).
        rbw_hz (float): Resolution bandwidth (Hz).
        vbw_hz (float): Video bandwidth (Hz).
        ref_level (float): The ADC reference level (dBm/mV depending on scale)
        ref_scale (ShrScale): The ADC reference scale.
        div (float): The division scale for the spectrum graph (dB). This is used by Spike to show the grid on the
        horizontal scale. For example, if the reference level is set to -20dB and has a div of 10dB, then grid lines
        will be shown at -30dB, -40dB, and so on.
        window (ShrWindow): The RBW shape.
        attenuation (int): Amplitude attenuation.
        gain (int): Amplitude gain.
        detector (ShrVideoDetector): Video acquisition detector.
        processing_units (ShrVideoUnits): Video processing units.
        window_bandwidth (float): The window bandwidth in bins.
        decimation_type (ShrDecimationType): The downsampling type.
        decimation_detector (ShrDecimationDetector): Downsampling detection.
        decimation_count (int): Amount of downsamples taken.
        decimation_time_ms (int): Downsampling time (ms).
        channelize_enable (bool): Channelizer enable.
        channel_output_units (ShrChannelizerOutputUnits):  Channelizer units.
        channel_center_hz (float): Center frequency of a channel (Hz).
        channel_width_hz (float): Channel spacing (Hz).
    """
    signature: int = 0  # 2 bytes
    version: int = 0  # 2 bytes

    # Byte offset where the sweep data starts
    data_offset: int = 0  # 8 bytes

    # Sweep parameters
    sweep_count: int = 0  # 4 bytes
    sweep_length: int = 0  # 4 bytes
    first_bin_freq_hz: float = 0  # 8 bytes
    bin_size_hz: float = 0  # 8 bytes

    # 127 total characters plus NULL
    title: bytes = b""  # 256 bytes

    # Device configuration at time of capture
    center_freq_hz: float = 0  # 8 bytes
    span_hz: float = 0  # 8 bytes
    rbw_hz: float = 0  # 8 bytes
    vbw_hz: float = 0  # 8 bytes
    ref_level: float = 0  # 4 bytes; dBm/mV depending on scale
    ref_scale: ShrScale = 0  # 4 bytes
    div: float = 0  # 4 bytes
    window: ShrWindow = 0  # 4 bytes
    attenuation: int = 0  # 4 bytes
    gain: int = 0  # 4 bytes
    detector: ShrVideoDetector = 0  # 4 bytes
    processing_units: ShrVideoUnits = 0  # 4 bytes
    window_bandwidth: float = 0  # 8 bytes; in bins

    # Time averaging configuration
    decimation_type: ShrDecimationType = 0  # 4 bytes
    decimation_detector: ShrDecimationDetector = 0  # 4 bytes
    decimation_count: int = 0  # 4 bytes
    decimation_time_ms: int = 0  # 4 bytes

    # Frequency averaging configuration
    channelize_enable: bool = False  # 4 bytes
    channel_output_units: ShrChannelizerOutputUnits = 0  # 4 bytes
    channel_center_hz: float = 0  # 8 bytes
    channel_width_hz: float = 0  # 8 bytes

    def from_tuple(self, d: tuple[any, ...]):
        """
        Extracts the file header data represented tuple. This is for internal use only.

        :param d: The tuple representing the SHR file header.
        """
        if not isinstance(d, tuple):
            raise TypeError("`d` must be a tuple type")
        if len(d) != 31:
            print(len(d))
            raise ValueError("Invalid data")
        self.signature = d[0]
        self.version = d[1]
        self.data_offset = d[3]
        self.sweep_count = d[4]
        self.sweep_length = d[5]
        self.first_bin_freq_hz = d[6]
        self.bin_size_hz = d[7]
        self.title = d[8]
        self.center_freq_hz = d[9]
        self.span_hz = d[10]
        self.rbw_hz = d[11]
        self.vbw_hz = d[12]
        self.ref_level = d[13]
        self.ref_scale = ShrScale(d[14])
        self.div = d[15]
        self.window = ShrWindow(d[16])
        self.attenuation = d[17]
        self.gain = d[18]
        self.detector = ShrVideoDetector(d[19])
        self.processing_units = ShrVideoUnits(d[20])
        self.window_bandwidth = d[21]
        self.decimation_type = ShrDecimationType(d[22])
        self.decimation_detector = ShrDecimationDetector(d[23])
        self.decimation_count = d[24]
        self.decimation_time_ms = d[25]
        self.channelize_enable = d[26] == 1
        self.channel_output_units = ShrChannelizerOutputUnits(d[27])
        self.channel_center_hz = d[28]
        self.channel_width_hz = d[29]

    def __repr__(self):
        ret = (f"Sweep Count: {self.sweep_count}\n"
               f"Sweep Size: {self.sweep_length}\n"
               f"Sweep Start Frequency: {self.first_bin_freq_hz}\n"
               f"Sweep Bin Size: {self.bin_size_hz}\n"
               f"Sweep Frequency Range: {(self.center_freq_hz - (self.span_hz / 2.0)) * 1.0e-6} MHz to "
               f"{(self.center_freq_hz + (self.span_hz / 2.0)) * 1.0e-6} MHz\n"
               f"RBW: {self.rbw_hz * 1.0e-3} kHz\n"
               f"VBW: {self.vbw_hz * 1.0e-3} kHz\n"
               f"Reference Level: {self.ref_level} {'dBm' if self.ref_scale == ShrScale.DBM else 'mV'}\n")
        if self.decimation_type == ShrDecimationType.COUNT:
            ret += (f"{'Averaged' if self.decimation_detector == ShrDecimationDetector.AVERAGE else 'Max held'} "
                    f"{self.decimation_count} trace(s) per output trace\n")
        else:
            ret += (f"{'Averaged' if self.decimation_detector == ShrDecimationDetector.AVERAGE else 'Max held'} for "
                    f"{self.decimation_count:.2f} seconds per output trace\n")
        ret += f"Channelize Enabled: {self.channelize_enable}"
        return ret


@dataclasses.dataclass
class ShrSweepHeader:
    """
    Sweep data header

    Attributes:
        timestamp (int): The timestamp of the sweep in milliseconds since epoch
        latitude (float): Latitude
        longitude (float): Longitude
        altitude (float): Altitude in meters.
        adc_overflow (bool): Flag indicating that the ADC overflowed.
    """
    timestamp: int = 0  # 8 bytes; milliseconds since epoch
    latitude: float = 0  # 8 bytes
    longitude: float = 0  # 8 bytes
    altitude: float = 0  # 8 bytes; meters
    adc_overflow: bool = 0  # 1 byte

    def from_tuple(self, d: tuple[any, ...]):
        """
        Extracts the sweep header data represented tuple. This is for internal use only.

        :param d: The tuple representing a SHR sweep header.
        """
        if not isinstance(d, tuple):
            raise TypeError("`d` must be a tuple type")
        if len(d) != 6:
            print(len(d))
            raise ValueError("Invalid data")
        self.timestamp = d[0]
        self.latitude = d[1]
        self.longitude = d[2]
        self.altitude = d[3]
        self.adc_overflow = d[4] == 1
