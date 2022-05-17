# API for Game Database
Simple Game Store web service

## To launch:
```bash
git clone --recurse-submodules https://github.com/Jkali8/GameStore-Api
cd GameStore-Api
docker-compose build
docker-compose up
```

## Usage
Test the API with [Postman](https://www.postman.com/).

### Example JSON

```JSON
[
    {
        "_id": "627a4ea18434ccb052449ec8",
        "title": "CIV5",
        "releaseYear": 2015,
        "genre": "strategy",
        "price": 55,
        "length": "not specified",
        "buyer_id": "74638"
    }
]
```
### Another Example JSON

```JSON
[
	{
		"_id": "6283c8a715ae3a76f97298d5",
		"title": "Mario",
		"releaseYear": 1994,
		"genre": "platformer",
		"price": 10,
		"length": 60,
		"buyer": [
			{
				"id": 12345,
				"surname": "Vangogh",
				"name": "Jake",
				"number": "+37065841738",
				"email": "jakevan@mail.com"
			}
		]
	}
]
```

## RESTFUL API:
### POST 

#### Add a game:

`http://172.20.10.2:80/api/v2/games`

#### Add a buyer to a game:

`http://172.20.10.2:80/api/v2/games/<game_id>/buyer`

#### Add a buyer:
`http://172.20.10.2:80/api/v2/games/buyer`

### GET
#### Get a game by id:

`http://172.20.10.2:80/api/v2/games/<game_id>`

#### Get all games:

`http://172.20.10.2:80/api/v2/games`

#### Get a game's buyer:

`http://172.20.10.2:80/api/v2/games/<game_id>/buyer`

#### Get all contacts

`http://172.20.10.2:80/api/v2/games/buyer`

### PUT
#### Update game by id(can leave blank spaces):

`http://172.20.10.2:80/api/v2/games/<game_id>`

### PATCH
#### Modify game fields by id:

`http://172.20.10.2:80/api/v2/games/<game_id>`

#### Modify buyer_id field:

`http://172.20.10.2:80/api/v2/games/<game_id>/buyer`

### DELETE 
#### Delete game by id:

`http://172.20.10.2:80/api/v2/games/<game_id>`

#### Delete buyer by game id:

`http://172.20.10.2:80/api/v2/games/<game_id>/buyer`