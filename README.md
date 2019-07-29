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
        "category": "SIGHTS",
        "city": "MIL",
        "geoCode": {
          "latitude": 45.47324,
          "longitude": 9.17601
        },
        "name": "Parco Sempione",
        "score": 0.2916666567325592,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "sightseeing",
          "attraction",
          "sights",
          "park"
        ],
        "type": "location"
      },
      {
        "category": "SIGHTS",
        "city": "MIL",
        "geoCode": {
          "latitude": 45.47324,
          "longitude": 9.17601
        },
        "name": "Parco Sempione",
        "score": 0.2916666567325592,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "sightseeing",
          "attraction",
          "sights",
          "park"
        ],
        "type": "location"
      },
      {
        "category": "SIGHTS",
        "city": "MIL",
        "geoCode": {
          "latitude": 45.47324,
          "longitude": 9.17601
        },
        "name": "Parco Sempione",
        "score": 0.2916666567325592,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "sightseeing",
          "attraction",
          "sights",
          "park"
        ],
        "type": "location"
      },
      {
        "category": "SIGHTS",
        "city": "MIL",
        "geoCode": {
          "latitude": 45.46992,
          "longitude": 9.179714
        },
        "name": "Castello Sforzesco",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "sightseeing",
          "museum",
          "landmark",
          "castle"
        ],
        "type": "location"
      },
      {
        "category": "SIGHTS",
        "city": "MIL",
        "geoCode": {
          "latitude": 45.466034,
          "longitude": 9.170694
        },
        "name": "Santa Maria delle Grazie",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "attraction",
          "activities",
          "church",
          "temple"
        ],
        "type": "location"
      }
    ],
    "city-name": "MILAN",
    "departureDate": "2019-08-28",
    "destination": "MIL",
    "itenary": {
      "dist_matrix": {
        "destination_addresses": [
          "Viale Guglielmo Shakespeare, 20121 Milano MI, Italy",
          "Viale Alessandro Puskin, 20121 Milano MI, Italy",
          "Viale Alessandro Puskin, 20121 Milano MI, Italy",
          "Viale Alessandro Puskin, 20121 Milano MI, Italy",
          "Unnamed Road, 20121 Milano MI, Italy",
          "Piazza di Santa Maria delle Grazie, 2, 20123 Milano MI, Italy"
        ],
        "origin_addresses": [
          "Viale Guglielmo Shakespeare, 20121 Milano MI, Italy",
          "Viale Alessandro Puskin, 20121 Milano MI, Italy",
          "Viale Alessandro Puskin, 20121 Milano MI, Italy",
          "Viale Alessandro Puskin, 20121 Milano MI, Italy",
          "Unnamed Road, 20121 Milano MI, Italy",
          "Piazza di Santa Maria delle Grazie, 2, 20123 Milano MI, Italy"
        ],
        "rows": [
          {
            "elements": [
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.3 km",
                  "value": 279
                },
                "duration": {
                  "text": "3 mins",
                  "value": 194
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.3 km",
                  "value": 279
                },
                "duration": {
                  "text": "3 mins",
                  "value": 194
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.3 km",
                  "value": 279
                },
                "duration": {
                  "text": "3 mins",
                  "value": 194
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.5 km",
                  "value": 455
                },
                "duration": {
                  "text": "6 mins",
                  "value": 337
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1.2 km",
                  "value": 1169
                },
                "duration": {
                  "text": "14 mins",
                  "value": 868
                },
                "status": "OK"
              }
            ]
          },
          {
            "elements": [
              {
                "distance": {
                  "text": "0.3 km",
                  "value": 279
                },
                "duration": {
                  "text": "3 mins",
                  "value": 209
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.5 km",
                  "value": 529
                },
                "duration": {
                  "text": "7 mins",
                  "value": 421
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1.3 km",
                  "value": 1331
                },
                "duration": {
                  "text": "17 mins",
                  "value": 1015
                },
                "status": "OK"
              }
            ]
          },
          {
            "elements": [
              {
                "distance": {
                  "text": "0.3 km",
                  "value": 279
                },
                "duration": {
                  "text": "3 mins",
                  "value": 209
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.5 km",
                  "value": 529
                },
                "duration": {
                  "text": "7 mins",
                  "value": 421
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1.3 km",
                  "value": 1331
                },
                "duration": {
                  "text": "17 mins",
                  "value": 1015
                },
                "status": "OK"
              }
            ]
          },
          {
            "elements": [
              {
                "distance": {
                  "text": "0.3 km",
                  "value": 279
                },
                "duration": {
                  "text": "3 mins",
                  "value": 209
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.5 km",
                  "value": 529
                },
                "duration": {
                  "text": "7 mins",
                  "value": 421
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1.3 km",
                  "value": 1331
                },
                "duration": {
                  "text": "17 mins",
                  "value": 1015
                },
                "status": "OK"
              }
            ]
          },
          {
            "elements": [
              {
                "distance": {
                  "text": "0.5 km",
                  "value": 455
                },
                "duration": {
                  "text": "5 mins",
                  "value": 321
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.5 km",
                  "value": 529
                },
                "duration": {
                  "text": "6 mins",
                  "value": 382
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.5 km",
                  "value": 529
                },
                "duration": {
                  "text": "6 mins",
                  "value": 382
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "0.5 km",
                  "value": 529
                },
                "duration": {
                  "text": "6 mins",
                  "value": 382
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1.1 km",
                  "value": 1052
                },
                "duration": {
                  "text": "13 mins",
                  "value": 777
                },
                "status": "OK"
              }
            ]
          },
          {
            "elements": [
              {
                "distance": {
                  "text": "1.8 km",
                  "value": 1832
                },
                "duration": {
                  "text": "15 mins",
                  "value": 880
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "2.1 km",
                  "value": 2111
                },
                "duration": {
                  "text": "18 mins",
                  "value": 1074
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "2.1 km",
                  "value": 2111
                },
                "duration": {
                  "text": "18 mins",
                  "value": 1074
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "2.1 km",
                  "value": 2111
                },
                "duration": {
                  "text": "18 mins",
                  "value": 1074
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1.1 km",
                  "value": 1052
                },
                "duration": {
                  "text": "13 mins",
                  "value": 806
                },
                "status": "OK"
              },
              {
                "distance": {
                  "text": "1 m",
                  "value": 0
                },
                "duration": {
                  "text": "1 min",
                  "value": 0
                },
                "status": "OK"
              }
            ]
          }
        ],
        "status": "OK"
      },
      "path": [
        4,
        3,
        2,
        0,
        1
      ],
      "travel_time": [
        [
          0,
          194,
          194,
          194,
          337,
          868
        ],
        [
          209,
          0,
          0,
          0,
          421,
          1015
        ],
        [
          209,
          0,
          0,
          0,
          421,
          1015
        ],
        [
          209,
          0,
          0,
          0,
          421,
          1015
        ],
        [
          321,
          382,
          382,
          382,
          0,
          777
        ],
        [
          880,
          1074,
          1074,
          1074,
          806,
          0
        ]
      ]
    },
    "links": {
      "flightDates": "https://api.amadeus.com/v1/shopping/flight-dates?origin=LON&destination=MIL&departureDate=2019-07-29,2019-08-28&oneWay=false&duration=1,15&nonStop=false&maxPrice=400&currency=GBP&viewBy=DURATION",
      "flightOffers": "https://api.amadeus.com/v1/shopping/flight-offers?origin=LON&destination=MIL&departureDate=2019-08-28&returnDate=2019-09-11&adults=1&nonStop=false&maxPrice=400&currency=GBP"
    },
    "origin": "LON",
    "price": {
      "total": "76.24"
    },
    "returnDate": "2019-09-11",
    "type": "flight-destination"
  },
  {
    "activities": [
      {
        "category": "SIGHTS",
        "city": "IEV",
        "geoCode": {
          "latitude": 50.44492,
          "longitude": 30.508732
        },
        "name": "St Volodymyr's Cathedral",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "sightseeing",
          "church",
          "temple",
          "sights",
          "historicplace"
        ],
        "type": "location"
      },
      {
        "category": "NIGHTLIFE",
        "city": "IEV",
        "geoCode": {
          "latitude": 50.43974,
          "longitude": 30.518206
        },
        "name": "Parovoz Speak Easy",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "restaurant",
          "pub",
          "nightlife"
        ],
        "type": "location"
      },
      {
        "category": "SIGHTS",
        "city": "IEV",
        "geoCode": {
          "latitude": 50.44936,
          "longitude": 30.530762
        },
        "name": "National Art Museum of Ukraine",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "sightseeing",
          "museum",
          "sights",
          "landmark",
          "historicplace"
        ],
        "type": "location"
      },
      {
        "category": "RESTAURANT",
        "city": "IEV",
        "geoCode": {
          "latitude": 50.459087,
          "longitude": 30.517462
        },
        "name": "Kanapa Restaurant Salon",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "restaurant"
        ],
        "type": "location"
      },
      {
        "category": "RESTAURANT",
        "city": "IEV",
        "geoCode": {
          "latitude": 50.438854,
          "longitude": 30.519646
        },
        "name": "Milk Bar",
        "score": 0.0,
        "subType": "POINT_OF_INTEREST",
        "tags": [
          "shopping",
          "restaurant"
        ],
        "type": "location"
      }
    ], ...
]
```