# GuardianEye: Edge-AI Privacy Pipeline

GuardianEye is een gesimuleerde, gecontaineriseerde Edge-AI pijplijn voor aardobservatiesatellieten. Het systeem implementeert Privacy by Design op de boordcomputer (Edge-Computing). Militaire doelen worden gedetecteerd (via YOLO-OBB), terwijl civiele objecten wiskundig en onomkeerbaar worden geanonimiseerd (91x91 Gaussian Filter) vóór de downlink naar de aarde.

## 1. Systeemvereisten

* **Docker Desktop** (of een actieve Docker daemon met Docker Compose).

* **DOTA Test Dataset**.

## 2. Installatie & Setup

Dit project maakt gebruik van dynamische Docker volume mounts om lokale bestanden direct in de container te lezen en te schrijven.

### Clone de repository

```bash
git clone <https://github.com/ColinPlug/GuardianEye>
cd GuardianEye
```

Voeg de gedownloade DOTA-beelden toe aan de actieve productiemap:
*data/satellietbeelden/*

(Let op: De map *data/satellietbeelden_test/* bevat reeds een vooraf geannoteerde 'Ground Truth Test Set' van 50 beelden, inclusief ground_truth.json voor directe academische evaluatie).

## 3. Starten van de Pipeline

Het systeem wordt bestuurd via een interface. Start de architectuur op met één commando in de terminal (vanuit de root van het project):

```bash
docker-compose run --rm GuardianEye
```

(Tip: Voeg de *--build* flag toe als je het project voor de allereerste keer opstart of na wijzigingen in de requirements.txt)

## 4. Module Overzicht (C2 Menu)

Vanuit het terminal-menu heb je toegang tot de volgende modules:

1. Main Pipeline: Analyseert de ruwe satellietbeelden, scheidt militaire van civiele doelen, voert de anonimisatie uit en genereert een S-Band metadata payload.

2. Evaluation: Berekent academische metrics (Precision, Recall, F1, MAE) over de Ground Truth Test Set en vergelijkt dense versus baseline scenario's.

3. Generate Visualizations: Maakt latency-taartdiagrammen en prestatie-scatterplots op basis van de testresultaten (opgeslagen in */visuals/*).

4. Interception: Een cybersecurity-test. Voert Unsharp Masking en AI-heridentificatie uit op het geblurde signaal om de robuustheid van het privacy-filter te valideren.

5. Dataset Utiliteiten: Tools om handmatig nieuwe test datasets te genereren en de bijbehorende JSON te sorteren.

## 5. Project Layout

* */src/*: Core Python modules voor detectie en anonimisatie.

* */evaluation/*: Academische evaluatie- en hackerscripts.

* */data/*: Hub voor input- en outputbeelden.

* */visuals/*: Automatisch gegenereerde grafieken.
