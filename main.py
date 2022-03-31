import discord
from discord.ext import commands
from config import *
import json
import time

entrée = "banword.json"
sorti = "banword.json"


client = commands.Bot(command_prefix = prefix)





@client.event
async def on_message(message):
    verif = message.content.lower()
    verif = verif.replace(" ", "")
    verif = verif.replace(".", "")
    if verif.startswith('*') == True:
        await client.process_commands(message)
    else:
        if message.author.bot:
            return

        else:
            with open(entrée, "r", encoding="utf-8") as fp:
                données = json.load(fp)
            for i in données["word"]:
                if i in verif:
                    
                    if message.author.id not in données["role"]:
                        if i == "":
                            données["word"].remove("")
                            with open(sorti, "w", encoding="utf-8") as fp:
                                json.dump(données, fp, sort_keys=True, indent=4) 
                        else:

                            await message.delete()
                            warn = await message.channel.send(f"{message.author.mention}mot interdit !")
                            time.sleep(5)
                            await warn.delete()
                            with open(sorti, "w", encoding="utf-8") as fp:
                                json.dump(données, fp, sort_keys=True, indent=4)     
    







@client.command()
async def addword(ctx, *, mot):
        mot = mot.lower()
        mot = mot.replace(" ", "")
        mot = mot.replace(".", "")
        with open(entrée, "r", encoding="utf-8") as fp:
            données = json.load(fp)


        if mot in données["word"]:
            await ctx.send("ce mot est deja dans la liste !")
            with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)

        else:
            données["word"].append(mot)
            await ctx.send("Le mot a bien étais envoyer dans la liste des ban word !")
            with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)








@client.command()
async def delword(ctx, mot):
        mot = mot.lower()
        with open(entrée, "r", encoding="utf-8") as fp:
            données = json.load(fp)


        if mot in données["word"]:
            await ctx.send("Le mot a bien étais supprimer !")
            données["word"].remove(mot)
            with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)

        else:
            données["word"].append(mot)
            await ctx.send("Le mot que vous avez tapez n'apparais pas dans ma liste !")
            with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)





@client.command()
async def listword(ctx):

    with open(entrée, "r", encoding="utf-8") as fp:
            données = json.load(fp)

    s = "\n"

    for objet in données["word"]:
        s += "`" + objet + "`" + "\n"


    if s == "\n":
        await ctx.send(f"Tu n'a tjr pas mis de ban word uttilise **{prefix}addword** pour en ajouter !")
    else:
        embed=discord.Embed(title="Ban Word List", description="Voici la liste des ban words c:", color=0x1a36c1)
        embed.add_field(name="Ban Word:", value=s, inline=True)
        await ctx.send(embed=embed)




    with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)





@client.command()
async def delbypass(ctx, member : discord.Member):
        with open(entrée, "r", encoding="utf-8") as fp:
            données = json.load(fp)


        if member.id in données["role"]:
            await ctx.send("Le role a bien étais supprimer de la liste bypass !")
            données["role"].remove(member.id)
            with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)

        else:
            await ctx.send("L' id que vous venez de tapez n'ai pas dans la liste !")
            with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)




@client.command()
async def addbypass(ctx, member : discord.Member):
        with open(entrée, "r", encoding="utf-8") as fp:
            données = json.load(fp)


        if member.id in données["role"]:
            await ctx.send("cette id est deja dans la liste !")
            with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)

        else:
            données["role"].append(member.id)
            await ctx.send("L' id a bien étais ajouter dans la liste !")
            with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)








@client.command()
async def listbypass(ctx):

    with open(entrée, "r", encoding="utf-8") as fp:
            données = json.load(fp)

    s = "\n"

    for objet in données["role"]:
        s += "<@" + str(objet) + ">" + "\n"


    if s == "\n":
        await ctx.send(f"Tu n'a tjr pas mis de Joueur anti bypass uttilise **+addbypass** pour en ajouter !")
    else:
        embed=discord.Embed(title="Role bypass List", description="Voici la liste des role qui bypass les ban word c:", color=0x1a36c1)
        embed.add_field(name="Role Bypass:", value=s, inline=True)
        await ctx.send(embed=embed)




    with open(sorti, "w", encoding="utf-8") as fp:
                    json.dump(données, fp, sort_keys=True, indent=4)












client.run(token)