# RiascloudAPI
[README.md](README.md)

# API

Cette API vous permet de récupérer les informations météo d'une ville.

## Endpoints

### Récupérer les informations météo par nom de ville

Endpoint : `/weather/<city_name>`

- `ville` : Le nom de la ville pour laquelle vous souhaitez obtenir les informations météo.

Exemple de requête : GET `/weather/paris`

## Paramètres de réponse

Les réponses de l'API sont au format JSON et contiennent les informations suivantes :

- `City` : Le nom de la ville.
- `Temp_celsius` : La température actuelle en degrés Celsius.
- `Feels_like_celsius` : La température ressentie en degrés Celsius.
- `Wind_speed`: La vitesse du vent en m/s.
- `Humidity` : Le taux d'humidité en pourcentage.
- `description` : Une description textuelle de l'état du temps (ensoleillé, nuageux, pluvieux, etc.).

Exemple de réponse :

```json
{
  "City": "Paris",
  "Temp_celsius": 25.2200000000 ,
  "Feels_like_celsius": 24.7500000000,
  "Wind_speed": 6.17,
  "Humidity": 36,
    "description": "clear sky"
}
