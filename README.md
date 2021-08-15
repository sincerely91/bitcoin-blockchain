# BlockChain

## Making a simulation of bitcoin in blockchain

#
## What Did We Do 
    1) making a web server with FLASK to get a node IP for making the bitcoin network

    2) there are 3 RestFul API :
##
        2.1) trx : for making a new transaction
             sending money(amout) from sender to reciever

        2.2) mine : making a block for validation of all
             transactions in mempool with POW

        2.3) chain : getting all the blocks of chain  
## 
    3) making a class of blockchain
##
        3.1) in any block there are : index , timestamp , transaction , proof(nounce) , previous hash

        3.2) every transaction will be added to mempool

        3.3) for mining any block we must do a POW(proof of work) that means we must add a nounce to our block and hash of this must be smaller than network difficulty

        3.4) for any our neighbour chains we must validate them based on two features : 1- validating hash of previous block 2- validating nounce that make hash be smaller than network difficulty
#
## How to use
        1) clone this repository 
            git clone https://github.com/saeed5959/blockchain

        2) install requirements in requirements.txt
            pip3 install -r requirements.txt

        3) run the code in localhost with specified port
            python3 bc.py 6000

        4) send a transaction request to localhost:port/trxs
        5) send a mine request to localhost:port/mine
        6) send a seeing blockchain request to localhost:port/chain

        Point : For sending request to api use postman
                sudo snap postman
