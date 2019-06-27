import argparse

from cronus.parser import CronParser


parser = argparse.ArgumentParser(description="Parse and render a crontab")
parser.add_argument("crontab", help="crontab to parse")
parser.add_argument("command", help="command to run")


def main():
    args = parser.parse_args()

    cp = CronParser(args.crontab, args.command)
    cp.parse()
    cp.render()
