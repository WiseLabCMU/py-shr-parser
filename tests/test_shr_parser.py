from shr_parser import *
import pytest
import pkg_resources


def test_open_file_does_not_exist():
    cut = ShrFileParser("dne.shr")
    with pytest.raises(FileNotFoundError):
        cut.open()
    assert cut._ShrFileParser__f is None


def test_empty_file(tmp_path):
    f = tmp_path / "empty.shr"
    f.write_text("")

    cut = ShrFileParser(str(f))
    with pytest.raises(ShrFileParserException):
        cut.open()
    assert cut._ShrFileParser__f is None


def test_incomplete_header(tmp_path):
    f = tmp_path / "incplt.shr"
    f.write_bytes(b'\x00' * 471)

    cut = ShrFileParser(str(f))
    with pytest.raises(ShrFileParserException):
        cut.open()
    assert cut._ShrFileParser__f is None


def test_bad_signature(tmp_path):
    f = tmp_path / "sig.shr"
    f.write_bytes(b'\x00' * 1024)

    cut = ShrFileParser(str(f))
    with pytest.raises(ShrFileParserException):
        cut.open()
    assert cut._ShrFileParser__f is None


def test_bad_version(tmp_path):
    f = tmp_path / "ver.shr"
    f.write_bytes(b'\x10\xAA\x03' + (b'\x00' * 1024))

    cut = ShrFileParser(str(f))
    with pytest.raises(ShrFileParserException):
        cut.open()
    assert cut._ShrFileParser__f is None


def test_incomplete_file(tmp_path):
    f = tmp_path / "incomplete.shr"
    f.write_bytes(
        b"\x10\xAA\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x10\x00\x00" + (
                    b"\x00" * 448))

    cut = ShrFileParser(str(f))
    with pytest.raises(ShrFileParserWarning):
        cut.open()
    assert cut._ShrFileParser__f is not None
    assert not cut._ShrFileParser__f.closed


def test_open_valid_file():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    cut = ShrFileParser(str(f))
    cut.open()
    assert cut._ShrFileParser__f is not None
    assert not cut._ShrFileParser__f.closed


def test_header_file_not_open():
    cut = ShrFileParser('foo.shr')
    with pytest.raises(FileNotOpenError):
        h = cut.header


def test_header():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        header = parser.header
        assert isinstance(header, ShrFileHeader)

    assert header.signature == 0xAA10
    assert header.version == 2
    assert header.data_offset == 472
    assert header.sweep_count == 417
    assert header.sweep_length == 16386
    assert header.first_bin_freq_hz == 2.9955e9
    assert header.bin_size_hz == 1220.703125
    assert header.center_freq_hz == 3.0055e9
    assert header.span_hz == 20e6
    assert header.rbw_hz == 10e3
    assert header.vbw_hz == 10e3
    assert header.ref_level == -20.0
    assert header.ref_scale == ShrScale.DBM
    assert header.div == 10.0
    assert header.window == ShrWindow.FLATTOP
    assert header.attenuation == 0
    assert header.gain == 0
    assert header.detector == ShrVideoDetector.AVERAGE
    assert header.processing_units == ShrVideoUnits.POWER
    assert header.window_bandwidth == 8.192
    assert header.decimation_type == ShrDecimationType.COUNT
    assert header.decimation_count == 1
    assert header.decimation_time_ms == 1000.0
    assert not header.channelize_enable
    assert header.channel_output_units == ShrChannelizerOutputUnits.DBM
    assert header.channel_center_hz == 100e6
    assert header.channel_width_hz == 20e6


def test_get_sweep_n_not_open():
    cut = ShrFileParser('foo.shr')
    with pytest.raises(FileNotOpenError):
        cut.get_sweep_n(0)


def test_get_sweep_n_bounds():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        with pytest.raises(ValueError):
            parser.get_sweep_n(-1)
        with pytest.raises(ValueError):
            parser.get_sweep_n(417)

        parser.get_sweep_n(0)
        parser.get_sweep_n(416)


def test_get_sweep_n_corrupted(tmp_path):
    f = tmp_path / "incomplete.shr"
    f.write_bytes(
        b"\x10\xAA\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x10\x00\x00" + (
                b"\x00" * 448))

    cut = ShrFileParser(str(f))
    try:
        cut.open()
    except ShrFileParserWarning:
        pass

    with pytest.raises(ShrFileParserException):
        cut.get_sweep_n(0)

    with pytest.raises(ValueError):
        cut.get_sweep_n(100)


def test_get_all_sweeps():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        sweeps = parser.get_all_sweeps()
        assert len(sweeps) == 417
    # No need to test errors since they are handled by `get_sweep_n()` test cases


def test_iter():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        i = 0
        for _ in parser:
            i += 1
        assert i == 417
    # Exceptions that can be thrown here are handled by other test cases


def test_len():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        assert len(parser) == 417


def test_no_sweeps(tmp_path):
    f = tmp_path / "no-sweeps.shr"
    f.write_bytes(b"\x10\xAA\x02\x00\x00\x00\x00\x00\xD8\x01\x00\x00\x00\x00\x00\x00" + (b"\x00" * 456))

    with ShrFileParser(str(f)) as parser:
        assert len(parser) == 0
        assert not parser.get_all_sweeps()
