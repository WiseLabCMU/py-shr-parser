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
