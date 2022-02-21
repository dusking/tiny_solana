# pylint: disable=missing-docstring, unused-variable, no-self-use, invalid-name, broad-except
import logging

import argh
import pkg_resources

from solen import Solen

from .log_print import LogPrint
from .bulk_transfer import run, init, confirm

log_print = LogPrint()

loggerpy = logging.getLogger("solen")
loggerpy.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
loggerpy.addHandler(ch)


def version():
    """
    Current installed version
    """
    log_print.info(pkg_resources.require("solen")[0].version)


@argh.arg("-e", "--env", help="Solana env (dev / main)")
def info(env=None):
    """
    Display local wallet balance of SOL & Token
    """
    log_print.header("get token info")
    solen = Solen(env)
    log_print.info(f"Token: {solen.token.pubkey}")
    log_print.info(f"Decimals: {solen.token_decimals}")


@argh.arg("-e", "--env", help="Solana env (dev / main)")
@argh.arg("-w", "--wallet", default=None, help="Wallet to receive the token balance for")
def balance(wallet=None, env=None):
    """
    Display local wallet balance of SOL & Token
    """
    log_print.header("get token balance")
    solen = Solen(env)
    wallet = wallet or solen.keypair.public_key
    log_print.info(f"get balance for: {wallet}")
    balance_sol = f"{solen.balance_sol(wallet):,}"
    balance_token = f"{solen.balance_token(wallet):,}"
    log_print.info(f"{balance_sol} SOL")
    log_print.info(f"{balance_token} Token")


@argh.arg("wallet", help="Wallet to receive the token")
@argh.arg("amount", help="Amount to transfer")
@argh.arg("-e", "--env", help="Solana env (dev / main)")
def transfer(wallet, amount, env=None):
    """
    Transfer token from local wallet ro recipient
    """
    log_print.header("transfer token")
    solen = Solen(env)
    solen.transfer_token(wallet, float(amount))


def main():
    parser = argh.ArghParser(description="Solana Token Util (Solen)")
    parser.add_commands([version, info, balance, transfer])
    parser.add_commands([init, run, confirm], namespace="bulk-transfer")
    parser.dispatch()


if __name__ == "__main__":
    main()
