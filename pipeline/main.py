import logging
import schedule
from services.pipeline import PipelineManager, PipelineOptions
import sys
import time

logging.basicConfig (
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
)

def main():
    try:
        logging.info("Executing pipeline operations ...")
        options: PipelineOptions = PipelineOptions(run_cbp_pipeline=True, run_pep_pipeline=True)
        mgr: PipelineManager = PipelineManager(options)
        mgr.ingest()
    except Exception as ex:
        logging.error(f"Pipeline encountered an error: {ex}")
    finally:
        logging.info("Pipeline operation complete")
    

if __name__ == "__main__":

    logging.info("Starting Data Pipeline Process")
    main()

    schedule.every(24).hours.do(main)

    while True:
        schedule.run_pending()
        time.sleep()
