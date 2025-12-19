# tools/validation_tool.py

import re


class ValidationError(Exception):
    pass


FR_PATTERN = re.compile(r"^FR-?\d+$", re.IGNORECASE)
NFR_PATTERN = re.compile(r"^NFR-?\d+$", re.IGNORECASE)


def validate_test_cases(test_cases: list):
    """
    Enterprise-grade validation with LLM-noise tolerance.
    """

    if not isinstance(test_cases, list) or not test_cases:
        raise ValidationError("Test cases must be a non-empty list")

    for tc in test_cases:
        # --- Mandatory fields ---
        required_fields = [
            "test_id",
            "title",
            "type",
            "steps",
            "expected_result",
            "mapped_requirements"
        ]

        for field in required_fields:
            if field not in tc or not tc[field]:
                raise ValidationError(
                    f"{tc.get('test_id', 'UNKNOWN')} missing required field: {field}"
                )

        # --- Steps ---
        if not isinstance(tc["steps"], list) or len(tc["steps"]) == 0:
            raise ValidationError(
                f"{tc['test_id']} must contain at least one step"
            )

        # --- Requirement sanitization ---
        raw_reqs = tc.get("mapped_requirements", [])

        valid_reqs = [
            r for r in raw_reqs
            if FR_PATTERN.match(r) or NFR_PATTERN.match(r)
        ]

        if not valid_reqs:
            raise ValidationError(
                f"{tc['test_id']} has no valid FR/NFR mapping. Found: {raw_reqs}"
            )

        # Replace with cleaned list
        tc["mapped_requirements"] = valid_reqs

    return True
