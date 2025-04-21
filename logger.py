# logger.py

class Logger:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    DIM = "\033[2m"
    BOLD = "\033[1m"

    @classmethod
    def snapshot(cls, snapshot, is_current=False, prefix=""):
        id_short = snapshot['id'][:8]
        date = snapshot['date']
        comment = snapshot['comment']
        marker = f"{cls.YELLOW}← CURRENT{cls.RESET}" if is_current else ""
        print(f"{prefix}{cls.GREEN}{id_short}{cls.RESET} {cls.DIM}[{date}]{cls.RESET} - {cls.CYAN}{comment}{cls.RESET} {marker}")

    @classmethod
    def info(cls, message):
        print(f"{cls.BOLD}{message}{cls.RESET}")

    @classmethod
    def error(cls, message):
        print(f"{cls.YELLOW}Error: {message}{cls.RESET}")

    @classmethod
    def plain(cls, message):
        print(message)
