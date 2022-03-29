from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f"The currrent Entrace fee is {entrance_fee}")
    print("Funding the account now......")
    fund_me.fund(
        {"from": account, "value": entrance_fee+50000}
    )  # this would be the msg.sender and msg.value
    print("Funding Completed")


def withdraw():
    # if you look at the function this automatically grabs the address of the account that will be
    # passed here.
    fund_me = FundMe[-1]
    account = get_account()
    print("Withdrawing the money")
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
