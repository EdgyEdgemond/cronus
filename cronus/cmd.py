import argparse

from cronus.parser import CronParser


parser = argparse.ArgumentParser(description="Parse and render a crontab")
parser.add_argument("args", help="crontab and command to parse")


def main():
    args = parser.parse_args()
    crontab, command = args.args.rsplit(" ", 1)

    cp = CronParser(crontab, command)
    cp.parse()
    cp.render()
