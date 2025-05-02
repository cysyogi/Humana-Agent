from utils.AI_QA_tester import query_and_validate

def test_if_reasoning_is_picked():
    assert query_and_validate(
        question="If my child that is 4 years old needs glasses how much do i have to pay?",
        expected_response="No charge, deductible does not apply",
    )


def test_no_of_chiropractor_visits():
    assert query_and_validate(
        question="Can I visit the chiropractor?",
        expected_response="Yes, 20 Visits per year are allowed but for spinal manipulation only.",
    )


def test_is_max_deductible_is_picked_right():
    assert not query_and_validate(
        question="How much is the max deductible?",
        expected_response="$35,000",
    )
