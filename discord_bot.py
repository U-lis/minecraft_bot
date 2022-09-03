import json
import os.path

import discord
from discord.ext import commands

from settings import DISCORD_BOT_TOKEN, SERVER_DATA_FILE

intents = discord.Intents.default()
intents.message_content = True

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


@bot.command(name="server_info")
async def server_info(ctx, *, server_name: str):
    data = load_server_data()
    target_server = None

    for d in data:
        if d["name"] == server_name:
            target_server = d
            break

    if not target_server:
        msg = f"Cannot find server named {server_name}. \nCheck server name using command `!server_list`"
    else:
        try:
            msg_list = [
                "```",
                "=== Server Info ===",
                f"Name        : {target_server['name']}",
                f"Access Info : {target_server['ip']}:{target_server['port']}",
                f"Seed        : {target_server['seed']}",
                "```",
            ]
            msg = "\n".join(msg_list)
        except:
            msg = "\n".join(
                [
                    f"An error occurred. Please contact to admin.(@ulismoon)",
                    "```",
                    "cmd         : server_info",
                    f"server_name : {server_name}"
                    "```",
                ]
            )

    await ctx.send(msg)


@bot.command(name="cmd")
async def help_function(ctx):
    print_list = [
        "Hello, I'm a minecraft discord bot.",
        "I can do following things:\n",
        "```",
        "Usage: ![command]\n",
        "command: ",
        "  ping                                 : Returns \"pong\" to check discord bot is working",
        "  server_list                          : Returns all saved server list",
        "  add_server [IP] [PORT] [NAME] [SEED] : Add new server to discord bot",
        "    [IP]   : IP address of minecraft server. ",
        "             This can be either public or private IP.",
        "    [PORT] : Port number of minecraft server. ",
        "             `[IP]:[PORT]` is used to connect to server.",
        "    [NAME] : Name of this minecraft server. ",
        "             You can identify server by this name.",
        "    [SEED] : The seed of minecraft server. ",
        "             This is important information to use various tools.",
        "  server_info [SERVER_NAME]            : Returns server information.",
        "    [SERVER_NAME] : Server name used when add server.",
        "                    You can get server name using `!server_list command.`",
        "```",
    ]
    await ctx.send("\n".join(print_list))


if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
