import inspect
import os
import time
from colorama import Fore


def debug(*msg: str, on_thread: str = "main"):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    caller = os.path.splitext(
        os.path.basename(
            inspect.currentframe()
            .f_back.f_globals["__file__"]
        )
    )[0]

    print(
        f"{Fore.BLUE}[{t}] {Fore.GREEN}[{on_thread}/DEBUG] {Fore.CYAN}({caller}) {Fore.RESET}{" ".join(msg)}"
    )


def info(*msg: str, on_thread: str = "main"):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    caller = os.path.splitext(
        os.path.basename(
            inspect.currentframe()
            .f_back.f_globals["__file__"]
        )
    )[0]

    print(
        f"{Fore.BLUE}[{t}] {Fore.GREEN}[{on_thread}/INFO] {Fore.CYAN}({caller}) {Fore.RESET}{" ".join(msg)}"
    )


def warn(*msg: str, on_thread: str = "main"):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    caller = os.path.splitext(
        os.path.basename(
            inspect.currentframe()
            .f_back.f_globals["__file__"]
        )
    )[0]

    print(
        f"{Fore.BLUE}[{t}] {Fore.GREEN}[{on_thread}/WARN] {Fore.CYAN}({caller}) {Fore.RESET}WARNING: {" ".join(msg)}"
    )


def fatal(*msg: str, on_thread: str = "main"):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    caller = os.path.splitext(
        os.path.basename(
            inspect.currentframe()
            .f_back.f_globals["__file__"]
        )
    )[0]

    print(
        f"{Fore.BLUE}[{t}] {Fore.GREEN}[{on_thread}/FATAL] {Fore.CYAN}({caller}) {Fore.RED}FATAL ERROR: {" ".join(msg)}{Fore.RESET}"
    )
    raise SystemExit(1)
