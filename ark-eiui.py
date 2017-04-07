# -*- encoding: utf-8 -*-
from arky import cfg, api, wallet, core, util
from yawTtk import dialog
import yawTtk

import os, imp, sys, math, json, binascii

# go  intoreal ARK world
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

	currency = "usd"
	ark2usd = 0.
	ark2eur = 0.
	ark2gbp = 0.

	support = False

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

		# update currencies values
		util.useExchange(Glob.price_platform)
		Glob.ark2usd = util.getArkPrice("usd")
		Glob.ark2eur = util.getArkPrice("eur")
		Glob.ark2gbp = util.getArkPrice("gbp")

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

	def checkSecondSignature(secret):
		if Glob.secondPublicKey:
			keyring = core.getKeys(secret)
			secondPublicKey = binascii.hexlify(keyring.public)
			secondPublicKey = secondPublicKey.decode() if isinstance(secondPublicKey, bytes) else secondPublicKey
			return (secondPublicKey == Glob.secondPublicKey)


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

			self.vote.set(round(votes, 3))
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
		in_ = open("pools.json", "r")
		pools = json.load(in_)
		in_.close()
		
		for child in list(self.children.values()):
			child.destroy()

		for d in sorted([d for d in Glob.delegates if d["username"] in pools], key=lambda d:d["rate"]):
			pool = Pool(self, relief="solid", padding=5)
			pool.set(**dict(d, **pools[d["username"]]))
			pool.compute()
			pool.update()
			PoolManager.tile_height = max(PoolManager.tile_height, float(pool.tk.call("winfo", "reqheight", pool)))
			PoolManager.tile_width = max(PoolManager.tile_width, float(pool.tk.call("winfo", "reqwidth", pool)))

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
			self.tk.setvar("ESTIMATED_USD", u"$%.1f/month" % (share*12600*Glob.ark2usd/100))


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
	Glob.update()
	print(Glob.rootfolder)

	# main window
	root = yawTtk.Tkinter.Tk()
	root.withdraw()
	root.title(u"\u0466rk Easy Investor - © 2016-2017 Toons")

	style = yawTtk.Style()

	toplevel = yawTtk.Toplevel(root)
	toplevel.withdraw()
	toplevel["border"] = 4
	toplevel.minsize(800, int(800/1.618033989))
	toplevel.maxsize(1024, int(1024/1.618033989))

	banner = Banner(toplevel, relief="solid", background="white", padding=2)
	support = ArkySupport(banner, cursor="hand2", padding=(5,0), foreground="blue")
	banner.pack(side="top", fill="x", padx=4, pady=4)

	paned = yawTtk.Tkinter.PanedWindow(toplevel, orient="horizontal", sashwidth=8, border=0)
	paned.pack(fill="both", expand=True, padx=4, pady=4)

	frame1 = yawTtk.Frame(paned, panned=4)
	frame1.columnconfigure(1, minsize=70)
	frame1.columnconfigure(2, weight=1)
	frame1.rowconfigure(2, weight=1)
	yawTtk.Label(frame1, text=u"Select \u0466RK \u0467ccount", padding=(0,0,2,0), font=("tahoma", 8, "bold")).grid(row=0, column=0, sticky="nesw")
	linker = Linker(frame1)
	linker.grid(row=1, column=0, columnspan=3, sticky="nesw", pady=2)
	status = Status(frame1, padding=2, text=u"St\u0467tus")
	status.grid(row=2, column=0, columnspan=3, sticky="nesw")
	paned.add(frame1, minsize=280, stretch="never")

	frame2 = yawTtk.Frame(paned, relief="flat", borderwidth=0)
	frame2.columnconfigure(0, weight=1)
	frame2.rowconfigure(0, weight=1)
	lock = VoteLocker(frame2, relief="solid", background="orange", padding=(5,0), cursor="hand2", foreground="blue", text="Account vote locked")
	lock.grid(row=1, column=0, columnspan=2, sticky="nes", pady=2)
	border = yawTtk.Frame(frame2, relief="sunken", borderwidth=2)
	dmg = PoolManager(border, border=0, relief="flat", highlightthickness=0)
	dmg.bind("<Configure>", dmg.arrange)
	dmg.pack(fill="both", expand=True, padx=0, pady=0)
	scrolly = yawTtk.Autoscrollbar(frame2, target=dmg, orient="vertical")
	border.grid(row=0, column=0, sticky="nesw")
	scrolly.grid(row=0, column=1, sticky="nesw")
	paned.add(frame2, minsize=350, stretch="always")

	linker.bind("<<ComboboxSelected>>", lambda e:[linker.linkAccount(), dmg.populate(), banner.update(), status.fill(), support.show()])
	
	def _loop(obj, func, ms):
		getattr(obj, func)()
		setattr(Glob, "_update%s"%id(obj), toplevel.after(ms, lambda o=obj,f=func,d=ms: _loop(o,f,d)))
	_loop(dmg,    "computeChecked", 1000)
	_loop(linker, "fill",           1000)

	toplevel.protocol('WM_DELETE_WINDOW', sys.exit)
	toplevel.deiconify()

	err = open(os.path.join(Glob.rootfolder, "err.log"), "a")
	sys.stderr = err
	root.mainloop()
	err.close()
