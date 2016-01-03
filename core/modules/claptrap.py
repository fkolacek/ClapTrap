#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import time

class Claptrap(object):

  meta = {
    'name': "Claptrap",
    'description': "Just few funny Clap Trap's quotes",
    'author': "F. Kolacek <fkolacek@redhat.com>",
    'version': "1.0",
    'triggers': {
      '^!clap': "haveSomeFun"
    },
    'usage': [
      "!clap - Shows random Clap Trap's quote"  
    ]
  }

  def __init__(self, bot):
    self._last = time.time()

    # Quotes from: http://borderlands.wikia.com/wiki/Claptrap/Quotes
    self._quotes = [
        [
          "Jack: Claptrap -- start bootup sequence.",
          "Claptrap: Directive one: Protect humanity! Directive two: Obey Jack at all costs. Directive three: Dance!",
          "Jack: No no no no! Cancel directive three!",
          "Claptrap: Commencing directive three! Uhntssuhntssuhntss--",
          "Jack: Ugh, friggin' hate that guy.",
          "Claptrap (commenting): Ahh -- one of my very first startup sequences! The memories..."
        ],
        [
          "Jack: Ah, man, I am so late!",
          "Jack: NO! Son of a... HEY! You! Yeah yeah, Claptrap unit!",
          "Claptrap: Who -- uh, me sir?",
          "Jack: Oh, no, I'm sorry the OTHER Hyperion piece of metal crap that can open doors for me. I'm sorry.",
          "Claptrap: I can do more than open doors sir! We CL4P-TP units can be programmed to do anything from open doors to ninja-sassinate highly important Janitory officals!",
          "Claptrap: I once started a revolution myself. There were lots of guns and a lot of dying. You'd think I would have gotten some better benefits out of the whole thing but no, demoted back to door-opening servitude!",
          "Jack: Yeahyeahyeahyeah, got it, just shut up and open the door. I'm late for the quarterly meeting."
        ],
        [
          "Claptrap: Booting sequence complete. Hello! I am your new steward bot. Designation: CL4P-TP, Hyperion Robot, Class C. Please adjust factory settings to meet your needs before deployment.",
          "Jack: Finally! Can you hear me? What do you remember?",
          "Claptrap: Yes. Remember what? Are... are you my father?",
          "Jack: Ah, no... uh, you --",
          "Claptrap: -- Are you god? Am I dead?",
          "Jack: Nonono, you're not dead, you're --",
          "Claptrap: I'M DEAD I'M DEAD OHMYGOD I'M DEAD!",
          "Jack: You. Are. Not. Dead! Your new designation is FR4G-TP. Fragtrap. You are a merciless killing machine. Got it?",
          "Claptrap: O-KAY! Thanks for giving me a second chance, God. I really appreciate it.",
          "Jack: What? No, nooo, you are so STUPID! Whatever. You're welcome."
        ],
        [ "Recompiling my combat code!" ],
        [ "This time it'll be awesome, I promise!" ],
        [ "Healsies!" ],
        [ "Crap, no more shots left!" ],
        [ "Watch as we observe the rare and beautiful Clappy Bird!" ],
        [ "Yeehaw!" ],
        [ "Badass!" ],
        [ "RUN FOR YOUR LIIIIIVES!!!" ],
        [ "That guy looks an awful lot like a Badass!" ],
        [ "Hehehehe, mwaa ha ha ha, MWAA HA HA HA!" ],
        [ "I am a tornado of death and bullets!" ],
        [ "Ha ha ha! Fall before your robot overlord!" ],
        [ "Is it dead? Can, can I open my eyes now?" ],
        [ "I didn't panic! Nope, not me!" ],
        [ "Ha ha ha! Suck it!" ],
        [ "Bad guy go boom!" ],
        [ "Take a chill pill!" ],
        [ "Freezy peezy!" ],
        [ "I can't feel my fingers! Gah! I don't have any fingers!" ],
        [ "Ow hohoho, that hurts! Yipes!" ],
        [ "If only my chassis... weren't made of recycled human body parts! Wahahaha!" ],
        [ "Disgusting. I love it!" ],
        [ "Ooooh! Terrabits!" ],
        [ "I'm pulling tricks outta my hat!" ],
        [ "Push this button, flip this dongle, voila! Help me!" ],
        [ "I have an IDEA!" ],
        [ "I AM ON FIRE!!! OH GOD, PUT ME OUT!!!" ],
        [ "Roses are red and/Violets are blue/Wait... how many syllables was that?" ],
        [ "Burn them, my mini-phoenix!" ],
        [ "Tell me I'm the prettiest!" ],
        [ "I am rubber, and you are so dead!" ],
        [ "Trouncy, flouncy... founcy... those aren't words." ],
        [ "Gotta blow up a bad guy, GOTTA BLOW UP A BAD GUY!" ],
        [ "You can call me Gundalf!" ],
        [ "Avada kedavra!" ],
        [ "Kill, reload! Kill, reload! KILL! RELOAD!" ],
        [ "Boogie time!" ],
        [ "Everybody, dance time! Da-da-da-dun-daaa-da-da-da-dun-daaa!" ],
        [ "I brought you a present: EXPLOSIONS!" ],
        [
            "Summoned bot: \"Knock Knock.\"",
            "Claptrap: \"Who's there?\"",
            "Summoned bot: \"Wub.\"",
            "Claptrap: \"Wub who?\"",
            "Summoned bot: \"Wubwubwubwubwub.\"",
            "Claptrap: \"... You're dead to me.\""
        ],
        [ "Wubwubwub. Dubstep dubstep. Wubwubwubwub DROP! Dubstep" ],
        [ "I'll die the way I lived: annoying!" ],
        [ "This could've gone better!" ],
        [ "What's that smell? Oh wait, it's just you!" ],
        [ "Yo momma's so dumb, she couldn't think of a good ending for this 'yo momma' joke!" ],
        [ "Oh yeah? Well, uh... yeah." ],
        [ "I'm too pretty to die!" ],
        [ "No, nononono NO!" ],
        [ "I will prove to you my robotic superiority!" ],
        [ "I am so impressed with myself!" ],
        [ "Argh arghargh death gurgle gurglegurgle urgh... death" ],
        [ "Don't bother with plastic surgery - there's NO fixing that!" ],
        [ "Uh... wasn't me!" ],
        [ "I am right behind you, Vault Hunting friend!" ],
        [ "So, uh... what OS does your drone use?" ],
        [ "I can do that to! ... Sorta... Except not!" ],
        [ "Bringing down the law, painfully!" ],
        [ "I did a challenge? I did a challenge!" ],
        [ "Everything's upside down!" ],
        [ "I'm Trap, Claptrap. Double oh... Trap." ],
        [ "Get ready for some Fragtrap face time!" ],
        [ "Coffee? Black... like my soul." ],
        [ "Crazy young whippersnappers..." ],
        [ "Guess who?" ],
        [ "Burn, baby, burn!" ],
        [ "Remember, use caution near an open flame" ],
        [ "Zippity doodah!" ],
        [ "Hyperiooooon Punch!" ],
        [ "High five!" ],
        [ "Can I shoot something now? Or climb some stairs? SOMETHING exciting?" ],
        [ " like these, I really start to question the meaning of my existence. Then I get distra-hey! What's this? This looks cool!" ],
        [ "It would really stink if I couldn't control what I was thinking. Like, who wants to know that I'm thinking about cheese and lint, right?" ],
        [ "How does math work? Does this skin make me look fat? If a giraffe and a car had a baby, would it be called a caraffe? Life's big questions, man." ],
        [ "Does this mean I can start dancing? Pleeeeeeaaaaase?" ],
        [ "It's really quiet... and lonely... (hums briefly) Also this 'stopped moving' thing makes me uncomfortable. It gives me time to stop and think... literally. I'VE STOPPED, AND I'M THINKING! IT HURTS ME!" ],
        [ "Oh. My. God. What if I'm like... a fish? And, if I'm not moving... I stop breathing? AND THEN I'LL DIE! HELP ME! HELP MEEEEE HEE HEE HEEE! HHHHHHHELP!" ],
        [ "So, this one time, I went to a party, and there was a beautiful subatomic particle accelerator there. Our circuits locked across the room and... I don't remember what happened next. I mean, I can't. We coulda gotten married and had gadgets together, but now, I'll never know." ],
        [ "Ahem, ahem. What's going on? Did I break something?" ]

    ]
    pass

  def haveSomeFun(self, bot, message):
    if message.isSystem():
      return
    
    cmd = message.cmd()

    if cmd and cmd == "!clap":
      if time.time() - self._last < 2:
        return

      quoteId = randint(0, len(self._quotes) - 1)
      quotes = self._quotes[quoteId]

      for quote in quotes:
        bot.addReply(message.channel, quote)

      self._last = time.time()

