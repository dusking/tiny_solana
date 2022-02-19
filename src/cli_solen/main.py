# pylint: disable=missing-docstring, unused-variable, no-self-use, invalid-name, broad-except
import sys
import logging

import argh
from colorama import Fore

from solen import Solen

loggerpy = logging.getLogger("solen")
loggerpy.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
loggerpy.addHandler(ch)


class Logger:
    @staticmethod
    def red(msg):
        return Fore.RED + msg + Fore.RESET

    @staticmethod
    def yellow(msg):
        return Fore.YELLOW + msg + Fore.RESET

    @staticmethod
    def green(msg):
        return Fore.GREEN + msg + Fore.RESET

    @staticmethod
    def blue(msg):
        return Fore.BLUE + msg + Fore.RESET

    def info(self, line):
        print(line)

    def header(self, header):
        header = self.yellow(header)
        header_length = 40
        header_padding = "-"
        print(f"{header:{header_padding}^{header_length}}")

    def warning(self, msg):
        print(self.yellow(msg))

    def error(self, msg, should_exit=True):
        print(self.red(msg))
        if should_exit:
            sys.exit(1)


logger = Logger()


@argh.arg("env", help="Solana env (dev / main)")
@argh.arg("-w", "--wallet", default=None, help="Wallet to receive the token balance for")
def balance(env, wallet=None):
    logger.header("get token balance")
    solen = Solen(env)
    wallet = wallet or solen.keypair.public_key
    logger.info(f"get balance for: {wallet}")
    balance_sol = f"{solen.balance_sol(wallet):,}"
    balance_token = f"{solen.balance_token(wallet):,}"
    logger.info(f"{balance_sol} SOL")
    logger.info(f"{balance_token} Token")


@argh.arg("env", help="Solana env (dev / main)")
@argh.arg("wallet", help="Wallet to receive the token")
@argh.arg("amount", help="Amount to transfer")
def transfer(env, wallet, amount):
    logger.header("transfer token")
    solen = Solen(env)
    solen.transfer_token(wallet, float(amount))


@argh.arg("env", help="Solana env (dev / main)")
@argh.arg("csv", help="A csv file with wallet,amount to be transfer")
def bulk_transfer_init(env, csv):
    logger.header("bulk transfer token init")
    solen = Solen(env)
    solen.bulk_transfer_token_init(csv)


@argh.arg("env", help="Solana env (dev / main)")
@argh.arg("csv", help="A csv file with wallet,amount to be transfer")
@argh.arg("-d", "--dry-run", action="store_true", help="Dry run - don't send transactions")
def bulk_transfer(env, csv, dry_run=False):
    logger.header(f"bulk transfer token (dry-run={dry_run})")
    solen = Solen(env)
    solen.bulk_transfer_token(csv, dry_run=dry_run)


@argh.arg("env", help="Solana env (dev / main)")
@argh.arg("csv", help="A csv file with wallet,amount to be transfer")
def bulk_transfer_confirm(env, csv):
    logger.header("bulk transfer confirm")
    solen = Solen(env)
    solen.bulk_confirm_transactions(csv)


def main():
    parser = argh.ArghParser(description="Solana Token Util (Solen)")
    parser.add_commands([balance, transfer, bulk_transfer, bulk_transfer_confirm, bulk_transfer_init])
    parser.dispatch()


if __name__ == "__main__":
    main()
