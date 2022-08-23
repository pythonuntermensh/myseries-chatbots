from vkbottle.bot import Bot
from vkbottle.tools import PhotoMessageUploader
from random import randint
from PIL import Image
import asyncio, requests, json, os

from data.config import SERIES_IP, NEW_SERIES_IP

async def check_new_series(sleep_for:int, bot:Bot):
    while 1:
        await asyncio.sleep(sleep_for)

        new_series_response = requests.get("http://" + NEW_SERIES_IP + "/rest/newSeries?vk=true")
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

        res = requests.get("http://" + SERIES_IP + "/rest/getSubscribersNewSeries?vk=true")
        subs = json.loads(res.text)     
        res = requests.get("http://" + NEW_SERIES_IP + "/rest/novelties?vk=true")
        novelties = json.loads(res.text)

        novelties_posters = dict()
        for novelty in novelties:
            photo = requests.get(novelty["pictureUrl"])
            photo_path = "temp-novelty/" + novelty["name"] + ".jpg"
            with open(photo_path, "wb") as out_file:
                out_file.write(photo.content)
                url = await PhotoMessageUploader(bot.api).upload(photo_path)
                os.remove(photo_path)
                novelties_posters[novelty["name"]] = url

        for sub in subs:
            for novelty in novelties:
                url = await bot.api.utils.get_short_link(novelty["url"])
                try:
                    await bot.api.messages.send(user_id=int(sub), message="Вышел новый сериал! - «" + novelty["name"] + "»" + "\n\n➤Смотреть: "\
                        + url.short_url, random_id=randint(0, 9999999), attachment=novelties_posters[novelty["name"]])
                except:
                    pass

        requests.get("http://" + NEW_SERIES_IP + "/rest/removeNovelties?vk=true")

        series_response = requests.get("http://" + SERIES_IP + "/rest/getSeries?names=" + ";".join(names))
        series_json = json.loads(series_response.text)

        series_posters = dict()
        for series in new_series_json:
            try:
                if ".webp" in series["pictureUrl"]:
                    photo = requests.get(series["pictureUrl"])
                    photo_path = "temp-new-series/" + series["name"] + ".webp"
                    with open(photo_path, "wb") as out_file:
                        out_file.write(photo.content)
                    photo_path_jpg = photo_path.replace(".webp", ".jpg")
                    img = Image.open(photo_path).convert("RGB")
                    img.save(photo_path_jpg, "jpeg")
                    series_posters[series["name"]] = ""
                    try:
                        url = await PhotoMessageUploader(bot.api).upload(photo_path_jpg)
                        series_posters[series["name"]] = url
                    except:
                        pass
                    os.remove(photo_path)
                    os.remove(photo_path_jpg)
                else:
                    photo = requests.get(series["pictureUrl"])
                    photo_path = "temp-new-series/" + series["name"] + ".jpg"
                    with open(photo_path, "wb") as out_file:
                        out_file.write(photo.content)
                        series_posters[series["name"]] = ""
                        try:
                            url = await PhotoMessageUploader(bot.api).upload(photo_path)
                            series_posters[series["name"]] = url
                        except:
                            pass
                        os.remove(photo_path)
            except:
                print("Error with ", series)

        for i in new_series_json:
            for x in series_json:
                if x["name"] == i["name"]:
                    if "vksubscribers" in x:
                        for id in x["vksubscribers"]:
                            url = await bot.api.utils.get_short_link(i["link"])
                            try:
                                await bot.api.messages.send(user_id=int(id), message="«" + i["name"] + "»" + "\n\n" + i["description"] + "\n" \
                                    + "Озвучки: " + ", ".join(i["translation"]) + "\n\nСмотреть: " + url.short_url,\
                                    random_id=randint(0, 9999999), attachment=series_posters[i["name"]])
                            except:
                                pass

        requests.get("http://" + NEW_SERIES_IP + "/rest/remove?vk=true")



