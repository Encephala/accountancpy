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
	- Laatste oepsie is dat ik `Count("id")` nam als aantal rows, maar dat is incorrect; er is altijd maar 1 `id` in een `Entry`,  het moest zijn `Count("entryrow")` (lowercase van type in `..._set`)
- [ ] Ook in `EntryDetails` wordt de ID van elke `EntryRow` erbij gezet, dat is beetje onnodig. Idk of ik dit ga fixen, mss in een refactor later
	- Kaolo fixbaar door een binary parameter toe te voegen aan template
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
- Dat gedaan
- Nu werkt filteren op `Journal` niet goed, wack
	- Ik had ook geen eigen `get_queryset` gedefiniëerd, afgeleid door `get_context_data` die gedefiniëerd was
	- Dat nu wel gedaan, maar nu returnt het niks. Gaat vast ergens iets mis met namen van variabelen
	- Ah, er kwam een error in de console. Omdat ik `get_queryset` override en een `list` return, is het geen `QuerySet` meer
	- Weggedaan met `get_list_or_404` en `super().get_queryset().filter()` gebruikt, werkt
	- Ik typte dat het zou werken voordat ik het getest had maar hè, het moest wel :)
#### `Books` app weg
- Eindelijk, party
- Was nog 1 referentie naar `books.journal` in een migration, heb die handmatig aangepast naar `journals.journal`, dat maakt vast niks stuk (^:
	- `makemigrations` heb er geen problemen mee, maar dat is logisch
	- ook `migrate` gaat priem, jeetje
	- Oh, de correcte manier om dit te doen was [`squashmigrations`](https://docs.djangoproject.com/en/4.2/topics/migrations/#migration-squashing), naja fixed
	- Er was ook nog een referentie in dependencies, ook handmatig aangepast om naar `journals` te verwijzen ipv naar `books`
- All good!


Al met al lekker daggie, volgende keer op naar CRUD en dan moet ik echt tests gaan doen.
Eigenlijk wel echt beter om eerst tests te doen hè, dan kan ik ook test-driven development doen voor CRUD.
## 25 sept
Vandaag gaan we tests maken
- Eerst nog wat aangekloot met kleine changes aan `Dockerfile` (all warnings aanzetten in entrypoint), kwam erachter dat interactie tussen drive client en `git rebase` niet optimaal is, rebase pauseert telkens, maar gewoon `--continue` spammen lost het op
- Ah ff geleerd tussendoor: ipv mijn gedoe met context om uit te rekenen hoeveel rows er in een entry zitten, had ik ook een method kunnen definiëren op het model
- Geen triviale tests maken, dus niet testen dat een gemaakt object ook echt bestaat ofzo
- Matig, je moet specificeren welke apps je wil testen als je `test` runt, want het zoekt niet automatisch je tests af.
- Test dat een gemaakte Ledger op de pagina staat:
	- Werkt niet want HTMX wordt niet gerenderd, tof
	- Dan maar gewoon die pagina testen op iets statisch
	- Turns out dat Django test `assertContains` case-sensitive is
- Test voor `QuerySetEquals` voelt ook beetje overkill, maar goed
- Omdat `django.urls.reverse` resolvet met een url argument in de text, moet in die call ook args gepasst worden. In de `get` call kan je alleen `GET`-data als `?foo=bar` gooien
- Enig tests, voor `Ledger` gemaakt in veel tijd. Nu snel rest knallen?
- Ook tussendoor even ordering toegevoegd aan alle QuerySets, want `QuerySetEquals` wordt autistisch als je een list (met impliciete ordering) vergelijkt met een QuerySet die geen impliciete/expliciete ordering heeft
	- `ordering = id` toegevoegd aan de view maar het lijkt nog steeds niet te werken, wack
	- `ordering = False` it is in `AssertQuerySetEqual`
- Wack, `Entry*` heeft als enige `pk` als primary key in plaats van `id`, bruh
	- Huh maar als ik instantieer met args ipv kwargs geeft het "expected number for id", heet het intern in Django impliciet id?
	- Ohhh, `id` is de default name voor primary key, maar `pk` is altijd een referentie naar deze primary key, ook als je zelf een andere PK instelt
- Wack, om `Entry` te instantiëren moet er een journal zijn maar dan moet je Journal importeren en dat moet via `from journals.model`, want `..` mag niet
- Maar hey omdat ik bij `Entry` niet de QuerySet slice is zn ordering we bewaard gebleven? `ordered = False` is iig niet nodig
- Hey handige, zo'n domme `Journal` die moet bestaan om entries te maken kan gemaakt worden in `__init__`
	- Oh nee niet `__init__`,  die gebruikt unittest specifiek. Blijkbaar heb unittest hiervoor de method `setUp`
	- Chill, joe
- Gedoe met testen dat `EntryRowByLedger` goed werkt, want "entry_row_list" zit telkens niet in de context
	- [Lijkt erop](https://forum.djangoproject.com/t/testing-class-based-views-with-custom-context-object-name/23628) dat Django niet zo lekker gaat context_object_name aanpassen
	- Wil hij dan gewoon dat ik `context["object_list"]` query? Doen ze ook niet in [het voorbeeld]()
	- Nee, `"object_list"` lost het niet op
	- `print(response.context)` helpt ook niet, daar staat helemaal niks met `*_list` in :/
	- Bruh like mn templates werken gewoon met `entry_row_list`, waarom de test niet?
	- Hmm had geen `status_code = 200`-check, mss vangt dat het af?
	- Ah yep ik kreeg telkens 404. Why?
	- Tsja, ik maak het hem ook niet makkelijk als ik wil testen of er een entry op een journal staat, maar ik schrijf code alsof ik wil testen of er een entryrow op een ledger staat
	- Gecorrigeerd, alleen nog `entry_row_list` aanpassen naar `entry_list`, en fixed (:

## 3 oct
Vandaag is CRUD, leggo
`Journal`/`Ledger` zijn root van relational data, dus ik pak mn OG, `Ledger`
- https://docs.djangoproject.com/en/4.2/topics/db/queries/
- `__str__`-methods toegevoegd aan models, goed om keer gedaan te hebben en voortaan te doen
- Dat was veel lezen over database models, wel genoeg van opgepikt, maar brein is ook beetje gefrituurd van vandaag + lezen dus uhhhh tsja idk wat is blijven hangen
	- Snap beter hoe `QuerySet` werken, die zijn wel cool
- Geen voorbeelden van views, dus nu moet ik nog gaan lezen over de generic views voor CUD (R is `ListView` en `DetailView`)
	- https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/
	- fun, here goes frituurd brein part 2
- Actually, should probably self-implement it first and then go with the class views-approach?
	- Eh can I be fucked? probably not idkkk
	- okay sure
- Big advantage of using built-in `CreateView` is that it probably automatically creates appropriate entry fields? Hopefully?
- Ah, an HTML form uses GET by default, let's set that to POST
- Also why doesn't my submit button align properly idk it just wants to be full width
	- Let's try wrapping it in a container, probs the btn class?
	- Nah, now it just has a button in a div that stretches full width
	- `.w-25` works now but `.float-end` still no bueno, ah but `.ms-auto` is bueno
	- `.float-end` probs does nothing if not in a float
	- neat `.w-10` does work, idk why I thought it didn't
	- Ah hmm the `.card-body` in the `.card` made it go wide
	- But without `.card-body` it doesn't get the proper height
	- Probs just need to actually separate `.card` and `.card-body` :^)
	- Yo that was it pog, now it behaves as I'd expect
	- Maybe `.column-gap-x` also works if I don't do this the wrong way
- Motherfuck why is it still a GET it literally says POST in the rendered HTML
	- Is Chrome being a caching cunt?
	- Probably, now I'm getting CSRF error, thanks Django
- Yo the Django extension for vscode is pretty okhand, it has like syntax highlighting and auto complete, that's like all you need in an IDE????
	- It is somewhat aggressive with autocomplete though idk
	- Also does it do all HTML always everywhere now? may be annoying but okhand for now
	- Never mind it breaks the HTML autocomplete which is just much more functional so uhh yeah bye
- Well that wasn't so hard
- Should also do validation, but before we get into that, let's go straight into the `CreateView`
- Didn't get the form to render, didn't realize `CreateView` is meant to load the page as well
	- Does it also do the creating of the object? 🤔
	- It sure does, poggies
- Have to use `reverse_lazy` if `reverse` is needed in a `views.py`, as those get imported by `urls.py` but `reverse` imports `urls.py` so import loop
- Getting some jank rendering:
![[Pasted image 20231004001138.png]]
- Honestly not sure why this happens, have spit it so every div is only one class
	- It still happens with notes field removed
	- Django only renders the input, nothing else, so that's not jank either
	- Real weird tbh
	- I don't get this whole html/css stuff yet yike
	- It's not because of the `<form>` either
	- It's not because of the form components either
	- Okay alignment was different if you do it right, so for consistent alignment have to do it wrong xd
	- Here "it" means usind `.card .card-body` on the same div
- In order to specify number of rows, have to create a custom Form class
	- https://stackoverflow.com/questions/6536373/how-can-i-set-the-size-of-rows-columns-in-textfield-in-django-models
	- https://www.valentinog.com/blog/django-widgets/
- Enough for today, next time is cleaning up the UI here, adding (cr)UD, and adding buttons for CUD (where do these go in UI?)

## 15 oct
- Default form styling can be adjusted only by making a custom form in Django
- [This StackOverflow answer](https://stackoverflow.com/a/64317285/5410751) seems like a nice concise way to get what I want
	- I specified the class property `form` rather than `form_class`, so it didn't work, but now it does
- Just adding class `.form-control` is enough styling for now tbh
- `UpdateView` is hopelijk gewoon copy paste van `CreateView` met zelfde template, zelfde form maar andere logica?
	- Krijg error `Generic detail view LedgerUpdate must be called with either an object pk or a slug in the URLconf.`
	- Nope, small difference: I used `ledger_id` in the URL as variable, so had to define a custom `get_object` as I did with the `DetailView`
	- Bit unnecessary, adjusted it to use `pk` in this app and all others
- Not entirely sure if I like the logic of using `is_update` in the view, seems error-prone, but ah well I guess?
	- Have to adjust page title, form button text and form action URL

- Updated 404 page to be explain that may have failed to add trailing `/`, added button to add it

- Finally a `DeleteView`
- `DeleteView` borrows from `DetailView` in lot of ways, perhaps some HTMX magic would be nice there to prevent repetition
- Created a template that shows a Ledger's attributes and allows a user to delete if a confirm box is checked

Next time: adding buttons to link to create/update/delete pages, adding number of rows on ledger to delete page, adding CRUD to other models

## 16 oct
`Journal` CRUD:
- Add create view by pretty much copy pasting
- Hmm, pushing the create button creates a Post request but doesn't return to the right page, nor does it create the journal?
	- Status 200 with 4 kB transferred, should be 302 for the redirect?
- Apparently I should be rendering form error messages but I'm not
	- https://docs.djangoproject.com/en/4.2/topics/forms/#rendering-form-error-messages
- Nah that wasn't it. Apparently I wasn't rendering the `id` form field so it was an invalid submission
	- Weird though, I'd expect Django to shit out an error then? But it didn't when I added `non_field_errors`
- [ ] Do need to render `non_field_errors` on all forms though
- Well, now my newly created journal gets entries rendered on it by default, that doesn't seem right
	- It's rendering entries, so it's going wrong in `entries:journal_rows`
	- I needed to define custom `get_queryset` for this view, fixed
	- Fixed this for all `EntryRow` views as well
- [ ] There's no way to see on an `EntryRow` what `Account` the row is tied to
	- Stupid
- [x] Also I should update URLs so they're like `journals/<pk>/delete/` etc, that makes more sense
- Quickly added update- and delete view, went smoothly

Neato, `Journal` CRUD done

Same trick for `Entry` and `EntryRow`
- Just realised you can edit the primary key in the update views so far, that's not what we want I guess
- I guess changing an `Entry`'s journal is fine?
- Difference here is that I want to edit the `EntryRow` edits on the page of the `Entry` edit, this'll be fun
	- No like unironically
	- Same thing for creating an `Entry`
	- Oof, creating is gonna require an auto-expanding form that adds extra rows
- Not sure if `create_update.html` is worthwhile here, might want to split it out
- Oof, this is gonna take some thinking to get right
- How do I properly render an `EntryRow` form? Can make it do multiple calls to the HTMX endpoint, that works I guess
- But then I have to add custom JS to submit all of them with a single button, that's kinda wack
- Definitely not gonna do it manually without Django though, all the validation etc. seems a hell
- First time rendering the page, only the `Journal` input gets rendered right, yike:
![[Pasted image 20231016224219.png]]
- Ah, had `form.name` instead of `.notes`, fixed that part
- And had `model = Entry` instead of `EntryRow`, that fixed the other part
- God Django's included batteries make life easier
- Now all that remains is making style less shit, having the create button work (xd), and automatically adding rows
- The last one seems most fun, let's go
- Had a medium struggle with it
	- The event to listen to is `input`, I was using `changed`, but that's just a modifier
	- Otherwise everything is intuitive
	- Had to pass the URL parameter `index` to the context explicitly
- Got it to work, neat
- Now adding a delete button to each row
	- Hmm that should re-enable the HTMX trigger, because otherwise you can never add a row again
	- Can either
		- Add a button to Add, or
		- Create a hidden element somewhere on the page to keep track and instead of trigger once, trigger if last row :^)
		- Do the latter but with Javascript to store a value
- Submit button needs to only submit non-empty rows and fail if any row fails, that's probably headache material
- `hx-on` is a much cleaner solution to deleting the row than `hx-get` to an empty response


## 17 oct
- If I submit all forms with the same button, it creates a race condition for creating the rows on the entry
- Best way is to trigger creating all rows when server responds with 200 for creating entry?
- Let's think how you'd do that
- Respond with hidden element which has HTMX to trigger them?
- That doesn't sound bad, let's go
- Hmm but then that doesn't trigger form validation for `EntryRow`s though
- Added `form`-tags for each individual entryrow, but didn't update `hx-target` for new entryrows so there were some logic errors there.

- Alternative solution is to use some JS and queue for send when pressing the button, then only send entry if all validation passed
	- Don't like that though, I feel like checking form validity isn't gonna be easy js? but I guess it should be idk

- Replaced djanky empty HTMX-endpoint to delete row with a script tag and an `onclick` event
- Still wondering how to do form validation here properly though

- Okay here's my take:
	- Customise behaviour of the `EntryCreate` view
	- While processing the view, probably in `Form.clean`, get all `EntryRow`, by sending a response to the client with an `HX-Trigger` header. If all `EntryRow` are valid and their sum is zero, save all of them and return the success url
- Yeah, that should work! Bit of work and bit of learning about Django but neato burrito

- With all the amending/force pushing I've been doing, I should really start working with branches
- Makes me learn git better anyways

- And I think I've finally stumbled onto some code that I really want to test, namely that validation properly catches all the invalid scenario's :)
## 18 oct
#### Making the `EntryRow` delete/add logic correct
- Yo easy solution to my problem of creating new one, pretty sure there's a CSS selector for last element?
- Okay yeah so that works, neat
- Now I moved the HTMX out of the `EntryRow` form and into the main page
- However, only issue that remains is that for the sake of the delete button, I need the index of the entry to delete it
- Sadly, javascript doesn't natively support something like nearest form
- Well, don't make it more difficult than it has to, I'm sure HTMX programmed the `once` tag well
- Well, it does, but `:last-child` doesn't seem to update?
- It does, but I guess this isn't how HTMX works
- Ah, because `once` is coded properly, it won't fire a second time. That almost entirely makes sense
- Fuck
- Hmm, jank solution is to have the delete button readd the HTMX trigger
- Not even that jank? Just looks ugly in the code
- Wait now it's firing multiple times? wat
- Is it time for a fuck-it moment and create an HTMX endpoint which returns this trigger element and is triggered upon clicking the button?
- Yeah sure why not
- No we're not doing that
- Why not? Because the `div` contains a URL and the variable `index`, both of which have to be properly templated, which idk how to and can't be fucked to figure out, there has to be a cleaner solution
- Significantly cleaned up the selector for the creation, can just listen on `form` `changed` event
- Have just been struggling to reset this trigger, wack
- Hmm can I just use JS `element.replaceWith(element)`?
	- Nah that doesn't seem to work, the HTMX event doesn't get reset
- Yo I can add the element to the entryrow_create and do an out-of-band swap? `hx-swap-oob`
- Wait no I have to reset the trigger on deleting, wack
- So looks like I either have to give up on auto-add, or accept that I need to have an add button for this case, or copy Exact and have new line created on pressing tab(?), or on delete trigger a request that replaces this element
- YO [`htmx.process()`](https://htmx.org/api/#process) may well be just what I'm looking for???!?!??!?!?!
	- Nope
- Dude why is this so hard
- Hmm, HTMX has a `handledFor` array which keeps track of elements for which the event has already triggered, maybe I can just reset that array?
- Meh, am not able to find that array in the code. It's part of the event, but all events I can find are plain javascript events rather than HTMX ones (well except for `htmx:load` on  the `body` but that doesn't help me)
- Insight: this logic isn't great either anwyays. Why would I want to edit a row that I just finished to create a new one?
- Am gonna just add a button and implement Exact's tab logic
- Hmm how does that work 