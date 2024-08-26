import subprocess

class SecurityManager:
    def run_command(self, command):
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {command}")
            print(f"Error details: {e}")
            exit(1)

    def secure_nginx(self):
        self.run_command("sed -i 's/# server_tokens off;/server_tokens off;/' /etc/nginx/nginx.conf")
        security_headers = """
        add_header X-Frame-Options SAMEORIGIN;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        """
        self.run_command(f"echo '{security_headers}' >> /etc/nginx/nginx.conf")

    def secure_php(self):
        php_ini_path = "/etc/php82/php.ini"
        self.run_command(f"sed -i 's/expose_php = On/expose_php = Off/' {php_ini_path}")
        self.run_command(f"sed -i 's/allow_url_fopen = On/allow_url_fopen = Off/' {php_ini_path}")
        self.run_command(f"sed -i 's/display_errors = On/display_errors = Off/' {php_ini_path}")

    def secure_mysql(self):
        self.run_command("mysql_secure_installation")