from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # knowledge: one to pass the  parameter in another module is passing it through deploy before
    # the from address though doesn't solve our problem of hard coded address.

    """
    In order for our contract to be network agnostic, we need to make sure it can work with
    any network. If we are working on external chain like rinkeby then, we will use the 
    addresses like before else in the local chain/development environment, we will do mocking
    """
    #----------------VERY VERY IMPORTATNT CONCEPT ON MOCKING. READ BELOW------------------
    '''
    Down below, when we were in the development environments, we used the profinal price feed
    contract that we grabbed from the chainlink, but incase of any other environment,
    we will be using the mocked version of that same price feed contract. There is already
    a repository of that called "MockV3Aggregator" from chainlink-mix repository. 
    Thats what we are using doing below.
    In order to save the mock contract, we will need to create a test folder under the contracts.
    '''
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        print(f"The new price feed for mainnet is {price_feed_address}")
    else:
        deploy_mocks()
        #Here down I am saying that among all the versions of the mocked contract get me the
        #latest one.
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
        # ["verify"] works just fine but .get() prevents any indexing error if there
    )
    print(f"Contract has been deployed at {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
