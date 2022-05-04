# API for Movie Database
Simple Web Service CRUD application movie database 

## Requirements:
* docker
* git

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
	"title": "Mario",
	"releaseYear": 2012,
	"genre": "Action",
	"price": 50,
	"length": 60,
	}
]
```

## RESTFUL API:
### POST 

`http://172.20.10.2:80/api/v2/games`

### GET
#### Get a movie by id:

`http://172.20.10.2:80/api/v2/games/<game_id>`

#### Get all movies:

`http://172.20.10.2:80/api/v2/games`

### PUT
#### Update movie by id(can leave blank spaces):

`http://172.20.10.2:80/api/v2/games/<game_id>`

### PATCH
#### Modify movie fields by id:

`http://172.20.10.2:80/api/v2/games/<game_id>`

### DELETE 
#### Delete movie by id:

`http://172.20.10.2:80/api/v2/games/<game_id>`