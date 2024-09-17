import platform
import psutil
import socket
import subprocess
import threading
import logging
from datetime import timedelta
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SystemInfo:
    def __init__(self):
        self.info = {}

    def gather_info(self, options):
        logging.debug("Starting to gather system information.")
        tasks = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            if options.basic:
                tasks.append(executor.submit(self.get_basic_info))
            if options.memory:
                tasks.append(executor.submit(self.get_memory_info))
            if options.disk:
                tasks.append(executor.submit(self.get_disk_info))
            if options.network:
                tasks.append(executor.submit(self.get_network_info))
            if options.wifi:
                tasks.append(executor.submit(self.get_wifi_name))
            if options.battery:
                tasks.append(executor.submit(self.get_battery_status))
            if options.uptime:
                tasks.append(executor.submit(self.get_system_uptime))

            for future in as_completed(tasks):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f'Error in one of the tasks: {e}')

    def get_basic_info(self):
        try:
            self.info['System'] = platform.system()
            self.info['Node Name'] = platform.node()
            self.info['Release'] = platform.release()
            self.info['Version'] = platform.version()
            self.info['Machine'] = platform.machine()
            self.info['Processor'] = platform.processor()
            logging.debug('Basic information gathered successfully.')
        except Exception as e:
            logging.error(f'Error gathering basic info: {e}')

    def get_memory_info(self):
        try:
            virtual_memory = psutil.virtual_memory()
            self.info['Total Memory (GB)'] = virtual_memory.total / (1024 ** 3)
            self.info['Available Memory (GB)'] = virtual_memory.available / (1024 ** 3)
            logging.debug('Memory information gathered successfully.')
        except psutil.PsutilError as e:
            logging.error(f'Error gathering memory info: {e}')
        except Exception as e:
            logging.error(f'Unexpected error gathering memory info: {e}')

    def get_disk_info(self):
        try:
            disk_usage = psutil.disk_usage('/')
            self.info['Total Disk Space (GB)'] = disk_usage.total / (1024 ** 3)
            self.info['Used Disk Space (GB)'] = disk_usage.used / (1024 ** 3)
            self.info['Free Disk Space (GB)'] = disk_usage.free / (1024 ** 3)
            logging.debug('Disk information gathered successfully.')
        except psutil.PsutilError as e:
            logging.error(f'Error gathering disk info: {e}')
        except Exception as e:
            logging.error(f'Unexpected error gathering disk info: {e}')

    def get_network_info(self):
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            self.info['IP Address'] = ip_address
            interfaces = psutil.net_if_addrs()
            self.info['Network Interfaces'] = {iface: [addr.address for addr in addrs] for iface, addrs in interfaces.items()}
            logging.debug('Network information gathered successfully.')
        except socket.error as e:
            logging.error(f'Network error: {e}')
        except psutil.PsutilError as e:
            logging.error(f'Error gathering network info: {e}')
        except Exception as e:
            logging.error(f'Unexpected error gathering network info: {e}')

    def get_wifi_name(self):
        try:
            if platform.system() == "Windows":
                wifi_name = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
                for line in wifi_name.split('\n'):
                    if "SSID" in line:
                        self.info['Wi-Fi Name'] = line.split(":")[1].strip()
                        return
                self.info['Wi-Fi Name'] = 'Not connected'
            else:
                self.info['Wi-Fi Name'] = 'Not available on non-Windows systems'
            logging.debug('Wi-Fi information gathered successfully.')
        except subprocess.CalledProcessError as e:
            logging.error(f'Command failed with error: {e}')
            self.info['Wi-Fi Name'] = 'Error retrieving Wi-Fi name'
        except Exception as e:
            logging.error(f'Unexpected error gathering Wi-Fi info: {e}')
            self.info['Wi-Fi Name'] = 'Error retrieving Wi-Fi name'

    def get_battery_status(self):
        try:
            if platform.system() in ["Windows", "Linux"]:
                battery = psutil.sensors_battery()
                if battery:
                    self.info['Battery Status'] = f"{battery.percent}%"
                    self.info['Battery Plugged In'] = "Yes" if battery.power_plugged else "No"
                else:
                    self.info['Battery Status'] = 'Not available'
            else:
                self.info['Battery Status'] = 'Not applicable on this OS'
            logging.debug('Battery information gathered successfully.')
        except psutil.PsutilError as e:
            logging.error(f'Error gathering battery info: {e}')
        except Exception as e:
            logging.error(f'Unexpected error gathering battery info: {e}')

    def get_system_uptime(self):
        try:
            boot_time = psutil.boot_time()
            now = psutil.time.time()
            uptime = now - boot_time
            self.info['System Uptime'] = str(timedelta(seconds=int(uptime)))
            logging.debug('System uptime gathered successfully.')
        except psutil.PsutilError as e:
            logging.error(f'Error gathering system uptime: {e}')
        except Exception as e:
            logging.error(f'Unexpected error gathering system uptime: {e}')

def print_system_info(info):
    print("=== System Information ===")
    for key, value in info.items():
        if isinstance(value, (int, float)):
            value = f'{value:.2f}' if 'GB' in key else value
        elif isinstance(value, dict):
            value = "\n".join([f"  {k}: {', '.join(v)}" for k, v in value.items()])
        print(f"{key}: {value}")

def main():
    parser = ArgumentParser(description="Gather system information.")
    parser.add_argument('--basic', action='store_true', help='Gather basic system information')
    parser.add_argument('--memory', action='store_true', help='Gather memory information')
    parser.add_argument('--disk', action='store_true', help='Gather disk information')
    parser.add_argument('--network', action='store_true', help='Gather network information')
    parser.add_argument('--wifi', action='store_true', help='Gather Wi-Fi name')
    parser.add_argument('--battery', action='store_true', help='Gather battery status')
    parser.add_argument('--uptime', action='store_true', help='Gather system uptime')
    args = parser.parse_args()

    sys_info = SystemInfo()
    sys_info.gather_info(args)
    print_system_info(sys_info.info)

if __name__ == "__main__":
    main()
