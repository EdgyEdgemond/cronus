section_config = [
    ("minute", 0, 59),  # minutes allowed values
    ("hour", 0, 23),  # hours allowed values
    ("day of month", 0, 30, True),  # day of month allowed values
    ("month", 0, 11, True),  # month allowed values
    ("day of week", 0, 6),  # day of week allowed values
]


class CronParser:
    def __init__(self, crontab, command):
        self._crontab = crontab
        self._command = command
        self._parsed_values = {}

    def parse(self):
        sections = self._crontab.split()
        if len(sections) != 5:
            raise SyntaxError("Invalid crontab")

        for i, section in enumerate(sections):
            type_ = section_config[i][0]
            self._parsed_values[type_] = parse_section(section, *section_config[i][1:])

    def render(self):
        for config in section_config:
            print(config[0].ljust(15), " ".join([str(v) for v in sorted(self._parsed_values[config[0]])]))
        print("command".ljust(15), self._command)


def parse_section(section, min_range, max_range, one_index=False):
    pieces = section.split(",")
    values = set()
    for piece in pieces:
        piece, step, has_step, is_range = parse_piece(piece)

        start, stop = extract_range(piece, has_step, is_range, one_index, min_range, max_range)

        for i in range(start, stop + 1):
            if step is None or i % step == 0:
                if one_index:
                    values.add(i + 1)
                else:
                    values.add(i)

    return values


def parse_piece(piece):
    has_step = "/" in piece
    is_range = "-" in piece
    step = None
    if has_step:
        piece, step = piece.split("/")
        step = int(step)

    return piece, step, has_step, is_range


def extract_range(piece, has_step, is_range, one_index, min_range, max_range):
    start, stop = 0, 0
    if is_range:
        start, stop = piece.split("-")
        if one_index:
            start, stop = int(start) - 1, int(stop) - 1
    elif piece == "*":
        start, stop = min_range, max_range
    else:
        start = piece
        stop = piece
        if has_step:
            stop = max_range
        if one_index:
            start, stop = int(start) - 1, int(stop) - 1

    return int(start), int(stop)
