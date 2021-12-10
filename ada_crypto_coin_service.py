from crypto_coin import CryptoCoin
from crypto_coin_service import CoinService

import hashlib
import cardano_utils as cardano
import bech32 as bech32
from mnemonic import Mnemonic

import re


class CardanoCoinService(CoinService):

    def __init__(self) -> None:
        super().__init__()
        self.mnemo = Mnemonic("english")

    @staticmethod
    def get_currency_name():
        return "ADA"

    def generate(self):
        mnemonic = Mnemonic('english').generate(strength=160)
        wif = mnemonic
        address = self.__generate_address_from_seed(mnemonic)
        return CryptoCoin(address, wif, '')

    def get_coin(self, mnemonic):
        wif = mnemonic
        address = self.__generate_address_from_seed(mnemonic)
        return CryptoCoin(address, wif, '')

    def generate_asset_id(self, coin):
        return re.search('^addr1q(\\w{6}).+$', coin.address).group(1)

    def format(self, coin):
        return "{},{}\n".format(coin.wif, coin.address)

    def get_csv_header(self):
        return "WIF,Address\n"

    def __generate_address_from_seed(self, mnemonic):

        # mk_type = "Icarus"

        # no password on wallet
        passphrase = ""
        mnemo = self.mnemo

        masterkey = cardano.generateMasterKey_Icarus(mnemonic=mnemonic, passphrase=passphrase.encode(),
                                                     wordlist=mnemo.wordlist, langcode="en",
                                                     trezor=False)

        # if mk_type == "Ledger":
        #     masterkey = cardano.generateMasterKey_Ledger(mnemonic=mnemonic, passphrase=passphrase.encode())

        # if mk_type == "Icarus":
        #     # This can all be done in one step with generateMasterKey_Icarus, but breaking it up to print the masterkey
        #     masterkey = cardano.generateMasterKey_Icarus(mnemonic=mnemonic, passphrase=passphrase.encode(),
        #                                                  wordlist=mnemo.wordlist, langcode="en",
        #                                                  trezor=False)
        #
        # if mk_type == "Icarus-Trezor":
        #     # This can all be done in one step with generateMasterKey_Icarus, but breaking it up to print the masterkey
        #     masterkey = cardano.generateMasterKey_Icarus(mnemonic=mnemonic, passphrase=passphrase.encode(),
        #                                                  wordlist=mnemo.wordlist, langcode="en",
        #                                                  trezor=True)

        (kL, kR), AP, cP = masterkey

        # print("MasterKey: ", (kL + kR + cP).hex())
        # print()
        #
        # print("Root Node")
        # print("kL:", kL.hex())
        # print("kR:", kR.hex())
        # print("AP:", AP.hex())
        # print("cP:", cP.hex())
        # print()

        account_path = "1852'/1815'/0'"
        account_node = cardano.derive_child_keys(masterkey, "1852'/1815'/0'", True)
        (kL, kR), AP, cP = account_node
        # print("Account Node (", account_path, ")")
        # print("kL:", kL.hex())
        # print("kR:", kR.hex())
        # print("AP:", AP.hex())
        # print("cP:", cP.hex())
        # print()

        spend_node = cardano.derive_child_keys(account_node, "0/0", False)
        (AP, cP) = spend_node
        # print("Spending Key")
        # print("AP:", AP.hex())
        # print("cP:", cP.hex())
        # print()

        spend_pubkeyhash = hashlib.blake2b(AP, digest_size=28).digest()

        stake_node = cardano.derive_child_keys(account_node, "2/0", False)
        (AP, cP) = stake_node
        # print("Staking Key")
        # print("AP:", AP.hex())
        # print("cP:", cP.hex())
        # print()

        stake_pubkeyhash = hashlib.blake2b(AP, digest_size=28).digest()

        bech32_data = b"\x01" + spend_pubkeyhash + stake_pubkeyhash

        data = bytes.fromhex(bech32_data.hex())

        out_data = bech32.convertbits(data, 8, 5)

        encoded_address = bech32.bech32_encode("addr", out_data)

        # print("First Base Address: ", encoded_address)
        return encoded_address


__all__ = ["CardanoCoinService"]
