import logging
import requests
import os
import uuid
import json
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from datetime import datetime,timezone

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    userId = req.params.get('userId')
    productId = req.params.get('productId')
    locationName = req.params.get('locationName')
    rating = req.params.get('rating')
    userNotes = req.params.get('userNotes')


    # Validate both userId and productId by calling the existing API endpoints. You can find a user id to test with from the sample payload above
    uidurl = "https://serverlessohuser.trafficmanager.net/api/GetUser"
    response1 = requests.get(uidurl, params={'userId': userId})

    if response1:
        logging.info('Success User Found!')
    else:
        return func.HttpResponse("User Not Found",status_code=404)

    
    produrl = "https://serverlessohproduct.trafficmanager.net/api/GetProduct"
    response2 = requests.get(produrl, params={'productId': productId})

    if response2:
        logging.info('Success Product Found!')
    else:
        return func.HttpResponse("Product Not Found",status_code=404)

    # Add a property called id with a GUID value

    id = uuid.uuid4()

    logging.info(id)

    # Add a property called timestamp with the current UTC date time

    timestamp = datetime.now(timezone.utc)

    logging.info(timestamp)

    # Validate that the rating field is an integer from 0 to 5
    if rating:
        if rating.isdigit():
            logging.info('Rating is a number')
            logging.info(type(rating))
            #RECAST
            rating = int(rating)
            logging.info(type(rating))

            if rating > 0 and rating <= 5:
                logging.info('Rating is a VALID')
            else:
                return func.HttpResponse("Bad Rating",status_code=404)
        else:
            return func.HttpResponse("Bad Rating",status_code=404)
    else:
        return func.HttpResponse("Missing Rating",status_code=404)


    # Use a data service to store the ratings information to the backend

    # Initialize the Cosmos client
    endpoint = os.environ["cosmosendpoint"]
    key = os.environ["cosmoskey"]

    logging.info(key)

    
    client = CosmosClient(endpoint, key)
    
    database_name = "customer-ratings"
    container_name = "ratings"
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    # Return the entire review JSON payload with the newly created id and timestamp

    data = {"id": str(id), "userId": userId, "productId": productId, "timestamp": str(timestamp), 
    "locationName": locationName, "rating": rating, "userNotes": userNotes}

    json_data = json.dumps(data)

    logging.info(json_data)

    container.upsert_item(data)
    

    
    if userId:
        return func.HttpResponse(json_data)
    else:
        return func.HttpResponse(
             f"response : {x}",
             status_code=200
        )

