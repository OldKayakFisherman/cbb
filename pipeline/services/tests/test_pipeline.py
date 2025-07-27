from services.data import PipelineRepository
from services.pipeline import (
    PipelineManager,
    PipelineOptions,
    PipelineResult
)

import unittest

class PipelineTests(unittest.TestCase):

    def test_injest(self):
  
        options: PipelineOptions = PipelineOptions(run_cbp_pipeline=True, run_pep_pipeline=True)
        mgr: PipelineManager = PipelineManager(options)

        #Purge the pipeline history
        PipelineRepository().purge()

        results:list[PipelineResult] = mgr.ingest()

        self.assertIsNotNone(results)
        self.assertEqual(len(results), 18)
        self.assertTrue(results[0].success)
        self.assertTrue(results[1].success)