from datetime import datetime
from typing import Tuple


UNITS = {
    "microsecond": "μs",
    "millisecond": "ms",
    "second": "s",
    "minute": "m",
    "hour": "h"
}
COLOR = "\033[31m"
RESET = "\033[0m"


def time_it(start_time: datetime, msg: str = "{}") -> Tuple[str, int]:
    elapsed = (datetime.now() - start_time).total_seconds() * 1_000_000

    if elapsed < 1_000:
        val = f"{round(elapsed, 2)}{UNITS['microsecond']}"
    elif elapsed < 1_000_000:
        val = f"{round(elapsed / 1_000, 2)}{UNITS['millisecond']}"
    elif elapsed < 60_000_000:
        val = f"{round(elapsed / 1_000_000, 2)}{UNITS['second']}"
    elif elapsed < 3_600_000_000:
        val = f"{round(elapsed / 60_000_000, 2)}{UNITS['minute']}"
    else:
        val = f"{round(elapsed / 3_600_000_000, 2)}{UNITS['hour']}"

    colored_val = f"{COLOR}{val}{RESET}"
    print(msg.format(colored_val))
    return msg.format(val), int(elapsed)
