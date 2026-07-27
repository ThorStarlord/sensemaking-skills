def add_decision_subcommand(subparsers):
    decision_parser = subparsers.add_parser(
        "decision",
        help="Inspect or update decision workspace state",
    )
    decision_parser.add_argument(
        "action",
        choices=["status", "list"],
    )
