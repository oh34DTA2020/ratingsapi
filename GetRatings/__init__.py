import logging

import azure.functions as func
import json

def main(req: func.HttpRequest,ratingsItems: func.DocumentList)  -> func.HttpResponse:

    records =[]

    for doc in ratingsItems:
        records.append(doc.to_json())
        logging.info(records)
    return func.HttpResponse(str(records))
