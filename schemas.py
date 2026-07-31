from pydantic import BaseModel, Field
from typing import Optional


class CitizenRequest(BaseModel):
    """
    Information provided by a citizen.
    """

    message: str = Field(
        ...,
        description="Citizen's passport question or request"
    )

    location: Optional[str] = Field(
        default=None,
        description="Citizen location"
    )

    passport_type: Optional[str] = Field(
        default=None,
        description="New passport, renewal, lost passport, correction etc."
    )


class CitizenResponse(BaseModel):
    """
    Response returned by GovEasy AI.
    """

    status: str

    answer: str

    required_documents: list[str] = []

    steps: list[str] = []

    warning: Optional[str] = None

    escalation_required: bool = False