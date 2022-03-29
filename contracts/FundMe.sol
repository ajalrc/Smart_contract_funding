//SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

//library to prevent int overflow

contract FundMe {
    using SafeMathChainlink for uint256; //this is how to use the safemathlibrary to prevent
    //overflow

    /*----Constructor are the ones that gets executed first as well-----**/
    //address of the owner (who deployed the contract)
    address public owner;
    // array of addresses who deposited
    address[] public funderList;
    AggregatorV3Interface public priceFeed;
    //mapping to store which address depositeded how much ETH
    mapping(address => uint256) public addressToAmountFunded;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        /**
        msg : it is a sepecial global variable that contain the properties which allow 
        access to the blockchain's contracts, their functions, and their values.
        msg.sender: person who is currently connecing with the contract i.e the address
        msg.value: transaction amount of the sender.
        */
        owner = msg.sender;
    }

    /**-----------------Payable Solidity------------------ */
    /*Use of "payable" modifier enables you to process transaction in your smart contract. */
    function fund() public payable {
        /**Here we will be creating a minimum payable for any sender*/
        uint256 minimumUSD = 50 * 10**18;
        //require(condition, else revert with error)
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more than $50 worth of ETH"
        );
        // this is a short way of setting the minimum using "require" instead of a loop.

        addressToAmountFunded[msg.sender] += msg.value;
        funderList.push(msg.sender);
    }

    /**---------------Get conversion rate, prices and versions using interfaces-------------------*/
    function getVersion() public view returns (uint256) {
        //what we are saying here is get me the access to all the functions defined in that
        //interface with that address
        /***
        In brownie we changed the hard coded version of Aggregator and instead will be getting
        the value from the constructor when called from another module.
         */
        return priceFeed.version();
    }

    //getting the price of Eth; default with 8 more zeros
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000); // changing to wei
    }

    // 1000000000 // the ETH -> USD conversion
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        //dividing by 18 zeros because of multiplication of 10
        //above and 8 by default.
        //4070050000000 => 0.000004070050000000 in Gwei
        return ethAmountInUsd;
    }

    /**---------Withdrawing the payabale by only the owner of the contract---------*/
    function withdraw() public payable onlyOwner {
        /**
        Here msg.sender grabs the address of whoeever is sending the money and this
        keywords get the address of the contract where the money is sent to. meaning
        we transfer all the balance from the contract to the sender address.*/

        //require(msg.sender == owner, "You are not the owner to receive fund.");//there might
        //be a time where the use of require might be extensive so to mitigate that for cleaner
        //code, we will be using ******modifier*********;

        msg.sender.transfer(address(this).balance);
        /*-----------------Resetting----------------------------------
        iterate through all the mappings and make them 0 since all the deposited amount has
         been withdrawn
        */
        for (
            uint256 funderIndex = 0;
            funderIndex < funderList.length;
            funderIndex++
        ) {
            address funder = funderList[funderIndex]; //grabbing the address
            addressToAmountFunded[funder] = 0; // mapping that address value to 0
        }
        //type[] memory typearray = new type[](n)// where n is the total capacity of array
        funderList = new address[](0);
    }

    /**-------------------Helper  function for fund and withdraw-------------------- */
    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice(); //current price of Eth
        uint256 precision = 10**18; //because the measurement is in wei so for extra precision
        return (minimumUSD * precision) / price;
    }

    /**----------------------Working with modifier------------------------------*/
    /*A modifier is use to change the behavior of a function in a declarative way.*/
    modifier onlyOwner() {
        /**Means that wherever this modifier is called check the criteria and _ means that
        if the criteria is meet, then run the code below it. 
        */
        require(msg.sender == owner, " You are not the owner boiiiii!");
        _;
    }
}
