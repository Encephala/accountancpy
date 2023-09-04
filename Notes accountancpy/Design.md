## Database
File, hoeft geen directory voor I guess.
Tables voor:
- [x] Categorieën (GBK)
	- id UNIQUE, naam, soort, notities
	- GBK soorten zijn inkomsten/uitgaven/bank/activa etc.
		- W&V of Balans is geïmpliceerd door GBK soort
- [x] Relaties
- [ ] Bankrekeningen?
- [ ] Boekingen
	- ID (auto is priem), notitie
	- Één grote tabel of tabel per GBK of tabel per jaar ofzo?
		- Kan opsplitsen per jaar (~5 tables)
		- Kan opsplitsen per GBK (~20 tables)
		- Kan één grote hoop maken
		- Boekingen worden één grote hoop, boekingsregels losse grote hoop
	- [ ] Boekingsoorten (Dagboeken)
	- [ ] Boekingsregels (1 grote hoop)
		- boeking FOREIGN
		- datum
		- GBK
		- document nullable
		- bedrag
			- +/- of debet/credit?
			- liefst een instelling I guess maar in begin uitgaan van +/-
## Backend (Django)

## Frontend (TBD)

