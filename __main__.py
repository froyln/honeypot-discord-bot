import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")


def load_data():
    if os.path.exists("honeypot.json"):
        with open("honeypot.json", "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open("honeypot.json", "w") as f:
        json.dump(data, f, indent=4)


honeypot_channels = load_data()
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


@bot.command()
@commands.has_permissions(administrator=True)
async def honeypot(ctx, channel: discord.TextChannel):
    """Configura un canal como honeypot"""
    guild_id = str(ctx.guild.id)
    honeypot_channels[guild_id] = channel.id
    save_data(honeypot_channels)

    warning_text = (
        "**NO ENVIAR MENSAJES**\n\n"
        "Cualquier mensaje enviado será considerado una violación a las reglas del servidor "
        "y obtendrás un baneo automático sin aviso, posteriormente también serás baneado automáticamente "
        "de distintos servidores.\n\n"
        "Este canal está destinado únicamente a fines de seguridad para proteger nuestro servidor "
        "de posibles actividades maliciosas, como el envío de mensajes no deseados (spam) o intentos de abuso."
    )

    warning = await channel.send(warning_text)
    await warning.pin()
    await ctx.send(f"Honeypot configurado en {channel.mention}")


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    guild_id = str(message.guild.id)

    if (
        guild_id in honeypot_channels
        and message.channel.id == honeypot_channels[guild_id]
    ):
        try:
            # Banear al usuario
            await message.author.ban(
                reason="Violación de zona restringida: Honeypot", delete_message_days=1
            )

            # Notificar en el canal
            notification = await message.channel.send(
                f"Usuario **{message.author}** baneado por violación de zona restringida",
                delete_after=10,
            )

            # Enviar DM al usuario
            try:
                await message.author.send(
                    f"Has sido baneado permanentemente de **{message.guild.name}** por enviar un mensaje "
                    "en un canal de seguridad restringido. Esta acción se realizó automáticamente como medida "
                    "contra actividades potencialmente maliciosas."
                )
            except:
                pass

        except discord.Forbidden:
            await message.channel.send(
                "Error: Permisos insuficientes para banear usuarios"
            )
        except Exception as e:
            await message.channel.send(f"Error en el sistema: {str(e)}")

    await bot.process_commands(message)


@bot.command()
@commands.has_permissions(administrator=True)
async def disable_honeypot(ctx):
    guild_id = str(ctx.guild.id)
    if guild_id in honeypot_channels:
        del honeypot_channels[guild_id]
        save_data(honeypot_channels)
        await ctx.send("Honeypot desactivado en este servidor")
    else:
        await ctx.send("No hay honeypot configurado en este servidor")


@bot.command()
@commands.has_permissions(administrator=True)
async def honeypot_help(ctx):
    await ctx.send(
        f"**Add honeypot channel**\n{PREFIX}honeypot #channel\n\n**Remove honeypot**\n{PREFIX}disable_honeypot"
    )


bot.run(BOT_TOKEN)
