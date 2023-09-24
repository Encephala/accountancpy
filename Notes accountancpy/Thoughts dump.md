# 2023
## 31 aug
- Begonnen met Django frontend opzetten, want dan volgt DB vanzelf wel?
- Opzich blij met hoe dit werkt
- Wat scaffolding gemaakt om gevoel te krijgen voor Django, maar nog geen content gemaakt
## 2 sept
- Dockerfile afgemaakt, voortan gewoon daarmee werken
- filewatch werkt goed met volume mount dus da's een vibe
- Server zegt telkens empty response though
	- Binnen de container `curl` werkt wel goed
	- Empty response is niet dat het geen verbinding krijgt, dus ports wel goed geforward?
	- Probleem zit hem niet in `ALLOWED_HOSTS`
	- Ah probleem was dat Django bind op `localhost`, moet `0.0.0.0:80` aan het einde van run commando gooien
	- Gotem, fixed
- Moet user auth nog wel fixen, vrij essentieel
	- Ga er maar vanuit dat database access enzo dan gefixt wordt door Django?
- Maar voordat we dat gaan doen: uitvogelen hoe de databases eruit moeten zien
## 4 sept
- `HttpResponseNotFound` gevonden, 404 handler aangepast daarnaar
- Nagedacht over database ontwerp, wel hoofdpijn dit, zie [[Design]]
- Hmm toch wel happy met uitkomst, namelijk KISS
## 11 sept
- Besloten Tabler te gebruiken als Frontend
	- Dat is een implementatie van Bootstrap
- Werkend gekregen met locale static directory
	- Kaolo, VSCode intellisense werkt niet dan. Dan maar wel gewoon remote URLS
	- TODO is er een nette manier om als X niet laadt, Y te proberen in HTML?
	- Scheelt sws hoofdpijn van static serven I guess
		- Kreeg dit niet werkend, uiteindelijk wel zodra `STATICFILES_DIRS` ingesteld was
		- Logisch I guess, `STATIC_URL` is voor de view, `DIRS` is om te zoeken in het filesystem
		- Dacht dat het ook niet werkte toen ik de directory `static` genoemd had, maar goed
- Side navbar of top navbar? Dat is de vraag
- Wordt nog wel hoofdpijn om dit een dynamische UI te maken maar goed, wat `hover`s en animations en het komt vast goed
## 12 sept
- Niet heel goed bijgehouden vandaag
- `ledgers` app gemaakt
	- Is veel logischer als het DB model voor Ledger dan ook daarheen gaat
	- Priem te doen: code overgooien, `makemigrations` (niet vergeten oude code weg te halen) en tot slot elke `ForeignKey` naar `Ledger` overzetten naar een string, á la `"ledgers.Ledger"`. The more you know!
	- Moet helaas dan wel opnieuw de test data in de DB maken, ah well, les voor volgende keer
		- Was sws beter geweest om dit component voor component op te bouwen en dan wijst [[Design#Database]] zich wel
- DB had overal impliciet `blank = True` staan bij kolommen, wat betekent dat de kolom leeg mag zijn. Da's nie bueno.
	- Overal `blank = False`  neergezet, maar vanuit de shell mag ik nog steeds objects maken, dat lijkt niet te kloppen?
	- TODO Hoe zit dit? Begrijp ik niet wat `blank` doet?
		- Hmm default is wel gewoon `False`. Hoezo mocht ik `.save()` doen dan?
		- Okay `blank` slaat alleen op form validation. Ff testen in shell
		- `null = False` slaat op de DB, maar empty string is niet `NULL`
		- Er is geen manier om dit te doen. `blank` fixt validation via `ModelForm`, en daar moet ik maar op vertrouwen, anders eigen logica bouwen
- Een simpele `ListView` gemaakt om wat TestLedgers te laten zien, werkt:
![[Pasted image 20230912232131.png]]
- Voelt verassend hard voor hoe simpel het is, maar die DB models werken gewoon chill
- Steady voortgang na wat haperingen over hoe te beginnen, let's go. Volgende keer:
	- Mooier maken
	- Manier maken om aan te passen
	- Details view maken per Ledger
	- HTMX gebruiken ipv direct hele template te renderen
## 13 sept
- `ledgers` gemaakt met HTMX
- Bootstrap (4 in ieder geval) ondersteunt viewport-dependent sizing niet, dan maar met classic HTML styles `width: x%` en `max-width: ypx` etc. doen
- Alle static content gedownload en door Django laten serven
	- Als ik deployment checklist afgaat fix ik static serven wel
- Door met 404 pagina en `landing` pagina
	- Voelt beetje omslachtig om het te doen, maar voor consistentie I guess
	- Kan wel relevant zijn als straks authenticatie geïmplementeerd is en dan redirect naar landing ofzo

- `details` pagina gaan maken voor `ledgers`
	- Voelt omslachtig om praktisch dezelfde pagina te copy-pasten voor als iemand van buiten `ledgers` app naar geredirect wordt, maar is denk enige manier om het te doen
	- Is fair enough ook qua separation of concerns soort van
	- We gaan het gewoon doen. Alle redirects binnen een app gaan dan met HTMX en alle buiten gaan met page reloads
	- Hmm hoe gaan we URL dan aanpassen telkens met HTMX?
	- En hoe gaan we page-title aanpassen?
		- Oh wacht dat kan letterlijk ook met HTMX, gewoon twee targets
		- https://stackoverflow.com/questions/75617392/multiple-targets-for-htmx
- Gaat opzich goed, behalve dat ik in de default `details.html` een `hx-get` request heb staan om de content te laden, maar deze is dan zonder argument, en die view bestaat niet.
- Oplossing die ik ga proberen: alleen maar details inladen via HTMX, nooit direct naar redirecten?
	- Nee dat kan niet, dan kan je niet meer naar details refereren vanuit een andere app
	- Of ik moet toch ook tussen apps laten redirecten met HTMX
- Poeh ik weet niet hoe ik dit moet doen met HTMX. Dan maar gewoon page reload?
	- Gezien dit, het lijkt er duidelijk niet voor gemaakt, mss toch maar within-page content met HTMX doen maar across-page content met page reloads? Performance boeit toch geen drol
- Maar het moet toch te doen zijn?
- Het is te doen, maar moet gewoon 1 view hebben voor een lege pagina en 1 view voor de content, zoals eerder. Idk waarom ik zo lang vast zat.
	- De URL is nu helaas niet zo mooi als eerst maar hè het moet maar
- Hmm wacht nee nu heb ik nog steeds het probleem van dat de details pagina niet weet welke `Ledger` hij in moet laden
- Nee dit is totaal niet de oplossing.
- Ik ga proberen om in de DetailsView de base template te renderen en dan de content erin te yeeten. Als je dan een andere Ledger opent vanaf daar kan het met HTMX
- Pff HTMX maar losgelaten hiervoor, met Django zelf is het ezpz

- HTMX gebruiken hele `<html>` te vervangen? (^:
- Of alleen `<body>` kan mss ook wel, ff kijken hoe dat gaat met templates
- Beetje jank, maar geeft wel mogelijkheid voor laad animaties etc.

- Hmm ik ben op het punt om HTMX zo min mogelijk te gebruiken en gewoon Django templating all the way
- Wat gekut met git, ben wel wat werk kwijt, maar heb het denk wel in mn hoofd?
- Was wat aankloten maar heb het weer zoals het ongeveer was hype
- HTMX kan dan wel priem gebruikt worden om bijv. ListView te laden van entries op een Ledger
## 23 sept
- Moet `entries` app gaan maken om de regels in te kunnen laden in `ledgers`
- Beetje rondgespeeld met Bootstrap en layouts maken
	- `.column-gap-x` is chill om gelijke spacing tussen kolommen te hebben maar wel nog `.col-x` te kunnen gebruiken voor sizing
	- Oh nee dat doet het helemaal niet?
- Wat gezeik toen ik `Entries` en `EntriesRow` models wilde verplaatsen. `makemigrations` had er geen zin in omdat de eerdere migrations voor `books` refereerden naar de functie `upload_path` die niet meer in de file stond. Heb een dummy functie in die file laten staan en de echte functie verplaatst naar `app/settings.py` zodat het een absolute globale referentie heeft
#### `EntriesRow` view aanmaken
- `content` directory in elke `templates` dir is voor elementen in een pagina, as before
- Proberen om te werken met een generic `EntryRowView` die via het `?...`-deel van de URL een filter query gepasst krijgt, maar dat kan niet; je kan dat nooit weer omzetten in code, kan alleen values passen
- Geaccepteerd dat het een view wordt voor elke mogelijke filter, dus nu `EntryRowByLedger` aangemaakt
- Werkt direct, welloe hoofdpijn. KISS?
- Interessant puntje, na for-loop over alle entries op een ledger, hoe bereken je het totaal? 🤔
	- Dat gaat in de Python code, niet in het template
	- Moet gewoon `aggregate` callen op een `QuerySet` 
- Was table heading en table footer aan het bouwen in de `content/entry_row_view.html`, da is niet helemaal hoe het hoort
- Heading en footer terug naar `ledgers` pagina, daar kan ook totaal van ledger opgevraagd worden
- Volledige copy-paste van deze view gemaakt maar dan voor by-entry, dat kan vast beter maar idk KISS joe
## 24 sept
#### Entry details en list
- Gevoel gekregen voor wat logische namen zijn voor templates/views etc, goed teken dat ik web dev/MVC begin te begrijpen
- Pretty much weer copy-paste van view voor `EntryRow` gemaakt voor list van `Entry`, maar niet te DRY want de kolommen en namen daarvan zijn elke keer anders
	- I guess dat ook die kolom-namen technisch gezien template kunnen worden? maar KISS
- Wilde `num_rows` van een entry laten zien in de `EntryList`, daar wat gedoe mee gehad
	- Moet in `get_context_data` de `QuerySet` annotaten en dan de geannotate set in de context plakken
	- In `context` zit `object_list`, maar dat is niet degene die je wil hebben. Je moet `class_list` hebben, in dit geval `context["entry_list"]`
	- Laatste oepsie is dat ik `Count("id")` nam als aantal rows, maar dat is incorrect; er is altijd maar 1 `id` in een `Entry`,  het moest zijn `Count("entryrow")` (lowercase van type van \_set)
- [ ] Ook in `EntryDetails` wordt de ID van elke `EntryRow` erbij gezet, dat is beetje onnodig. Idk of ik dit ga fixen, mss in een refactor later
#### `Accounts` app
- Ken het trucje inmiddels, `startapp` en dan models overzetten van `books`, basic views en urlpatterns maken, toevoegen aan apps in settings
- Interessante, urls resolven in volgorde van de lijst, dus als de url "list/" en "<account_id>/" allebei hebt, moet je de "list/" eerst zetten, anders resolvet list als een account en zegt hij dat gegeven `account_id` niet bestaat
	- URLs met parameters onderaan de lijst zetten
- Had wat dingen verneukt in de `entries` app, hardcoded entry ID en ergens `ListView` waar het `DetailsView` moest zijn
	- Jeetje wat zouden tests handig zijn (^:
	- Ben eigenlijk ook wel beetje voor het idee van test-driven development
- `DetailsView` van `Account` wordt nog wel fun om te maken, let's go
	- Context aantal regels op Account
- `Account` toegevoegd als `ForeignKey` van `EntryRow`, mag leeg zijn
	- Django heeft best chill systeem om dit te fixen, nice
	- Wacht dit mag helemaal niet fout gaan, foreignkey zou blank moeten mogen zijn
	- Fixed, `blank = True` staat nog niet `null` toe in de DB, `null = True` was nodig
- Had foutje gemaakt met copy-pasten, deed `get_list_or_404` met `entry = self.kwargs["account_id"]` :^)
#### `Journal` app
- Laatste app, daarna CRUD voor alle apps en afletteren gaan fixen
- Zelfde trucje, model verplaatsen en URL en view en details en list en navbar en app toevoegen aan settings
- Hmm enige complicatie: `EntryRow` hebben geen Journal ForeignKey, dat zijn de `Entry` zelf
	- Zal niet moeilijk te fixen zijn
	- Yup, was gewoon `journal = self.kwargs["journal_id"]` vervangen door `entry__journal...` ([documentatie](https://docs.djangoproject.com/en/4.2/intro/tutorial02/))
	- Hmm dan is het eigenlijk ook logischer om lijst van `Entry` te hebben staan ipv `EntryRow`
- 