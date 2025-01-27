#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2021 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
#
# This Borderlands 3 Hotfix Mod is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This Borderlands 3 Hotfix Mod is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this Borderlands 3 Hotfix Mod.  If not, see
# <https://www.gnu.org/licenses/>.

import sys
sys.path.append('../../../python_mod_helpers')
from bl3hotfixmod.bl3hotfixmod import Mod, BVC, BVCF

mod = Mod('dlc_loot_de-emphasizer.bl3hotfix',
        'DLC Loot De-Emphasizer',
        'Apocalyptech',
        [
            "So far, all story DLCs for BL3 have included specific legendary loot",
            "pools which world-drop pretty frequently throughout the DLC, so you get",
            "the same relatively-small set of drops often while playing.  This is",
            "great for the first playthrough or two, but after that, I'd typically",
            "prefer just getting the 'usual' world drops instead.  So, this mod aims",
            "to replace those specific drops with our ordinary legendary pool drops",
            "instead.",
            "",
            "This doesn't touch *specific* enemy drops, such as Gideon and The",
            "Procurer from DLC2, who drop from the same pool ordinarily used for DLC2",
            "legendary world drops.",
            "",
            "This is intended to be used alongside my Expanded Legendary Pools mod,",
            "so you've got interesting stuff dropping most of the time.",
        ],
        lic=Mod.CC_BY_SA_40,
        v='1.3.0',
        cats='loot-system, enemy-drops, chests',
        )

# Pools that we're redirecting stuff to
leg_pool_guns = Mod.get_full_cond('/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Legendary', 'ItemPoolData')
leg_pool_shields = Mod.get_full_cond('/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_05_Legendary', 'ItemPoolData')
leg_pool_coms = Mod.get_full_cond('/Game/Gear/ClassMods/_Design/ItemPools/ItemPool_ClassMods_05_Legendary', 'ItemPoolData')
leg_pool_artifacts = Mod.get_full_cond('/Game/Gear/Artifacts/_Design/ItemPools/ItemPool_Artifacts_05_Legendary', 'ItemPoolData')
leg_pool_grenades = Mod.get_full_cond('/Game/GameData/Loot/ItemPools/GrenadeMods/ItemPool_GrenadeMods_05_Legendary', 'ItemPoolData')

# Individual wepon type pools
leg_pool_ar = Mod.get_full_cond('/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Legendary', 'ItemPoolData')
leg_pool_hw = Mod.get_full_cond('/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Legendary', 'ItemPoolData')
leg_pool_ps = Mod.get_full_cond('/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Legendary', 'ItemPoolData')
leg_pool_sg = Mod.get_full_cond('/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Legendary', 'ItemPoolData')
leg_pool_sm = Mod.get_full_cond('/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Legendary', 'ItemPoolData')
leg_pool_sr = Mod.get_full_cond('/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SnipeRifles_Legendary', 'ItemPoolData')

# Support functions
def do_hotfix(char_name, object_name, attr_name, index, to_pool, is_map=False):
    global mod
    if is_map:
        hf_mode = Mod.LEVEL
    else:
        hf_mode = Mod.CHAR
    mod.reg_hotfix(hf_mode, char_name,
            object_name,
            attr_name.format(index),
            to_pool)

def do_itempoollist(char_name, list_name, index, to_pool, is_map=False):
    do_hotfix(char_name, list_name, 'ItemPools.ItemPools[{}].ItemPool', index, to_pool, is_map)

def do_itempool(char_name, pool_name, index, to_pool, is_map=False, clear=False):
    if clear:
        do_hotfix(char_name, pool_name, 'BalancedItems.BalancedItems[{}].InventoryBalanceData', index, 'None', is_map)
        do_hotfix(char_name, pool_name, 'BalancedItems.BalancedItems[{}].ResolvedInventoryBalanceData', index, 'None', is_map)
    do_hotfix(char_name, pool_name, 'BalancedItems.BalancedItems[{}].ItemPoolData', index, to_pool, is_map)

def legendary_guns_itempoollist(char_name, list_name, index, is_map=False):
    global leg_pool_guns
    do_itempoollist(char_name, list_name, index, leg_pool_guns, is_map)

def legendary_guns_itempool(char_name, pool_name, index, is_map=False):
    global leg_pool_guns
    do_itempool(char_name, pool_name, index, leg_pool_guns, is_map)

def legendary_shields_itempoollist(char_name, list_name, index, is_map=False):
    global leg_pool_shields
    do_itempoollist(char_name, list_name, index, leg_pool_shields, is_map)

def legendary_shields_itempool(char_name, pool_name, index, is_map=False):
    global leg_pool_shields
    do_itempool(char_name, pool_name, index, leg_pool_shields, is_map)

def legendary_coms_itempoollist(char_name, list_name, index, is_map=False):
    global leg_pool_coms
    do_itempoollist(char_name, list_name, index, leg_pool_coms, is_map)

def legendary_coms_itempool(char_name, pool_name, index, is_map=False):
    global leg_pool_coms
    do_itempool(char_name, pool_name, index, leg_pool_coms, is_map)

def zero_itempoollist(hf_mode, hf_target, poollist_name, index):
    global mod
    mod.reg_hotfix(hf_mode, hf_target,
            poollist_name,
            'ItemPools.ItemPools[{}].PoolProbability'.format(index),
            BVCF(bvc=0))

def zero_pool(hf_mode, hf_target, pool_name, index):
    global mod
    mod.reg_hotfix(hf_mode, hf_target,
            pool_name,
            'BalancedItems.BalancedItems[{}].Weight'.format(index),
            BVCF(bvc=0))

###
### DLC1 - Moxxi's Heist of the Handsome Jackpot
###

mod.header("DLC1 - Moxxi's Heist of the Handsome Jackpot")

# Main weapon pool
# The main guns pool actually already points to the global legendary pool, in addition to
# the custom one, so we're just zeroing out the probability of the DLC-specific one.
mod.comment('Main Weapon Pool')
for char_name in [
        # Via ItemPoolList_BadassEnemyGunsGearLoader1
        'BPChar_HyperionTurretBadass',
        'BPChar_LoaderBadass',
        # Via ItemPoolList_StandardEnemyGunsandGearLoader
        'BPChar_HyperionTurretBasic',
        'BPChar_LoaderShared',
        'BPChar_WeeLoaderBasic',
        'BPChar_DefenseCannonSuperBadass',
        'BPChar_DefenseCannonBasic',
        # Via ItemPoolList_BadassEnemyGunsGear_Dandelion
        'BPChar_SisterlyLove_DebtCollectorLoader',
        'BPChar_GreatEscape_Rudy',
        'BPChar_RagingBot_MachineGunMikey',
        'BPChar_EnforcerBadass_Looter',
        'BPChar_Enforcer_PrettyBoy',
        'BPChar_GoliathBadass_Looter',
        'BPChar_GoonBadass_Looter',
        'BPChar_PsychoBadass_Looter',
        'BPChar_PunkArmored_LooterVIP',
        'BPChar_PunkBadass_Looter',
        'BPChar_TinkBadass_Looter',
        'BPChar_TinkBadassArmored_Looter',
        'BPChar_ThePlan_TricksyNick',
        # Via ItemPoolList_Boss_Dandelion
        'BPChar_JackBot',
        # Via ItemPoolList_MiniBoss_Dandelion
        'BPChar_EnforcerBadass_Lawrence',
        'BPChar_GoonBadass_Coco',
        'BPChar_PunkBadass_Gaudy',
        'BPChar_TinkBadass_Giorgio',
        'BPChar_TraitorEddie',
        'BPChar_ClaptrapQueen',
        'BPChar_LoaderBadass_Venchy',
        # Via ItemPoolList_StandardEnemyGunsandGear_Dandelion
        'BPChar_AcidTrip_EarlyPrototype',
        'BPChar_EnforcerBruiser_Looter',
        'BPChar_GoliathBasic_Looter',
        'BPChar_GoliathMidget_Looter',
        'BPChar_GoonBasic_looter',
        'BPChar_GoonVortex_Looter',
        'BPChar_PsychoBasic_Looter',
        'BPChar_PsychoFirebrand_Looter',
        'BPChar_PsychoSlugger_Looter',
        'BPChar_PsychoSuicide_Looter',
        'BPChar_PunkAssaulter_Looter',
        'BPChar_PunkBasic_Looter',
        'BPChar_PunkShotgunner_Looter',
        'BPChar_PunkSniper_Looter',
        'BPChar_TinkBasic_Looter',
        'BPChar_TinkPsycho_Looter',
        'BPChar_TinkShotgun_Looter',
        'BPChar_TinkSuicide_Looter',
        'BPChar_CasinoBot_BigJanitor',
        ]:
    zero_pool(Mod.CHAR, char_name, '/Game/PatchDLC/Dandelion/GameData/Loot/ItemPool_Guns_All_Dandelion', 4)
mod.newline()

# Boss Weapon Pool
# Same story re: zeroing out
# ... though, in the end, this is really a dedicated drop type thing, so I'm leaving it.
#mod.comment('Boss Weapon Pool')
#for char_name in [
#        # Via ItemPoolList_Boss_Dandelion
#        'BPChar_JackBot',
#        ]:
#    zero_pool(Mod.CHAR, char_name, '/Game/PatchDLC/Dandelion/GameData/Loot/ItemPool_Guns_All_Dandelion_Boss', 4)
#mod.newline()

# COMs
# This also shows up in ItemPool_EquippablesNotGuns_Dandelion but I'm not sure
# what to make of that one
mod.comment('COM Pools')
for (pool_name, pool_idx, char_names) in [
        ('/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_BadassEnemyGunsGear_Dandelion', 5, [
                'BPChar_SisterlyLove_DebtCollectorLoader',
                'BPChar_GreatEscape_Rudy',
                'BPChar_RagingBot_MachineGunMikey',
                'BPChar_EnforcerBadass_Looter',
                'BPChar_Enforcer_PrettyBoy',
                'BPChar_GoliathBadass_Looter',
                'BPChar_GoonBadass_Looter',
                'BPChar_PsychoBadass_Looter',
                'BPChar_PunkArmored_LooterVIP',
                'BPChar_PunkBadass_Looter',
                'BPChar_TinkBadass_Looter',
                'BPChar_TinkBadassArmored_Looter',
                'BPChar_ThePlan_TricksyNick',
                ]),
        # The boss drop here really seems like it should stay; omitting this one.
        #('/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_Boss_Dandelion', 5, [
        #        'BPChar_JackBot',
        #        ]),
        ('/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_MiniBoss_Dandelion', 5, [
                'BPChar_EnforcerBadass_Lawrence',
                'BPChar_GoonBadass_Coco',
                'BPChar_PunkBadass_Gaudy',
                'BPChar_TinkBadass_Giorgio',
                'BPChar_TraitorEddie',
                'BPChar_ClaptrapQueen',
                'BPChar_LoaderBadass_Venchy',
                ]),
        ('/Game/PatchDLC/Dandelion/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Dandelion', 5, [
                'BPChar_AcidTrip_EarlyPrototype',
                'BPChar_EnforcerBruiser_Looter',
                'BPChar_GoliathBasic_Looter',
                'BPChar_GoliathMidget_Looter',
                'BPChar_GoonBasic_looter',
                'BPChar_GoonVortex_Looter',
                'BPChar_PsychoBasic_Looter',
                'BPChar_PsychoFirebrand_Looter',
                'BPChar_PsychoSlugger_Looter',
                'BPChar_PsychoSuicide_Looter',
                'BPChar_PunkAssaulter_Looter',
                'BPChar_PunkBasic_Looter',
                'BPChar_PunkShotgunner_Looter',
                'BPChar_PunkSniper_Looter',
                'BPChar_TinkBasic_Looter',
                'BPChar_TinkPsycho_Looter',
                'BPChar_TinkShotgun_Looter',
                'BPChar_TinkSuicide_Looter',
                'BPChar_CasinoBot_BigJanitor',
                ]),
        ]:
    for char_name in char_names:
        legendary_coms_itempoollist(char_name, pool_name, pool_idx)

mod.newline()

###
### DLC2 - Guns, Love, and Tentacles
### Grenade pool doesn't need to be touched because it's empty
###

mod.header('DLC2 - Guns, Love, and Tentacles')

# Main weapon pool
mod.comment('Main Weapon Pool')
for char_name in [
        # References via ItemPoolList_Boss_Hibiscus
        'BPChar_HeartBoss',
        'BPChar_LostTwo_BigBro',
        'BPChar_LostTwo_ToughBro',
        'BPChar_Vincent',
        # References via ItemPoolList_Eista
        'BPChar_Hib_EistaChild_Radiation',
        # References via ItemPoolList_MiniBoss_Hibiscus
        'BPChar_ZealotNightmareShocker_Rare',
        'BPChar_ZealotPilfer_Child_Rare',
        'BPChar_LunaticPossessed',
        # References via ItemPoolList_StandardEnemyGunsandGear_Hibiscus
        'BPChar_FlyingSlugBasic',
        'BPChar_LostOneBadass',
        'BPChar_LostOneFlailing',
        'BPChar_Lunatic',
        'BPChar_Minion',
        'BPChar_Slug',
        'BPChar_Wolven_Shared',
        'BPChar_Zealot',
        # References via SpawnOptions that reference ItemPoolList_StandardEnemyGunsandGear_Hibiscus
        'BPChar_FrostEnforcerBruiser',
        'BPChar_FrostEnforcerMelee',
        'BPChar_FrostPsychoFirebrand',
        'BPChar_FrostPsychoSlugger',
        'BPChar_FrostPsychoSuicide',
        'BPChar_FrostPunk_Assaulter',
        'BPChar_FrostPunk_Badass',
        'BPChar_FrostPunk_Basic',
        'BPChar_FrostPunk_Shotgunner',
        'BPChar_FrostPunk_Sniper',
        'BPChar_FrostTinkBadass',
        'BPChar_FrostTinkBasic',
        'BPChar_FrostTinkShotgun',
        'BPChar_Spinsmouth',
        # References via SpawnOptions_Hib_Badass_Empowered_Spirit_WithLoot
        'BPChar_Hib_Nekro_Spirit',
        # Direct references from char
        'BPChar_Hib_Mancubite',
        ]:
    legendary_guns_itempool(char_name,
            '/Game/PatchDLC/Hibiscus/GameData/Loot/ItemPool_Guns_All_Hibiscus', 4)
mod.newline()

# Loot Skritaari
mod.comment('Loot Skritaari Weapons')
legendary_guns_itempoollist('BPChar_MinionLoot',
        '/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_Hib_MinionLoot', 12)
mod.newline()

# Sniper/Heavy Pool
# I assume the level hotfixes here are good enough?
mod.comment('Sniper/Heavy Pool (for chests)')
for level_name in [
        'Archive_P',
        'Camp_P',
        'Lake_P',
        'Venue_P',
        'Village_P',
        'Woods_P',
        ]:
    zero_pool(Mod.LEVEL, level_name, '/Game/PatchDLC/Hibiscus/GameData/Loot/Legendary/ItemPool__Hib_Sniper_Heavy_Legendary', 2)
mod.newline()

# Shield Pool
mod.comment('Shield Pool')
for char_name in [
        # References via ItemPoolList_StandardEnemyGunsandGear_Hibiscus
        'BPChar_FlyingSlugBasic',
        'BPChar_LostOneBadass',
        'BPChar_LostOneFlailing',
        'BPChar_Lunatic',
        'BPChar_Minion',
        'BPChar_Slug',
        'BPChar_Wolven_Shared',
        'BPChar_Zealot',
        # References via SpawnOptions that reference ItemPoolList_StandardEnemyGunsandGear_Hibiscus
        'BPChar_FrostEnforcerBruiser',
        'BPChar_FrostEnforcerMelee',
        'BPChar_FrostPsychoFirebrand',
        'BPChar_FrostPsychoSlugger',
        'BPChar_FrostPsychoSuicide',
        'BPChar_FrostPunk_Assaulter',
        'BPChar_FrostPunk_Badass',
        'BPChar_FrostPunk_Basic',
        'BPChar_FrostPunk_Shotgunner',
        'BPChar_FrostPunk_Sniper',
        'BPChar_FrostTinkBadass',
        'BPChar_FrostTinkBasic',
        'BPChar_FrostTinkShotgun',
        'BPChar_Spinsmouth',
        # There's also ItemPool_EquippablesNotGuns_Hibiscus, but that sounds like equippables?
        ]:
    legendary_shields_itempool(char_name,
            '/Game/PatchDLC/Hibiscus/GameData/Loot/ItemPool_Shields_All_Hibiscus', 4)
mod.newline()

# COMs
# They're also mentioned in ItemPool_EquippablesNotGuns_Hibiscus but that sounds like equippables?
mod.comment('COM Pool - Badass Enemies')
for char_name in [
        # Direct char references
        'BPChar_Hib_Hunt_Hampton',
        'BPChar_SlugBadass_Kratch',
        'BPChar_Hib_Nekro_Spirit_Invisible',
        'BPChar_Hib_Nekro_SpiritBadass',
        'BPChar_Lost_Mush_Child',
        'BPChar_FlyingSlugBadass',
        'BPChar_Wolven_Badass',
        'BPChar_Zealot_Badass',
        'BPChar_Zealot_Badass_Procurer',
        ]:
    legendary_coms_itempoollist(char_name,
            '/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_BadassEnemyGunsGear_Hibiscus', 5)
mod.newline()
mod.comment('COM Pool - Standard Enemies')
for char_name in [
        # References via ItemPoolList_StandardEnemyGunsandGear_Hibiscus
        'BPChar_FlyingSlugBasic',
        'BPChar_LostOneBadass',
        'BPChar_LostOneFlailing',
        'BPChar_Lunatic',
        'BPChar_Minion',
        'BPChar_Slug',
        'BPChar_Wolven_Shared',
        'BPChar_Zealot',
        # References via SpawnOptions that reference ItemPoolList_StandardEnemyGunsandGear_Hibiscus
        'BPChar_FrostEnforcerBruiser',
        'BPChar_FrostEnforcerMelee',
        'BPChar_FrostPsychoFirebrand',
        'BPChar_FrostPsychoSlugger',
        'BPChar_FrostPsychoSuicide',
        'BPChar_FrostPunk_Assaulter',
        'BPChar_FrostPunk_Badass',
        'BPChar_FrostPunk_Basic',
        'BPChar_FrostPunk_Shotgunner',
        'BPChar_FrostPunk_Sniper',
        'BPChar_FrostTinkBadass',
        'BPChar_FrostTinkBasic',
        'BPChar_FrostTinkShotgun',
        'BPChar_Spinsmouth',
        ]:
    legendary_coms_itempoollist(char_name,
            '/Game/PatchDLC/Hibiscus/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Hibiscus', 5)
mod.newline()

###
### DLC3 - Bounty of Blood
### Getting lazy here and just using MatchAll...
###

mod.header('DLC3 - Bounty of Blood')

# Main weapon pool
# No need to do main shield pool 'cause it's empty
mod.comment('Main Weapon Pool')
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Geranium/GameData/Loot/ItemPool_Guns_All_Geranium', 4)
mod.newline()

# Individual weapon pools -- DLC3 seems to have duplicated each weapon type legendary
# pool; going to just redirect all of those to our default ones.
mod.comment('Individual Weapon Pools')
for src, dst in [
        ('/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_AssaultRifles_Legendary', leg_pool_ar),
        ('/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_Heavy_Legendary', leg_pool_hw),
        ('/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_Pistols_Legendary', leg_pool_ps),
        ('/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_Shotguns_Legendary', leg_pool_sg),
        ('/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_SMGs_Legendary', leg_pool_sm),
        ('/Game/PatchDLC/Geranium/GameData/Loot/Guns/ItemPool_GER_SnipeRifles_Legendary', leg_pool_sr),
        ]:
    mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
            src,
            'BalancedItems',
            '((ItemPoolData={}))'.format(dst))
mod.newline()

###
### DLC4 - Psycho Krieg
### Continuing to be lazy here and just using MatchAll...
###

mod.header('DLC4 - Psycho Krieg and the Fantastic Fustercluck')

# Main weapon pool.  This is used by standard enemies, badasses, and bosses
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Alisma/GameData/Loot/ItemPool_Guns_All_Alisma', 4)

# Extra badass purple drops
zero_itempoollist(Mod.CHAR, 'MatchAll',
        '/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_BadassEnemyGunsGear_Alisma', 10)

# Main shield pool.  Only used by badasses, it seems
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Alisma/GameData/Loot/ItemPool_Shields_All_Alisma', 4)

# Fix standard enemy shield drop (ordinarily is hardcoded to have a 1% chance of DLC
# legendary shields, and nothing else).
mod.reg_hotfix(Mod.CHAR, 'MatchAll',
        '/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Alisma',
        'ItemPools.ItemPools[5]',
        """(
            ItemPool={},
            PoolProbability={},
            NumberOfTimesToSelectFromThisPool={}
        )""".format(
            Mod.get_full_cond('/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_All', 'ItemPoolData'),
            BVCF(bva='/Game/GameData/Loot/ItemPools/Attributes/Att_Shields_DropOddsWithMayhem_Total'),
            BVCF(bvc=1),
            ))

# Main COM pool.  Used by standard enemies, badasses, and bosses
legendary_coms_itempool('MatchAll', '/Game/PatchDLC/Alisma/GameData/Loot/ItemPool_ClassMods_All_Alisma', 4)

# Boss Shields
legendary_shields_itempoollist('MatchAll', '/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma', 7)

# Boss Guns
legendary_guns_itempoollist('MatchAll', '/Game/PatchDLC/Alisma/GameData/Loot/EnemyPools/ItemPoolList_Boss_Alisma', 8)

mod.newline()

###
### DLC5 - Designer's Cut
### Note that these are level-based, since the objects are tied to containers rather than characters
###

mod.header('DLC5 - Designer\'s Cut')

dlc5map = 'FrostSite_P'
for src, idx, dst in [
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_CreatureSewers_Legendary', 0, leg_pool_ar),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_CreatureSewers_Legendary', 1, leg_pool_sg),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Dam_Legendary', 0, leg_pool_sr),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Dam_Legendary', 1, leg_pool_sr),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Dam_Legendary', 2, leg_pool_coms),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_HQ_Legendary', 0, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_HQ_Legendary', 1, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_HQ_Legendary', 2, leg_pool_coms),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Industry_Legendary', 0, leg_pool_sm),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Industry_Legendary', 1, leg_pool_sm),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Industry_Legendary', 2, leg_pool_coms),
        # This last COM in ItemPool_GearUp_Event_Industry_Legendary just here to support the Provocateur COM mod, should
        # it be enabled.  Will do nothing if not.
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Industry_Legendary', 3, leg_pool_coms),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Silo_Legendary', 0, leg_pool_grenades),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Silo_Legendary', 1, leg_pool_shields),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Spaceport_Legendary', 0, leg_pool_artifacts),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Spaceport_Legendary', 1, leg_pool_artifacts),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Spaceport_Legendary', 2, leg_pool_coms),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Thunderdome_Legendary', 0, leg_pool_shields),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_Thunderdome_Legendary', 1, leg_pool_shields),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_WaterWorks_Legendary', 0, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/Event/ItemPool_GearUp_Event_WaterWorks_Legendary', 1, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/ItemPool_GearUp_Chest_AR_SG_SMG_Unequippable', 0, leg_pool_sg),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/ItemPool_GearUp_Chest_AR_SG_SMG_Unequippable', 1, leg_pool_ar),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/ItemPool_GearUp_Chest_AR_SG_SMG_Unequippable', 2, leg_pool_sm),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/ItemPool_GearUp_Chest_PS_Unequippable', 0, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/ItemPool_GearUp_Chest_PS_Unequippable', 1, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/ItemPool_GearUp_Chest_SR_HW_Unequippable', 0, leg_pool_sr),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/Chest/ItemPool_GearUp_Chest_SR_HW_Unequippable', 1, leg_pool_sr),
        # This one especially is a bit silly, should probably just redefine the whole pool like we do for
        # ItemPool_Ixora_Guns_Legendary below...
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 0, leg_pool_sr),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 1, leg_pool_sr),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 2, leg_pool_sg),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 3, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 4, leg_pool_ar),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 5, leg_pool_sm),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 6, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 7, leg_pool_artifacts),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 8, leg_pool_grenades),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 9, leg_pool_shields),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 10, leg_pool_shields),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 11, leg_pool_shields),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 12, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 13, leg_pool_sm),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 14, leg_pool_artifacts),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 15, leg_pool_ps),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 16, leg_pool_coms),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 17, leg_pool_coms),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 18, leg_pool_coms),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 19, leg_pool_coms),
        # This last COM in ItemPool_Ixora_All_Legendary just here to support the Provocateur COM mod, should
        # it be enabled.  Will do nothing if not.
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_All_Legendary', 20, leg_pool_coms),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_Artifacts_Legendary', 0, leg_pool_artifacts),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_Artifacts_Legendary', 1, leg_pool_artifacts),
        # Nothing actually references this one, and it's not present in the level.
        #('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_ClassMods_Legendary', 0, leg_pool_coms),
        #('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_ClassMods_Legendary', 1, leg_pool_coms),
        #('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_ClassMods_Legendary', 2, leg_pool_coms),
        #('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_ClassMods_Legendary', 3, leg_pool_coms),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_Grenades_Legendary', 0, leg_pool_grenades),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_Shields_Legendary', 0, leg_pool_shields),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_Shields_Legendary', 1, leg_pool_shields),
        ('/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_Shields_Legendary', 2, leg_pool_shields),
        ]:
    do_itempool(dlc5map, src, idx, dst, is_map=True, clear=True)

# This object exists at the beginning of the level, but must (apparently) get loaded somehow after
# the level-based hotfixes; seems it must tied to a BPChar which technically gets loaded after,
# despite the fact that this is only used in Air Drop containers.  Whatever, the MatchAll char-based
# hotfix works fine.
mod.reg_hotfix(Mod.CHAR, 'MatchAll',
        '/Game/PatchDLC/Ixora/GameData/Loot/ItemPools/ItemPool_Ixora_Guns_Legendary',
        'BalancedItems',
        """(
            (
                ItemPoolData={},
                Weight={}
            )
        )""".format(
            leg_pool_guns,
            BVC(bvc=1),
            ))

mod.newline()

###
### DLC6 - Director's Cut
### Continuing to be lazy here and just using MatchAll...
###

mod.header("DLC6 - Director's Cut")

# Artifacts
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_Artifacts_All_Ixora2', 5)

# COMs (removes purple-tree COMs entirely; use World Drop Designer's Cut COMs to put 'em into world drop pools)
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_ClassMods_All_Ixora2', 1)
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_ClassMods_All_Ixora2', 3)
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_ClassMods_All_Ixora2', 5)
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_ClassMods_All_Ixora2', 7)
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_ClassMods_All_Ixora2', 9)

# Grenades
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_GrenadeMods_All_Ixora2', 4)

# Guns
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_Guns_All_Ixora2', 5)
# Nothing seems to actually reference this one, don't bother.
#zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_SniperAndHeavy_All_Ixora2', 5)

# Shields
zero_pool(Mod.CHAR, 'MatchAll', '/Game/PatchDLC/Ixora2/GameData/Loot/ItemPool_Shields_All_Ixora2', 5)

# Finish
mod.close()
