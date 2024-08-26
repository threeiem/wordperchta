import argparse
from wordperchta.site_manager import SiteManager

def main():
    parser = argparse.ArgumentParser(description="Manage WordPress sites")
    parser.add_argument("--config", default="config/sites_config.json", help="Path to the sites configuration file")
    parser.add_argument("--add-site", help="Add a new site")
    parser.add_argument("--vanity", nargs="*", default=[], help="Vanity hosts for the new site")
    args = parser.parse_args()

    site_manager = SiteManager(args.config)

    if args.add_site:
        site_manager.create_site({"domain": args.add_site, "vanity_hosts": args.vanity})
    else:
        site_manager.setup_sites()

if __name__ == "__main__":
    main()