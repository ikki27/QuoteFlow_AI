# Pregled prevzetega projekta

Pregled je narejen na stanju `main` ob prevzemu (commit `7574664`). Pregledal sem dokumentacijo (`docs/01–06`, ADR-0001–0013, razvojne zapise v `docs/razvoj/`), kodo backenda, frontenda in migracij ter aplikacijo zagnal lokalno.

## Lokalni zagon in testi

| Preverjanje | Rezultat |
|---|---|
| Backend `pytest` | 1417 uspešnih, 603 preskočenih (testi baze potrebujejo lokalni Supabase prek `TEST_DATABASE_URL`) |
| Frontend `npm test` (Vitest) | 234/234 uspešnih |
| Frontend `npm run build` | uspešno |
| Frontend `npm run test:e2e` (Playwright, API nadomeščen) | 495 uspešnih, 2 preskočena, 1 neuspešen |
| Zagon (`uvicorn` + `npm run dev`) | `/api/health` vrne 200, frontend na `localhost:5173` deluje, `/api/ready` brez baze vrne 503 (pričakovano) |

Neuspešen e2e test je `brez prefers-reduced-motion panel drsi (kontrolni test)` na mobilni širini: pričakuje animacijo `drawer-in`, po zadnji prenovi dizajna pa ima panel na telefonu animacijo `sheet-in`. Test ni bil posodobljen ob spremembi dizajna, delovanje aplikacije pa je pravilno.

Za polni potek (prijava, podatki) sta potrebna ključ in povezava do Supabase oziroma lokalni Supabase (`supabase start`, `supabase db reset`), ki ju v repozitoriju ni (`.env` je izključen iz Gita).

## Implementirane funkcionalnosti MVP

Obseg MVP so F1–F7 (`docs/02`). Vse so implementirane v bazi (migracije in funkcije v `quoteflow_private`), API-ju (`backend/app/routers/`) in vmesniku (`frontend/src/features/`).

| ID | Funkcionalnost | Stanje | Kje |
|---|---|---|---|
| F1 | Registracija, prijava, vloge, prošnja mojstra in odobritev | Implementirano | `identity`, `prosnje`, `admin`; `features/identity`, `features/administration` |
| F2 | Vrste dela, cenik, materiali, zaloga po lokacijah | Implementirano | `vrste_dela`, `cenik`, `materiali`; `features/supplier` |
| F3 | Projekt za stranko, faza pregled in ogled | Implementirano | `projekti`; `features/projects` |
| F4 | Postavke z izmerami, izračun (formula A), posnetek ob pošiljanju | Implementirano | `postavke`, `ponudbe`, `pricing.py`; `features/items`, `features/quotes` |
| F5 | Pošiljanje ponudbe, sprejem ali zavrnitev, različice | Implementirano | `ponudbe`; `CustomerQuote` |
| F6 | Termin in zaključek izvedbe | Implementirano | `projekti` (`termin`, `izvedba`); `ProjectProgress` |
| F7 | Osnutek računa ob sprejemu, izdaja, evidenca plačila | Implementirano | `racuni`; `features/invoices` |

Poleg MVP je implementirana še F8 (povabila delavcev in skrbniški pregled vlog). Ekipe (F9–F10), PDF, e-pošta in AI (F16–F20) niso implementirani, kar se ujema z dokumentacijo.

## Ali funkcionalnosti zadoščajo uporabniškim zgodbam

V `docs/05` so trenutno zapisane zgodbe US-01–US-04 in US-08. Zgodbe US-05–US-07 so bile v commitu `bb6f65f` po pomoti odstranjene iz dokumenta (njihova implementacija in razvojni zapis `docs/razvoj/us-04-us-07-ponudbe-in-racuni.md` obstajata). Zato sem pregledal pet zgodb, ki so v dokumentu.

| Zgodba | Zadošča | Ugotovitev |
|---|---|---|
| US-01 Identiteta, pravice in prošnja mojstra | Da | Vloga `stranka` po potrditvi e-pošte, vsak zahtevek preveri žeton in aktivno sejo (`auth.py`, `access.py`). Odobritev prošnje v eni transakciji ustvari podjetje, lastništvo in vlogo mojstra. Lastniku ni mogoče odvzeti vloge mojstra, admin si ne more sam dodeliti vloge v podjetju (`QFP22`). |
| US-02 Cenik, vrste dela in materiali | Da | Cena dela je izpeljana iz urne postavke, ur in delavcev. Meje (500 vrst dela, 50 materialov, enote `m`, `m2`, `m3`, `kos`) preverjata Pydantic in SQL. Zaloga je ločena od postavk. Izolacija podjetij je pokrita s testi (`test_varnost_*`, `supabase/tests/tenant_isolation.sql`). |
| US-03 Začetek projekta | Da | Projekt začne v fazi `pregled`, ogled je neobvezen, faze `ponudba` ni mogoče nastaviti ročno. Stranka vidi samo svoje projekte, tuj projekt vrne 404. |
| US-04 Priprava ponudbe | Da | Izmere seštevajo in odštevajo, izračun je v SQL. Primer iz meril sprejema (540,00 / 118,80 / 658,80 €) je pokrit s testi. Ob pošiljanju nastane nespremenljiv posnetek postavk, izmer, materialov in dela. Stranka ne vidi osnutkov, urne postavke, ur, delavcev ali materialov. |
| US-08 Delavci podjetja | Da | Povabilo poteče po 14 dneh, odgovor ne razkrije obstoja računa, vloga `delavec` nastane šele ob sprejemu. Odvzem in ponovna aktivacija ohranita zgodovino. Admin ima pogled »Podjetja in pravice«. |

Implementacija pokriva vseh pet zgodb. Tudi odstranjene US-05–US-07 so implementirane in pokrite s testom celotnega poteka `frontend/e2e/acceptance.spec.ts`.

## Opažene pomanjkljivosti

- V `docs/05` manjkajo zgodbe US-05–US-07, čeprav jih dokument v uvodu omenja kot MVP.
- E2E test animacije panela na mobilni širini ni usklajen z novim dizajnom (glej zgoraj).
- `docs/04` še omenja 17 tabel, model ima po migracijah v3 22 tabel.
- Testi baze (603) se brez lokalnega Supabase preskočijo, zato je za polno preverjanje potreben Supabase CLI.
