from nextcord.ext import commands
import nextcord, json, database
class End(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(name='end', description='Finit un fin!')
  async def end_slash(self, interaction: nextcord.Interaction, file: str = nextcord.SlashOption(name="mode", description="Le mode d'enchère", choices={"daily": "daily.json", "hebdomadaire": "hebdomadaire.json", 'mensuel': "mensuel.json"})):
    if not 1091822410770153573 in [role.id for role in interaction.user.roles]:
      await interaction.response.send_message("Tu dois être un directeur pour faire cela!", ephemeral=True)
      return
    with open("json/daily.json", 'r') as f:
      data = json.loads(f.read())
    database.remove(data['win'], data['Bet'])
    msg = await self.bot.get_channel(id).fetch_message(data['id'])
    await msg.delete()
    data['en_cours'] = False
    with open('json/daily.json', 'w') as f:
      json.dump(data, f, indent=3)

def setup(bot):
  bot.add_cog(End(bot))
