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

## Frontend (HTMX + TBD)
Een lightweight framework gaat me te veel werk kosten, nty
Dus iets als:
- [Tabler](https://tabler.io/)
- [Black and white](https://www.figma.com/community/file/1201935147948130925)
- [Basic](https://www.figma.com/community/file/1088468250791967662)

- Pre- and post-processors? Fireship gebruikt bijv. SASS en PostCSS
- Ook Javascript bundler (Webpack?)?
	- Meh, wss toch amper javascript
- [Django compressor](https://django-compressor.readthedocs.io/en/stable/) is wss alles en meer dat dit project nodig heeft
