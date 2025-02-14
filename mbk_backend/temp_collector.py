import os
import subprocess
import time
import sys
import django
import random

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbk_backend.settings')
django.setup()

from monitor.models import Temperature

def get_temperatures():
    try:
        # Run the iStats command
        result = subprocess.run(['istats'], capture_output=True, text=True)
        output = result.stdout

        # Parse CPU and GPU temperatures
        cpu_temp_line = [line for line in output.split('\n') if "CPU temp:" in line]
        gpu_temp_line = [line for line in output.split('\n') if "Battery temp:" in line]

        cpu_temp = float(cpu_temp_line[0].split(':')[1].strip().split('°')[0]) if cpu_temp_line else None
        battery_temp = float(gpu_temp_line[0].split(':')[1].strip().split('°')[0]) if gpu_temp_line else None

        return {"cpu_temp": cpu_temp, "battery_temp": battery_temp}
    except Exception as e:
        print(f"Error fetching temperatures: {e}")
        return None


def get_random_temperatures():
    return {
        "cpu_temp": round(random.uniform(40.0, 80.0), 1),
        "battery_temp": round(random.uniform(38.0, 70.0), 1),
    }


def collect_and_store_data():
    while True:
        # temps = get_temperatures()
        temps = get_random_temperatures()
        if temps:
            Temperature.objects.create(cpu_temp=temps['cpu_temp'], battery_temp=temps['battery_temp'])
            print(f"Data saved: CPU {temps['cpu_temp']}°C, Battery Temp {temps['battery_temp']}°C")
        time.sleep(10)  # Collect every 10 seconds

if __name__ == "__main__":
    collect_and_store_data()
