import logging

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram

from overhave.db import DraftStatus, TestRunStatus

logger = logging.getLogger(__name__)


class OverhaveMetricContainer:
    """Overhave prometheus metric container."""

    def __init__(self, registry: CollectorRegistry):
        self.registry = registry
        self._init_product_metrics()

    def _init_product_metrics(self) -> None:
        self.test_run_tasks = Counter(
            "test_run_tasks",
            "How many test run tasks is running right now",
            registry=self.registry,
        )
        self.publication_tasks = Counter(
            "publication_tasks",
            "How many publication tasks is running right now",
            registry=self.registry,
        )
        self.test_run_tasks_statuses = Counter(
            "test_run_tasks_statuses",
            "Counter for test run statuses",
            labelnames=("status",),
            registry=self.registry,
        )
        self.publication_tasks_statuses = Counter(
            "publication_tasks_statuses",
            "Counter for publication run statuses",
            labelnames=("status",),
            registry=self.registry,
        )

    def add_test_run_task(self) -> None:
        self.test_run_tasks.inc()

    def add_test_run_status(self, status: TestRunStatus) -> None:
        self.test_run_tasks_statuses.labels(status=status).inc()

    def add_publication_task(self) -> None:
        self.publication_tasks.inc()

    def add_publication_task_status(self, status: DraftStatus) -> None:
        self.publication_tasks_statuses.labels(status=status).inc()
