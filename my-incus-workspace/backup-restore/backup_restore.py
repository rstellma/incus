#!/usr/bin/env python3

import argparse
import sys

import exporter
import importer as imp


def main() -> int:
    try:
        parser = argparse.ArgumentParser(
            prog="backup_restore.py",
            description="Incus Backup & Restore",
        )

        sub = parser.add_subparsers(dest="command", required=True)

        export_parser = sub.add_parser("export", help="Export Incus objects")
        export_parser.add_argument(
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
        export_parser.add_argument(
            "name",
            nargs="?",
            help="Object name (required for singular export)",
        )

        import_parser = sub.add_parser("import", help="Import Incus objects")
        import_parser.add_argument(
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
        import_parser.add_argument(
            "name",
            nargs="?",
            help="Object name (required for singular import)",
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

        elif args.command == "import":
            match args.object:
                case "all":
                    imp.import_all()

                case "instances":
                    imp.import_all_instances()

                case "profiles":
                    imp.import_all_profiles()

                case "networks":
                    imp.import_all_networks()

                case "pools":
                    imp.import_all_storage()

                case "projects":
                    imp.import_all_projects()

                case "instance":
                    if not args.name:
                        parser.error("import instance requires <name>")
                    imp.import_instance(args.name)

                case "profile":
                    if not args.name:
                        parser.error("import profile requires <name>")
                    imp.import_profile(args.name)

                case "network":
                    if not args.name:
                        parser.error("import network requires <name>")
                    imp.import_network(args.name)

                case "pool":
                    if not args.name:
                        parser.error("import pool requires <name>")
                    imp.import_storage(args.name)

                case "project":
                    if not args.name:
                        parser.error("import project requires <name>")
                    imp.import_project(args.name)
        else:
            print(f"[ERROR] unknown command: {args.command}")

        return 0

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
