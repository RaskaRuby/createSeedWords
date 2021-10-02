#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Create 25 XMR seed words from 256 bits of user-provided binary, d6, or hex entropy.
# Requires python3, but no other libraries.
# Public domain
#
# Test Data
#	Binary Input: 1110010011111100111000010111111101010100101000010010000010111001110010001010111011001010001000001010111110010100110001010111011001011010100010101001001101101110101010101101100100010011111011110001101100111001101000011101101110100000101000000011001000010101
#	Hex Input   : e4fce17f54a120b9c8aeca20af94c5765a8a936eaad913ef1b39a1dba0a03215
#	Mnemonic      : actress lynx adhesive abbey selfish leisure annoyed cabin essential eldest venomous hunter pairing gadget satin sunken vein tomorrow aloof rumble obliged juicy whipped annoyed cabin
#	Address       : 49Muee99SBUbXpYUXAK49s4qYygHaYXmAJ48B2y7x1qwiRyFMtr9B7mMCyQSgyRLbVSKhujpTDghs5KpeR88rhrP9az76Z6
#	SecretSpendKey: f728ec223a3e0e61f211d37dd09ae6615a8a936eaad913ef1b39a1dba0a03205
#	SecretViewKey : 3859c4887c3dc6fba1d1554f7fb5e5bbb3e6336ee189ab8dc8d1132d2bd45401
#	PublicSpendKey: cc30f12dcebe03ce7318cb93ac6fce16f0c2e1d2fbf2e165f5562658f21b4ef7
#	PublicViewKey : b265308ae5612078ce6a001219cfdc9764b3e61afbd81e19dac36bc4961ac84c
#

import binascii				# hex - byte conversions
import hashlib				# sha256
import operator as _oper 	# ed25519
import os					# urandom
import re					# string testing
import sys					# sys.exit()

# XMR wordlist (English)
wordListCount = 1626
wordListArray = '''\
abbey abducts ability ablaze abnormal abort abrasive absorb abyss academy aces aching acidic acoustic acquire across actress acumen adapt addicted adept adhesive adjust adopt adrenalin adult adventure aerial afar affair afield afloat afoot afraid after against agenda aggravate agile aglow agnostic agony agreed ahead aided ailments aimless airport aisle ajar akin alarms album alchemy alerts algebra alkaline alley almost aloof alpine already also altitude alumni always amaze ambush amended amidst ammo amnesty among amply amused anchor android anecdote angled ankle annoyed answers antics anvil anxiety anybody apart apex aphid aplomb apology apply apricot aptitude aquarium arbitrary archer ardent arena argue arises army around arrow arsenic artistic ascend ashtray aside asked asleep aspire assorted asylum athlete atlas atom atrium attire auburn auctions audio august aunt austere autumn avatar avidly avoid awakened awesome awful awkward awning awoken axes axis axle aztec azure baby bacon badge baffles bagpipe bailed bakery balding bamboo banjo baptism basin batch bawled bays because beer befit begun behind being below bemused benches berries bested betting bevel beware beyond bias bicycle bids bifocals biggest bikini bimonthly binocular biology biplane birth biscuit bite biweekly blender blip bluntly boat bobsled bodies bogeys boil boldly bomb border boss both bounced bovine bowling boxes boyfriend broken brunt bubble buckets budget buffet bugs building bulb bumper bunch business butter buying buzzer bygones byline bypass cabin cactus cadets cafe cage cajun cake calamity camp candy casket catch cause cavernous cease cedar ceiling cell cement cent certain chlorine chrome cider cigar cinema circle cistern citadel civilian claim click clue coal cobra cocoa code coexist coffee cogs cohesive coils colony comb cool copy corrode costume cottage cousin cowl criminal cube cucumber cuddled cuffs cuisine cunning cupcake custom cycling cylinder cynical dabbing dads daft dagger daily damp dangerous dapper darted dash dating dauntless dawn daytime dazed debut decay dedicated deepest deftly degrees dehydrate deity dejected delayed demonstrate dented deodorant depth desk devoid dewdrop dexterity dialect dice diet different digit dilute dime dinner diode diplomat directed distance ditch divers dizzy doctor dodge does dogs doing dolphin domestic donuts doorway dormant dosage dotted double dove down dozen dreams drinks drowning drunk drying dual dubbed duckling dude duets duke dullness dummy dunes duplex duration dusted duties dwarf dwelt dwindling dying dynamite dyslexic each eagle earth easy eating eavesdrop eccentric echo eclipse economics ecstatic eden edgy edited educated eels efficient eggs egotistic eight either eject elapse elbow eldest eleven elite elope else eluded emails ember emerge emit emotion empty emulate energy enforce enhanced enigma enjoy enlist enmity enough enraged ensign entrance envy epoxy equip erase erected erosion error eskimos espionage essential estate etched eternal ethics etiquette evaluate evenings evicted evolved examine excess exhale exit exotic exquisite extra exult fabrics factual fading fainted faked fall family fancy farming fatal faulty fawns faxed fazed feast february federal feel feline females fences ferry festival fetches fever fewest fiat fibula fictional fidget fierce fifteen fight films firm fishing fitting five fixate fizzle fleet flippant flying foamy focus foes foggy foiled folding fonts foolish fossil fountain fowls foxes foyer framed friendly frown fruit frying fudge fuel fugitive fully fuming fungal furnished fuselage future fuzzy gables gadget gags gained galaxy gambit gang gasp gather gauze gave gawk gaze gearbox gecko geek gels gemstone general geometry germs gesture getting geyser ghetto ghost giant giddy gifts gigantic gills gimmick ginger girth giving glass gleeful glide gnaw gnome goat goblet godfather goes goggles going goldfish gone goodbye gopher gorilla gossip gotten gourmet governing gown greater grunt guarded guest guide gulp gumball guru gusts gutter guys gymnast gypsy gyrate habitat hacksaw haggled hairy hamburger happens hashing hatchet haunted having hawk haystack hazard hectare hedgehog heels hefty height hemlock hence heron hesitate hexagon hickory hiding highway hijack hiker hills himself hinder hippo hire history hitched hive hoax hobby hockey hoisting hold honked hookup hope hornet hospital hotel hounded hover howls hubcaps huddle huge hull humid hunter hurried husband huts hybrid hydrogen hyper iceberg icing icon identity idiom idled idols igloo ignore iguana illness imagine imbalance imitate impel inactive inbound incur industrial inexact inflamed ingested initiate injury inkling inline inmate innocent inorganic input inquest inroads insult intended inundate invoke inwardly ionic irate iris irony irritate island isolated issued italics itches items itinerary itself ivory jabbed jackets jaded jagged jailed jamming january jargon jaunt javelin jaws jazz jeans jeers jellyfish jeopardy jerseys jester jetting jewels jigsaw jingle jittery jive jobs jockey jogger joining joking jolted jostle journal joyous jubilee judge juggled juicy jukebox july jump junk jury justice juvenile kangaroo karate keep kennel kept kernels kettle keyboard kickoff kidneys king kiosk kisses kitchens kiwi knapsack knee knife knowledge knuckle koala laboratory ladder lagoon lair lakes lamb language laptop large last later launching lava lawsuit layout lazy lectures ledge leech left legion leisure lemon lending leopard lesson lettuce lexicon liar library licks lids lied lifestyle light likewise lilac limits linen lion lipstick liquid listen lively loaded lobster locker lodge lofty logic loincloth long looking lopped lordship losing lottery loudly love lower loyal lucky luggage lukewarm lullaby lumber lunar lurk lush luxury lymph lynx lyrics macro madness magically mailed major makeup malady mammal maps masterful match maul maverick maximum mayor maze meant mechanic medicate meeting megabyte melting memoir menu merger mesh metro mews mice midst mighty mime mirror misery mittens mixture moat mobile mocked mohawk moisture molten moment money moon mops morsel mostly motherly mouth movement mowing much muddy muffin mugged mullet mumble mundane muppet mural musical muzzle myriad mystery myth nabbing nagged nail names nanny napkin narrate nasty natural nautical navy nearby necklace needed negative neither neon nephew nerves nestle network neutral never newt nexus nibs niche niece nifty nightly nimbly nineteen nirvana nitrogen nobody nocturnal nodes noises nomad noodles northern nostril noted nouns novelty nowhere nozzle nuance nucleus nudged nugget nuisance null number nuns nurse nutshell nylon oaks oars oasis oatmeal obedient object obliged obnoxious observant obtains obvious occur ocean october odds odometer offend often oilfield ointment okay older olive olympics omega omission omnibus onboard oncoming oneself ongoing onion online onslaught onto onward oozed opacity opened opposite optical opus orange orbit orchid orders organs origin ornament orphans oscar ostrich otherwise otter ouch ought ounce ourselves oust outbreak oval oven owed owls owner oxidant oxygen oyster ozone pact paddles pager pairing palace pamphlet pancakes paper paradise pastry patio pause pavements pawnshop payment peaches pebbles peculiar pedantic peeled pegs pelican pencil people pepper perfect pests petals phase pheasants phone phrases physics piano picked pierce pigment piloted pimple pinched pioneer pipeline pirate pistons pitched pivot pixels pizza playful pledge pliers plotting plus plywood poaching pockets podcast poetry point poker polar ponies pool popular portents possible potato pouch poverty powder pram present pride problems pruned prying psychic public puck puddle puffin pulp pumpkins punch puppy purged push putty puzzled pylons pyramid python queen quick quote rabbits racetrack radar rafts rage railway raking rally ramped randomly rapid rarest rash rated ravine rays razor react rebel recipe reduce reef refer regular reheat reinvest rejoices rekindle relic remedy renting reorder repent request reruns rest return reunion revamp rewind rhino rhythm ribbon richly ridges rift rigid rims ringing riots ripped rising ritual river roared robot rockets rodent rogue roles romance roomy roped roster rotate rounded rover rowboat royal ruby rudely ruffled rugged ruined ruling rumble runway rural rustled ruthless sabotage sack sadness safety saga sailor sake salads sample sanity sapling sarcasm sash satin saucepan saved sawmill saxophone sayings scamper scenic school science scoop scrub scuba seasons second sedan seeded segments seismic selfish semifinal sensible september sequence serving session setup seventh sewage shackles shelter shipped shocking shrugged shuffled shyness siblings sickness sidekick sieve sifting sighting silk simplest sincerely sipped siren situated sixteen sizes skater skew skirting skulls skydive slackens sleepless slid slower slug smash smelting smidgen smog smuggled snake sneeze sniff snout snug soapy sober soccer soda software soggy soil solved somewhere sonic soothe soprano sorry southern sovereign sowed soya space speedy sphere spiders splendid spout sprig spud spying square stacking stellar stick stockpile strained stunning stylishly subtly succeed suddenly suede suffice sugar suitcase sulking summon sunken superior surfer sushi suture swagger swept swiftly sword swung syllabus symptoms syndrome syringe system taboo tacit tadpoles tagged tail taken talent tamper tanks tapestry tarnished tasked tattoo taunts tavern tawny taxi teardrop technical tedious teeming tell template tender tepid tequila terminal testing tether textbook thaw theatrics thirsty thorn threaten thumbs thwart ticket tidy tiers tiger tilt timber tinted tipsy tirade tissue titans toaster tobacco today toenail toffee together toilet token tolerant tomorrow tonic toolbox topic torch tossed total touchy towel toxic toyed trash trendy tribal trolling truth trying tsunami tubes tucks tudor tuesday tufts tugs tuition tulips tumbling tunnel turnip tusks tutor tuxedo twang tweezers twice twofold tycoon typist tyrant ugly ulcers ultimate umbrella umpire unafraid unbending uncle under uneven unfit ungainly unhappy union unjustly unknown unlikely unmask unnoticed unopened unplugs unquoted unrest unsafe until unusual unveil unwind unzip upbeat upcoming update upgrade uphill upkeep upload upon upper upright upstairs uptight upwards urban urchins urgent usage useful usher using usual utensils utility utmost utopia uttered vacation vague vain value vampire vane vapidly vary vastness vats vaults vector veered vegan vehicle vein velvet venomous verification vessel veteran vexed vials vibrate victim video viewpoint vigilant viking village vinegar violin vipers virtual visited vitals vivid vixen vocal vogue voice volcano vortex voted voucher vowels voyage vulture wade waffle wagtail waist waking wallets wanted warped washing water waveform waxing wayside weavers website wedge weekday weird welders went wept were western wetsuit whale when whipped whole wickets width wield wife wiggle wildly winter wipeout wiring wise withdrawn wives wizard wobbly woes woken wolf womanly wonders woozy worry wounded woven wrap wrist wrong yacht yahoo yanks yard yawning yearbook yellow yesterday yeti yields yodel yoga younger yoyo zapped zeal zebra zero zesty zigzags zinger zippers zodiac zombie zones zoom'''.split()

# ed25519
ed25519_indexbytes = _oper.getitem
ed25519_int2byte = _oper.methodcaller("to_bytes", 1, "big")
ed25519_bits = 256
ed25519_limit = 2**252 + 27742317777372353535851937790883648493
def ed25519_bit(h, i):
    return (ed25519_indexbytes(h, i//8) >> (i%8)) & 1
def ed25519_encodeint(y):
    bits = [(y >> i) & 1 for i in range(ed25519_bits)]
    return b''.join([ed25519_int2byte(sum([bits[i*8 + j] << j for j in range(8)])) for i in range(ed25519_bits//8)])
def ed25519_decodeint(s):
    return sum(2**i * ed25519_bit(s, i) for i in range(0, ed25519_bits))


# Given string, swap bits and return string.
def utils_endian_swap(word):
    return "".join([word[i:i+2] for i in [6, 4, 2, 0]])


# convert hex string to integer
def utils_hex2int(hex):
    return ed25519_decodeint(binascii.unhexlify(hex))


# convert integer to little endian encoded hex string
def utils_int2hex(int):
    return binascii.hexlify(ed25519_encodeint(int))


def utils_sc_reduce32(input):
    int = utils_hex2int(input)		# convert hex string input to integer
    modulo = int % (ed25519_limit)	# reduce mod ed25519_limit
    return utils_int2hex(modulo)	# convert back to hex string


def printUsage():
	print("Usage  : create XMR seed words from user entropy (25 word seed requires 256 bits entropy)")
	print("WARNING: for maximum security, run only on a secure OFFLINE system like Tails")
	print("         revealing any of the below data could allow theft of wallet")
	print("Verify : run monero-wallet-cli OFFLINE (download from https://getmonero.org)")
	print("         restore from seed words should create wallet with same secret spend key")
	print("Input  : any of these formats")
	print("   NONE                 : uses python pseudo-random number generator urandom(32)")
	print("   BINARY [0,1]         : exactly 256 coin flips")
	print("   DICE-6 [1-6]         : any number dice rolls (50+ is safe), hashed to 256 bits")
	print("   DICE-16 [0-9,a-f,A-F]: exactly 64 hexadecimal characters")
	print()


def printOutput(hexInputString, seedWordsArray, secretSpendKey):
	print("SECRET SPEND KEY  : " + secretSpendKey)
	print("XMR SEED WORDS(" + str(len(seedWordsArray)) + "): " + ' '.join('%s' % (val) for i, val in enumerate(seedWordsArray)))
	#print('\n'.join('%3d: %s' % (i+1, val) for i, val in enumerate(seedWordsArray)))	# print numbered seed words on separate lines
	#print("Entropy         : " + hexInputString)


def isBinaryString(string):
    charRe = re.compile(r'[^0-1.]')
    string = charRe.search(string)
    return not bool(string)


def isD6String(string):
    charRe = re.compile(r'[^1-6.]')
    string = charRe.search(string)
    return not bool(string)


def isHexString(string):
    charRe = re.compile(r'[^a-fA-F0-9.]')
    string = charRe.search(string)
    return not bool(string)


def main():

	printUsage()

	# Read input, remove whitespace around it
	inputString = input().strip()
	print()

	# make sure word list has the correct number of words
	wordListLen = len(wordListArray)
	if wordListLen != wordListCount:
		print("Error - wordListArray should contain " + str(wordListCount) + " words, and it instead contains  " + str(wordListLen))
		return

	# validate input string, and convert it to a hex string
	inputLen = len(inputString)
	hexInputString = ''
	if inputLen == 0:
		hexInputString = os.urandom(32).hex()
		print("RANDOM")
	elif isBinaryString(inputString):
		if inputLen ==  256:
			print("BINARY")
			hexInputString = hex(int(inputString, 2))	# convert binary string to hex
			hexInputString = hexInputString[2:]			# remove leading '0x' added by hex()
		else:
			print("ERROR - Binary input length is " + str(inputLen) + ". Must only be 256.")
			return
	elif isD6String(inputString):
		print("DICE-6")
		hexInputString = hashlib.sha256(inputString.encode()).hexdigest()	# hash D6 string to 64 hex chars
	elif isHexString(inputString):
		if inputLen == 64:
			print("DICE-16")
			hexInputString = inputString
		else:
			print("ERROR - Hex input length is " + str(inputLen) + ". Must only be 64.")
			return
	else:
		print("ERROR - Unknown input character - must be [0-9,a-f,A-F] or none")
		return

	# convert hexInputString into seed words (24 words plus one checksum word)
	seedWordsArray = []
	checkSumString = ''
	for i in range(len(hexInputString) // 8):
		word = utils_endian_swap(hexInputString[8*i:8*i+8])
		x = int(word, 16)
		w1 = x % wordListCount
		w2 = (x // wordListCount + w1) % wordListCount
		w3 = (x // wordListCount // wordListCount + w2) % wordListCount
		seedWordsArray += [wordListArray[w1], wordListArray[w2], wordListArray[w3]]
		checkSumString += wordListArray[w1][0:3]
		checkSumString += wordListArray[w2][0:3]
		checkSumString += wordListArray[w3][0:3]
	checkSumIndex = binascii.crc32(checkSumString.encode('utf-8')) % 24
	seedWordsArray.append(seedWordsArray[checkSumIndex])

    # secretSpendKey is the hexInputString value reduced to make it a valid ed25519 scalar
	secretSpendKey = utils_sc_reduce32(hexInputString)

	# print seed words and other output
	printOutput(hexInputString, seedWordsArray, secretSpendKey.decode('utf-8'))

	return


if __name__ == "__main__":
	# Try/except below just keeps ctrl-c from printing an ugly stacktrace
	try:
		main()
	except (KeyboardInterrupt, SystemExit):
		sys.exit()

