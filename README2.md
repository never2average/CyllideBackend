

# Secure Electronic Voting using Azure Blockchain 

## [How to use it / How to contribute to it?](https://github.com/never2average/CODEFUNDO-2019/blob/master/HowToUse.md)

## Our Aim

We aim to tackle two issues which plague the current system of Electronic Voting Machines,

 1. Delayed vote counting and result declaration - The whole 2019 Lok Sabha Election process took just over 2 months to complete. We believe this can be accelerated using Blockchain.
 2. Accusations of tampering EVMs - By using properties of immutability of blockchains, we believe EVMs can be made virtually tamper-proof.

## Proposed Stages

We want our election Proof-of-Concept to be modelled around the following stages:

### Before Polling Day
####  Voter Verification:
- First, we need to verify the person through Aadhar card or Voter ID card API available here: https://electoralsearch.in/ 
- Secondly, a picture of the person will be taken, which will be used later on.
- Finally, the person would be granted a secret passphrase (generated randomly) required to vote at the voting camp.<br/>
Once voter-verification for all the voters is done, a function will be called on the smart contract to make sure it does not accept any new requests to add voters.
### On Polling Day
#### At the EVM:
- **Step 1**: On entering voting camp, the EVM will have our portal open, where the voter will have to enter the pass-phrase given to him in the pre-voting phase
- **Step 2**: On supplying his pass-phrase, the portal will show a list of candidates from the constituency the voter is in. He will be able to choose one candidate to vote for.
- **Step 3**: A confirmation page will pop up with the name and face of the candidate. The user will confirm his choice or be able to go back.
- **Step 4**: A QR code will be presented to the voter. The voter can then use the camera on his phone to confirm whether that vote is truly his. This ensures that the EVM has not been tampered with. Once that is confirmed, a confirmatory message is shown.

Once polling days are over, another function will be called on the smart contract to ensure it stops accepting any further vote requests by voters .
### After Polling Day
- After the election is over, the blockchain will be made public and voters will be able to see their transaction.

## Characteristics of our project
We aim to implement the following features to make our system secure, reliable, and transparent.

- Each voter should be able to see his vote has been counted and be able to see who he voted for. This will ensure the elections are completely transparent.
- Each candidate should be able to see the number of votes he has gotten and be able to see that in a way which doesn't expose the identity of the voters. That way, the candidate can see it and just count, but won't know who voted for him. This will eradicate the accusations of EVM tampering and vote miscounting.
- The user will have voted by confirmating the presented QR code from his phone. This ensures that the vote is valid and has not been tampered in any way.


## Technologies used
- Microsoft Azure
- Truffle
- Ganache
- Solidity
- Javascript
- Web3.js
