import sys
import types
from pathlib import Path
from unittest import mock

# Provide dummy 'serial' and 'paramiko' modules so pi_devops.device can import.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

serial_mod = types.ModuleType('serial')
class DummySerialException(Exception):
    pass
serial_mod.SerialException = DummySerialException
serial_mod.Serial = mock.MagicMock()
sys.modules['serial'] = serial_mod

paramiko_mod = types.ModuleType('paramiko')
# minimal attributes used by PiDevice.run_test; not needed here
sys.modules['paramiko'] = paramiko_mod

from pi_devops.device import PiDevice


def test_wait_login_serial_exception():
    device = PiDevice()
    with mock.patch('pi_devops.device.serial.Serial', side_effect=serial_mod.SerialException('err')):
        assert device.wait_login(port='/dev/ttyUSB0', timeout=1) is False


def test_wait_login_no_prompt():
    device = PiDevice()

    class DummySerial:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
        def read(self, size=1):
            return b""

    with mock.patch('pi_devops.device.serial.Serial', return_value=DummySerial()):
        assert device.wait_login(timeout=0.1) is False

