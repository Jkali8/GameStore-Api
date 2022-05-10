# API for Game Database
Simple Game Store web service

## To launch:
```bash
git clone https://github.com/Jkali8/GameStore-Api
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

## RESTFUL API:
### POST 

#### Add a game:

`http://172.20.10.2:80/api/v2/games`

#### Add a buyer to a game:

`http://172.20.10.2:80/api/v2/games/<game_id>/buyer`

### GET
#### Get a game by id:

`http://172.20.10.2:80/api/v2/games/<game_id>`

#### Get all games:

`http://172.20.10.2:80/api/v2/games`

#### Get a game's buyer:

`http://172.20.10.2:80/api/v2/games/<game_id>/buyer`

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