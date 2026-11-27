import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("smoke_markers", Path(__file__).parents[1] / "tools" / "smoke_markers.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SmokeMarkersTest(unittest.TestCase):
    def test_log_evidence_not_duration(self):
        result = module.classify(["BOOT_EVENT phase=guest_start mode=scheduler\n", "running for 999 seconds\n"])
        self.assertTrue(result["ENTRY_REACHED"]["observed"])
        self.assertFalse(result["FIRST_FRAME_DUMPED"]["observed"])
        self.assertFalse(result["INTRO_VIDEO_OPEN_ATTEMPTED"]["observed"])

    def test_frame_and_hle_are_independent(self):
        result = module.classify(["HLE: calling sceKernelCreateThread\n", "[FIRST_FRAME] dumped BGRA\n"])
        self.assertEqual(result["FIRST_THREAD_CREATE_CALLED"]["line"], 1)
        self.assertEqual(result["FIRST_FRAME_DUMPED"]["line"], 2)
        self.assertFalse(result["FIRST_AVC_DECODE_REPORTED"]["observed"])


if __name__ == "__main__":
    unittest.main()
