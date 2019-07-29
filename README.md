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
```

Returns JSON Array containing Inspirations with recommended activities:  
```

```