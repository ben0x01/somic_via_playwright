from web3 import Web3

RPC_URL = "https://rpc.testnet.soniclabs.com"
EXPLORER_URL = "https://testnet.soniclabs.com/tx/"


# Контракты токенов
DIAMONDS_CONTRACT = Web3.to_checksum_address("0x30BF3761147Ef0c86E2f84c3784FBD89E7954670")
CORAL_CONTRACT = Web3.to_checksum_address("0xAF93888cbD250300470A1618206e036E11470149")
OBSIDIAN_CONTRACT = Web3.to_checksum_address("0x3e6eE2F3f33766294C7148bc85c7d145E70cBD9A")
MALACHITE_CONTRACT = Web3.to_checksum_address("0x50971F8978C431D560ff658a83a8a03fdf199055")
RUBY_CONTRACT = Web3.to_checksum_address("0x75190d6e62B8984b987B2336fD10552eD0e6a538")
OPAL_CONTRACT = Web3.to_checksum_address("0xdB9a47bB64961E1eE511CB8aB252e6102a1b956C")
ONYX_CONTRACT = Web3.to_checksum_address("0xE73c4f6A0A3B0EF8337fD080b76C08172b3eB958")
TOPAZ_CONTRACT = Web3.to_checksum_address("0x72778BA7c44b3bF218954175A9480D8b8f841C08")

# Адреса дополнительных контрактов для свапа
CORAL_DIAMOND = Web3.to_checksum_address("0x908562F2aCA4d9bd0370fc7Bd0d2FDF59395082c")
DIAMOND_OBSIDIAN = Web3.to_checksum_address("0x19Ca461273989efF78C466c4B566AA0735113684")
CORAL_OBSIDIAN = Web3.to_checksum_address("0xD7D04d8A33b6E6EB42a2e0e273e0fe1F23f818fD")
DIAMOND_MALACHITE = Web3.to_checksum_address("0x92e668fFF2054d9A1C77cc0489F1EcdA5928696c")
CORAL_RUBY = Web3.to_checksum_address("0x46c12c3b0b0221e2b30930Bf17C3564ba8720C56")
CORAL_OPAL = Web3.to_checksum_address("0x9540714aB1F26c0d920BE704214638A59760ff47")
MALACHITE_ONYX = Web3.to_checksum_address("0x72E9130B3400Ce71de271a0f3d9d08909CCBBA54")
MALACHITE_TOPAZ = Web3.to_checksum_address("0x28ecC5BaCadf35264888BF41Fc51Ce3b087f8cbB")

# Создание словаря токенов и их пар для свапа
token_swap_mapping = {
    DIAMONDS_CONTRACT: {
        "swap_with": [CORAL_CONTRACT, OBSIDIAN_CONTRACT, MALACHITE_CONTRACT],
        "additional_contracts": {
            CORAL_CONTRACT: CORAL_DIAMOND,
            OBSIDIAN_CONTRACT: DIAMOND_OBSIDIAN,
            MALACHITE_CONTRACT: DIAMOND_MALACHITE
        }
    },
    CORAL_CONTRACT: {
        "swap_with": [DIAMONDS_CONTRACT, OBSIDIAN_CONTRACT, RUBY_CONTRACT, OPAL_CONTRACT],
        "additional_contracts": {
            DIAMONDS_CONTRACT: CORAL_DIAMOND,
            OBSIDIAN_CONTRACT: CORAL_OBSIDIAN,
            RUBY_CONTRACT: CORAL_RUBY,
            OPAL_CONTRACT: CORAL_OPAL
        }
    },
    OBSIDIAN_CONTRACT: {
        "swap_with": [DIAMONDS_CONTRACT, CORAL_CONTRACT],
        "additional_contracts": {
            DIAMONDS_CONTRACT: DIAMOND_OBSIDIAN,
            CORAL_CONTRACT: CORAL_OBSIDIAN
        }
    },
    MALACHITE_CONTRACT: {
        "swap_with": [DIAMONDS_CONTRACT, ONYX_CONTRACT, TOPAZ_CONTRACT],
        "additional_contracts": {
            DIAMONDS_CONTRACT: DIAMOND_MALACHITE,
            ONYX_CONTRACT: MALACHITE_ONYX,
            TOPAZ_CONTRACT: MALACHITE_TOPAZ
        }
    },
    RUBY_CONTRACT: {
        "swap_with": [CORAL_CONTRACT],
        "additional_contracts": {
            CORAL_CONTRACT: CORAL_RUBY
        }
    },
    OPAL_CONTRACT: {
        "swap_with": [CORAL_CONTRACT],
        "additional_contracts": {
            CORAL_CONTRACT: CORAL_OPAL
        }
    },
    ONYX_CONTRACT: {
        "swap_with": [MALACHITE_CONTRACT],
        "additional_contracts": {
            MALACHITE_CONTRACT: MALACHITE_ONYX
        }
    },
    TOPAZ_CONTRACT: {
        "swap_with": [MALACHITE_CONTRACT],
        "additional_contracts": {
            MALACHITE_CONTRACT: MALACHITE_TOPAZ
        }
    }
}

#Diamond Coral Malachite Obsidian Onyx Opal Ruby Topaz