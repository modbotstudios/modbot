##### PREMIUM commands and premium redeem script (currently not used) #####

# @bot.command()
# @commands.is_owner()
# async def cupon(ctx, code):
#
# 		if code == None:
# 			await ctx.send('No argument given')
# 		else:
# 			with open('db/codes.json','r') as f:
# 				cupon = json.load(f)
# 			if str(code) not in cupon:
# 				cupon[str(code)] = "active"
# 				with open('db/codes.json','w') as f:
# 					json.dump(cupon,f)
# 				await ctx.send(f'Adding cupon done')
# 				await ctx.message.delete()
# 			else:
# 				await ctx.send("Ooops, that cupon is already registered!")
#
#
#
# @bot.command()
# async def redeem(ctx, code):
# 	if code == None:
# 		await ctx.send('No cupon code given')
# 	else:
# 		with open('db/codes.json','r') as f:
# 			cupon = json.load(f)
# 		if str(code) not in cupon:
# 			await ctx.send('Ooops, cupon is invalid or already redeemed!')
# 			await ctx.message.delete()
#
# 		else:
# 			with open('db/premium.json','r') as f:
# 					premium = json.load(f)
# 			if str(ctx.author.id) not in premium:
# 				cupon.pop(code)
# 				with open('db/codes.json','w') as f:
# 					json.dump(cupon,f)
# 				with open('db/premium.json','r') as f:
# 					premium = json.load(f)
#
# 					premium[str(ctx.author.id)] = "premium"
# 					with open('db/premium.json','w') as f:
# 						json.dump(premium,f)
# 					await ctx.send(f'Code redeemed.')
# 					await ctx.message.delete()
# 			else:
# 				await ctx.message.delete()
# 				await ctx.send('Ooops, you already have premium!')
#
#
#
# @bot.command()
# async def join(ctx):
# 			await ctx.send('Ooops, the giveaway has ended! Try to get lucky the next time!')





## ACTIVATION PROCESS ##
# @bot.event
# async def on_member_update(before, after):
#     if before.guild.id == 782661120858259477:
#         if after.roles != before.roles:
#             a = after.roles
#             user = after.id
#             print(user)
#             try:
#                 with open('db/premium.json','r') as f:
#                     premium = json.load(f)
#
#                 b=str(a).index("<Role id=799296810203611136 name='Premium'>")
#
#
#
#                 print('The above user ID bought and reedemed premium')
#                 if str(after.id) in premium:
#                     print('Already Premium')
#
#                 else:
#                     premium[str(after.id)] = "premium"
#                     with open('db/premium.json','w') as f:
#                         json.dump(premium,f)
#
#
#                     embed=discord.Embed(title="Premium")
#                     embed.set_author(name="modbot premium", url=website, icon_url=url)
#                     embed.add_field(name="Premium redeemed!", value=f"Hi {after.mention}, you are now premium!! We appreciate your help so much!! Starting from now you will get access to all the premium benefits, including upcoming ones!", inline=True)
#                     await after.send(embed=embed)
#             except:
#                 with open('db/premium.json','r') as f:
#                     premium = json.load(f)
#                 if str(after.id) in premium:
#                     premium.pop(str(after.id))
#                     with open('db/premium.json','w') as f:
#                         json.dump(premium,f)
#                         print('Premium expired')
#                 else:
#
#                     print('Roles updated but premium not redeemed')
#
#







