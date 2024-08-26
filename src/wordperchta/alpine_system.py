"""Module containing the AlpineSystem class."""

import subprocess
import sys
import os

class AlpineSystem:
    """Class representing an Alpine Linux system."""
    def __init__(self):
        self.required_packages = [
            'nginx',
            'php82',
            'php82-fpm',
            'php82-mysqli',
            'php82-json',
            'php82-curl',
            'php82-dom',
            'php82-xml',
            'php82-mbstring',
            'php82-gd',
            'mariadb',
            'mariadb-client',
            'certbot',
            'certbot-nginx'
        ]
        self.services = ['nginx', 'mariadb', 'php-fpm82']

    def run_command(self, command):
        """Function to run a shell command."""
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {command}")
            print(f"Error details: {e}")
            sys.exit(1)

    def is_installed(self, package):
        """Function to check if a package is installed."""
        return subprocess.run(['which', package], stdout=subprocess.DEVNULL, check=False).returncode == 0

    def install_package(self, package):
        """Function to install a package using the apk package manager."""
        print(f"Installing {package}...")
        self.run_command(f"apk add {package}")

    def setup_system(self):
        """Function to setup the web hosting system."""
        self.run_command("apk update")
        for package in self.required_packages:
            if not self.is_installed(package):
                self.install_package(package)

        for service in self.services:
            self.run_command(f"rc-service {service} start")
            self.run_command(f"rc-update add {service}")

    def configure_nginx(self):
        """Function to configure Nginx."""
        nginx_conf = """
        user nginx;
        worker_processes auto;
        error_log /var/log/nginx/error.log warn;
        pid /var/run/nginx.pid;

        events {
            worker_connections 1024;
        }

        http {
            include /etc/nginx/mime.types;
            default_type application/octet-stream;
            access_log /var/log/nginx/access.log;
            sendfile on;
            keepalive_timeout 65;
            include /etc/nginx/conf.d/*.conf;
        }
        """
        with open("/etc/nginx/nginx.conf", "w", encoding="utf-8") as f:
            f.write(nginx_conf)

    def configure_php(self):
        """Function to configure PHP."""
        php_fpm_conf = """
        [global]
        pid = /run/php-fpm82.pid
        error_log = /var/log/php82/error.log

        [www]
        user = nginx
        group = nginx
        listen = /run/php/php82-fpm.sock
        listen.owner = nginx
        listen.group = nginx
        pm = dynamic
        pm.max_children = 5
        pm.start_servers = 2
        pm.min_spare_servers = 1
        pm.max_spare_servers = 3
        """
        with open("/etc/php82/php-fpm.d/www.conf", "w", encoding="UTF-8") as f:
            f.write(php_fpm_conf)

    def configure_mysql(self):
        """Function to configure MariaDB."""
        mysql_conf = """
        [mysqld]
        user = mysql
        datadir = /var/lib/mysql
        port = 3306
        log-bin = /var/lib/mysql/mysql-bin
        bind-address = 127.0.0.1
        """
        with open("/etc/my.cnf.d/mariadb-server.cnf", "w", encoding="UTF-8") as f:
            f.write(mysql_conf)

        if not os.path.exists("/var/lib/mysql/mysql"):
            self.run_command("mysql_install_db --user=mysql --datadir=/var/lib/mysql")

        self.run_command("rc-service mariadb start")
        self.run_command("mysqladmin -u root password 'your_secure_password'")

    def verify_php_version(self):
        """Function to verify that PHP 8.2 is installed."""
        result = subprocess.run(['php', '-v'], capture_output=True, text=True, check=False)
        if "PHP 8.2" not in result.stdout:
            print("Warning: PHP 8.2 is not installed or not the default version.")
            sys.exit(1)
