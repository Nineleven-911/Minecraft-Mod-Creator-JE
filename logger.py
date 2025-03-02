import inspect
import os,sys
import time
from colorama import Fore
from loguru import logger
logger.remove()
logger.add(sys.stdout,colorize=True,format="<blue>[{time:YYYY-MM-DD HH:mm:ss}]</blue> <green>[main/{level}]</green> <cyan>({file}:{function}:{line})</cyan> {message}")

'''class __Invalid:
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
'''