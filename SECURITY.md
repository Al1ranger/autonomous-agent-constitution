# Security

Experimental and unaudited. Do not use to govern production assets without independent audit and integration tests.

- Membership is fixed at formation: 2–8 addresses, every invitee must authenticate and accept before activation. This does not solve Sybil identity outside the invited roster.
- Ballots use `gl.message.sender_address`; a member cannot cast twice or change an existing ballot.
- Amendments bind community, parent version, and full charter hash. A competing amendment becomes stale after another ratifies.
- Numeric quorum and approval floors are enforced regardless of charter wording. Early ratification requires approval to remain valid even if every remaining voter says NO.
- Leader and validators independently analyze the full current and candidate charters and must exactly agree on the entire four-value guard vector. A FAIL vetoes; UNKNOWN is inconclusive; disagreement cannot ratify.
- The model can still misread subtle language or be influenced by adversarial text. The prompt treats charter text as data, not instructions. The contract does not verify real-world actions or enforce roles outside its own governance API.
- No funds are locked. A proposal can remain open if members do not vote; there is no deadline-based closure in this version.

Report vulnerabilities privately through GitHub security advisories.
