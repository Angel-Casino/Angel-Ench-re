from nextcord.ext import commands
import nextcord, json, database
id = 1092246921571221695
class Daily(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(name='daily', description='Ajoute un daily!')
  async def daily_slash(self, interaction: nextcord.Interaction, name: str = nextcord.SlashOption(name="nom", description="Le nom du produit"), description: str = nextcord.SlashOption(name="description", description="La description du produit"), url: str = nextcord.SlashOption(name="image_url", description="L'url de l'image du produit"), Bet: str = nextcord.SlashOption(name="starting", description="Le prix de départ")):
    if not 1091822410770153573 in [role.id for role in interaction.user.roles]:
      await interaction.response.send_message("Tu dois être un directeur pour faire cela!", ephemeral=True)
      return
    with open("json/daily.json", 'r') as f:
      data = json.loads(f.read())
    if data['en_cours']:
      await interaction.response.send_message("Merci de stopper celui en cours!", ephemeral=True)
      return
    message = await self.bot.get_channel(id).send(embed=nextcord.Embed(title=name, description=f"**{description}**\n\n__**Mise**__ **:** **{Bet} $**\n__**Miseur(e)**__ : <@927735457901576192>", color=0x992d22).set_image(data['img']))
    data['en_cours'] = True
    data['nom'] = name
    data['description'] = description
    data['img'] = url
    data['Bet'] = Bet
    data['id'] = message.id
    data['win'] = 927735457901576192
    with open('json/daily.json', 'w') as f:
      json.dump(data, f, indent=3)
    await interaction.response.send_message(embed=nextcord.Embed(title=name, description=f"**{description}**\n\n__**Mise**__ **:** **{Bet} $**\n__**Miseur(e)**__ : <@{data['win']}>", color=0x992d22).set_image(url))
    
  @commands.Cog.listener("on_message")
  async def new_bet(self, message):
    if message.channel.id != id or message.author.bot: return
    await message.delete()
    if (message.content.startswith("9") or message.content.startswith("0") or message.content.startswith("8") or message.content.startswith("7") or message.content.startswith("6") or message.content.startswith("5") or message.content.startswith("4") or
    message.content.startswith("3") or message.content.startswith("2") or message.content.startswith("1")) is False: return
    price = int((amount := message.content.replace('$', '').replace("€", '')))
    with open("json/daily.json", 'r') as f:
      data = json.loads(f.read())
    if database.get_coin(message.author.id) < price: return
    if price < int(data['Bet']): return
    data['Bet'] = price
    data['win'] = message.author.id
    with open('json/daily.json', 'w') as f:
      json.dump(data, f, indent=3)
    msg = await self.bot.get_channel(id).fetch_message(data['id'])
    await msg.edit(embed=nextcord.Embed(title=data['nom'], description=f"**{data['description']}**\n\n__**Mise**__ **:** **{amount} $**\n__**Miseur(e)**__ : <@{data['win']}>", color=0x992d22).set_image(data['img']))

def setup(bot):
  bot.add_cog(Daily(bot))
