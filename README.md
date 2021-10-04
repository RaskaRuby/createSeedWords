## Create Seed Words

Create bitcoin BIP39 and Monero wallet mneumonic seed words using simple python scripts and user-provided entropy.

### How Safe Are Your Private Keys?

When creating a new wallet, modern wallet software creates a unique set of seed words, and those represent the private key of the wallet. Your prefered wallet software probably does this securely, but even with open-source, it is difficult to tell if the pseudo-random number generator (PRNG) used is really secure, or if it has been maliciously tweaked to permit a later retirement attack.

### Creating Your Own Entropy

A way to mitigate this risk is to generate your own entropy and create your own seed words. One way to do this by hand is [described here by ArmanTheParman](https://armantheparman.com/bitcoin-seed-with-dice/), where coins or dice are used, and a computer is only needed at the very end to calculate the final seed word.

The bitcoin hardware wallet [ColdCard](https://coldcardwallet.com/) also allows you to provide [your own entropy via D6 dice rolls](https://coldcardwallet.com/docs/verifying-dice-roll-math). They realized that even that wasn't transparent enough, so they also provide a [very simple python script `rolls.py`](https://coldcardwallet.com/docs/rolls.py) with which to verify that your D6 dice rolls generate the same seed words that the ColdCard came up with.

### Usage

This project builds on [`rolls.py`](https://coldcardwallet.com/docs/rolls.py) by allowing a variety of input, including D6 dice, binary from coins, and [hexadecimal D16 dice](https://github.com/Samourai-Wallet/hexadecimal-die). No extra python libraries are needed, so these scripts should run almost anywhere, and should be fairly readable to beginning python programmers.

**WARNING** - For maximum security, run only on a secure OFFLINE system like Tails. Revealing any of the user entropy, seed words or keys generated could allow theft of the wallet.

The following user input is supported to create 256 bits of entropy:
* **No Input** (not recommended) - uses python PRNG urandom(32)
* **Binary** [0,1] - requires exactly 256 coin flips, or D6 dice rolls where 1-3 is a zero, and 4-6 is a one
* **Regular D6 Dice** [1-6] - any number dice rolls (50+ is safe), hashed to 256 bits (This is the ColdCard rolls.py method)
* **[Hex D16 Dice](https://github.com/Samourai-Wallet/hexadecimal-die)** [0-9,a-f,A-F] - requires exactly 64 hexadecimal characters

### Python Scripts

* [`createSeedWordsBTC.py`](https://github.com/RaskaRuby/createSeedWords/blob/master/createSeedWordsBTC.py) - Creates bitcoin BIP39 seed words. Verify results by running [`bip39-standalone.html`](https://github.com/iancoleman/bip39) OFFLINE. Enter created seed words, Show Entropy Details, and the hex entropy should match.
* [`createSeedWordsXMR.py`](https://github.com/RaskaRuby/createSeedWords/blob/master/createSeedWordsXMR.py) - Creates Monero seed words. Verify results by running [`monero-wallet-cli`](https://getmonero.org) OFFLINE, restoring from seed words, and comparing the secret spend keys.

