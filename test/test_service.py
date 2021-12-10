from ada_crypto_coin_service import CardanoCoinService

ada_crypto_coin_service = CardanoCoinService()


def test_generate():
    coin = ada_crypto_coin_service.generate()
    print()
    print("Coin address: ", coin.address)
    print("Coin wif: ", coin.wif)
    print("Coin seed: ", coin.seed)
    print("Coin asset ID: ", ada_crypto_coin_service.generate_asset_id(coin))

    assert coin.address is not None
    assert coin.wif is not None


# def test_get_coin():
#     mnemonic = "cave table seven there praise limit fat decorate middle gold ten battle trigger luggage demand"
#     coin = ada_crypto_coin_service.get_coin(mnemonic)
#     print()
#     print("Coin address: ", coin.address)
#     print("Coin wif: ", coin.wif)
#     print("Coin seed: ", coin.seed)
#     print("Coin asset ID: ", ada_crypto_coin_service.generate_asset_id(coin))
#
#     assert coin.address is not None
#     assert coin.wif is not None