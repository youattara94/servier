import pytest
from hamcrest import assert_that, contains_string, equal_to
from pydantic import ValidationError

from drug_publication_pipeline.schemas.drug import Drug


def test_should_return_two_drug_objects():
    # Given
    drugs_in_list = [
        {"atccode": "1", "drug": "Drug1"},
        {"atccode": "2", "drug": "Drug2"},
    ]

    # When
    drugs = [Drug(**drug) for drug in drugs_in_list]

    # Then
    assert_that(
        drugs, equal_to([Drug(id="1", name="Drug1"), Drug(id="2", name="Drug2")])
    )
    assert_that(len(drugs), equal_to(2))


def test_should_raise_validation_error_on_missing_fields():
    # Given
    drug_in_dict = {"atccode": "2"}

    # When
    with pytest.raises(ValidationError) as err:
        Drug(**drug_in_dict)

    # Then
    assert_that(
        str(err.value),
        contains_string("1 validation error for Drug"),
    )
