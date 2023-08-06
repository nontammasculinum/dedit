import discord
import random
import os

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        _ = message.content.replace("```", '\1').replace("\\\1", "```")
        print(len(_.split('\n')))
        if len(_.split('\n')) < 4:
            return
        __ = _.split('\n')[3:]
        if __[0] != "\1C":
            return
        _name = _.split('\n')[0].replace('-n', '')
        _platform = _.split('\n')[1].replace('-p', '').replace(' ', '')
        _flags = _.split('\n')[2].replace('-f', '').replace(' ', '')
        print(f"{_name}.c for {_platform} with {_flags}")
        _ = "\n".join(_.split('\n')[3:])
        _ = _.replace('\1C', '').replace('\1', '')
        print(_)
        name = f"{_name}".replace(' ', '')
        f = open(name, "w")
        f.write(_)
        f.close()
        if _platform == "linux":
            os.system(f"gcc {name.replace(' ', '')} -o {name.replace(' ', '')}_main {_flags}")
        elif _platform == "windows":
            os.system(f"x86_64-w64-mingw32-gcc {name.replace(' ', '')} -o {name.replace(' ', '')}_main {_flags}")
        await message.channel.purge(limit = 1)
        await message.channel.send(file=discord.File(f'{name}_main'))
        os.remove(name)
        os.remove(f'{name}_main')
        

intents = discord.Intents.default()
intents.message_content = True

SETTINGS = open("./SETTINGS")
settings = SETTINGS.read().split(' ')
for i in settings:
    i.replace('\n', '')
settings_dict = {
    "token": "",
}
for idx, i in enumerate(settings):
    if i == "token:":
        settings_dict["token"] = settings[idx + 1]
SETTINGS.close()

client = Client(intents=intents)
client.run(settings_dict["token"])
