from discord_webhook import DiscordWebhook
from FLog.LOGGER import Log
import time

Log = Log("Clients.Social.Discord.TiffanySays")
n = "\n"
channels = {
        "process_alerts": "https://discord.com/api/webhooks/968249751403384843/0Fqt4BUGtGBdAqgnCHD5RmVQzrXyV-fGy-6N3gdHUyS-kptuikFzGqDVDm63508D1Ng8",
        "tiffany_says": 'https://discord.com/api/webhooks/932535997172953149/CBjFq5R1g6hWqviA6-33XaK28QwUfIfUGIF5uTKZaJzMSu423BOisYSlyLLVH-YdyVGZ',
        "news_metaverse": 'https://discord.com/api/webhooks/933106712523702343/ZfR60S1X9ZeytpEmaOB78PpB1tJoj6ZErl1mL190fcMT6PXsU7T8lNR831hxUZhbJWEX',
        "news_crypto": "https://discord.com/api/webhooks/933127110384566382/SfAi947-8yq8Mjmt_7lO0BSMsvkKpGl_0lb_x-AIf_eoELhCOPdDd5ankPE1PcfIqrYK"
    }

def getChannelUrl(channalName):
    return channels[channalName]

def send_process_alert(alert):
    execute_send_message(getChannelUrl("process_alerts"), alert)

def execute_send_message(channel, message):
    webhook = DiscordWebhook(url=channel, content=message)
    response = webhook.execute()
    print(f"tiffany-says: [ {channel} ] -> [ {message} ] response= [ {response} ]")

send_process_alert("Testing first alert!")


class Say:
    channels = {
        "process_alerts": "https://discord.com/api/webhooks/968249751403384843/0Fqt4BUGtGBdAqgnCHD5RmVQzrXyV-fGy-6N3gdHUyS-kptuikFzGqDVDm63508D1Ng8",
        "tiffany_says": 'https://discord.com/api/webhooks/932535997172953149/CBjFq5R1g6hWqviA6-33XaK28QwUfIfUGIF5uTKZaJzMSu423BOisYSlyLLVH-YdyVGZ',
        "news_metaverse": 'https://discord.com/api/webhooks/933106712523702343/ZfR60S1X9ZeytpEmaOB78PpB1tJoj6ZErl1mL190fcMT6PXsU7T8lNR831hxUZhbJWEX',
        "news_crypto": "https://discord.com/api/webhooks/933127110384566382/SfAi947-8yq8Mjmt_7lO0BSMsvkKpGl_0lb_x-AIf_eoELhCOPdDd5ankPE1PcfIqrYK"
    }

    def say(self, articles):
        self.send_article("tiffany_says", articles)

    def news_metaverse(self, articles):
        self.send_article("news_metaverse", articles)

    def news_crypto(self, articles):
        self.send_article("news_crypto", articles)

    def process_alert(self, alert):
        self.send_article("process_alerts", alert)

    def send_article(self, channel, articles):
        if type(articles) in [list]:
            temp = Say.prepare_list_of_hookups(articles)
            for message in temp:
                self.execute_message(self.channels[str(channel)], message)
                time.sleep(5)
        else:
            message = self.prepare_article(articles)
            self.execute_message(self.channels[str(channel)], message)

    @staticmethod
    def execute_message(channel, message):
        webhook = DiscordWebhook(url=channel, content=message)
        response = webhook.execute()
        Log.i(f"tiffany-says: [ {channel} ] -> [ {message} ]", d=response)

    @staticmethod
    def prepare_list_of_hookups(list_of_hookups):
        temp = []
        for item in list_of_hookups:
            newItem = Say.prepare_article(item)
            temp.append(newItem)
        return temp

    @staticmethod
    def prepare_article(hookup):
        rank = str(hookup.get("rank"))
        score = str(hookup.get("score"))
        category = str(hookup.get("category"))
        date = str(hookup.get("published_date"))
        title = hookup.get("title")
        tickers = hookup.get("tickers")
        url = hookup.get("url")
        return f" {n} -------------------------------------------------------- {n}" \
               f"Rank: {rank} {n} " \
               f"Score: {score} {n} " \
               f"Topic: {category} {n} " \
               f"Date: {date} {n} " \
               f"Tickers: {tickers} {n} " \
               f"{title} {n} " \
               f"{url} {n} "


# if __name__ == '__main__':
    # from Mongodb.MongoHookup import MongoHookup
    # hookups = MongoHookup().find_last_amount(2)
    # l = Say.prepare_list_of_hookups(hookups)
    # say = Say()
    # say.say(hookups)