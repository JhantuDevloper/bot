import os
import discord
from discord.ext import commands

# Bot ke intents setup karna
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_code="!", intents=intents)

# Target channel ka naam jahan registration hoga
TARGET_CHANNEL_NAME = "trial-checkin"

@bot.event
async def on_ready():
    print(f'Bot connect ho gaya hai: {bot.user.name}')

@bot.event
async def on_message(message):
    # Agar message bot khud bhej raha hai, to kuch nahi karna
    if message.author == bot.user:
        return

    # Check karna ki message 'trial-checkin' channel mein aaya hai ya nahi
    if message.channel.name == TARGET_CHANNEL_NAME:
        content = message.content.lower()
        
        # Check karna ki saare zaroori keywords message mein hain ya nahi
        has_ign = "in game name" in content or "ign:" in content
        has_id = "game id" in content or "id:" in content
        has_insta = "instagram id" in content or "insta" in content

        # Agar format sahi hai, to message ko delete nahi karna hai
        if has_ign and has_id and has_insta:
            return  # Sahi format hai, kuch mat karo
        
        else:
            # Galat format hone par user ka message delete karna
            try:
                await message.delete()
            except discord.Forbidden:
                print("Bot ke paas message delete karne ki permission nahi hai.")
                return

            # User ko sahi format batane ke liye message bhejna (Ye delete nahi hoga)
            format_msg = (
                f"Hey {message.author.mention}, aapne galat format use kiya hai! "
                f"Kripya niche diye gaye format mein hi detail bhejin, warna aapka message delete ho jayega.\n\n"
                f"**Sahi Format:**\n"
                f"In Game Name (IGN):\n"
                f"Game ID:\n"
                f"Instagram ID Link:"
            )
            await message.channel.send(format_msg)

    await bot.process_commands(message)

# Bot ko run karne ke liye (Token environment variable se aayega)
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: DISCORD_TOKEN nahi mila!")