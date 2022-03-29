from scripts.deploy import deploy_fund_me
from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import get_account,LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest
from brownie import network,accounts, exceptions

#here we will be testing the fund and withdrawing 
def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrace_fee = fund_me.getEntranceFee() + 100 #100 wei tip just in case
    tx = fund_me.fund({"from" : account, "value" : entrace_fee})
    tx.wait(1)
    #since I am using mapping, I am passing the address to get the value
    assert (fund_me.addressToAmountFunded(account.address) == entrace_fee)
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    #remember, we are not actually doing the transfer but checking that after transfer, it is 0
    assert (fund_me.addressToAmountFunded(account.address) == 0)

#testing only the withdrawing capabilities of the owner
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        #this is the pytest way of skipping the test if criteria not met
        pytest.skip("Testing only for the local environments.")
    fund_me = deploy_fund_me()
    not_owner = accounts.add() #random new account created by brownie
    #we expected the error so, this is the pytest way to handle the error to pass the test
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from" : not_owner})
