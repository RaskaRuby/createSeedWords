## Create Seed Words

This project provides a brief explanation as to why you might want to create new wallet seed words from your own entropy, and it contains some simple instructions and python scripts to help you do that.

### What are Private Keys and Seed Words?

A private key is essentially a very large random number in a particular format that can create a wallet. A private key is used to sign transactions, and to derive all addresses and public keys for that wallet. It must be stored securely and kept private, as anyone knowing the private key can restore a wallet and have complete access to the funds in it.

To make it easier for users to record their private keys, standards have been adopted to convert that very large number into a series of mneumonic seed words, usually 12-24 words in length. Wallets can often be restored using either the private key or the seed words, as they represent the same value.

### Where Does That Random Number Come From?

Wallet software usually [generates the large random number](https://en.wikipedia.org/wiki/Random_number_generation) it needs from something called a [pseudo-random number generator](https://en.wikipedia.org/wiki/Pseudorandom_number_generator) (PRNG). These are not truly random numbers (hence the pseudo), but are random enough for most uses, as a lot of effort has been devoted to making them as secure as possible. But PRNGs have been successfully attacked in the past, and using one is exposing you to that risk. Even with open-source software, it is difficult to tell if the PRNG used in your wallet is really secure, or if the software has been maliciously tweaked to permit a later retirement attack. If you are securing large amounts of value, or are just really paranoid, you might want to consider skipping PRNGs completely, and getting your entropy either from hardware sources or generating it yourself.

### Using Your Own Entropy (Randomness)

Generating your own entropy for use in a new wallet can be done with a variety of methods, including coin flips, dice rolls and card decks. Most wallet software does not allow you to input your own entropy, but it is possible using the following methods. Ideally, you would create your seed words with one of these methods, restore a wallet using those seed words in your preferred wallet software, and then verify that all the keys and addresses match by restoring with even different software. For maximum security, these should only be performed on OFFLINE computers, preferably on a system like [Tails](https://tails.boum.org/).

* **[Ian Coleman BIP39](https://iancoleman.io/bip39/)** - the swiss army knife of converters. Make sure to download [`bip39-standalone.html`](https://github.com/iancoleman/bip39) and run it OFFLINE. Clicking the "Show entropy details" box allows you to enter your own entropy from a variety of sources. You can also use this to see the address and public keys that belong to a set of seed words, which can be compared with what your wallet shows.

* **[ArmanTheParman](https://armantheparman.com/bitcoin-seed-with-dice/)** - detailed article describing exacly how a large binary number is converted into BIP39 seed words. Use D6 dice to create entropy, then determine the seed words, and a computer is only needed at the very end to calculate the final seed word.

* **[ColdCard and D6 Dice](https://coldcardwallet.com/docs/verifying-dice-roll-math)** - new wallets can be created on a ColdCard hardware wallet by entering a series of D6 dice rolls. Those same dice rolls can also be input into a very simple python script [`rolls.py`](https://coldcardwallet.com/docs/rolls.py) that calculates seed words, and you can verify that the seed words match.

* **[This Project](https://github.com/RaskaRuby/createSeedWords)** - expands on [`rolls.py`](https://coldcardwallet.com/docs/rolls.py) by allowing more types of input, including binary coins and hexadecimal [D16 dice](https://github.com/Samourai-Wallet/hexadecimal-die), as well as Monero support. No extra python libraries are needed, so these scripts can be run almost anywhere, and should be fairly readable to beginning python programmers.

### Python Scripts

* [`createSeedWordsBTC.py`](https://github.com/RaskaRuby/createSeedWords/blob/master/createSeedWordsBTC.py) - Creates bitcoin BIP39 seed words. Verify results by running [`bip39-standalone.html`](https://github.com/iancoleman/bip39) OFFLINE. Enter created seed words, Show Entropy Details, and the hex entropy should match.
* [`createSeedWordsXMR.py`](https://github.com/RaskaRuby/createSeedWords/blob/master/createSeedWordsXMR.py) - Creates Monero seed words. Verify results by running [`monero-wallet-cli`](https://getmonero.org) OFFLINE, restoring from seed words, and comparing the secret spend keys.

### Usage

**WARNING** - For maximum security, run only on a secure OFFLINE system like [Tails](https://tails.boum.org/). Revealing any of the user entropy, seed words or keys generated could allow theft of the wallet.

The following user input is supported to create 256 bits of entropy:

* **Binary** [0,1] - requires exactly 256 coin flips, or D6 dice rolls where 1-3 is a zero, and 4-6 is a one
* **Regular D6 Dice** [1-6] - any number dice rolls (50+ is safe), hashed to 256 bits (This is the ColdCard [`rolls.py`](https://coldcardwallet.com/docs/rolls.py) method)
* **Hexadecimal [D16 Dice](https://github.com/Samourai-Wallet/hexadecimal-die)** [0-9,a-f,A-F] - requires exactly 64 hexadecimal characters
* **No Input** (not recommended) - uses python PRNG urandom(32)

