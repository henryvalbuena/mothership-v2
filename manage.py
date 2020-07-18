#!/usr/bin/env python3
import os
import json
import signal
import subprocess

import click


def setenv(variable: str, default: str) -> None:
    """Set an environment variable
    Args:
        variable: environment variable
        default: default value if variable is not set
    """

    os.environ[variable] = os.getenv(variable, default)


setenv("APPLICATION_CONFIG", "development")

config_json_filename = os.getenv("APPLICATION_CONFIG") + ".json"
with open(os.path.join("config", config_json_filename)) as f:
    config = json.load(f)

config = dict((i["name"], i["value"]) for i in config)

for key, value in config.items():
    setenv(key, value)


@click.group()
def cli():
    pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    """Command to start Flask server"""

    cmdline = ["flask"] + list(subcommand)
    p = None

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


cli.add_command(flask)

if __name__ == "__main__":
    cli()
