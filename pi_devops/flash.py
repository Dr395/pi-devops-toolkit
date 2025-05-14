import subprocess
import logging

LOG = logging.getLogger("pi-dev.flash")

def flash(img_path: str, target: str = "/dev/sdX") -> None:
    """
    使用 rpi-imager CLI 烧写 Raspberry Pi 镜像到 SD 卡。
    """
    cmd = [
        "rpi-imager",
        "--cli",
        "--img",
        img_path,
        "--target",
        target
    ]
    LOG.info("Flashing image %s to %s", img_path, target)
    subprocess.run(cmd, check=True)
    LOG.info("Flash complete")
