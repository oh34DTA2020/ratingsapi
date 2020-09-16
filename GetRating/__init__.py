import logging
import azure.functions as func

def main(req: func.HttpRequest,getratings: func.DocumentList) -> func.HttpResponse:
    logging.info("Found Ratings items,%s", getratings[0].to_json())
    return func.HttpResponse(getratings[0].to_json())
