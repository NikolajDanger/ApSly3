# Sly 3: Honor Among Thieves Archipelago
An archipelago implementation of Sly 3.

## What does randomization do in this game?
Each gadget, episode, and crew member (Bentley, Murray, Guru, Penelope, Panda King, Dimitri, and Carmelita).

You complete checks by completing jobs, master thief challenges, as well as purchasing items from ThiefNet.

**Additional features:**
- The ability to skip video cutscenes by pressing the X button.

## Setup

### Requirements
In order to play the Sly 3 Archipelago randomizer, you need:

- [Archipelago Multiworld Randomizer](https://github.com/ArchipelagoMW/Archipelago/releases).
- [The Sly 3 apworld](https://github.com/NikolajDanger/APSly3/releases).
- [PCSX2](https://pcsx2.net/downloads/). Must be v1.7 or higher.
- A Sly 3 US ISO (`SCUS-97464`).

### PCSX2 Settings
Enable PINE in PCSX2
- In PCSX2, under `Tools`, check `Show Advanced Settings`.
- In PCSX2, `System -> Settings -> Advanced -> PINE Settings`, check `Enable` and ensure `Slot` is set to `28011`.

### Generating and hosting a multiworld
Refer to [the official guide](https://archipelago.gg/tutorial/Archipelago/setup_en) on how to set up your game. Be aware that Sly 3 is not in core, so you cannot generate a game on the website.

### Playing a game
1. Start the game in PCSX2.
2. Start the Sly 3 client from the Archipelago launcher, and connect to the multiworld.
3. Ensure that the "Press START ..." message has changed to "Connected to Archipelago" before playing.
4. Start a new game.

## Skipping the intro
You can skip the intro with the `/menu` command in the client. This might disable saving, so refer to "There's no "save and quit" option in the pause menu" in the Troubleshooting section.

## Tracker
The randomizer has support for [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/blob/tracker/worlds/tracker/docs/setup.md).

## Troubleshooting
### The client won't connect to my PCSX2 instance
Before asking for help in the discord channel:
- Make sure you have PINE enabled. Also check that you've not turned it off in the game-specific settings.
- Make sure that you're playing the US version of the game (`SCUS-97464`).
- If you've enabled discord's rich presence for PCSX2, try disabling it.
- If you're using the flatpack version of PCSX2, try installing a different version.

If all these fail, please ask for help in the [discord channel](https://discord.com/channels/731205301247803413/1403124437464649868).

### There's no "save and quit" option in the pause menu
You can save the game manually in Options.

## Acknowledgment
This project was heavily inspired by and built upon the structure and PINE code from [Evilwb's Archipelago Ratchet and Clank 2 implementation](https://github.com/evilwb/APRac2).
