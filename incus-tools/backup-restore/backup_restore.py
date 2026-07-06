#!/usr/bin/env python3

import argparse
import sys

import exporter


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="backup_restore.py",
        description="Incus Backup & Restore",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    export = sub.add_parser("export", help="Export Incus objects")
    export.add_argument(
        "object",
        choices=[
            "all",
            "instances",
            "profiles",
            "networks",
            "pools",
            "projects",
            "instance",
            "profile",
            "network",
            "pool",
            "project",
        ],
    )
    export.add_argument(
        "name",
        nargs="?",
        help="Object name (required for singular export)",
    )

    args = parser.parse_args()

    if args.command == "export":

        match args.object:
            case "all":
                exporter.export_all()

            case "instances":
                exporter.export_all_instances()

            case "profiles":
                exporter.export_all_profiles()

            case "networks":
                exporter.export_all_networks()

            case "pools":
                exporter.export_all_pools()

            case "projects":
                exporter.export_all_projects()

            case "instance":
                if not args.name:
                    parser.error("export instance requires <name>")
                exporter.export_instance(args.name)

            case "profile":
                if not args.name:
                    parser.error("export profile requires <name>")
                exporter.export_profile(args.name)

            case "network":
                if not args.name:
                    parser.error("export network requires <name>")
                exporter.export_network(args.name)

            case "pool":
                if not args.name:
                    parser.error("export pool requires <name>")
                exporter.export_pool(args.name)

            case "project":
                if not args.name:
                    parser.error("export project requires <name>")
                exporter.export_project(args.name)

    return 0


if __name__ == "__main__":
    sys.exit(main())
