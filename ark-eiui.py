# -*- encoding: utf8 -*-
# © Toons

from arky import cfg, api, wallet, core, util
from yawTtk import dialog
import yawTtk

import os, imp, sys, math, json, binascii

_exit=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAG7AAABuwBHnU4NQAAAAd0SU1FB9sMFws0LDm0tJ4AAAKWSURBVDjLjZJNSxtR"\
"FIafO6OGMaMkuhCF0A8DAbd1W8yq1IWbQin40eImLjSiXUhIgwS1aiOoiY2g4sIPuutKqq104V9QpCK0pV0NipQx6kykzp0ubIJSW3p2997zPuflvQduqImJCQBGRka6BwYGRgESiQT/VWNjYwBMT0/3ZDIZN5vN"\
"ut3d3c8BOjs7/+gXN0FSqVSitrZ22DRN6TgOiqIo29vb0cXFxdd/ndzX14frusVzf39/aHZ21k2n0y7gK9xvbGyg63qxrwSgtbWVqakphBBks9m3uVzuVmVlZZuqqti2DeCmUqmvpmm+aW5uTmxtbREOhwFQAObn"\
"5xFCsLCw8KW6uvqREOJHPp/H4/HgOA6AUFU1FwgEXsTj8dVwOMzMzMwloKOjA13XmZubG9N1/a6UEsMw3juO49E0DSklQOn5+fmOlJL6+vq2SCTSEo1GLwErKysAlJeXxwD29vZW0un0pGmaOcMwPliWtSmEkPF4"\
"/Klt258dxyEUCqWvZTA5OXm/pKSEi4sLhoeHewFGR0e/AQ+vBn16ehqtqKjY8Pv9dwAVcJTfbwGAk5MTAPNvP7W7u7vtui6KolBTUxMohuj1eg9d10XTtH8uWTAYrAWQUnJwcHBYBHR1dX0sAHp6enoB2tvbi8Kh"\
"oSEAfD5fDOD4+PgUsACUQppnZ2frUkoaGxvTTU1N91ZXV4uAwcFBYrFYRNO0x0IIDMN4eeMqLy0tuaWlpQWLm7Ztr5eVlXm8Xu8zv9/fcHR0hGVZ32Ox2O2CRrlqcXl52W9ZlqWqKnV1dQ+CweB0IBB4VVVV1aAo"\
"Cvl8fqcgDoVC1x0kk0mSySQA4+PjEZ/P9wSoB346jvNpf39/PpPJvANoaWlhbW0NgF/89hAL3mpSPAAAAABJRU5ErkJggg=="\

_coinmarketcap=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QQICjQMnvPWogAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3"\
"aXRoIEdJTVBkLmUHAAACS0lEQVQ4y31STU8TURQ9702hwLQZMEDZ2dhiaG3KR4nRmKokoK0xGBcslYUJG3eu/AEu/ANu3LhwYWKCKJGvVImkMZhYUi2k1UpLWz5bmpZ2RkLhvRlXVATGuznJybkn99wcAp0JByc1"\
"pbgNy9kOZNM/YGpqQbf3Fjmuo3oGciEH7+Aw2UrF4B0cJnIhd6rOcJxIxZe0bCaOfHYTAFCWlSrOvX2hmRpb4Ll+m5xqkPq5qGWiIZx3dcLt6bUpeV9IoIYBJe8PCdQwAABfPgUCuhE2VmJov+BGnakOka/zCQL6"\
"YWZ8LHCInz/OBESpWT/CrlKCSZIWKvu7nvW1NTi6PCNiQz24ykfEhnr0D438/4nGehMK+ZxHVVW0WizgnDeVSmVwzpvKsozgxCttOfpNO7rzj+NyNKwlIvOwO10wS43gKvsrJBRKaQeJWBQ292XYnd3kxAV2Zzc5"\
"57qEzEoKs1MTEIQazE1PQxBqEPseRp0owu5wYfXXon4P2l09pO/OfWKsrQHnHEZjLTjnWM+sgTEGUZIg7xT0ezD77qVWyG2iLCtQVV7F1jYLVFVFMb8NY4NZ32B7YxXemz4wdoBKZQ99fj8qlT10dHahXCwivhSB"\
"o/eafgSp2YLZ9+OYHB0FpUIVp8beIBlfRkfPVTg6LxLdC3xDDwgAPHvySKOUgnMGSinYwT4G7z080YMTRDKZfK0oylBwehS/C1uw2NzIJiIQz7Thyo27MJvNCzabrVfXAADS6XQ/Y+wpY8xzyAmCUDQYDI+tVuvz"\
"o9o/WW39IFljfp4AAAAASUVORK5CYII="\

_cryptocompare=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QQICjUIgIUj+gAAAZJJREFUOMutk00rRFEYx3/n3plRplwyYmVh"\
"IaV8ASyO2MjLQrKwIrO1UNeUKGnIZYH1pazViMjGrbtQVj6DjclbXpqNt3HnWDjqdiN5eTZP5+n5nfN/ev4H/hjip0DazzQCTUAr0Bz7xaP9wDxQAnLGLy6o0MoFcGxE5MV1jtaFzlvANJB7Kca7hFAnItSUAJLA"\
"MdACvLrSUWk/E3Ol85r2M0dAG7DhSmesdvqg/SrbfWREpN0BDcALYKX9jNBwXsNLrnTGLNsbenpObAEILbcWyAMBsA/0ASZQB5wDBjDhSmfFsr05PUa+sNxZb2i554DhSiexmetdUEpktapLDY9oeAeYCa/fAEaB"\
"e1c6omrycDtZ/ji43rE4G5SMEYAgMIdd6WyGVhgxkrwR+ClVOXm4q5ToA7LAQnVVwTqdGrhMTvg1MTNYLSx3Dlu2p0Ls2fsIfkpZtrenYaXlld3eWxeW7Y3HzOAaiH9lio8t9Gg4HEVg7TvLR50YvaT0SV2Fc/gv"\
"POhiMXQ2dc9zpE8Aj/xHvAGlSo95lhJTqQAAAABJRU5ErkJggg=="\

_exchange=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QQICjUksl1PGQAAATpJREFUOMul0ztLnFEQBuBns+sdQURQxEUb"\
"zR8QFgstBAvBUjvRxmptBEEsLNIIFkmZTsgvSJU/EFe7BCwsRBC8gLfGVQRBMa7NLHzZfN7IC4czZ87MnHln5pCOD8hgGg3eibqE/ANbIWeQe825arSGCh5iLyKPltcCdOIMmyjgOz7H3TfcogvZNOdG7GM1oRtK"\
"0MpiCeXnXp/CThRwEhMYQGvQakMzfmM5LcAGxjAfvKtrD79iX8EITpLtqqIPh7hL6Ir4iEH0ox4ldFcNcjW9r9RkVcBNyI8p938FOEZPGG3jCrOxRBHrMIzTtBrM4WeKfhxfMBPnXSymBajHdfBO1mc0YfMJ5y8N"\
"Ui/+YD3Og0GpKca6jPZ47J8uZHCEDhxEfUoxzhfRujwucf/Wj7UQGeT8B74mU67FE1YlPE1Rqil5AAAAAElFTkSuQmCC"\

_dollar=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAIISURBVDjLlZPRT1JxFMf5E+6fwL9Ri8lsI5cSV7sw"\
"L82w0SZTB6zWXOuB0cLU8HKhuAooTNrFupcAsYWjh1sRIaDgTLGXxmubD2w+9Prth29tXMWH83J+Z5/vOd9zfhoAml7h+mg3ReuhUxIdR37CrVanUXvgvvsOtk4kbJ+kEaos/bkSYCZv0wcri7/zrTS2f32AUOX+"\
"2nPWACvd1V4KmM7fnxQP1pE+2kSuJUM+EpFpvUOS5MJVHgQSuBCwWuU72eP3EA8TWCx523NFl+Iv+zrxRgRr+wKeFJ1NVYA9y+o3mjFskbkj9SDGpTGqm2dSJmosZfRYZXPClLxNqQJsGYt2bS+MbEtCF2SVmQCT"\
"ukOPikaqbxPnik4l3ohC+ilivbGKcC0Af/klXAVHczhuoC8FmDdpyl2YUrjyAlmfHytklATpJronwP9jAYbYIN3XHXTDuDGkJ6qeRzsz7XCNh1AjvshmRRXQnZWVmIQxOfTf5RFV/fw3LyJkC+6d2U5PwOjbEe3T"\
"z4/bQp0/b92WY5VbsZtuQ3SQfpC71+R3/eAqr2ASR7I9AUSVepibUHhSFCVKQv31uXm+0nPwVQ5dgOfLM+jeXNdf6AFRnZz9NNVeKs8jtr+CCDHvRcmL8bSlqQtdo/v+TBaZ+RrcXUaQqLMZy+GVf+OAcGPaWXCc"\
"kW7OBgTdslrdPxtwvK6n/CCRAAAAAElFTkSuQmCC"\

_euro=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAHvSURBVDjLjZPfSxRRFMf3T9g/wRdRkfKmRbkq3gfp"\
"YSvUHiIVZHqRiH7MbogW2GD1KOxrIVuUoOiKI+2isMleJXPZ3Np2NegstHNpGJg7K8yfcLquUII7sz183+7ne875nnMDiBjwEmz0ECkKqRCFZHew3pv64GbvkJkbN+zSExTFp1LTaBciWE72xUC/HPQ1kBUVcTiD"\
"zo9ZCUWRbw8y8/OIIb5Po1Oawd/bwwVPAwk32cUpdA6e4a/0wFv4cOVvNVi7NGRl77iQ6NK8DZIh1TnQ0MyOGnVHW+kkdTOAVE+wkgnrVn7CPfo5h8ct88wNxreuM/7xmlSYVTYGdM8Qy5t9Mbs4idXDF1IvURQm"\
"UXx7LBVFkY+g2FcRlojmuwWZLrGPAQlD4iKVs1JY7qSwdEGKUK9VB06FROyvkVpVOauET0BY7CB+t3IKVrFa0rBa1Goti/2HKHIPEBbOq40NEl0KT4eZtTvmHpWeo/VpxOWpq6yy3q/7wWfXuNihiC9RtHZuu/D+"\
"3JnWYb5VhfkW4nuJ5tawUc1PoZW55ZYXSAzetFGItyl8jTJn7x7aO+MIr5ubvE/5XTsx04OGyN5HJydD3Z1AsXcXnewjtNI3XQkrDT9TzSjeqlSWQzpfpYyv9rNyvD0Gr/5Vbmjwv/oDiJrRGbut70sAAAAASUVO"\
"RK5CYII="\

_money=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAJ0SURBVDjLlZPdT9JRGMe5qFu2Lrt1a63LWv9ATRdN"\
"5xvLsnLRipzZpIVpigjyIs3XAOUHgopoWkggP5QXSRJwJQmtm/IlAWtt3XXTfubS+nZ+P1eby6ldPGdn5+zzfb7Pc57DA8DbL9rjrYxuVsXf7W5fuC2mYawpE7QRJZpDDfz/EngYVTN9qR4EPvlgXjCiKVCPWvou"\
"/0ACxDJjSbIwDefqMPxrEzC87IDUW4Pq8Vv8PQVaX7Qw5qQRgY9ePP0wDMeSFfWTUkxmPeiI61DlFOP6SAV/VwFtRMFQCwb4CdwW10IbVcK+aMHgohmPlwdBZ11oCctx1X5p/R8B9Uzzuum1ntj1Iv1tGRtb3zH2"\
"dgSa2eZtOOOCMizD5cGyzR0lGBNdx1TP5T96E4+4WttiWg6mYr3Ifk1DF1PBmxmHYlrGZkbFUDku2oSHOAFjolOuIpZ65rs5+MmKg9hWcJlZWB1UbsOhRjYz5r/MoSn4AKWWQg0nwFoyzndhijRobGWIq3XgPQU1"\
"sa2LqjCRHoc81IBK9w0OnvscRWQtBGFfEc4b8o7wNDMKOwnY3lDwZZ+h1idB/zsThpf6CezkstVN3yNwHFMrNGqCVRvlA2UQ6POkud1nTvE0EcVR1gU7JNSCnrPrWLRtw+RM7BKBXnJDP9eOYqogVNAj0Av0uTk7"\
"mtjov2+1p2yQ0hIYXnXCs+qEzF+HC9YSyIiIsK84XWTKP5tvPHdi11GupSXHW8JNW+FMAHdclSCCKDEX/iKdDgotRY17jTu31LhvHybT5RGPin5K3NWs1c0yW+lp0umc/T7b383NUdHJa44rSfJU+Qf54n/iNzi8"\
"zBtL0z1zAAAAAElFTkSuQmCC"\

_pound=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAHHSURBVDjLpdPNTuJQGAZgL4FL4BK4BFcuNEZ03Mwk"\
"41+MMbNQok7UqCkGJWrGiZKiYJXKERgLpUVEIagcULSTii3KxC2X0Et4bXcmisq4+DYn53ve89sCoOUz9WJgnJXs7nBeJrlb8NlbBFKKMelL84PLcfu7wJhPcnDHipEs3SNz8wipVEPq8h/+nOnYjJeNb+6Y402A"\
"la7qyeIDhEIVfunaWODydC1arB/kNERzOqbYLG0I/FgXnbEzDfJlDV5S0PuXBJs1/pWJ2ZZ4WuczFbAJBT2TxP4qMLKWYA4vdETMtD6PMPB8Uu9MtPXLFGG6XcTVNRa2vQoMeeOuSF7DQVaDmepq+ha+ewQHl1YR"\
"v3jAr2jJaBrYEhUzXYdYqGEnpeJ3rGxCZaySMkaWU/RdgE1cIyirIKfWid9jW1TN5it4+RIGFz8AWNU9QZxs4i+2kyo6R0NM0y9xdCVN944q2DxU0D4cGvgw4BwP22f8+bpPUEBOquDkO6xHbuAOUjABivktijl/"\
"AR3DPN9wBdZeSaaK/WMdobSGvSMNu7IGTrpD0KyAWMG07xwNgX5Gph6u+CJ11myyGqc3zvFz4w2grW/H9j/f+Qn6r94u36IRBwAAAABJRU5ErkJggg=="\

_yen=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAHESURBVDjLY/j//z8DJRjO8F3q3d9ypOF/9b7y9x7z"\
"XAXQFTpPcaiv2VX+v2Bzznv7HlsFDAM857sJFOzIuT/hRO//wMW+81E0T3JQAGls29f8377Lph6rC0DYfZZLQOfh1v9tB5v/u0x1coCJB8zzW9+xv/1/xOKw8zi9AMPBSwPX9xzu+h+/KhqsGOjcgMZddf+rt1X+"\
"t26xNCBoAMS5eUDntvx3meDYn7Qy7n7rrsb/9h22/XgDERkDbS1o2d3wv31vy//+A73/S9YXvbesNRcg2gAQLtlU8H/KoUn/e/d1/89YnnafYDSC/T8vcH/ppqL/xRsK/tdvr/0/6cCE/9MPTf3fsr35f/byjP9Z"\
"y9L/5y3PeYnTgIBJ/g1+E3wbfPu8G5IWJR7o39v3v3h1wfvIuZEHnJudGhwbHBrs6+0aiPKCe4dbQ/XGqv/Ji5KeOzY6NBDlBd8pPvtzVmb9z16Z8b9hc/3/CXv7//fv7vtfu6Hqf8r8pP9J8xP/A124D6cBbm1u"\
"Da6tLg0g54bNDD3Qs6v7f/ayjM9BUwIPWFdaNViWWzZYlJsT5wW7WtuGnGXZ/8Nnht23rLAkzgsU5UZyMQAcp633iiwCvgAAAABJRU5ErkJggg=="\


# go  into real ARK world
api.use("ark")

# class containing all global vars and functions
class Glob:

	rootfolder = ""

	price_platform = "coinmarketcap"

	delegates = []
	ratings = {}

	wallet = None
	secondPublicKey = None
	balance = 0.
	votes = []
	lock_votes = True

	support = False
	exchange_rate = 1.
	currency_symbol = u"\u0466"

	# return True if it runs from a frozen script (py2exe, cx_Freeze...)
	@staticmethod
	def main_is_frozen():
		return (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__"))

	@staticmethod
	def getRootFolder():
		Glob.rootfolder = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable if Glob.main_is_frozen() else __file__)))
	
	@staticmethod
	def getKeyringPath(address):
		return os.path.join(Glob.rootfolder, ".keyring", cfg.__NET__, address+".akr")

	@staticmethod
	def getWalletStatus():
		data = {}
		if Glob.wallet.account: data.update(**Glob.wallet.account)
		if Glob.wallet.delegate: data.update(**Glob.wallet.delegate)
		if len(data): data["delegate votes"] = ", ".join(Glob.votes)
		return sorted([(k, ",".join(v) if isinstance(v, list) else v) for k,v in data.items()], key=lambda i:i[0])

	@staticmethod
	def update():
		# update rootfolder
		Glob.getRootFolder()
		try: os.makedirs(os.path.join(Glob.rootfolder, ".keyring", cfg.__NET__))
		except: pass

		# updates info about delegates
		Glob.delegates = api.Delegate.getCandidates()
		Glob.ratings = dict((d["username"],float(d["vote"])/100000000) for d in Glob.delegates)

		if isinstance(Glob.wallet, wallet.Wallet):
			Glob.secondPublicKey = Glob.wallet.account.get("secondPublicKey", None)
			Glob.balance = Glob.wallet.balance
			Glob.votes = Glob.wallet.votes
			Glob.support = True if "arky" in Glob.votes else False
		else:
			Glob.secondPublicKey = None
			Glob.balance = 0.
			Glob.votes = []
			Glob.support = False

	@staticmethod
	def checkSecondSignature(secret):
		if Glob.secondPublicKey:
			keyring = core.getKeys(secret)
			secondPublicKey = binascii.hexlify(keyring.public)
			secondPublicKey = secondPublicKey.decode() if isinstance(secondPublicKey, bytes) else secondPublicKey
			return (secondPublicKey == Glob.secondPublicKey)

	@staticmethod
	def useCurrency(currency=None, exchange=None):
		data = {"usd":"$", "eur":"€", "gbp":"£", "cny":"¥"}
		if exchange:
			util.useExchange(exchange)
			Glob.price_platform = exchange
		if currency in data:
			Glob.exchange_rate = util.getArkPrice(currency)
			Glob.currency_symbol = data[currency]

class Share:

	@staticmethod
	def arkyShare(votes, contrib, sharing=100., ceil=100., floor=0., **trash):
		ratio = contrib/(votes+contrib)*100
		return min(ratio, ceil) if ratio >= floor else 0.

# dialog to ask second secret when needed
class SecondSecretDialog(dialog.BaseDialog):
	
	check = False

	def fillMainFrame(self):
		self.transient(self.master)
		self.mainframe.columnconfigure(1, weight=1)
		yawTtk.Label(self.mainframe, image=dialog.password,compound="image", padding=5).grid(row=0, rowspan=2, column=0, sticky="nesw")
		yawTtk.Label(self.mainframe, text="Please enter your second secret", font=("tahoma", 10, "bold")).grid(row=0, column=1, sticky="nesw")
		yawTtk.Label(self.mainframe, text="Second secret will be checked with the one defined\n"\
                                          "in keyring file\n").grid(row=1, column=1, sticky="nesw")
		self.secret = yawTtk.Entry(self.mainframe, justify="center", show="-")
		self.secret.grid(row=2, column=0, columnspan=2, sticky="nesw")
		self.secret.focus()

	def fillButton(self):
		yawTtk.Button(self.buttonframe, font=("tahoma", 8, "bold"), image=dialog.tick16, compound="left",
		              background=self.background, default="active", text="Check", width=-1, padding=2,
		              command=self.check).pack(side="right")
		b = yawTtk.Button(self.buttonframe, image=dialog.stop16, compound="left", text="Show secrets",
		                  background=self.background, style="Toolbutton", padding=(5,0))
		b.pack(side="left")
		b.bind("<ButtonPress>", lambda e,o=self: o.secret.configure(show=""))
		b.bind("<ButtonRelease>", lambda e,o=self: o.secret.configure(show="-"))

	def check(self):
		secret = self.secret.get()
		if secret != "" and Status.secondPublicKey != None:
			SecondSecretDialog.check = Glob.checkSecondSignature(secret)
			self.secret.delete(0, "end")
			self.destroy()


# dialog to ask secret when needed
class WalletDialog(dialog.BaseDialog):

	def fillMainFrame(self):
		self.transient(self.master)
		self.mainframe.columnconfigure(1, weight=1)
		yawTtk.Label(self.mainframe, image=dialog.password,compound="image", padding=5).grid(row=0, rowspan=2, column=0, sticky="nesw")
		yawTtk.Label(self.mainframe, text="Please enter your secret(s)", font=("tahoma", 10, "bold")).grid(row=0, column=1, sticky="nesw")
		yawTtk.Label(self.mainframe, text="Your secret will not be saved locally. A keyring\n"\
                                          "file will be registered for this acccount so it\n"\
                                          "can be linked later without ascing secret.").grid(row=1, column=1, sticky="nesw")
		yawTtk.Label(self.mainframe, text="First passphrase", font=("tahoma", 10, "bold")).grid(row=2, column=0, columnspan=2, sticky="nesw", padx=20)
		self.secret = yawTtk.Entry(self.mainframe, justify="center", show="-")
		self.secret.grid(row=3, column=0, columnspan=2, sticky="nesw", padx=20)
		self.secret.focus()
		yawTtk.Label(self.mainframe, text="Second passphrase (if needed)", font=("tahoma", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky="nesw", padx=20)
		self.secondsecret = yawTtk.Entry(self.mainframe, justify="center", show="-")
		self.secondsecret.grid(row=5, column=0, columnspan=2, sticky="nesw", padx=20)

	def fillButton(self):
		yawTtk.Button(self.buttonframe, font=("tahoma", 8, "bold"), image=dialog.tick16, compound="left",
		              background=self.background, default="active", text="Link", width=-1, padding=2,
		              command=self.link).pack(side="right")
		b = yawTtk.Button(self.buttonframe, image=dialog.stop16, compound="left", text="Show secrets",
		                  background=self.background, style="Toolbutton", padding=(5,0))
		b.pack(side="left")
		b.bind("<ButtonPress>", lambda e,o=self: [o.secret.configure(show=""), o.secondsecret.configure(show="")])
		b.bind("<ButtonRelease>", lambda e,o=self: [o.secret.configure(show="-"), o.secondsecret.configure(show="-")])

	def link(self):
		secret = self.secret.get()
		secondsecret = self.secondsecret.get()
		if secret != "":
			try: Glob.wallet = wallet.Wallet(secret, None if secondsecret == "" else secondsecret)
			except: Glob.wallet = None
			self.secret.delete(0, "end")
			self.secondsecret.delete(0, "end")
			self.destroy()


# an network connection colored indicator
class Indicator(yawTtk.Label):

	def __init__(self, master=None, cnf={}, **kw):
		config = dict(cnf, **kw)
		config.update(text=u"\u0466", font=("tahoma", 12, "bold"))
		yawTtk.Label.__init__(self, master, **config)

	def update(self, widget=None):
		self["foreground"] = "white" if cfg.__NET__ in ["testnet", "devnet"] else "blue"
		if wallet.api.Loader.getLoadingStatus().get("success", False):
			self["background"] = "lightblue" 
			self["relief"] = "sunken"
		else:
			self["background"] =  "orange"
			self["relief"] =  "solid"

	def destroy(self):
		yawTtk.Label.destroy(self)


# an ARK address linker
class Linker(yawTtk.Combobox):

	def __init__(self, master=None, cnf={}, **kw):
		config = dict(cnf, **kw)
		yawTtk.Combobox.__init__(self, master, **config)
		self.update()

	def update(self, value=None):
		self["state"] = "normal"
		self.delete(0,"end")
		if value: self.insert(0, value)
		self["state"] = "readonly"

	def linkAccount(self, *args, **kw):
		former_wallet = Glob.wallet
		value = self.get()
		if value == u"--- Link \u0466ccount ---":
			toplevel = self.winfo_toplevel()
			toplevel.wm_attributes("-disable", True)
			dlg = WalletDialog(toplevel, title=u"Link \u0466ccount")
			dlg.show()
			toplevel.wait_window(dlg)
			toplevel.wm_attributes("-disable", False)
			self.tkraise()
			if former_wallet != Glob.wallet and isinstance(Glob.wallet, wallet.Wallet):
				Glob.wallet.save(Glob.getKeyringPath(Glob.wallet.address))
			if isinstance(Glob.wallet, wallet.Wallet):
				self.update(Glob.wallet.address)
			else:
				self.update()
		else:
			pathfile = Glob.getKeyringPath(value)
			if os.path.exists(pathfile):
				Glob.wallet = wallet.open(pathfile)
		Glob.update()

	def fill(self, event=None):
		self["values"] = tuple(sorted([os.path.splitext(f)[0] for f in os.listdir(os.path.join(Glob.rootfolder, ".keyring", cfg.__NET__)) if f.endswith(".akr")])) + (u"--- Link \u0466ccount ---",)


# a status frame that shows all ARK account properties
class Status(yawTtk.Labelframe):
	
	def __init__(self, *args, **kw):
		yawTtk.Labelframe.__init__(self, *args, **kw)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.content = yawTtk.Scrolledframe(self, border=0, padding=0, stretch=True)
		self.content.grid(row=0, column=0, sticky="nesw")
		yawTtk.Autoscrollbar(self, target=self.content, orient = "vertical").grid(row=0, column=1, sticky="nesw")

	def clear(self):
		self.content.content.columnconfigure(1, weight=1)
		for child in list(self.content.content.children.values()):
			if isinstance(child, yawTtk.Label):
				self.tk.unsetvar(child["text"])
			child.destroy()
		self.content.update_scrollregion()

	def fill(self):
		self.clear()
		i = 0
		for key, value in Glob.getWalletStatus():
			yawTtk.Label(self.content.content, text=key).grid(row=i, column=0, sticky="ew")
			yawTtk.Entry(self.content.content, textvariable=key, state="readonly").grid(row=i, column=1, sticky="ew", pady=1)
			self.tk.setvar(key, value)
			i += 1
		yawTtk.Frame.update(self)
		self.content.update_scrollregion()


# pool frame
class Pool(yawTtk.Frame):

	_weakref = {}
	
	def __init__(self, parent=None, cnf={}, **kw):
		self.rate = 0
		self.weight = 0.
		self.share = 0.

		yawTtk.Frame.__init__(self, parent, cnf, **kw)
		self.columnconfigure(2, weight=1)
		Pool._weakref[self._w] = self

		i=0
		self.name = yawTtk.StringVar(self)
		self.check = yawTtk.StringVar(self)
		self.selector = yawTtk.Checkbutton(self, font=("tahoma", "9", "bold"), textvariable=self.name, variable=self.check, command=self.compute)
		self.selector.grid(row=i, column=0, columnspan=3, sticky="nesw")

		i+=1
		self.vote = yawTtk.IntVar(self)
		yawTtk.Label(self, text="Votes :").grid(row=i, column=0, sticky="nesw")
		e = yawTtk.Entry(self, width=12, textvariable=self.vote, justify="right")
		e.grid(row=i, column=1, sticky="nesw")
		e.state("disabled")
		yawTtk.Label(self, text=u"\u0466").grid(row=i, column=2, sticky="nesw")

		i+=1
		self.sharing = yawTtk.DoubleVar(self)
		yawTtk.Label(self, text="Sharing :").grid(row=i, column=0, columnspan=2, sticky="nesw")
		e = yawTtk.Entry(self, width=5, textvariable=self.sharing, justify="right")
		e.grid(row=i, column=1, sticky="nes")
		e.state("disabled")
		yawTtk.Label(self, text="%").grid(row=i, column=2, sticky="nesw")

		i+=1
		self.ceil = yawTtk.DoubleVar(self)
		yawTtk.Label(self, text="Ceil :").grid(row=i, column=0, columnspan=2, sticky="nesw")
		e = yawTtk.Entry(self, width=5, textvariable=self.ceil, justify="right")
		e.grid(row=i, column=1, sticky="nes")
		e.state("disabled")
		yawTtk.Label(self, text="%").grid(row=i, column=2, sticky="nesw")

		i+=1
		self.floor = yawTtk.DoubleVar(self)
		yawTtk.Label(self, text="Floor :").grid(row=i, column=0, columnspan=2, sticky="nesw")
		e = yawTtk.Entry(self, width=5, textvariable=self.floor, justify="right")
		e.grid(row=i, column=1, sticky="nes")
		e.state("disabled")
		yawTtk.Label(self, text="%").grid(row=i, column=2, sticky="nesw")

		self.info = yawTtk.Label(self, relief="solid", font=("tahoma", "9", "bold"), foreground="steelblue", background="white", padding=5)
		self.update()

	def set(self, **info):
		username = info.get("username", "<username>")
		self.name.set(username)
		self.vote.set(int(info.get("vote", 0)))
		self.sharing.set(round(info.get("sharing", 0.), 1))
		self.floor.set(round(info.get("floor", 0.), 1))
		self.ceil.set(round(info.get("ceil", 100.), 1))
		self.check.set("1" if username in Glob.votes else "0")

	def compute(self, nb_votes=None):
		username = self.name.get()
		search = [d for d in Glob.delegates if d["username"] == username]
		if len(search):
			delegate = search[0]
			ratings = dict(Glob.ratings) 
			votes = float(delegate["vote"])/100000000 - (Glob.balance if username in Glob.votes else 0)
			if self.check.get() == "1":
				contrib = Glob.balance / Pool.countChecked()
				votes += contrib
				ratio = contrib/votes*100
				self.info.place(relx=0.5, rely=0.7, anchor="center")
			else:
				contrib = - Glob.balance / max(1, Pool.countChecked())
				votes += contrib
				ratio = 0.
				self.info.place_forget()

			ratings[username] += contrib
			ratings = [p[0] for p in sorted([i for i in ratings.items()], key=lambda i:i[-1], reverse=True)]
			self.rate = ratings.index(username) +1

			self.vote.set(max(0., round(votes, 3)))
			self.weight = ratio
			if self.rate <= 52:
				self.setDelegate()
				ratio = min(ratio, self.ceil.get()) if ratio >= self.floor.get() else 0.
				self.share = ((ratio/100.) * (self.sharing.get()/100.))*100.
				self.info["background"] = "white"
			else:
				self.setRelay()
				self.share = 0.
				self.info["background"] = "orange"
			self.info["text"] = "Weight: %.1f%%\nShare: %.1f%%" % (self.weight, self.share)

		return self.share

	@staticmethod
	def countChecked(): return len([elem for elem in Pool._weakref.values() if elem.check.get() == "1"])
	def isChecked(self): return True if self.check.get() == "1" else False
	def setDelegate(self): self["background"] = "lightgreen"
	def setRelay(self): self["background"] = "red"
	def destroy(self): yawTtk.Frame.destroy(Pool._weakref.pop(self._w))


class PoolManager(yawTtk.Canvas):

	nb_column = 1
	tile_width = 1
	tile_height = 1
	padding = 10

	def placeDelegate(self, tagorid, nb_column=1, index=None):
		step_w = PoolManager.tile_width + PoolManager.padding
		step_h = PoolManager.tile_height + PoolManager.padding
		if not index:
			x, y = self.coords(tagorid)
			index = (int(y)//step_h) * PoolManager.nb_column + int(x)//step_w
		index = int(index)
		self.coords(
			tagorid,
			int((index%nb_column)*step_w + PoolManager.padding),
			int((index//nb_column)*step_h + PoolManager.padding)
		)

	def populate(self, event=None, sortby="rate", reverse=False):
		self.tk.setvar("best_pool", "Best share with ...")
		in_ = open("pools.json", "r")
		pools = json.load(in_)
		in_.close()
		
		for child in list(self.children.values()):
			child.destroy()

		single = {}
		for d in sorted([d for d in Glob.delegates if d["username"] in pools], key=lambda d:d["rate"]):
			p = pools[d["username"]]
			pool = Pool(self, relief="solid", padding=5)
			pool.set(**dict(d, **p))
			pool.compute()
			pool.update()
			PoolManager.tile_height = max(PoolManager.tile_height, float(pool.tk.call("winfo", "reqheight", pool)))
			PoolManager.tile_width = max(PoolManager.tile_width, float(pool.tk.call("winfo", "reqwidth", pool)))
			if d["rate"] <= 52: single[d["username"]] = Share.arkyShare(float(d["vote"])/100000000, Glob.balance, **p)

		self.tk.setvar("best_pool", "Best share with %s" % sorted(single.items(), key=lambda i:i[-1], reverse=True)[0][0])
		self.sort(sortby, reverse)
		self.arrange()

	def updateScrollregion(self):
		step_w = PoolManager.tile_width + PoolManager.padding
		step_h = PoolManager.tile_height + PoolManager.padding
		nb_delegates = len(self.children)
		x2 = int(step_w * PoolManager.nb_column)
		y2 = int(step_h * math.ceil(float(nb_delegates)/PoolManager.nb_column))
		self["scrollregion"] = (0, 0, x2 + PoolManager.padding, y2 + PoolManager.padding)

	def sort(self, attr, reverse=False):
		if attr in ["name", "sharing", "vote", "floor", "ceil"]:
			sortlist = sorted([c for c in self.children.values() if isinstance(c, Pool)], key=lambda c:getattr(c, attr).get(), reverse=reverse)
		else:
			sortlist = sorted([c for c in self.children.values() if isinstance(c, Pool)], key=lambda c:getattr(c, attr), reverse=reverse)
		place = 0
		self.delete(*self.find_all())
		for child in sortlist:
			tagorid = self.create_window(0, 0, width=int(PoolManager.tile_width), height=int(PoolManager.tile_height), window=child, anchor="nw")
			self.placeDelegate(tagorid, PoolManager.nb_column, place)
			place += 1
		self.updateScrollregion()

	def arrange(self, *args, **kw):
		size = PoolManager.tile_width + PoolManager.padding
		nb_column = max(1, (float(self.tk.call("winfo", "width", self._w)) - PoolManager.padding)//size)

		if nb_column != PoolManager.nb_column:
			for tagorid in self.find_all():
				self.placeDelegate(tagorid, nb_column)
			PoolManager.nb_column = nb_column
			self.updateScrollregion()

	def computeChecked(self):
		if isinstance(Glob.wallet, wallet.Wallet):
			checked = []
			for child in [c for c in self.children.values() if isinstance(c, Pool)]:
				username = child.name.get()
				if username in Glob.votes:
					if Glob.lock_votes: 
						child.check.set("1")
						child.selector.state("disabled")
					else:
						child.selector.state("!disabled")
				elif username == "arky":
					if Glob.support:
						child.check.set("1")
						child.selector.state("disabled")
					else:
						child.selector.state("!disabled")
				if child.isChecked():
					checked.append(child)

			share = 0.
			for child in checked:
				share += child.compute()

			self.tk.setvar("GLOBAL_SHARE", "total %.1f%%" % share)
			self.tk.setvar("ESTIMATED_ARK", u"\u0466%.1f/month" % (share*12600/100))
			self.tk.setvar("ESTIMATED_USD", Glob.currency_symbol + u"%.1f/month" % (share*12600*Glob.exchange_rate/100))


class Banner(yawTtk.Frame):

	def __init__(self, *args, **kw):
		yawTtk.Frame.__init__(self, *args, **kw)
		self["height"] = 80

		yawTtk.Label(self, background=self["background"], textvariable="GLOBAL_SHARE", font=("tahoma", 24, "bold"), padding=10).place(relx=0, rely=0.4, anchor="w")
		yawTtk.Label(self, background=self["background"], textvariable="ESTIMATED_ARK", font=("tahoma", 24, "bold"), padding=10).place(relx=0.5, rely=0.4, anchor="center")
		yawTtk.Label(self, background=self["background"], textvariable="ESTIMATED_USD", font=("tahoma", 24, "bold"), padding=10).place(relx=1.0, rely=0.4, anchor="e")


class VoteLocker(yawTtk.Label):

	def __init__(self, *args, **kw):
		yawTtk.Label.__init__(self, *args, **kw)
		self.bind("<Button-1>", self.lockActualVote)

	def lockActualVote(self, event=None):
		Glob.lock_votes = not Glob.lock_votes
		if Glob.lock_votes:
			self["background"] = "orange"
			self["text"] = "Account vote locked"
		else:
			self["background"] = "white"
			self["text"] = "Account vote unlocked"


class ArkySupport(yawTtk.Label):

	def __init__(self, *args, **kw):
		yawTtk.Label.__init__(self, *args, **kw)
		self.bind("<Button-1>", self.SupportArky)
		self.SupportArky()

	def SupportArky(self, event=None):
		if event: Glob.support = not Glob.support
		if Glob.support:
			self["background"] = "orange"
			self["text"] = "Unlock arky vote"
		else:
			self["background"] = "lightgreen"
			self["text"] = "Support my work, vote for arky delegate"

	def show(self):
		if "arky" in Glob.votes:
			self.place_forget()
		else:
			self.place(relx=1.0, rely=1.0, anchor="se")

if __name__ == "__main__":
	if Glob.main_is_frozen():
		err = open(os.path.join(Glob.rootfolder, "err.log"), "a")
		sys.stdout = err
		sys.stderr = err
	
	Glob.update()
	Glob.useCurrency("usd", "coinmarketcap")

	# main window
	root = yawTtk.Tkinter.Tk()
	root.withdraw()
	root.title(u"\u0466rk Easy Investor - © 2016-2017 Toons")
	root.setvar("currency", "usd")
	root.setvar("exchange_price", "coinmarketcap")

	style = yawTtk.Style()

	toplevel = yawTtk.Toplevel(root)
	# toplevel.iconbitmap('ark.ico')
	toplevel.withdraw()
	toplevel["border"] = 4
	toplevel.minsize(800, int(800/1.618033989))
	toplevel.maxsize(1024, int(1024/1.618033989))

	# menu widget
	menubar = yawTtk.Menu(root)
	appmenu = yawTtk.Menu(menubar, tearoff=False, name="appmenu")
	pricemenu = yawTtk.Menu(appmenu, tearoff=False, name="pricemenu")
	pricemenu.add("radiobutton", variable="exchange_price", value="coinmarketcap", image=_coinmarketcap, compound="left", ulabel="_Coinmarketcap", command=lambda: Glob.useCurrency(None, "coinmarketcap"))
	pricemenu.add("radiobutton", variable="exchange_price", value="cryptocompare", image=_cryptocompare, compound="left", ulabel="Cryptoco_mpare", command=lambda: Glob.useCurrency(None, "cryptocompare"))
	currencymenu = yawTtk.Menu(appmenu, tearoff=False, name="currencymenu")
	currencymenu.add("radiobutton", variable="currency", value="usd", image=_dollar, compound="left", ulabel="_US Dollar", command=lambda: Glob.useCurrency("usd"))
	currencymenu.add("radiobutton", variable="currency", value="eur", image=_euro, compound="left", ulabel="_Euro", command=lambda: Glob.useCurrency("eur"))
	currencymenu.add("radiobutton", variable="currency", value="gbp", image=_pound, compound="left", ulabel="_British Pound", command=lambda: Glob.useCurrency("gbp"))
	currencymenu.add("radiobutton", variable="currency", value="cny", image=_yen, compound="left", ulabel="_Yen", command=lambda: Glob.useCurrency("cny"))
	appmenu.add("cascade", image=_exchange, compound="left", ulabel="E_xchange price", menu=pricemenu)
	appmenu.add("cascade", image=_money, compound="left", ulabel="_Currency", menu=currencymenu)
	appmenu.add("separator")
	appmenu.add("command", image=_exit, compound="left", ulabel="E_xit", command=sys.exit)
	menubar.add("cascade", ulabel="_App", menu=appmenu)

	banner = Banner(toplevel, relief="solid", background="white", padding=2)
	support = ArkySupport(banner, cursor="hand2", padding=(5,0), foreground="blue")
	banner.pack(side="top", fill="x", padx=4, pady=4)

	paned = yawTtk.Frame(toplevel, border=0)
	paned.pack(fill="both", expand=True, padx=4, pady=4)
	paned.rowconfigure(0, weight=1)
	paned.columnconfigure(0, minsize=280)
	paned.columnconfigure(1, minsize=8)
	paned.columnconfigure(2, weight=1, minsize=350)

	# paned = yawTtk.Tkinter.PanedWindow(toplevel, orient="horizontal", sashwidth=8, border=0)
	# paned.pack(fill="both", expand=True, padx=4, pady=4)

	frame1 = yawTtk.Frame(paned, padding=0)
	frame1.grid(row=0, column=0, sticky="nesw")
	frame1.columnconfigure(1, minsize=70)
	frame1.columnconfigure(2, weight=1)
	frame1.rowconfigure(2, weight=1)
	yawTtk.Label(frame1, text=u"Select \u0466RK \u0467ccount", padding=(0,0,2,0), font=("tahoma", 8, "bold")).grid(row=0, column=0, sticky="nesw")
	linker = Linker(frame1)
	linker.grid(row=1, column=0, columnspan=3, sticky="nesw", pady=2)
	status = Status(frame1, padding=2, text=u"St\u0467tus")
	status.grid(row=2, column=0, columnspan=3, sticky="nesw")
	# paned.add(frame1, minsize=280, stretch="never")

	frame2 = yawTtk.Frame(paned, name="bottom", relief="flat", borderwidth=0)
	frame2.grid(row=0, column=2, sticky="nesw")
	frame2.columnconfigure(0, weight=1)
	frame2.rowconfigure(0, weight=1)
	yawTtk.Label(frame2, relief="solid", padding=(5,0), textvariable="best_pool", font=("tahome", 8, "bold")).grid(row=1, column=0, columnspan=2, sticky="nesw", pady=2)
	lock = VoteLocker(frame2, relief="solid", background="orange", padding=(5,0), cursor="hand2", foreground="blue", text="Account vote locked")
	lock.grid(row=1, column=0, columnspan=2, sticky="nes", pady=2)
	border = yawTtk.Frame(frame2, relief="sunken", borderwidth=2)
	dmg = PoolManager(border, border=0, relief="flat", highlightthickness=0)
	dmg.bind("<Configure>", dmg.arrange)
	dmg.pack(fill="both", expand=True, padx=0, pady=0)
	scrolly = yawTtk.Autoscrollbar(frame2, target=dmg, orient="vertical")
	border.grid(row=0, column=0, sticky="nesw")
	scrolly.grid(row=0, column=1, sticky="nesw")
	# paned.add(frame2, minsize=350, stretch="always")

	linker.bind("<<ComboboxSelected>>", lambda e:[
		linker.linkAccount(),
		dmg.populate(),
		banner.update(),
		status.fill(),
		support.show()
	])

	def _loop(obj, func, ms):
		getattr(obj, func)()
		setattr(Glob, "_update%s"%id(obj), toplevel.after(ms, lambda o=obj,f=func,d=ms: _loop(o,f,d)))
	_loop(dmg,    "computeChecked", 1000)
	_loop(linker, "fill",           1000)

	toplevel.protocol('WM_DELETE_WINDOW', sys.exit)
	toplevel.configure(menu=menubar)
	toplevel.deiconify()

	root.mainloop()
	err.close()
