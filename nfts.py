import requests, time, sys

webhook_url = "https://discord.com/api/webhooks/944193369444335636/5aHibosUOR_ZyD845oIga4wi21SCvBumUtPIrDvV1IhpMqA3vadyQgKZYi0WMZO0XGAV"
sleep_time = .25


offset = 0

while True:
    print("NFT")
    url = f"https://api.opensea.io/api/v1/assets?order_direction=desc&offset={offset}&limit=1"
    response = requests.request("GET", url)
    
    responselist = response.text.split(",")
    print(responselist)
    for item in responselist:
        if '"image_url"' in item and "null" not in item:
            item = item.split('":"')
            if len(item[1]) > 5:
                url = item[1][:-1]
                urlparts = url.split("/")
                name = urlparts[-1]
                
                image = requests.get(url)
                print(webhook_url)
                if webhook_url:
                    r = requests.post(webhook_url, files={"file": ('nft.png', image.content)})
                    print(r.text)

                else:
                    if "." not in name:
                        with open(name + ".png", "wb") as myfile:
                            myfile.write(image.content)
                    else:
                        with open(name, "wb") as myfile:
                            myfile.write(image.content)
            break
    offset += 1
    time.sleep(sleep_time)