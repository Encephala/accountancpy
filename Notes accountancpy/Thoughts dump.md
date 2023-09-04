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