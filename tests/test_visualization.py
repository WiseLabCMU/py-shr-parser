from shr_parser import ShrFileParser
from shr_parser.visualization import *
import pytest
import pkg_resources


def test_spectrogram_errors():
    with pytest.raises(TypeError):
        spectrogram(69)

    with pytest.raises(ValueError):
        spectrogram([])

    with pytest.raises(TypeError):
        spectrogram([69])

    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        sweeps = parser.get_all_sweeps()

    sweeps += [69]

    with pytest.raises(TypeError):
        spectrogram(sweeps)


def test_animated_spectrogram_errors():
    with pytest.raises(TypeError):
        animate_spectrogram(69)

    with pytest.raises(ValueError):
        animate_spectrogram([])

    with pytest.raises(TypeError):
        animate_spectrogram([69])

    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        sweeps = parser.get_all_sweeps()

    sweeps += [69]

    with pytest.raises(TypeError):
        animate_spectrogram(sweeps)


def test_spectrum_errors():
    with pytest.raises(TypeError):
        plot_spectrum(69)


def test_animate_spectrum_errors():
    with pytest.raises(TypeError):
        animate_spectrum(69)

    with pytest.raises(ValueError):
        animate_spectrum([])

    with pytest.raises(TypeError):
        animate_spectrum([69])

    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        sweeps = parser.get_all_sweeps()

    sweeps += [69]

    with pytest.raises(TypeError):
        animate_spectrum(sweeps)
