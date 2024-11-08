## Create Seed Words

There are a variety of methods of securing one's wallet's private keys/seed words (hardware wallets, metal backup plates, etc), but another factor to consider is where those private keys/seed words came from, and whether they are truly secure. This project provides a brief explanation as to why you might want to create new wallet seed words using your own entropy, and it contains some simple instructions and python scripts to help you do that. After reading this, you should be able to safely generate your own wallet seed words, find the public key for that wallet, and then import that public key into your own watch-only wallet. This gives you a true cold wallet that you can send funds to while never revealing your wallet's seed words.

### What are Seed Words?

A list of seed words is essentially a very large random number in a particular format. This random number is used as the starting point to derive all public addresses and private keys for that wallet. This random number must be stored securely and kept private, as anyone knowing it can restore a wallet and have complete access to the funds in it.

To make it easier for users to record this large random number, standards like BIP39 have been adopted to convert it into a series of mnemonic seed words, usually 12-24 words in length. Be aware the the seed words alone may not be enough alone to restore your wallet, especially if you switch to different wallet software. In addition to recording your wallet seed words, also record the [derivation path the wallet uses](https://walletsrecovery.org/).

### Where Does That Random Number Come From?

Wallet software usually [generates the large random number](https://en.wikipedia.org/wiki/Random_number_generation) it needs from something called a [pseudo-random number generator](https://en.wikipedia.org/wiki/Pseudorandom_number_generator) (PRNG). These are not truly random numbers (hence the pseudo), but are random enough for most uses, as a lot of effort has been devoted to making them as secure as possible. But PRNGs have been successfully attacked in the past, and using one is exposing you to that risk. Even with open-source software, it is difficult to tell if the PRNG used in your wallet is really secure, or if the software has been maliciously tweaked to permit a later retirement attack. If you are securing large amounts of value, or are just really paranoid, you might want to consider skipping PRNGs completely, and getting your entropy either from hardware sources or generating it yourself.

### Using Your Own Entropy (Randomness)

Generating your own entropy for use in a new wallet can be done with a variety of methods, including drawing from a hat, coin flips, dice rolls and card decks. Most wallet software does not allow you to input your own entropy, but it is possible using any of the methods below. [ArmanTheParman](https://armantheparman.com/bitcoin-seed-with-dice/) has a nice step-by-step article on how to do it completely by hand with a D6 dice.

### Best Practices

1. **Use [Tails](https://tails.boum.org/)**, an amnesic Linux operating system that boots from a USB stick. Create your own Tails stick, and create a Persistent partition during setup. Download all the tools below that you like, and copy them onto a separate USB stick. Boot into Tails, and then copy those files into your Persistant folder, with html files going into the Persistent/TorBrowser folder.
2. **Generate new wallet seed words** using whichever method below you like.
3. **Find public key (zpub) and addresses** for your seed words.
4. **Verify public key (zpub) and addresses** by checking them again using another method.

* **Draw Words From a Hat** - if you mix all the words from the [BIP39 word list](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt), you could create your own n word seed by randomly picking n-1 words (with replacement), then using a computer to calculate the last seed word (which is a checksum of the previous words). If you don't want to cut up all 2048 seed words, then you could buy some [Entropia Seed Tablets](https://btc-hardware-solutions.square.site/product/entropia-v2-seed-tablets/11?cs=true&cst=custom), which are a very nice 3-D printed set. To calculate the final checksum word, use [SeedTool](https://bitcoiner.guide/seed/) below, or use my [`createSeedWordsBTC.py`](https://github.com/RaskaRuby/createSeedWords/blob/master/createSeedWordsBTC.py) script, which also works with shortened Entropia-style 3-4 letter seed words.

* **Hardware Wallets** - both [ColdCard](https://coldcardwallet.com/docs/verifying-dice-roll-math) and [SeedSigner](https://seedsigner.com/) allow new wallets to be created using user entropy from D6 dice rolls. Coldcard also provides a very simple python script [`rolls.py`](https://coldcardwallet.com/docs/rolls.py) that does the same function so you can verify that the seed words match.

* **[Seed Tool](https://bitcoiner.guide/seed/)** - 

* **[Ian Coleman BIP39](https://iancoleman.io/bip39/)** - the Swiss Army knife of converters. Make sure to download [`bip39-standalone.html`](https://github.com/iancoleman/bip39) and run it OFFLINE. Clicking the "Show entropy details" box allows you to enter your own entropy from a variety of sources. You can also use this to see the public addresses and keys that belong to a set of seed words, which can be compared with what your wallet shows. Also allows you to choose between a variety of [derivation paths](https://walletsrecovery.org/).

* **[This Project](https://github.com/RaskaRuby/createSeedWords)** - mostly an exercise for myself, but expands on [`rolls.py`](https://coldcardwallet.com/docs/rolls.py) by allowing more types of input, including seed words, binary (coins) and hexadecimal [D16 dice](https://github.com/Samourai-Wallet/hexadecimal-die), as well as Monero support. No extra python libraries are needed, so these scripts can be run almost anywhere, and should be fairly readable to beginning python programmers.

### Python Scripts

* [`createSeedWordsBTC.py`](https://github.com/RaskaRuby/createSeedWords/blob/master/createSeedWordsBTC.py) - Creates bitcoin BIP39 seed words. Verify your results by running [`bip39-standalone.html`](https://github.com/iancoleman/bip39) OFFLINE, then Show Entropy Details. Paste your Hex Entropy output value into the Entropy field, and the generated seed words should match.
* [`createSeedWordsXMR.py`](https://github.com/RaskaRuby/createSeedWords/blob/master/createSeedWordsXMR.py) - Creates Monero seed words. Verify results by running [`monero-wallet-cli`](https://getmonero.org) OFFLINE, restoring from seed words, and comparing the secret spend keys.

### Usage

**WARNING** - For maximum security, run only on a secure OFFLINE system like [Tails](https://tails.boum.org/). Revealing any of the user entropy, seed words or keys generated could allow theft of the wallet.

Enter random data from any of these formats to generate BIP39 seed words:

* **No Input** - PRNG number from python urandom(32), 256 bits -> 24 words (NOT RECOMMENDED, as you depend on someone else's entropy)
* **Seed Words** - enter 11-23 space-separated seed words, and final checksum word is computed. Supports shortened 3-4 letter words.
* **Binary** [0,1] - coin flips, or D6 dice rolls where 1-3 is a zero, and 4-6 is a one.
* **Regular D6 Dice** [1-6] - Ian Coleman style with bias removal, 1.67 bits entropy per roll.
* **Hexadecimal [D16 Dice](https://github.com/Samourai-Wallet/hexadecimal-die)** [0-9,a-f,A-F] - 4 bits per character, 32-64 chars -> 12-24 words.


