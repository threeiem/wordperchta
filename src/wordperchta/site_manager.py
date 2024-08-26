import json
from .domain import Domain
from .alpine_system import AlpineSystem

class SiteManager:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.alpine_system = AlpineSystem()

    def setup_sites(self):
        for site in self.config['sites']:
            domain = Domain(site['domain'], site['vanity_hosts'])
            if not self.site_exists(site):
                self.create_site(site, domain)
            else:
                self.update_site(site, domain)

    def site_exists(self, site):
        return self.alpine_system.run_command(f"test -d {site['document_root']}")

    def create_site(self, site, domain):
        domain.setup(self.alpine_system)
        self.configure_nginx(site, domain)

    def update_site(self, site, domain):
        self.configure_nginx(site, domain)

    def configure_nginx(self, site, domain):
        nginx_conf = f"/etc/nginx/conf.d/{site['domain']}.conf"
        config_content = f"""
server {{
    listen 80;
    server_name {site['domain']} {' '.join(f'{host}.{site["domain"]}' for host in site['vanity_hosts'])};
    root {site['document_root']};
    index index.php;

    access_log {site['log_path']}/access.log;
    error_log {site['log_path']}/error.log;

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
        self.alpine_system.run_command(f"echo '{config_content}' > {nginx_conf}")
        self.alpine_system.run_command("nginx -t && rc-service nginx reload")