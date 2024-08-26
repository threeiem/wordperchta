import os
import random
import string

class Domain:
    def __init__(self, name, vanity_hosts=None):
        self.name = name
        self.vanity_hosts = vanity_hosts or []
        self.db_name = f"wp_{name.replace('.', '_')}"
        self.db_user = f"wpuser_{name.replace('.', '_')}"
        self.db_pass = self.generate_password()
        self.wp_dir = f"/var/www/wordpress_{name}"

    @staticmethod
    def generate_password(length=16):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def setup_database(self, system):
        system.run_command(f"mysql -e \"CREATE DATABASE {self.db_name}; \
                            CREATE USER '{self.db_user}'@'localhost' IDENTIFIED BY '{self.db_pass}'; \
                            GRANT ALL PRIVILEGES ON {self.db_name}.* TO '{self.db_user}'@'localhost'; \
                            FLUSH PRIVILEGES;\"")

    def setup_wordpress(self, system):
        if not os.path.exists(self.wp_dir):
            system.run_command(f"wget -q -O /tmp/wordpress.tar.gz https://wordpress.org/latest.tar.gz")
            system.run_command(f"tar -xzf /tmp/wordpress.tar.gz -C /tmp")
            system.run_command(f"mv /tmp/wordpress {self.wp_dir}")
            system.run_command(f"chown -R nginx:nginx {self.wp_dir}")

    def configure_nginx(self, system):
        server_names = f"{self.name} www.{self.name} " + " ".join(f"{host}.{self.name}" for host in self.vanity_hosts)
        nginx_conf = f"/etc/nginx/conf.d/{self.name}.conf"
        config_content = f"""
server {{
    listen 80;
    server_name {server_names};
    root {self.wp_dir};
    index index.php;

    location / {{
        try_files $uri $uri/ /index.php?$args;
    }}

    location ~ \\.php$ {{
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
        fastcgi_index index.php;
        include fastcgi.conf;
    }}
}}
"""
        system.run_command(f"echo '{config_content}' > {nginx_conf}")
        system.run_command("nginx -t && rc-service nginx reload")

    def setup_ssl(self, system):
        ssl_domains = f"-d {self.name} -d www.{self.name} " + " ".join(f"-d {host}.{self.name}" for host in self.vanity_hosts)
        system.run_command(f"certbot --nginx {ssl_domains}")

    def add_vanity_host(self, host):
        if host not in self.vanity_hosts:
            self.vanity_hosts.append(host)
            print(f"Added vanity host: {host}.{self.name}")

    def setup(self, system):
        self.setup_database(system)
        self.setup_wordpress(system)
        self.configure_nginx(system)
        self.setup_ssl(system)
        print(f"WordPress setup completed for {self.name}")