from shr_parser import *
import pkg_resources


def test_sweep_header():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        sweeps = parser.get_all_sweeps()
        file_header = parser.header

    swp_id = []
    for sweep in sweeps:
        assert isinstance(sweep.header, ShrSweepHeader)
        assert sweep.timestamp == sweep.header.timestamp
        assert sweep.adc_overflow == sweep.header.adc_overflow
        assert sweep.file_header == file_header
        swp_id.append(sweep.n)

    assert len(swp_id) == len(set(swp_id))


def test_sweep_f_attr():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        sweeps = parser.get_all_sweeps()
        file_header = parser.header

    for sweep in sweeps:
        assert sweep.sweep_bins == file_header.sweep_length
        assert sweep.f_min == 2.9955e9
        assert sweep.f_max == 3.0155e9


def test_sweep_sweep_data():
    f = pkg_resources.resource_filename(__name__, 'test_files/sweep0v2.shr')

    with ShrFileParser(str(f)) as parser:
        sweeps = parser.get_all_sweeps()
        file_header = parser.header

    for sweep in sweeps:
        swp = sweep.sweep
        assert len(swp) == file_header.sweep_length
        assert float(sweep.peak) == float(max(swp.tolist()))
