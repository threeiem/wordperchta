import subprocess
import os
from wordperchta.alpine_system import AlpineSystem
from wordperchta.security_manager import SecurityManager

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error details: {e}")
        exit(1)

def setup_environment():
    alpine_system = AlpineSystem()
    security_manager = SecurityManager()

    alpine_system.setup_system()
    alpine_system.configure_nginx()
    alpine_system.configure_php()
    alpine_system.configure_mysql()

    security_manager.secure_nginx()
    security_manager.secure_php()
    security_manager.secure_mysql()

    setup_test_virtual_hosts()

def setup_test_virtual_hosts():
    test_sites = [
        {"domain": "test1.local", "vanity_hosts": ["www", "blog"]},
        {"domain": "test2.local", "vanity_hosts": ["www", "shop"]}
    ]

    for site in test_sites:
        run_command(f"python3 scripts/manage_sites.py --add-site {site['domain']} --vanity {' '.join(site['vanity_hosts'])}")

if __name__ == "__main__":
    setup_environment()