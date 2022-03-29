from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

# always a good practise to have constant values defined seperate
'''
Here decimals means how many decimals the contract should have and initial answer like a
starting value of the eth price, like 2000
'''
DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
'''
When we want to interact with the mainnet-fork, we will get the error saying you don't have
any eth so, we want to create a fake account with 100 eth in it, but we also don't want to
mock it as we are working with the real external contracts that doesn't need mocking.
But since brownie cannot create these fake accounts for us, we use third parties like alchemy
and infura that will create us fake mainnet-fork accounts with fake money.
'''
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork","mainnet-fork-dev"]

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mock.............")
    if len(MockV3Aggregator) <= 0:
        # instead of writing too many zeros web3 has a function towei to convert our ethtowei
        MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )
        #below is much bettwer way of doing it using the "towei" function of web3, but since
        #we are trying to match our get_price function in FundMe, we will skip that for now.
        #MockV3Aggregator.deploy(DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()})
    print("Mock deployed.......")
