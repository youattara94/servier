import re
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PubMed(BaseModel):
    """Schema for PubMed article data."""

    id: int = Field(description="Unique identifier for the article", exclude=True)
    title: str = Field(description="Title of the article")
    journal: str = Field(
        description="Journal in which the article was published", exclude=True
    )
    publication_date: date = Field(
        description="Publication date of the article", alias="date"
    )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("publication_date", mode="before")
    def validate_publication_date(cls, value: date | str) -> date:
        """
        Validate and parse multiple date formats:
        - '27 April 2020'
        - '25/05/2020'
        - '2020-01-01'
        """
        if isinstance(value, date):
            return value  # Already a date
        if isinstance(value, str):
            for fmt in ("%d %B %Y", "%d/%m/%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
        raise ValueError(f"Invalid date format for publication_date: {value}")

    @field_validator("title", "journal", mode="after")
    def clean_string(cls, text: str) -> str:
        """
        Removes escaped hex sequences and any resulting partial characters.
        """
        # Remove all \xNN patterns directly
        return re.sub(r"\\x[0-9a-fA-F]{2}", "", text)
