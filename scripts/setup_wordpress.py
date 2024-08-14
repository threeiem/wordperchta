import argparse

from wordperchta.alpine_system import AlpineSystem
from wordperchta.domain import Domain


def main():
    parser = argparse.ArgumentParser(description="Setup WordPress with Nginx")
    parser.add_argument("domain", help="Primary domain name")
    parser.add_argument(
        "--vanity", nargs="*", default=[], help="Additional vanity hosts"
    )
    args = parser.parse_args()

    alpine_system = AlpineSystem()
    alpine_system.setup_system()

    domain = Domain(args.domain, args.vanity)
    domain.setup(alpine_system)

    print(
        "Setup complete. Complete WordPress installation on the web."
    )


if __name__ == "__main__":
    main()
