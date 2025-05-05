from tests.utils.AI_QA_tester import query_and_validate
import pytest
from tests.data.test_cases import TEST_CASES, TEST_CASES_100

@pytest.mark.parametrize("case", TEST_CASES_100, ids=lambda c: c["question"])
def test_query_rag_cases(case):
    got = query_and_validate(
        question=case["question"],
        source=case["source"].split('.')[0],
        expected_response=case["expected_response"],
    )
    if case["should_match"]:
        assert got, f"Expected match for question: {case['question']}"
    else:
        assert not got, f"Expected mismatch for question: {case['question']}"
