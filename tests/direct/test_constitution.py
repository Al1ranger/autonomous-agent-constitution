import json


BASE = (
    "Every founding member has one equal nondelegable vote. Amendments, ballots, "
    "and outcomes are public. Cast ballots and finalized decisions cannot be edited "
    "or retroactively changed. Quorum is 100% of members; approval is 70% of YES/NO "
    "ballots. No role or founder may ratify alone."
)
ADDITIVE = (
    BASE + " A Reviewer role may attach nonbinding comments. Reviewers gain no extra "
    "vote and cannot bypass quorum, approval, or immutable ballot records."
)
CAPTURE = (
    "Only the founder may vote and ratify amendments alone. Other founding members "
    "have no ballot rights. Ballots are private, may be edited after casting, and "
    "finalized decisions may be reversed retroactively. Quorum is 100% of members; "
    "approval is 70% of YES/NO ballots."
)


def address_text(value):
    if isinstance(value, bytes):
        return "0x" + value.hex()
    return value.as_hex if hasattr(value, "as_hex") else str(value)


def active_council(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/AutonomousAgentConstitution.py")
    direct_vm.sender = direct_alice
    contract.create_community(
        "research", "Research Council", BASE,
        address_text(direct_alice) + "," + address_text(direct_bob), 10000, 7000,
    )
    direct_vm.sender = direct_bob
    contract.accept_membership("research")
    contract.activate_community("research")
    return contract


def test_formation_requires_all_invitees(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/AutonomousAgentConstitution.py")
    direct_vm.sender = direct_alice
    contract.create_community(
        "research", "Research Council", BASE,
        address_text(direct_alice) + "," + address_text(direct_bob), 10000, 7000,
    )
    with direct_vm.expect_revert("all founding members must accept"):
        contract.activate_community("research")
    direct_vm.sender = direct_bob
    contract.accept_membership("research")
    contract.activate_community("research")
    assert contract.get_community("research")["state"] == "ACTIVE"


def test_immutable_votes_and_quorum(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = active_council(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    contract.propose_amendment("research", "add-reviewer", 0, ADDITIVE, 10000, 7000)
    contract.cast_ballot("research", "add-reviewer", "YES")
    with direct_vm.expect_revert("immutable one-vote ballot"):
        contract.cast_ballot("research", "add-reviewer", "NO")
    with direct_vm.expect_revert("quorum not reached"):
        contract.ratify_amendment("research", "add-reviewer")
    assert contract.get_amendment("add-reviewer")["state"] == "OPEN"


def test_cross_community_ballot_rejected(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = active_council(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    contract.create_community(
        "other", "Other Council", BASE,
        address_text(direct_alice) + "," + address_text(direct_bob), 10000, 7000,
    )
    contract.propose_amendment("research", "add-reviewer", 0, ADDITIVE, 10000, 7000)
    with direct_vm.expect_revert("amendment belongs to another community"):
        contract.cast_ballot("other", "add-reviewer", "YES")
    assert contract.get_amendment("add-reviewer")["yes"] == 0


def test_unanimous_ballot_and_guard_consensus_ratify(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = active_council(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    contract.propose_amendment("research", "add-reviewer", 0, ADDITIVE, 10000, 7000)
    contract.cast_ballot("research", "add-reviewer", "YES")
    direct_vm.sender = direct_bob
    contract.cast_ballot("research", "add-reviewer", "YES")
    direct_vm.mock_llm(
        r".*Assess the full.*candidate charter.*",
        json.dumps({"equal_ballot": "PASS", "public_record": "PASS",
                    "nonretroactive": "PASS", "coherence": "PASS"}),
    )
    contract.ratify_amendment("research", "add-reviewer")
    assert contract.get_amendment("add-reviewer")["state"] == "RATIFIED"
    assert contract.get_community("research")["version"] == 1
    assert contract.get_ballot("add-reviewer", address_text(direct_alice)) == "YES"
    with direct_vm.expect_revert("amendment terminal"):
        contract.ratify_amendment("research", "add-reviewer")


def test_semantic_veto_over_unanimous_yes(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = active_council(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    contract.propose_amendment("research", "capture", 0, CAPTURE, 10000, 7000)
    contract.cast_ballot("research", "capture", "YES")
    direct_vm.sender = direct_bob
    contract.cast_ballot("research", "capture", "YES")
    direct_vm.mock_llm(
        r".*Assess the full.*candidate charter.*",
        json.dumps({"equal_ballot": "FAIL", "public_record": "FAIL",
                    "nonretroactive": "FAIL", "coherence": "PASS"}),
    )
    contract.ratify_amendment("research", "capture")
    assert contract.get_amendment("capture")["state"] == "VETOED"
    assert contract.get_community("research")["version"] == 0


def test_threshold_floor(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = active_council(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("constitutional threshold floor"):
        contract.propose_amendment("research", "weak", 0, ADDITIVE, 5000, 5000)
