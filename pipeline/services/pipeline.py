from dataclasses import dataclass
import logging
from services.api import (
    APIResponse,
    CBPCountyAPIClient,
    CBPStateAPIClient
)
from services.config import AppSettings
from services.data import(
    IngestionRepository,
    CBPCountyRepository,
    CBPStateRepository,
    PipelineRepository
)
from services.timers import PipelineTimer

settings = AppSettings()

#api clients
cbp_county_api_client = CBPCountyAPIClient()
cbp_state_api_client = CBPStateAPIClient()

#repositories
ingestion_repo = IngestionRepository()
cbp_county_repo = CBPCountyRepository()
cbp_state_repo = CBPStateRepository()
pipeline_repo = PipelineRepository()

@dataclass
class PipelineOptions:
    run_cbp_pipeline: bool = False
    run_pep_pipeline: bool = False


@dataclass
class PipelineResult:
    name: str
    execution_time: float = 0.0
    success: bool = False
    error: Exception = None

class PipelineManager:

    def __init__(self, options: PipelineOptions):
        self.__options = options

    @property
    def options(self) -> PipelineOptions:
        return self.__options
    

    def __purge(self) -> bool:

        timer: PipelineTimer = PipelineTimer()
        errors: bool = False

        try:
            with timer:
                logging.info("Starting Database purge")

                if self.options.run_cbp_pipeline == True:
                    logging.info("Purging CBP County Records")
                    cbp_county_repo.purge()
                    logging.info("CBP County Records Purged")

                    logging.info("Purging CBP State Records")
                    cbp_state_repo.purge()
                    logging.info("CBP State Records Purged")


        except Exception as ex:
            logging.error(f"Pipeline purge encountered an error and maybe in an inconsistent state. --error: {ex}")
            errors = True
        finally:
            if errors == True:
                logging.error(f"Pipeline Purge did not complete successfully")
            else:
                logging.error(f"Pipeline Purge completed successfully")

            return (errors == False)
        
    def ingest(self) -> list[PipelineResult]:
        
        ingest_results:list[PipelineResult] = []

        if pipeline_repo.run_needed(settings.pipeline_hour_check) == True:
            if self.options.run_cbp_pipeline == True:
                
                for target_year in range(settings.cbp_start_year, (settings.cbp_end_year + 1)):
                    
                    #Import the CBP County Records
                    pipeline_timer = PipelineTimer()
                    cbp_pipeline_result = PipelineResult("CBP County Pipeline")

                    try:
                        with pipeline_timer:    
                            api_response: APIResponse = CBPCountyAPIClient().poll(target_year)
                            if api_response.success:
                                #save the records
                                cbp_county_repo.save(api_response.data, target_year)
                                cbp_pipeline_result.success = True
                    except Exception as ex:
                        cbp_pipeline_result.error = ex
                        cbp_pipeline_result.success = False
                    finally:
                        cbp_pipeline_result.execution_time = pipeline_timer.expired_milliseconds
                        ingest_results.append(cbp_pipeline_result)

                    #Import the CBP State Records
                    pipeline_timer = PipelineTimer()
                    cbp_pipeline_result = PipelineResult("CBP State Pipeline")

                    try:
                        with pipeline_timer:    
                            api_response: APIResponse = CBPStateAPIClient().poll(target_year)
                            if api_response.success:
                                #save the records
                                cbp_state_repo.save(api_response.data, target_year)
                                cbp_pipeline_result.success = True
                    except Exception as ex:
                        cbp_pipeline_result.error = ex
                        cbp_pipeline_result.success = False
                    finally:
                        cbp_pipeline_result.execution_time = pipeline_timer.expired_milliseconds
                        ingest_results.append(cbp_pipeline_result)

        return ingest_results