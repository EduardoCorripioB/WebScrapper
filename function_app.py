#Import function
from app import cryptoscrapper

#Time Trigger
import logging
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 0 */3 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    ###########################################################################################################################
    cryptoscrapper()
    ###########################################################################################################################
    logging.info('Python timer trigger function executed.')








