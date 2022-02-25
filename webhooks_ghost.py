import os, dotenv, json
from flask import *
from discord_webhook import DiscordWebhook, DiscordEmbed

dotenv.load_dotenv(".env")

app = Flask("ghosthooks")


@app.route("/receive", methods=["GET", "POST"])
def receive_hook():

    data = json.loads(request.data)
    webhook = DiscordWebhook(url=os.environ["WEBHOOK"])

    embed = DiscordEmbed(
        title=f'New blog post: {data["post"]["current"]["title"]}',
        description=f'Go check it out at {data["post"]["current"]["url"]}!',
        color="03b2f8",
    )

    # add embed object to webhook
    webhook.add_embed(embed)
    webhook.execute()
    return "ok"


app.run(host="0.0.0.0", port=8756)
