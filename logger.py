import inspect
import os
import time
from colorama import Fore


def debug(*msg: str):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    caller = os.path.splitext(
        os.path.basename(
            inspect.currentframe()
            .f_back.f_globals["__file__"]
        )
    )[0]

    print(
        f"{Fore.BLUE}[{t}] {Fore.GREEN}[main/DEBUG] {Fore.CYAN}({caller}) {Fore.RESET}{" ".join(msg)}"
    )


def info(*msg: str):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    caller = os.path.splitext(
        os.path.basename(
            inspect.currentframe()
            .f_back.f_globals["__file__"]
        )
    )[0]

    print(
        f"{Fore.BLUE}[{t}] {Fore.GREEN}[main/INFO] {Fore.CYAN}({caller}) {Fore.RESET}{" ".join(msg)}"
    )


def warn(*msg: str):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    caller = os.path.splitext(
        os.path.basename(
            inspect.currentframe()
            .f_back.f_globals["__file__"]
        )
    )[0]

    print(
        f"{Fore.BLUE}[{t}] {Fore.GREEN}[main/WARN] {Fore.CYAN}({caller}) {Fore.RESET}WARNING: {" ".join(msg)}"
    )


def fatal(*msg: str):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    caller = os.path.splitext(
        os.path.basename(
            inspect.currentframe()
            .f_back.f_globals["__file__"]
        )
    )[0]

    print(
        f"{Fore.BLUE}[{t}] {Fore.GREEN}[main/FATAL] {Fore.CYAN}({caller}) {Fore.RED}FATAL ERROR: {" ".join(msg)}{Fore.RESET}"
    )
    raise SystemExit(1)
