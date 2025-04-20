# logger.py

class Logger:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    DIM = "\033[2m"
    BOLD = "\033[1m"

    @classmethod
    def snapshot(cls, snapshot, is_current=False):
        id_fmt = f"{cls.GREEN}{snapshot['id']}{cls.RESET}" if is_current else snapshot['id']
        date_fmt = f"{cls.DIM}[{snapshot['date']}] {cls.RESET}"
        comment_fmt = f"{cls.CYAN}{snapshot['comment']}{cls.RESET}"
        ptr_marker = f"{cls.YELLOW}← PTR{cls.RESET}" if is_current else ""
        print(f"{id_fmt} {date_fmt}- {comment_fmt} {ptr_marker}")

    @classmethod
    def info(cls, message):
        print(f"{cls.BOLD}{message}{cls.RESET}")

    @classmethod
    def error(cls, message):
        print(f"{cls.YELLOW}Error: {message}{cls.RESET}")

    @classmethod
    def plain(cls, message):
        print(message)
