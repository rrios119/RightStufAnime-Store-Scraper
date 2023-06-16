import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
from discord import DiscordWebhook, DiscordEmbed


class Discord:
    def send_hook(track):
        webhook = DiscordWebhook(url = "https://discord.com/api/webhooks/895381957792387132/myY-1_lvU10xP0oJUlJdG3WZY7uczC_F2IpAdAUQNV_ENBD43uiaGma-wZuvgbJDlmsC", username = "RightStufAnime")
        activity = discord.Game(name = '-help')

        embed = DiscordEmbed(title='Embed Title', description='Your Embed Description', color='03b2f8')
        embed.set_author(name='Author Name', url='https://github.com/lovvskillz', icon_url='https://avatars0.githubusercontent.com/u/14542790')
        embed.set_footer(text='Embed Footer Text')
        embed.set_timestamp()
        embed.add_embed_field(name='Field 1', value='Lorem ipsum')
        embed.add_embed_field(name='Field 2', value='dolor sit')
        embed.add_embed_field(name='Field 3', value='amet consetetur')
        embed.add_embed_field(name='Field 4', value='sadipscing elitr')

        webhook.add_embed(embed)
        response = webhook.execute()

    async def track(ctx, ID, items, tracker):
        ID = int(ID)
        cond = [i for i in items['ID'] if ID in items['ID']]
        if (len(cond) > 0):
            tracker.append(ID)
            string = 'Successfully Tracking Item #: ', str(ID)
            await ctx.send(string)
        else:
            await ctx.send('Not Valid Item ID. Please Try Again.')

    async def search(ctx, *, name, items):
        name = name.title()
        found3 = items['Name'].str.contains(name)
        limit3 = found3.count()

        for i in range(limit3):
            if (found3[i]):
                string = ['-----------------------------------------------------------------------------------', '\n' ,'**ID:** ', str(items.loc[i].at['ID']), '\t', '**MSRP:** ', str(items.loc[i].at['MSRP']), '\t', '**Current Price:** ', str(items.loc[i].at['Current Price']), '\n', items.loc[i].at['URL']]
                string = ' '.join(string)
                await ctx.send(string)
                #await ctx.send('\n') 