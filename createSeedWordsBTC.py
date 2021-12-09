#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Create new BIP39 seed words from user-provided raw entropy.
# Requires python3, but no other libraries.
#
# Based off of CoinKite code at <https://coldcardwallet.com/docs/rolls.py>
# Public domain
#
#
# Test Data - 256 bit entropy - generates 24 seed words
#	Binary: 1110010011111100111000010111111101010100101000010010000010111001110010001010111011001010001000001010111110010100110001010111011001011010100010101001001101101110101010101101100100010011111011110001101100111001101000011101101110100000101000000011001000010101
#	Hex   : e4fce17f54a120b9c8aeca20af94c5765a8a936eaad913ef1b39a1dba0a03215
#	Words : top train garlic power bamboo friend cargo sun camera lake course uncover post endless rival forest become juice solar dry ring exotic sign rack
#
#   Dice-6: 123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123456123
#   Binary: 0110110100011011010001101101000110110100011011010001101101000110110100011011010001101101000110110100011011010001101101000110110100011011010001101101000110110100011011010001101101000110110100011011010001101101000110110100011011010001101101000110110100011011
#   Hex   : 6d1b46d1b46d1b46d1b46d1b46d1b46d1b46d1b46d1b46d1b46d1b46d1b46d1b
#   Words : home surface refuse hand spider pet egg misery brave custom home surface refuse hand spider pet egg misery brave custom home surface refuse legend
#

import binascii		# hex - byte conversions
import hashlib		# sha256
import os			# urandom
import re			# string testing
import sys			# sys.exit()

# BIP39 wordlist (English)
wordListCount = 2048
wordListArray = '''\
abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acid acoustic acquire across act action actor actress actual adapt add addict address adjust admit adult advance advice aerobic affair afford afraid again age agent agree ahead aim air airport aisle alarm album alcohol alert alien all alley allow almost alone alpha already also alter always amateur amazing among amount amused analyst anchor ancient anger angle angry animal ankle announce annual another answer antenna antique anxiety any apart apology appear apple approve april arch arctic area arena argue arm armed armor army around arrange arrest arrive arrow art artefact artist artwork ask aspect assault asset assist assume asthma athlete atom attack attend attitude attract auction audit august aunt author auto autumn average avocado avoid awake aware away awesome awful awkward axis baby bachelor bacon badge bag balance balcony ball bamboo banana banner bar barely bargain barrel base basic basket battle beach bean beauty because become beef before begin behave behind believe below belt bench benefit best betray better between beyond bicycle bid bike bind biology bird birth bitter black blade blame blanket blast bleak bless blind blood blossom blouse blue blur blush board boat body boil bomb bone bonus book boost border boring borrow boss bottom bounce box boy bracket brain brand brass brave bread breeze brick bridge brief bright bring brisk broccoli broken bronze broom brother brown brush bubble buddy budget buffalo build bulb bulk bullet bundle bunker burden burger burst bus business busy butter buyer buzz cabbage cabin cable cactus cage cake call calm camera camp can canal cancel candy cannon canoe canvas canyon capable capital captain car carbon card cargo carpet carry cart case cash casino castle casual cat catalog catch category cattle caught cause caution cave ceiling celery cement census century cereal certain chair chalk champion change chaos chapter charge chase chat cheap check cheese chef cherry chest chicken chief child chimney choice choose chronic chuckle chunk churn cigar cinnamon circle citizen city civil claim clap clarify claw clay clean clerk clever click client cliff climb clinic clip clock clog close cloth cloud clown club clump cluster clutch coach coast coconut code coffee coil coin collect color column combine come comfort comic common company concert conduct confirm congress connect consider control convince cook cool copper copy coral core corn correct cost cotton couch country couple course cousin cover coyote crack cradle craft cram crane crash crater crawl crazy cream credit creek crew cricket crime crisp critic crop cross crouch crowd crucial cruel cruise crumble crunch crush cry crystal cube culture cup cupboard curious current curtain curve cushion custom cute cycle dad damage damp dance danger daring dash daughter dawn day deal debate debris decade december decide decline decorate decrease deer defense define defy degree delay deliver demand demise denial dentist deny depart depend deposit depth deputy derive describe desert design desk despair destroy detail detect develop device devote diagram dial diamond diary dice diesel diet differ digital dignity dilemma dinner dinosaur direct dirt disagree discover disease dish dismiss disorder display distance divert divide divorce dizzy doctor document dog doll dolphin domain donate donkey donor door dose double dove draft dragon drama drastic draw dream dress drift drill drink drip drive drop drum dry duck dumb dune during dust dutch duty dwarf dynamic eager eagle early earn earth easily east easy echo ecology economy edge edit educate effort egg eight either elbow elder electric elegant element elephant elevator elite else embark embody embrace emerge emotion employ empower empty enable enact end endless endorse enemy energy enforce engage engine enhance enjoy enlist enough enrich enroll ensure enter entire entry envelope episode equal equip era erase erode erosion error erupt escape essay essence estate eternal ethics evidence evil evoke evolve exact example excess exchange excite exclude excuse execute exercise exhaust exhibit exile exist exit exotic expand expect expire explain expose express extend extra eye eyebrow fabric face faculty fade faint faith fall false fame family famous fan fancy fantasy farm fashion fat fatal father fatigue fault favorite feature february federal fee feed feel female fence festival fetch fever few fiber fiction field figure file film filter final find fine finger finish fire firm first fiscal fish fit fitness fix flag flame flash flat flavor flee flight flip float flock floor flower fluid flush fly foam focus fog foil fold follow food foot force forest forget fork fortune forum forward fossil foster found fox fragile frame frequent fresh friend fringe frog front frost frown frozen fruit fuel fun funny furnace fury future gadget gain galaxy gallery game gap garage garbage garden garlic garment gas gasp gate gather gauge gaze general genius genre gentle genuine gesture ghost giant gift giggle ginger giraffe girl give glad glance glare glass glide glimpse globe gloom glory glove glow glue goat goddess gold good goose gorilla gospel gossip govern gown grab grace grain grant grape grass gravity great green grid grief grit grocery group grow grunt guard guess guide guilt guitar gun gym habit hair half hammer hamster hand happy harbor hard harsh harvest hat have hawk hazard head health heart heavy hedgehog height hello helmet help hen hero hidden high hill hint hip hire history hobby hockey hold hole holiday hollow home honey hood hope horn horror horse hospital host hotel hour hover hub huge human humble humor hundred hungry hunt hurdle hurry hurt husband hybrid ice icon idea identify idle ignore ill illegal illness image imitate immense immune impact impose improve impulse inch include income increase index indicate indoor industry infant inflict inform inhale inherit initial inject injury inmate inner innocent input inquiry insane insect inside inspire install intact interest into invest invite involve iron island isolate issue item ivory jacket jaguar jar jazz jealous jeans jelly jewel job join joke journey joy judge juice jump jungle junior junk just kangaroo keen keep ketchup key kick kid kidney kind kingdom kiss kit kitchen kite kitten kiwi knee knife knock know lab label labor ladder lady lake lamp language laptop large later latin laugh laundry lava law lawn lawsuit layer lazy leader leaf learn leave lecture left leg legal legend leisure lemon lend length lens leopard lesson letter level liar liberty library license life lift light like limb limit link lion liquid list little live lizard load loan lobster local lock logic lonely long loop lottery loud lounge love loyal lucky luggage lumber lunar lunch luxury lyrics machine mad magic magnet maid mail main major make mammal man manage mandate mango mansion manual maple marble march margin marine market marriage mask mass master match material math matrix matter maximum maze meadow mean measure meat mechanic medal media melody melt member memory mention menu mercy merge merit merry mesh message metal method middle midnight milk million mimic mind minimum minor minute miracle mirror misery miss mistake mix mixed mixture mobile model modify mom moment monitor monkey monster month moon moral more morning mosquito mother motion motor mountain mouse move movie much muffin mule multiply muscle museum mushroom music must mutual myself mystery myth naive name napkin narrow nasty nation nature near neck need negative neglect neither nephew nerve nest net network neutral never news next nice night noble noise nominee noodle normal north nose notable note nothing notice novel now nuclear number nurse nut oak obey object oblige obscure observe obtain obvious occur ocean october odor off offer office often oil okay old olive olympic omit once one onion online only open opera opinion oppose option orange orbit orchard order ordinary organ orient original orphan ostrich other outdoor outer output outside oval oven over own owner oxygen oyster ozone pact paddle page pair palace palm panda panel panic panther paper parade parent park parrot party pass patch path patient patrol pattern pause pave payment peace peanut pear peasant pelican pen penalty pencil people pepper perfect permit person pet phone photo phrase physical piano picnic picture piece pig pigeon pill pilot pink pioneer pipe pistol pitch pizza place planet plastic plate play please pledge pluck plug plunge poem poet point polar pole police pond pony pool popular portion position possible post potato pottery poverty powder power practice praise predict prefer prepare present pretty prevent price pride primary print priority prison private prize problem process produce profit program project promote proof property prosper protect proud provide public pudding pull pulp pulse pumpkin punch pupil puppy purchase purity purpose purse push put puzzle pyramid quality quantum quarter question quick quit quiz quote rabbit raccoon race rack radar radio rail rain raise rally ramp ranch random range rapid rare rate rather raven raw razor ready real reason rebel rebuild recall receive recipe record recycle reduce reflect reform refuse region regret regular reject relax release relief rely remain remember remind remove render renew rent reopen repair repeat replace report require rescue resemble resist resource response result retire retreat return reunion reveal review reward rhythm rib ribbon rice rich ride ridge rifle right rigid ring riot ripple risk ritual rival river road roast robot robust rocket romance roof rookie room rose rotate rough round route royal rubber rude rug rule run runway rural sad saddle sadness safe sail salad salmon salon salt salute same sample sand satisfy satoshi sauce sausage save say scale scan scare scatter scene scheme school science scissors scorpion scout scrap screen script scrub sea search season seat second secret section security seed seek segment select sell seminar senior sense sentence series service session settle setup seven shadow shaft shallow share shed shell sheriff shield shift shine ship shiver shock shoe shoot shop short shoulder shove shrimp shrug shuffle shy sibling sick side siege sight sign silent silk silly silver similar simple since sing siren sister situate six size skate sketch ski skill skin skirt skull slab slam sleep slender slice slide slight slim slogan slot slow slush small smart smile smoke smooth snack snake snap sniff snow soap soccer social sock soda soft solar soldier solid solution solve someone song soon sorry sort soul sound soup source south space spare spatial spawn speak special speed spell spend sphere spice spider spike spin spirit split spoil sponsor spoon sport spot spray spread spring spy square squeeze squirrel stable stadium staff stage stairs stamp stand start state stay steak steel stem step stereo stick still sting stock stomach stone stool story stove strategy street strike strong struggle student stuff stumble style subject submit subway success such sudden suffer sugar suggest suit summer sun sunny sunset super supply supreme sure surface surge surprise surround survey suspect sustain swallow swamp swap swarm swear sweet swift swim swing switch sword symbol symptom syrup system table tackle tag tail talent talk tank tape target task taste tattoo taxi teach team tell ten tenant tennis tent term test text thank that theme then theory there they thing this thought three thrive throw thumb thunder ticket tide tiger tilt timber time tiny tip tired tissue title toast tobacco today toddler toe together toilet token tomato tomorrow tone tongue tonight tool tooth top topic topple torch tornado tortoise toss total tourist toward tower town toy track trade traffic tragic train transfer trap trash travel tray treat tree trend trial tribe trick trigger trim trip trophy trouble truck true truly trumpet trust truth try tube tuition tumble tuna tunnel turkey turn turtle twelve twenty twice twin twist two type typical ugly umbrella unable unaware uncle uncover under undo unfair unfold unhappy uniform unique unit universe unknown unlock until unusual unveil update upgrade uphold upon upper upset urban urge usage use used useful useless usual utility vacant vacuum vague valid valley valve van vanish vapor various vast vault vehicle velvet vendor venture venue verb verify version very vessel veteran viable vibrant vicious victory video view village vintage violin virtual virus visa visit visual vital vivid vocal voice void volcano volume vote voyage wage wagon wait walk wall walnut want warfare warm warrior wash wasp waste water wave way wealth weapon wear weasel weather web wedding weekend weird welcome west wet whale what wheat wheel when where whip whisper wide width wife wild will win window wine wing wink winner winter wire wisdom wise wish witness wolf woman wonder wood wool word work world worry worth wrap wreck wrestle wrist write wrong yard year yellow you young youth zebra zero zone zoo'''.split()


def printUsage():
	print("Usage  : Create BIP39 seed words from user-provided raw entropy")
	print("         Entropy bit count makes (seed words): 128 bits (12 words), 160 (15), 192 (18), 224 (21), 256 bits (24 words)")
	print("         Entropy bits must be exactly 128 bits (minimum), 160, 192, 224 or 256 (maximum)")
	print("WARNING: For maximum security, run only on a secure OFFLINE system like Tails")
	print("         Revealing any of the below data could allow theft of wallet")
	print("Verify : Run bip39-standalone.html OFFLINE (https://github.com/iancoleman/bip39)")
	print("         Show entropy details, Use Raw Entropy, and enter entropy")
	print("         Seed words should match those generated here")
	print("Input  : any of these formats")
	print("   None                 : python pseudo-random number generator urandom(32) makes 256 bits (NOT RECOMMENDED)")
	print("   Binary [0,1]         : coin flips, etc.")
	print("   Dice-6 [1-6]         : Ian Coleman style with bias removal, 1.67 bits per roll")
	print("   Dice-16 [0-9,a-f,A-F]: 4 bits per character, 32 chars -> 12 words, 64 chars -> 24 words")
	print()


def printResults(hexString, seedWordsArray):
	print("RaW Hex: " + hexString)
	print()
	print("BIP39 Seed Words(" + str(len(seedWordsArray)) + "): " + ' '.join('%s' % (val) for i, val in enumerate(seedWordsArray)))
	#print('\n'.join('%3d: %s' % (i+1, val) for i, val in enumerate(seedWordsArray)))	# print numbered seed words on separate lines
	print()


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


# Truncate binary string to greater of length 256, 224, 192, 160, or 128
# Do nothing if less than 128
def truncateBinaryString(binaryString):
	strLen = len(binaryString)
	if strLen > 255:
		binaryString = binaryString[0:256]
	elif strLen > 223:
		binaryString = binaryString[0:224]
	elif strLen > 191:
		binaryString = binaryString[0:192]
	elif strLen > 159:
		binaryString = binaryString[0:160]
	elif strLen > 127:
		binaryString = binaryString[0:128]
	return binaryString


# Truncate hex string to greater of length 32, 40, 48, 56, or 64
# Do nothing if less than 32
def truncateHexString(hexString):
	strLen = len(hexString)
	if strLen > 63:
		hexString = hexString[0:64]
	elif strLen > 55:
		hexString = hexString[0:56]
	elif strLen > 47:
		hexString = hexString[0:48]
	elif strLen > 39:
		hexString = hexString[0:40]
	elif strLen > 31:
		hexString = hexString[0:32]
	return hexString


# ian coleman method to remove bias from D6 rolls
def removeBiasFromBase6(base6String):
	binaryString = ""
	for element in base6String:
		if element == '0':
			binaryString += "00"
		elif element == '1':
			binaryString += "01"
		elif element == '2':
			binaryString += "10"
		elif element == '3':
			binaryString += "11"
		elif element == '4':
			binaryString += "0"
		elif element == '5':
			binaryString += "1"
	return binaryString


def main():

	printUsage()

	# Read input
	inputString = input().strip()				# remove leading and trailing whitespace
	inputString = inputString.replace(" ","")	# remove any spaces (Ian Coleman Raw Binary has spaces in it)
	print()

	# Make sure word list has the correct number of words
	wordListLen = len(wordListArray)
	if wordListLen != wordListCount:
		print("ERROR - wordListArray should contain " + str(wordListCount) + " words, and it instead contains  " + str(wordListLen))
		return

	# Validate input string, and convert it to a hex string
	hexString = ''
	inputLen = len(inputString)
	if inputLen == 0:

		hexString = os.urandom(32).hex()
		print("Input: Random (256 bits)  NOT RECOMMENDED")

	elif isBinaryString(inputString):

		binaryString = inputString
		#binaryString = truncateBinaryString(binaryString)
		binaryLen = len(binaryString)
		if binaryLen == 128 or binaryLen == 160 or binaryLen == 192 or binaryLen == 224 or binaryLen == 256:
			print("Input: Binary (" + str(binaryLen) + " bits): " + binaryString)
			hexString = hex(int(inputString, 2))	# convert binary string to hex
			hexString = hexString[2:]			# remove leading '0x' added by hex()
		else:
			print("ERROR - Binary bits " + str(inputLen) + ", but must only be [128,160,192,224,256].")
			return

	elif isD6String(inputString):

		# ColdCard method (unused)
		#print("Input: Dice-6 (" + str(len(inputString)) + " rolls) ColdCard SHA256")
		#hexString = hashlib.sha256(inputString.encode()).hexdigest()	# hash D6 string to 64 hex chars

		# convert D6 to Base6, remove bias and truncate
		base6String = inputString.replace('6', '0')
		binaryString = removeBiasFromBase6(base6String)
		#binaryString = truncateBinaryString(binaryString)
		binaryLen = len(binaryString)

		if binaryLen == 128 or binaryLen == 160 or binaryLen == 192 or binaryLen == 224 or binaryLen == 256:
			print("Input: Dice-6 (" + str(inputLen) + " rolls)")
			print("Raw Binary (" + str(binaryLen) + " bits): " + binaryString)
			hexString = hex(int(binaryString, 2))	# convert binary string to hex
			hexString = hexString[2:]			# remove leading '0x' added by hex()
		else:
			print("ERROR - Dice-6 bit count is " + str(binaryLen) + ", but must only be [128,160,192,224,256].")
			return

	elif isHexString(inputString):

		hexString = inputString
		#hexString = truncateHexString(hexString)
		hexLen = len(hexString)

		if hexLen == 32 or hexLen == 40 or hexLen == 48 or hexLen == 56 or hexLen == 64:
			print("Input: Dice-16 (" + str(hexLen*4) + " bits)")
		else:
			print("ERROR - Hex input length is " + str(hexLen) + ", but must only be [32,40,48,56,64].")
			return
	else:

		print("ERROR - Unknown input character - must be [0-9,a-f,A-F] or none")
		return

	# convert hex input string to binary data (a large number)
	binaryData = binascii.unhexlify(hexString)

	# calculate hash of binary data (used for final checksum word)
	binaryDataHash = hashlib.sha256(binaryData).hexdigest()

	# append checksum to binary data
	binaryData = bin(int(binascii.hexlify(binaryData),16))[2:].zfill(len(binaryData)*8) + bin(int(binaryDataHash,16))[2:].zfill(256)[: 	len(binaryData)* 8//32]

	# convert to seed words
	seedWordsArray = []
	for seedWordIndex in range(len(binaryData)//11):
		wordListIndex = int(binaryData[11*seedWordIndex:11*(seedWordIndex+1)],2)
		seedWordsArray.append(wordListArray[wordListIndex])

	# print results
	printResults(hexString, seedWordsArray)
	return


if __name__ == "__main__":
	# Try/except below just keeps ctrl-c from printing an ugly stacktrace
	try:
		main()
	except (KeyboardInterrupt, SystemExit):
		sys.exit()

