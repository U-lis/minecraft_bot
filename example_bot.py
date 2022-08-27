import json
import os.path
from json import JSONDecodeError
from pathlib import Path

import discord
from discord.ext import commands

from settings import DISCORD_BOT_TOKEN, SERVER_DATA_FILE

intents = discord.Intents.default()
intents.message_content = True

# bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)


def touch_server_file():
    if not os.path.exists(SERVER_DATA_FILE):
        with open(SERVER_DATA_FILE, "w") as f:
            f.write(json.dumps([]))


def load_server_data():
    with open(SERVER_DATA_FILE, "r") as f:
        data = json.loads(f.read())
    return data


def save_server_data(data):
    with open(SERVER_DATA_FILE, "w") as f:
        f.write(json.dumps(data))


@bot.event
async def on_ready():
    touch_server_file()
    print(f'We have logged in as {bot.user}')


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command(name="add_server")
async def add_server(ctx, *, name: str, ip: str, port: int, seed: str):
    data = load_server_data()
    data.append({"ip": ip, "port": port, "name": name, "seed": seed})
    save_server_data(data)
    await ctx.send(f"Server {name} added")


@bot.command(name="server_list")
async def get_server_list(ctx):
    data = load_server_data()

    if not data:
        await ctx.send("No servers found. Use `!add_server` command to add new server")
    else:
        server_name_list = [f"{x['name']}: {x['ip']}:{x['port']}" for x in data]
        await ctx.send(
            "\n".join(
                [
                    f"Found {len(server_name_list)} Server(s):",
                    *server_name_list
                ]
            )
        )


if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
