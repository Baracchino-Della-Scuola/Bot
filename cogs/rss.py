import discord, feedparser, json, random
from discord.ext import commands, tasks


class RssNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rss_url = "https://www.repubblica.it/rss/esteri/rss2.0.xml"
        self.corriere_url = "http://xml2.corriereobjects.it/rss/esteri.xml"
        ses = open("articles.json", "r")
        self.articles = json.loads(ses.read())
        ses.close()
        self.send_announcements.start()
        self.send_announcements_corriere.start()

    def cog_unload(self):

        self.send_announcements_corriere.cancel()
        self.send_announcements.cancel()

    @tasks.loop(minutes=1)
    async def send_announcements(self):

        fil = open("articles.json", "w")
        feed = feedparser.parse(self.rss_url)

        entry = feed.entries[0]

        if entry["title"] in self.articles:

            fil.write(json.dumps(self.articles))
            fil.close()
            return
        else:
            print("oof")

            emb = discord.Embed(
                title=feed.entries[0]["title"], url=feed.entries[0]["link"]
            )
            ch = self.bot.get_channel(946354506214539315)

            self.articles.append(entry["title"])

            fil.write(json.dumps(self.articles))
            print("closing...")
            fil.close()

            # print(json.dumps(feed.entries[0]))
            # print(entry["links"][1]["href"])
            emb.set_author(name=entry["author_detail"]["name"])
            emb.set_footer(text="Published at: " + entry["published"])
            emb.set_thumbnail(url=entry["links"][1]["href"])

            await ch.send(embed=emb)

    @tasks.loop(minutes=1)
    async def send_announcements_corriere(self):

        corriere = feedparser.parse(self.corriere_url)
        cor = corriere.entries[0]
        print("a")
        session = open("corriere.json ", "r")

        cor_articles = json.loads(session.read())
        session.close()
        print("corriere")
        print(cor.title in cor_articles)
        fil = open("corriere.json", "w")
        if cor.title in cor_articles:
            print("exists")
            fil.write(json.dumps(self.articles))
            fil.close()

        else:
            print("oof")

            cor_articles.append(cor.title)
            fil.write(json.dumps(cor_articles))
            fil.close()
            ch = self.bot.get_channel(946354506214539315)

            embed = discord.Embed(
                title=cor["title"], url=cor["link"], description=cor["summary"]
            )
            embed.set_thumbnail(url=cor["thumbimage"]["url"])
            embed.set_footer(text="Published at: " + cor["published"])
            embed.set_author(name=cor.author)

            await ch.send(embed=embed)


def setup(bot):
    bot.add_cog(RssNews(bot))
