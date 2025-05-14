import time
import serial
import paramiko
import logging

LOG = logging.getLogger("pi-dev.device")

class PiDevice:
    """
    Raspberry Pi 设备操作：串口启动检测和远程测试。
    """

    def wait_login(self, port: str = "/dev/ttyUSB0", baud: int = 115200, timeout: int = 120) -> bool:
        LOG.info("Waiting for login prompt on %s", port)
        deadline = time.time() + timeout
        buffer = ""
        prompt = "login:"
        try:
            with serial.Serial(port, baud, timeout=1) as ser:
                while time.time() < deadline:
                    data = ser.read(256)
                    if data:
                        buffer += data.decode(errors='ignore')
                        if prompt in buffer:
                            LOG.info("Login prompt detected")
                            return True
        except serial.SerialException as e:
            LOG.error("Serial error: %s", e)
        return False

    def run_test(self, host: str = "raspberrypi.local", user: str = "pi", password: str = "raspberry") -> bool:
        LOG.info("Running test on %s", host)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=host, username=user, password=password, timeout=10)
            stdin, stdout, stderr = ssh.exec_command('echo "#RESULT# PASS"')
            output = stdout.read().decode()
            LOG.debug("Test output: %s", output)
            return "#RESULT# PASS" in output
        except Exception as e:
            LOG.error("SSH test failed: %s", e)
            return False
        finally:
            ssh.close()
