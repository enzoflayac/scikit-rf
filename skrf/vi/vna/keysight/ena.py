from __future__ import annotations

from enum import Enum
from logging import getLogger

import skrf
from skrf.vi import vna
from skrf.vi.validators import (
    BooleanValidator,
    EnumValidator,
    FreqValidator,
    IntValidator,
)
from skrf.vi.vna import VNA

logger = getLogger(__name__)


class SweepType(Enum):
    LINEAR = "LIN"
    LOG = "LOG"
    POWER = "POW"
    CW = "CW"
    SEGMENT = "SEGM"
    PHASE = "PHAS"


class ENA(VNA):
    """
    Keysight ENA.

    ENA Models
    ==========
    E5061B, E5071C
    """

    class Channel(vna.Channel):
        def __init__(self, parent: ENA, cnum: int, cname: str | None = None):
            super().__init__(parent, cnum, cname)

            if cnum != 1:
                default_msmnt = f"CH{self.cnum}_S11_1"
                self.create_measurement(default_msmnt, "S11")

        freq_start = VNA.command(
            get_cmd="SENS<self:cnum>:FREQ:STAR?",
            set_cmd="SENS<self:cnum>:FREQ:STAR <arg>",
            doc="""The start frequency [Hz]""",
            validator=FreqValidator(),
        )

        freq_stop = VNA.command(
            get_cmd="SENS<self:cnum>:FREQ:STOP?",
            set_cmd="SENS<self:cnum>:FREQ:STOP <arg>",
            doc="""The stop frequency [Hz]""",
            validator=FreqValidator(),
        )

        npoints = VNA.command(
            get_cmd="SENS<self:cnum>:SWE:POIN?",
            set_cmd="SENS<self:cnum>:SWE:POIN <arg>",
            doc="""The number of frequency points. Sets the frequency step as a
                side effect
            """,
            validator=IntValidator(),
        )

        if_bandwidth = VNA.command(
            get_cmd="SENS<self:cnum>:BAND?",
            set_cmd="SENS<self:cnum>:BAND <arg>",
            doc="""The IF bandwidth [Hz]""",
            validator=FreqValidator(),
        )

        sweep_type = VNA.command(
            get_cmd="SENS<self:cnum>:SWE:TYPE?",
            set_cmd="SENS<self:cnum>:SWE:TYPE <arg>",
            doc="""The type of sweep (linear, log, etc)""",
            validator=EnumValidator(SweepType),
        )

        @property
        def freq_step(self) -> int:
            raise NotImplementedError()

        @freq_step.setter
        def freq_step(self, value: int):
            raise NotImplementedError()

        @property
        def frequency(self) -> skrf.Frequency:
            f = skrf.Frequency(
                start=self.freq_start,
                stop=self.freq_stop,
                npoints=self.npoints,
                unit="hz",
            )
            return f

        @frequency.setter
        def frequency(self, f: skrf.Frequency) -> None:
            self.freq_start = f.start
            self.freq_stop = f.stop
            self.npoints = f.npoints

        @property
        def calibration(self) -> skrf.Calibration:
            raise NotImplementedError()

        @calibration.setter
        def calibration(self, cal: skrf.Calibration) -> None:
            raise NotImplementedError()

