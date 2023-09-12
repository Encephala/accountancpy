## Filosofie
- Snel en toegankelijk te gebruiken
- Flexibel voor power users/moeilijke usecases
## Database
File, hoeft geen directory voor I guess.
Tables voor:
- [x] Categorieën (GBK)
	- id UNIQUE, naam, soort, notities
	- GBK soorten zijn inkomsten/uitgaven/bank/activa etc.
		- W&V of Balans is geïmpliceerd door GBK soort
- [x] Relaties
- [ ] Bankrekeningen?
	- Komt later wel if at all
- [x] Boekingen
	- ID (auto is priem), notitie
	- Één grote tabel of tabel per GBK of tabel per jaar ofzo?
		- Kan opsplitsen per jaar (~5 tables)
		- Kan opsplitsen per GBK (~20 tables)
		- Kan één grote hoop maken
		- Boekingen worden één grote hoop, boekingsregels losse grote hoop
	- [x] Boekingsoorten (Dagboeken)
	- [x] Boekingsregels (1 grote hoop)
		- boeking FOREIGN
		- datum
		- GBK
		- document nullable
		- bedrag
			- +/- of debet/credit?
			- liefst een instelling I guess maar in begin uitgaan van +/-
## Backend (Django)

## Frontend (HTMX + Tabler)
### Keuze
Een lightweight framework gaat me te veel werk kosten, nty
Dus iets als:
- [Tabler](https://tabler.io/)
- [Black and white](https://www.figma.com/community/file/1201935147948130925)
- [Basic](https://www.figma.com/community/file/1088468250791967662)
- B&W en Basic zijn wat leeg imo
- [Shards Dashboard](https://designrevision.com/downloads/shards-dashboard-lite/)
- Shards wordt het, ziet er het relaxt uit imo, Tabler iets te scherp. Vast customize-baar maar hè
- [Shards zelf](https://designrevision.com/downloads/shards/) is ook nog een optie, is general purpose, idk hoe hard je een Dashboard in ge-shoeholed wordt met Shards Dashboard, maar zal wel goed zijn
- Nvm toch Tabler, Shards heeft ook een hele backend jakkie

- Pre- and post-processors? Fireship gebruikt bijv. SASS en PostCSS
- Ook Javascript bundler (Webpack?)?
	- Meh, wss toch amper javascript, zeker met HTMX
- [Django compressor](https://django-compressor.readthedocs.io/en/stable/) is wss alles en meer dat dit project nodig heeft

Tabler is een implementatie van Bootstrap schijnt, gezel
### Hoe HTMX te gebruiken
HTMX zal binnen elke Django het fetchen etc. doen. URL structure wordt dan ook chill, gewoon `/app` als maximale lengte. Dat betekent een sub-`base.html` voor elke app en daarin bouwen. 
Mogelijke downsides? Verlies van application state als je een reload doet.

Hmm wacht HTMX kan ook URL rewrite doen, dan gaat het wel gewoon goed met state bewaren?
Is er dan nog meerwaarde om template per ding te hebben? Mss wel leuk voor wat grafische leukigheidjes.

