def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"

def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    for name in reseller_names:
        if name and name in text:
            return False
    return True

if __name__ == "__main__":
    # Acceptance Criteria Tests
    assert alias_for("RS019") == "ALIAS-19", f"Expected ALIAS-19, got {alias_for('RS019')}"
    assert alias_for("RS006") == "ALIAS-06", f"Expected ALIAS-06, got {alias_for('RS006')}"

    raw_names = ["Mumbai Reseller 1", "Mumbai Reseller 4", "Hyderabad Reseller 6", "Lucknow Reseller 6", "Jaipur Reseller 5"]
    
    # Negative test case (contains raw name)
    dirty_text = "Top seller was Mumbai Reseller 1 with revenue 75295.09."
    assert assert_no_raw_names_leak(dirty_text, raw_names) is False, "Negative case failed: raw name not detected"

    # Positive test case (masked text)
    clean_text = "Top seller was ALIAS-19 in West region with revenue 75295.09."
    assert assert_no_raw_names_leak(clean_text, raw_names) is True, "Positive case failed: masked text flagged as leak"

    print("All Part 3 masking tests passed successfully!")
