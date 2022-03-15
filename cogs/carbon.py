import discord
from discord.ext import commands
import urllib.parse
from .constants import themes, controls, languages, fonts, escales
import os
from pathlib import Path
from typing import Any

# from pyppeteer import launch
from io import *
import requests


def encode_url(text: str) -> str:
    first_encoding = urllib.parse.quote(text, safe="*()")
    return urllib.parse.quote(first_encoding, safe="*")  # Carbonsh encodes text twice


def hex_to_rgb(hex: str) -> tuple:
    """
    Args:
        hex (str):
    """
    return tuple(int(hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))


def parse_bg(background) -> str:
    if background == "":
        return "rgba(171, 184, 195, 1)"
    elif background[0] == "#" or "(" not in background:
        return f"rgba{hex_to_rgb(background) + (1,)}"
    return background


def int_to_px(number) -> str:
    return f"{number}px"


def int_to_percent(number) -> str:
    return f"{number}%"


def trim_url(text: str) -> str:
    if len(text) < 2000:
        return text

    if "%25" not in text:
        return text[:2000]

    if text[:2003][:-3] == "%25":
        return text[:2000]

    last_percent = text[:2000].rindex("%25")
    return text[:last_percent]


_carbon_url = "https://carbonnowsh.herokuapp.com/"


def code_to_url(code: str) -> str:
    return f"{_carbon_url}?&code={trim_url(encode_url(code))}"


class Carbon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def carbonate(self, ctx, *, code):

        carbon_url = code_to_url(code)
        r = requests.get(carbon_url)

        b = BytesIO(r.content)
        await ctx.send(file=discord.File(fp=b, filename="code.png"))


def setup(bot):
    bot.add_cog(Carbon(bot))
