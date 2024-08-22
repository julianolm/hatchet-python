import asyncio
import atexit
import threading
from typing import Any

from hatchet_sdk.clients.rest.api.event_api import EventApi
from hatchet_sdk.clients.rest.api.log_api import LogApi
from hatchet_sdk.clients.rest.api.step_run_api import StepRunApi
from hatchet_sdk.clients.rest.api.workflow_api import WorkflowApi
from hatchet_sdk.clients.rest.api.workflow_run_api import WorkflowRunApi
from hatchet_sdk.clients.rest.api_client import ApiClient
from hatchet_sdk.clients.rest.configuration import Configuration
from hatchet_sdk.clients.rest.models import TriggerWorkflowRunRequest
from hatchet_sdk.clients.rest.models.event_list import EventList
from hatchet_sdk.clients.rest.models.event_order_by_direction import (
    EventOrderByDirection,
)
from hatchet_sdk.clients.rest.models.event_order_by_field import EventOrderByField
from hatchet_sdk.clients.rest.models.log_line_level import LogLineLevel
from hatchet_sdk.clients.rest.models.log_line_list import LogLineList
from hatchet_sdk.clients.rest.models.log_line_order_by_direction import (
    LogLineOrderByDirection,
)
from hatchet_sdk.clients.rest.models.log_line_order_by_field import LogLineOrderByField
from hatchet_sdk.clients.rest.models.replay_event_request import ReplayEventRequest
from hatchet_sdk.clients.rest.models.workflow import Workflow
from hatchet_sdk.clients.rest.models.workflow_kind import WorkflowKind
from hatchet_sdk.clients.rest.models.workflow_list import WorkflowList
from hatchet_sdk.clients.rest.models.workflow_run import WorkflowRun
from hatchet_sdk.clients.rest.models.workflow_run_cancel200_response import (
    WorkflowRunCancel200Response,
)
from hatchet_sdk.clients.rest.models.workflow_run_list import WorkflowRunList
from hatchet_sdk.clients.rest.models.workflow_run_order_by_direction import (
    WorkflowRunOrderByDirection,
)
from hatchet_sdk.clients.rest.models.workflow_run_order_by_field import (
    WorkflowRunOrderByField,
)
from hatchet_sdk.clients.rest.models.workflow_run_status import WorkflowRunStatus
from hatchet_sdk.clients.rest.models.workflow_runs_cancel_request import (
    WorkflowRunsCancelRequest,
)
from hatchet_sdk.clients.rest.models.workflow_version import WorkflowVersion


class AsyncRestApi:
    def __init__(self, host: str, api_key: str, tenant_id: str):
        self.tenant_id = tenant_id

        self.config = Configuration(
            host=host,
            access_token=api_key,
        )

        self._api_client = None
        self._workflow_api = None
        self._workflow_run_api = None
        self._step_run_api = None
        self._event_api = None
        self._log_api = None

    @property
    def api_client(self):
        if self._api_client is None:
            self._api_client = ApiClient(configuration=self.config)
        return self._api_client

    @property
    def workflow_api(self):
        if self._workflow_api is None:
            self._workflow_api = WorkflowApi(self.api_client)
        return self._workflow_api

    @property
    def workflow_run_api(self):
        if self._workflow_run_api is None:
            self._workflow_run_api = WorkflowRunApi(self.api_client)
        return self._workflow_run_api

    @property
    def step_run_api(self):
        if self._step_run_api is None:
            self._step_run_api = StepRunApi(self.api_client)
        return self._step_run_api

    @property
    def event_api(self):
        if self._event_api is None:
            self._event_api = EventApi(self.api_client)
        return self._event_api

    @property
    def log_api(self):
        if self._log_api is None:
            self._log_api = LogApi(self.api_client)
        return self._log_api

    async def close(self):
        # Ensure the aiohttp client session is closed
        if self._api_client is not None:
            await self._api_client.close()

    async def workflow_list(self) -> WorkflowList:
        return await self.workflow_api.workflow_list(
            tenant=self.tenant_id,
        )

    async def workflow_get(self, workflow_id: str) -> Workflow:
        return await self.workflow_api.workflow_get(
            workflow=workflow_id,
        )

    async def workflow_version_get(
        self, workflow_id: str, version: str | None = None
    ) -> WorkflowVersion:
        return await self.workflow_api.workflow_version_get(
            workflow=workflow_id,
            version=version,
        )

    async def workflow_run_list(
        self,
        workflow_id: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        event_id: str | None = None,
        parent_workflow_run_id: str | None = None,
        parent_step_run_id: str | None = None,
        statuses: list[WorkflowRunStatus] | None = None,
        kinds: list[WorkflowKind] | None = None,
        additional_metadata: list[str] | None = None,
        order_by_field: WorkflowRunOrderByField | None = None,
        order_by_direction: WorkflowRunOrderByDirection | None = None,
    ) -> WorkflowRunList:
        return await self.workflow_run_api.workflow_run_list(
            tenant=self.tenant_id,
            offset=offset,
            limit=limit,
            workflow_id=workflow_id,
            event_id=event_id,
            parent_workflow_run_id=parent_workflow_run_id,
            parent_step_run_id=parent_step_run_id,
            statuses=statuses,
            kinds=kinds,
            additional_metadata=additional_metadata,
            order_by_field=order_by_field,
            order_by_direction=order_by_direction,
        )

    async def workflow_run_get(self, workflow_run_id: str) -> WorkflowRun:
        return await self.workflow_api.workflow_run_get(
            tenant=self.tenant_id,
            workflow_run=workflow_run_id,
        )

    async def workflow_run_cancel(
        self, workflow_run_id: str
    ) -> WorkflowRunCancel200Response:
        return await self.workflow_run_api.workflow_run_cancel(
            tenant=self.tenant_id,
            workflow_runs_cancel_request=WorkflowRunsCancelRequest(
                workflowRunIds=[workflow_run_id],
            ),
        )

    async def workflow_run_bulk_cancel(
        self, workflow_run_ids: list[str]
    ) -> WorkflowRunCancel200Response:
        return await self.workflow_run_api.workflow_run_cancel(
            tenant=self.tenant_id,
            workflow_runs_cancel_request=WorkflowRunsCancelRequest(
                workflowRunIds=workflow_run_ids,
            ),
        )

    async def workflow_run_create(
        self,
        workflow_id: str,
        input: dict[str, Any],
        version: str | None = None,
        additional_metadata: list[str] | None = None,
    ) -> WorkflowRun:
        return await self.workflow_run_api.workflow_run_create(
            workflow=workflow_id,
            version=version,
            trigger_workflow_run_request=TriggerWorkflowRunRequest(
                input=input,
            ),
        )

    async def list_logs(
        self,
        step_run_id: str,
        offset: int | None = None,
        limit: int | None = None,
        levels: list[LogLineLevel] | None = None,
        search: str | None = None,
        order_by_field: LogLineOrderByField | None = None,
        order_by_direction: LogLineOrderByDirection | None = None,
    ) -> LogLineList:
        return await self.log_api.log_line_list(
            step_run=step_run_id,
            offset=offset,
            limit=limit,
            levels=levels,
            search=search,
            order_by_field=order_by_field,
            order_by_direction=order_by_direction,
        )

    async def events_list(
        self,
        offset: int | None = None,
        limit: int | None = None,
        keys: list[str] | None = None,
        workflows: list[str] | None = None,
        statuses: list[WorkflowRunStatus] | None = None,
        search: str | None = None,
        order_by_field: EventOrderByField | None = None,
        order_by_direction: EventOrderByDirection | None = None,
        additional_metadata: list[str] | None = None,
    ) -> EventList:
        return await self.event_api.event_list(
            tenant=self.tenant_id,
            offset=offset,
            limit=limit,
            keys=keys,
            workflows=workflows,
            statuses=statuses,
            search=search,
            order_by_field=order_by_field,
            order_by_direction=order_by_direction,
            additional_metadata=additional_metadata,
        )

    async def events_replay(self, event_ids: list[str] | EventList) -> EventList:
        if isinstance(event_ids, EventList):
            event_ids = [r.metadata.id for r in event_ids.rows]

        return self.event_api.event_update_replay(
            tenant=self.tenant_id,
            replay_event_request=ReplayEventRequest(eventIds=event_ids),
        )


class RestApi:
    def __init__(self, host: str, api_key: str, tenant_id: str):
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self._thread.start()

        # Initialize AsyncRestApi inside the event loop to ensure an active loop
        self.aio = AsyncRestApi(host, api_key, tenant_id)

        # Register the cleanup method to be called on exit
        atexit.register(self._cleanup)

    def _cleanup(self):
        """
        Stop the running thread and clean up the event loop.
        """
        self._run_coroutine(self.aio.close())
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join()

    def _run_event_loop(self):
        """
        Run the asyncio event loop in a separate thread.
        """
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def _run_coroutine(self, coro) -> Any:
        """
        Execute a coroutine in the event loop and return the result.
        """
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

    def workflow_list(self) -> WorkflowList:
        return self._run_coroutine(self.aio.workflow_list())

    def workflow_get(self, workflow_id: str) -> Workflow:
        return self._run_coroutine(self.aio.workflow_get(workflow_id))

    def workflow_version_get(
        self, workflow_id: str, version: str | None = None
    ) -> WorkflowVersion:
        return self._run_coroutine(self.aio.workflow_version_get(workflow_id, version))

    def workflow_run_list(
        self,
        workflow_id: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        event_id: str | None = None,
        parent_workflow_run_id: str | None = None,
        parent_step_run_id: str | None = None,
        statuses: list[WorkflowRunStatus] | None = None,
        kinds: list[WorkflowKind] | None = None,
        additional_metadata: list[str] | None = None,
        order_by_field: WorkflowRunOrderByField | None = None,
        order_by_direction: WorkflowRunOrderByDirection | None = None,
    ) -> WorkflowRunList:
        return self._run_coroutine(
            self.aio.workflow_run_list(
                workflow_id=workflow_id,
                offset=offset,
                limit=limit,
                event_id=event_id,
                parent_workflow_run_id=parent_workflow_run_id,
                parent_step_run_id=parent_step_run_id,
                statuses=statuses,
                kinds=kinds,
                additional_metadata=additional_metadata,
                order_by_field=order_by_field,
                order_by_direction=order_by_direction,
            )
        )

    def workflow_run_get(self, workflow_run_id: str) -> WorkflowRun:
        return self._run_coroutine(self.aio.workflow_run_get(workflow_run_id))

    def workflow_run_cancel(self, workflow_run_id: str) -> WorkflowRunCancel200Response:
        return self._run_coroutine(self.aio.workflow_run_cancel(workflow_run_id))

    def workflow_run_bulk_cancel(
        self, workflow_run_ids: list[str]
    ) -> WorkflowRunCancel200Response:
        return self._run_coroutine(self.aio.workflow_run_bulk_cancel(workflow_run_ids))

    def workflow_run_create(
        self,
        workflow_id: str,
        input: dict[str, Any],
        version: str | None = None,
        additional_metadata: list[str] | None = None,
    ) -> WorkflowRun:
        return self._run_coroutine(
            self.aio.workflow_run_create(
                workflow_id, input, version, additional_metadata
            )
        )

    def list_logs(
        self,
        step_run_id: str,
        offset: int | None = None,
        limit: int | None = None,
        levels: list[LogLineLevel] | None = None,
        search: str | None = None,
        order_by_field: LogLineOrderByField | None = None,
        order_by_direction: LogLineOrderByDirection | None = None,
    ) -> LogLineList:
        return self._run_coroutine(
            self.aio.list_logs(
                step_run_id=step_run_id,
                offset=offset,
                limit=limit,
                levels=levels,
                search=search,
                order_by_field=order_by_field,
                order_by_direction=order_by_direction,
            )
        )

    def events_list(
        self,
        offset: int | None = None,
        limit: int | None = None,
        keys: list[str] | None = None,
        workflows: list[str] | None = None,
        statuses: list[WorkflowRunStatus] | None = None,
        search: str | None = None,
        order_by_field: EventOrderByField | None = None,
        order_by_direction: EventOrderByDirection | None = None,
        additional_metadata: list[str] | None = None,
    ) -> EventList:
        return self._run_coroutine(
            self.aio.events_list(
                offset=offset,
                limit=limit,
                keys=keys,
                workflows=workflows,
                statuses=statuses,
                search=search,
                order_by_field=order_by_field,
                order_by_direction=order_by_direction,
                additional_metadata=additional_metadata,
            )
        )

    def events_replay(self, event_ids: list[str] | EventList) -> EventList:
        return self._run_coroutine(self.aio.events_replay(event_ids))
