import subprocess
import pytest
from unittest import mock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pi_devops.flash import flash


def test_flash_called_process_error():
    with mock.patch('pi_devops.flash.subprocess.run', side_effect=subprocess.CalledProcessError(returncode=1, cmd='rpi-imager')):
        with pytest.raises(subprocess.CalledProcessError):
            flash('image.img', '/dev/sdX')


