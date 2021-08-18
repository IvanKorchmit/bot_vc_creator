
from funcs import append, load_ac, delete_empty, save_ac
from discord import *
from classes import CustomOptions, ActiveChannels
from discord.utils import get
import discord_slash as slash
import os
from discord_slash.utils.manage_commands import create_option
import joblib as j
FILENAME = "actives.pc"
OPTIONS = "opt.pc"
guilds = []
global bot
global sl

class VCC(Client):
    def __init__(self, *, loop = None, **options):
        self.active_channels : list[ActiveChannels]
        self.active_channels = []

        self.options : list[CustomOptions]
        self.options = []
        if os.path.isfile(FILENAME) and os.path.getsize(FILENAME) > 0:
            print("Importing active channels")
            load_ac(self)


        super().__init__(loop=loop, **options)

    async def on_ready(self):
        print("Connected as " + str(self.user))
        guilds = [i.id for i in self.guilds]
        await delete_empty(self.active_channels,self)
    
    async def on_voice_state_update(self, member : Member, before : VoiceState, after : VoiceState):
        chan : VoiceChannel
        chan = after.channel
        t_index = find_opt_matches(member.guild.id)[1]
        if chan != None:
            if chan.id == self.options[t_index].vc:
                await self.create_vc(member,t_index, after)
        await delete_empty(self.active_channels,self)
    async def create_vc(self, member : Member, t_index : int, after : VoiceState):
        g : Guild
        g = member.guild
        perms : Permissions
        perms = Permissions(permissions = 53478144, manage_permissions=True, manage_channels=True)
        cat = get(g.categories,id=self.options[t_index].category)
        nick = member.nick if member.nick != None else member.display_name
        new_vc = await g.create_voice_channel(f"{nick}'s channel",category=cat)
        await new_vc.set_permissions(target=member, manage_channels=True)
        append(self,g,new_vc)
        if after.channel != None:
            await member.move_to(new_vc)

bot = VCC()
sl = slash.SlashCommand(bot,sync_commands=True)

params = [create_option("channel_id", "Channel ID where users should join in order create a channel", 3,True),create_option("category_id","The category ID where Voice Channels will be created at.",3,True)]

@sl.slash(name="adjust", guild_ids=guilds, description="Set your bot to use specific channel and category", options=params)
async def settings(ctx : slash.SlashContext, channel_id : str, category_id : str):
    perms : Permissions
    perms = ctx.author.guild_permissions
    admin = bool(perms.administrator)
    # checking for administrator permission in order to proceed
    if admin and await check_input(ctx,category_id,channel_id):
        category_id = int(category_id)
        channel_id = int(channel_id)
        try:
            bot.get_channel(channel_id)
        except:
            await ctx.send("Invalid input, either this channel doesn't exist or it is not valid.")
            return
        has_matches, index = find_opt_matches(ctx.author.guild.id)
        if has_matches:
            bot.options[index].vc = channel_id
            bot.options[index].category = category_id
        else:
            bot.options.append(CustomOptions(ctx.guild.id,channel_id,category_id))
        cat = get(ctx.guild.categories,id=category_id)
        save_ac(bot)
        await ctx.send(f"Target voice channel is set to: **{get(ctx.guild.channels,id=channel_id)}** and channels will be created at **{cat.name}**")
    elif not admin:
        await ctx.send("Not enough permissions!")

async def check_input(ctx,category_id, channel_id):
    if not channel_id.isdigit():
        await ctx.send("Invalid input")
        return False
    if not category_id.isdigit():
        await ctx.send("Invalid input")
        return False
    try:
        get(ctx.guild.categories, id=category_id)
    except:
        await ctx.send("Invalid input, this category doesn't exist or it is not valid.")
        return False
    return True
def find_opt_matches(guild_id : int):
    index = 0       
    for i in bot.options:
        if i.guild == guild_id:
            return True, index
        index += 1
    return False, -1    



bot.run("TOKEN")