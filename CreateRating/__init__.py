import logging
import requests
import uuid
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
        logging.info('User Not Found.')
    
    produrl = "https://serverlessohproduct.trafficmanager.net/api/GetProduct"
    response2 = requests.get(produrl, params={'productId': productId})

    if response2:
        logging.info('Success Product Found!')
    else:
        logging.info('Product Not Found.')

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
                logging.info('Rating is INVALID')
        else:
            logging.info('Rating is NOT a number')
    else:
        logging.info('Missing Rating')


    # Use a data service to store the ratings information to the backend
    # Return the entire review JSON payload with the newly created id and timestamp

    
    if userId:
        return func.HttpResponse(f"Hello, {userId}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             f"response : {x}",
             status_code=200
        )

