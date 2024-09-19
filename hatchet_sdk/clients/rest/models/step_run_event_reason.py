# coding: utf-8

"""
    Hatchet API

    The Hatchet API

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
from enum import Enum

from typing_extensions import Self


class StepRunEventReason(str, Enum):
    """
    StepRunEventReason
    """

    """
    allowed enum values
    """
    REQUEUED_NO_WORKER = "REQUEUED_NO_WORKER"
    REQUEUED_RATE_LIMIT = "REQUEUED_RATE_LIMIT"
    SCHEDULING_TIMED_OUT = "SCHEDULING_TIMED_OUT"
    ASSIGNED = "ASSIGNED"
    STARTED = "STARTED"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"
    TIMEOUT_REFRESHED = "TIMEOUT_REFRESHED"
    REASSIGNED = "REASSIGNED"
    TIMED_OUT = "TIMED_OUT"
    SLOT_RELEASED = "SLOT_RELEASED"
    RETRIED_BY_USER = "RETRIED_BY_USER"
    WORKFLOW_RUN_GROUP_KEY_SUCCEEDED = "WORKFLOW_RUN_GROUP_KEY_SUCCEEDED"
    WORKFLOW_RUN_GROUP_KEY_FAILED = "WORKFLOW_RUN_GROUP_KEY_FAILED"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of StepRunEventReason from a JSON string"""
        return cls(json.loads(json_str))
