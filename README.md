# Database Management Systems course project

## Project Theme : Online service for digital distribution of computer games and programs

### Project Description

#### TODO: FOR_THE_FUTURE

#### Current architecture
![logical_store_schema](./store-schema.png)

![logical_bank_schema](./bank-schema.png)

#### About bank-service api

##### How to get user balance ( example )
```
curl -X GET -H 'Content-Type: application/json' -u "seregga:seregga" 127.0.0.1:5001/api/balance
```

##### How to add account in our great bank ( example )
```
curl -X POST -H 'Content-Type: application/json' -d '{"uuid" : "test", "password" : "test"}' 127.0.0.1:5001/api/add-account
```

##### How to delete bank account ( example )
```
curl -X POST -H 'Content-Type: application/json' -u "test:test" 127.0.0.1:5001/api/delete-account
```

##### How to transfer money from one account to another ( example )
```
curl -X POST -H 'Content-Type: application/json' -u "test:test" -d '{"uuid_to" : "seregga", "amount" : 500 }' 127.0.0.1:5001/api/transfer
```

##### Return codes for bank api service
  * 401 -- authorization failed
  * 402 -- wrong requested data
  * 404 -- wrong request

### Development Stack : Docker, Python(backend + frontend), sqlite3

### Requirements list for running services on the local server :
  * docker
  * docker-compose

## The composition of our team:
  * Gubanov Peter (@gubanovpm)
  * Khrol Ivan    (@ent1r)
  * Potapova Anna (@ann37)



