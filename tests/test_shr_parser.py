from shr_parser import ShrFileParser, ShrFileParserException, ShrFileParserWarning
import pytest


def test_open_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        cut = ShrFileParser("dne.shr")
        cut.open()


def test_empty_file(tmp_path):
    f = tmp_path / "empty.shr"
    f.write_text("")

    with pytest.raises(ShrFileParserException):
        cut = ShrFileParser(str(f))
        cut.open()


def test_incomplete_header(tmp_path):
    f = tmp_path / "incplt.shr"
    f.write_bytes(b'\x00' * 471)

    with pytest.raises(ShrFileParserException):
        cut = ShrFileParser(str(f))
        cut.open()


def test_bad_signature(tmp_path):
    f = tmp_path / "sig.shr"
    f.write_bytes(b'\x00' * 1024)

    with pytest.raises(ShrFileParserException):
        cut = ShrFileParser(str(f))
        cut.open()


def test_bad_version(tmp_path):
    f = tmp_path / "ver.shr"
    f.write_bytes(b'\x10\xAA\x03' + (b'\x00' * 1024))

    with pytest.raises(ShrFileParserException):
        cut = ShrFileParser(str(f))
        cut.open()


def test_incomplete_file(tmp_path):
    f = tmp_path / "incomplete.shr"
    f.write_bytes(b"\x10\xAA\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x10\x00\x00" + (b"\x00" * 448))

    with pytest.raises(ShrFileParserWarning):
        cut = ShrFileParser(str(f))
        cut.open()
