from aiogram.bot.bot import Bot
from PIL import Image
import asyncio, aiogram, requests, json, os

from data.config import SERIES_IP, NEW_SERIES_IP

async def check_new_series(sleep_for:int, bot:Bot):
    while 1:
        await asyncio.sleep(sleep_for)

        new_series_response = requests.get("http://" + NEW_SERIES_IP + "/rest/newSeries?vk=false")
        new_series_json = json.loads(new_series_response.text)
        
        names = dict()
        for i in new_series_json:
            names[i["name"]] = i["additional"]

        series_response = requests.get("http://" + SERIES_IP + "/rest/getSeries?names=" + ";".join(names.keys()))
        series_json = json.loads(series_response.text)

        found_names = dict()
        for i in series_json:
            if not i == None:
                found_names[i["name"]] = i["additional"]
        
        difference = set(names.items()) - set(found_names.items())
        if len(difference) > 0:
            for i in difference:
                requests.get("http://" + SERIES_IP + "/rest/addNewSeries?name=" + i[0].strip() + "&additional=" + i[1].strip())

        res = requests.get("http://" + SERIES_IP + "/rest/getSubscribersNewSeries?vk=false")
        subs = json.loads(res.text)     
        res = requests.get("http://" + NEW_SERIES_IP + "/rest/novelties?vk=false")
        novelties = json.loads(res.text)
        for sub in subs:
            for novelty in novelties:
                try:
                    await bot.send_photo(int(sub), \
                        photo=novelty["pictureUrl"],\
                        caption=("Вышел новый сериал! - «" + novelty["name"] + "»" + "\n\n➤Смотреть: " + novelty["url"]))
                except:
                    pass

        requests.get("http://" + NEW_SERIES_IP + "/rest/removeNovelties?vk=false")

        series_response = requests.get("http://" + SERIES_IP + "/rest/getSeries?names=" + ";".join(names))
        series_json = json.loads(series_response.text)

        series_posters = dict()
        for series in new_series_json:
            if ".webp" in series["pictureUrl"]:
                photo = requests.get(series["pictureUrl"])
                photo_path = "temp-new-series/" + series["name"] + ".webp"
                with open(photo_path, "wb") as out_file:
                    out_file.write(photo.content)
                photo_path_jpg = photo_path.replace(".webp", ".jpg")
                img = Image.open(photo_path).convert("RGB")
                img.save(photo_path_jpg, "jpeg")
                series_posters[series["name"]] = photo_path_jpg
            else:
                series_posters[series["name"]] = series["pictureUrl"]

        for i in new_series_json:
            for x in series_json:
                if x["name"] == i["name"]:
                    if "tgsubscribers" in x:
                        for id in x["tgsubscribers"]:
                            if "http://" in series_posters[i["name"]]:
                                photo = series_posters[i["name"]]
                            else:
                                photo = open(series_posters[i["name"]], "rb")
                            try:
                                await bot.send_photo(int(id), photo=photo,
                                caption=("«" + i["name"] + "»" + "\n\n" + i["description"] + "\n" \
                                    + "Озвучки: " + ", ".join(i["translation"]) + "\n\n➤Смотреть: " + i["link"]))
                            except:
                                pass

        for path in os.listdir("temp-new-series"):
            os.remove("temp-new-series/" + path)

        requests.get("http://" + NEW_SERIES_IP + "/rest/remove?vk=false")



