from typing import Any, List, Optional
from uuid import UUID

from .base import BaseClient
from .types import CriteriaResultAnalysis, CriteriaResultEntity, CriteriaResultQA


class CriteriaResult:
    def __init__(self, base: BaseClient):
        self._base = base

    def _validate_params(
        self, file_uuid: Optional[Any], criteria_result_uuid: Optional[Any]
    ):
        if not file_uuid and not criteria_result_uuid:
            raise ValueError(
                "Either file_uuid or criteria_result_qa_uuid must be provided"
            )

    def get_qa(
        self,
        file_uuid: Optional[UUID | str] = None,
        criteria_result_qa_uuid: Optional[UUID | str] = None,
        client_uuid: Optional[UUID | str] = None,
    ) -> List[CriteriaResultQA]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        self._validate_params(file_uuid, criteria_result_qa_uuid)
        params = {
            "client_uuid": client_uuid,
            "file_uuid": str(file_uuid) if file_uuid else None,
            "criteria_result_qa_uuid": str(criteria_result_qa_uuid)
            if criteria_result_qa_uuid
            else None,
        }
        resp = self._base.make_request(
            "criteria-result-qa", method="GET", params=params
        )
        # Validate response structure
        if isinstance(resp, str):
            raise ValueError(f"NeuroHub returned string instead of object: {resp}")
        if not isinstance(resp, dict):
            raise ValueError(f"NeuroHub returned unexpected type: {type(resp)}, value: {resp}")
        if "results" not in resp:
            raise ValueError(f"NeuroHub response missing 'results' field. Response: {resp}")

        # Extract file_uuid from file_info (it's not in each result item)
        file_uuid_from_response = resp.get("file_info", {}).get("file_uuid")

        return [self._parse_qa_result(item, file_uuid_from_response) for item in resp["results"]]

    def get_entity(
        self,
        file_uuid: Optional[UUID | str] = None,
        criteria_result_entity_uuid: Optional[UUID | str] = None,
        client_uuid: Optional[UUID | str] = None,
    ) -> List[CriteriaResultEntity]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        self._validate_params(criteria_result_entity_uuid, file_uuid)
        params = {
            "client_uuid": client_uuid,
            "file_uuid": str(file_uuid) if file_uuid else None,
            "criteria_result_entity_uuid": str(criteria_result_entity_uuid)
            if criteria_result_entity_uuid
            else None,
        }
        resp = self._base.make_request(
            "criteria-result-entity", method="GET", params=params
        )
        # Validate response structure
        if isinstance(resp, str):
            raise ValueError(f"NeuroHub returned string instead of object: {resp}")
        if not isinstance(resp, dict):
            raise ValueError(f"NeuroHub returned unexpected type: {type(resp)}, value: {resp}")
        if "results" not in resp:
            raise ValueError(f"NeuroHub response missing 'results' field. Response: {resp}")

        # Extract file_uuid from file_info (it's not in each result item)
        file_uuid_from_response = resp.get("file_info", {}).get("file_uuid")

        return [self._parse_entity_result(item, file_uuid_from_response) for item in resp["results"]]

    def get_analysis(
        self,
        file_uuid: Optional[UUID | str] = None,
        criteria_result_analysis_uuid: Optional[UUID | str] = None,
        client_uuid: Optional[UUID | str] = None,
    ) -> List[CriteriaResultAnalysis]:
        client_uuid = self._base._handle_client_uuid(client_uuid)
        self._validate_params(file_uuid, criteria_result_analysis_uuid)
        params = {
            "client_uuid": client_uuid,
            "file_uuid": str(file_uuid) if file_uuid else None,
            "criteria_result_analysis_uuid": str(criteria_result_analysis_uuid)
            if criteria_result_analysis_uuid
            else None,
        }
        resp = self._base.make_request(
            "criteria-result-analysis", method="GET", params=params
        )
        # Validate response structure
        if isinstance(resp, str):
            raise ValueError(f"NeuroHub returned string instead of object: {resp}")
        if not isinstance(resp, dict):
            raise ValueError(f"NeuroHub returned unexpected type: {type(resp)}, value: {resp}")
        if "results" not in resp:
            raise ValueError(f"NeuroHub response missing 'results' field. Response: {resp}")

        # Extract file_uuid from file_info (it's not in each result item)
        file_uuid_from_response = resp.get("file_info", {}).get("file_uuid")

        return [self._parse_analysis_result(item, file_uuid_from_response) for item in resp["results"]]

    def _parse_qa_result(self, data: dict, file_uuid: Optional[str] = None) -> CriteriaResultQA:
        return CriteriaResultQA(
            criteria_result_qa_uuid=data["criteria_result_qa_uuid"],
            file_uuid=file_uuid or data.get("file_uuid"),  # Use passed file_uuid or fallback to data
            criteria_uuid=data["criteria_uuid"],
            situation_id=data["situation_id"],
            criteria_score=data["criteria_score"],
            qa_time_1=data["qa_time_1"],
            qa_time_2=data["qa_time_2"],
            qa_time_3=data["qa_time_3"],
            criteria=data["criteria"],
        )

    def _parse_entity_result(self, data: dict, file_uuid: Optional[str] = None) -> CriteriaResultEntity:
        return CriteriaResultEntity(
            criteria_result_entity_uuid=data["criteria_result_entity_uuid"],
            file_uuid=file_uuid or data.get("file_uuid"),  # Use passed file_uuid or fallback to data
            criteria_uuid=data["criteria_uuid"],
            criteria_value=data["criteria_value"],
            entity_time=data["entity_time"],
            criteria=data["criteria"],
            criteria_clasification_list=data["criteria_clasification_list"],
        )

    def _parse_analysis_result(self, data: dict, file_uuid: Optional[str] = None) -> CriteriaResultAnalysis:
        # Add file_uuid to data if not present
        if file_uuid and "file_uuid" not in data:
            data["file_uuid"] = file_uuid
        return data
