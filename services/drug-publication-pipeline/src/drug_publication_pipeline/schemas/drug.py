from pydantic import BaseModel, ConfigDict, Field


class Drug(BaseModel):
    """
    Schema for drug data.
    """

    id: str = Field(description="Unique identifier for the drug", alias="atccode")
    name: str = Field(description="Name of the drug", alias="drug")

    model_config = ConfigDict(populate_by_name=True)
