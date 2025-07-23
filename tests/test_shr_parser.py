from shr_parser import ShrFileParser, ShrFileParserException, ShrFileParserWarning
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
    f.write_bytes(b"\x10\xAA\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x10\x00\x00" + (b"\x00" * 448))

    cut = ShrFileParser(str(f))
    with pytest.raises(ShrFileParserWarning):
        cut.open()
    assert cut._ShrFileParser__f is not None
    assert not cut._ShrFileParser__f.closed


def test_open_valid_file():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0.shr')

    cut = ShrFileParser(str(f))
    cut.open()
    assert cut._ShrFileParser__f is not None
    assert not cut._ShrFileParser__f.closed
