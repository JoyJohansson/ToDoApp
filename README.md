# ToDoApp
Python and Flask
# Inlämningsuppgift
Er uppgift är att skapa en "To-do App" med hjälp av Python och Flask.

Uppgiften utförs med fördel i par. Gemensam betygsättning sker såvida inte något framkommer under projektets gång.

Inlämningen sker via LearnPoint senast den 9 november 23.59

## Backend
Du ska göra ett API i Flask som läser data från filen `tasks.json` och modifierar denna vid vissa requests.

### Endpoints

`GET /tasks` Hämtar alla tasks. För VG: lägg till en parameter `completed` som kan filtrera på färdiga eller ofärdiga tasks. (Joy)

`POST /tasks` Lägger till en ny task. Tasken är ofärdig när den först läggs till. (Joy)

`GET /tasks/{task_id}` Hämtar en task med ett specifikt id. (Joy)

`DELETE /tasks/{task_id}` Tar bort en task med ett specifikt id. (Joy)

`PUT /tasks/{task_id}` Uppdaterar en task med ett specifikt id. (Johanna)

`PUT /tasks/{task_id}/complete` Markerar en task som färdig. (Johanna)

`GET /tasks/categories/` Hämtar alla olika kategorier. (Johanna)

`GET /tasks/categories/{category_name}` Hämtar alla tasks från en specifik kategori. (Johanna)

## Frontend
Du ska göra en frontend med hjälp av en template i Flask. Från den här frontenden ska man kunna se alla tasks. För VG ska det också finnas ett formulär där man kan lägga till en ny task. Frontenden läggs med fördel i roten ("/").

## Betygskrav

### För godkänt
- Frontenden visar alla tasks. (Joy)
- Alla endpoints är implementerade. (1-4 Joy och 5-9 Johanna)


### För väl godkänt
- Alla implementerade endpoints ger användarvänliga svar ifall man förser dem med felaktig information. Om du exempelvis använder `POST /tasks` och skickar med en task i fel format får du ett felmeddelande med hjälpsam text. En task i ett felaktigt format läggs då inte heller till. (Joy)
- Alla endpoints har relevanta enhetstest. (Johanna)
- Testningen modifierar inte filen `tasks.json`(Johanna)
- `DELETE /tasks/{task_id}` kräver auktorisering via förslagsvis en token. (Joy)
- Man kan lägga till en ny task via Frontenden. (Joy)
