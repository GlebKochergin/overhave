import logging
from pathlib import Path
from typing import List, Optional, cast

import pytest

from overhave.testing.settings import OverhaveTestSettings

logger = logging.getLogger(__name__)


class PytestRunner:
    """ Class for running `PyTest` in test and collect-only modes. """

    def __init__(self, test_settings: OverhaveTestSettings) -> None:
        self._test_settings = test_settings

    @staticmethod
    def _extend_cmd_args(cmd: List[str], addoptions: Optional[str]) -> None:
        if not isinstance(addoptions, str):
            return
        cmd.extend(addoptions.split(" "))

    def run(self, fixture_file: str, alluredir: str) -> int:
        pytest_cmd = [fixture_file, f"--alluredir={alluredir}", f"--rootdir={self._test_settings.pytest_rootdir}"]
        for addoptions in (self._test_settings.default_pytest_addoptions, self._test_settings.extra_pytest_addoptions):
            self._extend_cmd_args(cmd=pytest_cmd, addoptions=addoptions)
        if self._test_settings.workers is not None:
            pytest_cmd.extend(["-n", f"{self._test_settings.workers}"])

        logger.debug("Prepared pytest args: %s", pytest_cmd)
        return cast(int, pytest.main(pytest_cmd))

    def collect_only(self, fixture_file: Path) -> None:
        logger.info("Started tests collection process with '%s'...", fixture_file.name)
        pytest_cmd = [fixture_file.as_posix(), "--collect-only", "-qq", "--disable-pytest-warnings"]
        self._extend_cmd_args(cmd=pytest_cmd, addoptions=self._test_settings.extra_pytest_addoptions)
        logger.debug("Prepared pytest args: %s", pytest_cmd)
        pytest.main(pytest_cmd)
        logger.info("Finished tests collection process with '%s'.", fixture_file.name)
