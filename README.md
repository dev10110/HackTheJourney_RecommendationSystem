# HackTheJourney_RecommendationSystem
 
###Get inital cards with:  
This endpoint returned a random set of POI's

`http://3.84.54.231:8080/getPOI`  
Parameters:   
`limit <Integer>: limit amount of returned points, defaults to 10`

Returns JSON Array containing points:  
```
[
  {
    "data": {
      "category": "SIGHTS",
      "city": "VCE",
      "geoCode": {
        "latitude": 45.43833,
        "longitude": 12.336388
      },
      "name": "Fondaco dei Tedeschi",
      "subType": "POINT_OF_INTEREST",
      "tags": [
        "sightseeing",
        "restaurant",
        "sights",
        "historicplace",
        "historic"
      ],
      "type": "location"
    },
    "id": 269
  }, ...]
 ```
 
 ###Get IATA code for city:   
 This endpoint translates city name into iata code
 
 `http://3.84.54.231:8080/getIATA`  
 Parameters  
 `city <String>: city to get IATA code for`
 
  ###Get City name for IATA code:   
  This endpoint translates iata code into city name
  
 `http://3.84.54.231:8080/getCITY`  
 Parameters  
 `iata <String>: IATA code to get city name for`
 
 ###Get Recommendations with:  
 This endpoint returns recommended POI's based on given liked POI's.
 
 `http://3.84.54.231:8080/getRecommendations`  
 Paramters:  
 ```
likes List<Integer>: List of liked POI id's 
limit <Integer>: Limits amount of recommendations, defaults to 10
```

Returns JSON Array:  
```
[
  {
    "category": "SIGHTS",
    "city": "paris",
    "geoCode": {
      "latitude": 48.84844,
      "longitude": 2.334057
    },
    "name": "Mus\u00e9e du Luxembourg",
    "score": 0.8309330940246582,
    "subType": "POINT_OF_INTEREST",
    "tags": [
      "sightseeing",
      "museum",
      "sights"
    ],
    "type": "location"
  }, ...
]
```
 
 ###Generate Inspirations with:  
 This endpoint generates Inspirations with different cities and POI's based on liked POI's
 
 `http://3.84.54.231:8080/generateInspiration`

Parameters  
```
likes List<Integer>: List containing id value of liked POIs
origin <String>: 3 Letter IATA city code of origin city, defaults to LON
budget <Integer>: Size of budget, defaults to unlimited
currency <String>: currency of budget, defaults to GBP
limit_inspirations <Integer>: Sets limit for returned inspirations to travel to, defaults to 10
limit_activities <Integer>: Sets limit for returned activities, defaults to 10
startdate <String>: Date in format YYYY-MM-DD, defaults to toda, can't be more then 180 days in future
```

Returns JSON Array containing Inspirations with recommended activities:  
```
[
  {
    "activities": [
      {
        "category": "RESTAURANT",
        "city": "NTE",
        "geoCode": {
          "latitude": 47.20602,
          "longitude": -1.564156
        },
        "name": "Les Machines de L'ile",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "sightseeing",
          "restaurant",
          "activities",
          "sights"
        ],
        "type": "location"
      },
      {
        "category": "SIGHTS",
        "city": "NTE",
        "geoCode": {
          "latitude": 47.219414,
          "longitude": -1.547152
        },
        "name": "Mus\u00e9e des Beaux Arts de Nantes",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "restaurant",
          "artgallerie",
          "museum"
        ],
        "type": "location"
      },
      {
        "category": "SIGHTS",
        "city": "NTE",
        "geoCode": {
          "latitude": 47.218346,
          "longitude": -1.550154
        },
        "name": "Cath\u00e9drale Saint Pierre et Saint Paul de Nantes",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "sightseeing",
          "restaurant",
          "church",
          "temple"
        ],
        "type": "location"
      },
      {
        "category": "SIGHTS",
        "city": "NTE",
        "geoCode": {
          "latitude": 47.2177,
          "longitude": -1.55832
        },
        "name": "Le Nid",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "sightseeing",
          "activities",
          "bar"
        ],
        "type": "location"
      },
      {
        "category": "RESTAURANT",
        "city": "NTE",
        "geoCode": {
          "latitude": 47.224133,
          "longitude": -1.582069
        },
        "name": "Parc de Proc\u00e9",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "restaurant",
          "park"
        ],
        "type": "location"
      }
    ],
    "city-name": "NANTES",
    "departureDate": "2019-07-30",
    "destination": "NTE",
    "links": {
      "flightDates": "https://api.amadeus.com/v1/shopping/flight-dates?origin=LON&destination=NTE&departureDate=2019-07-29,2019-07-31&oneWay=false&duration=1,15&nonStop=false&maxPrice=400&currency=GBP&viewBy=DURATION",
      "flightOffers": "https://api.amadeus.com/v1/shopping/flight-offers?origin=LON&destination=NTE&departureDate=2019-07-30&returnDate=2019-08-07&adults=1&nonStop=false&maxPrice=400&currency=GBP"
    },
    "origin": "LON",
    "price": {
      "total": "96.74"
    },
    "returnDate": "2019-08-07",
    "type": "flight-destination"
  }, ...
]
```