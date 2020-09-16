import logging
import requests

import azure.functions as func


def main(req: func.HttpRequest,getratings: func.DocumentList) -> func.HttpResponse:
    #req_body = req.get_json()
    logging.info("Found Ratings items,%s", getratings)
    #if not req_body:
    #    logging.warning("Ratings item not found")
    #else:
    #    logging.info("Found Ratings items,%s",
    #                 req_body)


    #return func.HttpResponse(req_body)
    return("OK")
