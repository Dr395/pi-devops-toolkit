import typer
import logging
from .flash import flash
from .device import PiDevice

app = typer.Typer()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

@app.command()
def flash_test(
    img: str = typer.Argument(..., help="Path to Raspberry Pi image file"),
    port: str = typer.Option("/dev/ttyUSB0", help="Serial port for boot detection"),
    target: str = typer.Option("/dev/sdX", help="SD card device to flash")
):
    """
    烧写镜像，等待启动，然后运行简单测试，PASS/FAIL 输出。
    """
    typer.secho(f"[FLASH] Flashing {img} to {target}", fg=typer.colors.GREEN)
    flash(img, target)

    dev = PiDevice()
    typer.secho("[BOOT] Waiting for login prompt...", fg=typer.colors.YELLOW)
    if not dev.wait_login(port):
        typer.secho("Boot FAIL", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho("[TEST] Running remote test...", fg=typer.colors.YELLOW)
    if dev.run_test():
        typer.secho("PASS", fg=typer.colors.GREEN)
        raise typer.Exit(code=0)
    else:
        typer.secho("FAIL", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
