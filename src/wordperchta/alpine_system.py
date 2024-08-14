import subprocess
import sys
import os

class AlpineSystem:
    def __init__(self):
        self.required_packages = ['nginx', 'php-fpm', 'mariadb', 'certbot', 'certbot-nginx']
        self.services = ['nginx', 'mariadb', 'php-fpm7']

    def run_command(self, command):
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {command}")
            print(f"Error details: {e}")
            sys.exit(1)

    def is_installed(self, package):
        return subprocess.run(['which', package], stdout=subprocess.DEVNULL).returncode == 0

    def install_package(self, package):
        print(f"Installing {package}...")
        self.run_command(f"apk add {package}")

    def secure_mariadb(self):
        print("Securing MariaDB...")
        self.run_command("mysql_secure_installation")

    def secure_nginx(self):
        print("Securing Nginx...")
        nginx_conf = "/etc/nginx/nginx.conf"
        with open(nginx_conf, 'a') as f:
            f.write("\nserver_tokens off;\n")
        self.run_command("nginx -t && rc-service nginx reload")

    def setup_system(self):
        for package in self.required_packages:
            if not self.is_installed(package):
                self.install_package(package)

        for service in self.services:
            self.run_command(f"rc-service {service} start")
            self.run_command(f"rc-update add {service}")

        if not os.path.exists("/root/.my.cnf"):
            self.secure_mariadb()
        self.secure_nginx()

        self.setup_ssl_renewal()

    def setup_ssl_renewal(self):
        self.run_command("(crontab -l 2>/dev/null; echo \"0 12 * * * /usr/bin/certbot renew --quiet\") | crontab -")