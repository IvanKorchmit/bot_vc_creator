import os
from discord import VoiceChannel, Guild
from discord.ext.commands import bot
import joblib as j
from classes import ActiveChannels
FILENAME = "actives.pc"
OPTIONS = "opt.pc"
def save_ac(bot):
    with open(FILENAME, "wb"):
        j.dump(bot.active_channels, FILENAME)
    with open(OPTIONS, "wb"):
        j.dump(bot.options, OPTIONS)

async def delete_empty(actives : list["ActiveChannels"], bot):
    print("Trying to delete empty channels")
    i : ActiveChannels
    for i in actives:
        for j in i.active_channels:
            chan : VoiceChannel
            chan = bot.get_channel(j)
            if chan != None:
                print(chan.voice_states)
                if not chan.voice_states:
                    remove(bot, bot.get_guild(i.guild), chan)
                    if chan != None:
                        try:
                            await chan.delete()
                        except:
                            print("Could not delete channel. Probably it was removed by user")

def remove(self, guild : Guild, vc : VoiceChannel):
    copy_ac = self.active_channels.copy()
    ind = 0
    for i in copy_ac:
        if i.guild == guild.id:
            anymatches = False
            j : VoiceChannel
            for j in self.active_channels[ind].active_channels:
                if vc.id == j:
                    anymatches = True
                    break
            if anymatches:
                self.active_channels[ind].active_channels.remove(vc.id)
                save_ac(self)
                return
            else:
                return
        ind += 1
def load_ac(bot):

    bot.active_channels = j.load(open(FILENAME, "rb", -1))
    if os.path.isfile(OPTIONS):
        bot.options = j.load(open(OPTIONS,"rb",-1))
    else:
        with open(OPTIONS,"wb") as _file:
            j.dump(" ", _file)

def append(self, guild : Guild, vc : VoiceChannel):
    clone_ac = self.active_channels.copy()
    index = 0
    i : "ActiveChannels"
    for i in clone_ac:

        if i.guild == guild.id:
            anymatches = False
            j : int
            for j in i.active_channels:
                if vc.id == j:
                    anymatches = True
                    break
            if not anymatches:
                self.active_channels[index].active_channels.append(vc.id)
                save_ac(self)    
                return
            else:
                return
        index += 1
    newAC = ActiveChannels(guild.id)
    newAC.active_channels.append(vc.id)
    self.active_channels.append(newAC)
    save_ac(self)