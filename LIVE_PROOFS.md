# Live StudioNet proofs

Contract: [0x46376CaD05E867EC703Aa636cD1972f807d4887C](https://explorer-studio.genlayer.com/address/0x46376CaD05E867EC703Aa636cD1972f807d4887C) on StudioNet (chain ID 61999). The deployed source returned by `genlayer code` is byte-for-byte equal to [`contracts/AutonomousAgentConstitution.py`](contracts/AutonomousAgentConstitution.py) after newline normalization (15,322 characters). Every transaction below reached `FINALIZED` with successful leader execution; reads were performed after finalization. Direct tests are separate from these live consensus transactions.

| Step | Finalized transaction | Observed result |
| --- | --- | --- |
| Deploy | [0xa90895a6…](https://explorer-studio.genlayer.com/tx/0xa90895a6e8e381d1dae5745f44015830a7f0e47bd1d25723a5a8e336c552475a) | Contract created |
| Fix two-member electorate and initial charter | [0x1353803e…](https://explorer-studio.genlayer.com/tx/0x1353803ecec09bc3c921a4e1442c9553b729bb4683e4376b816bf0bd2fb6865f) | `FORMING`, founder accepted |
| Second member accepts | [0x5c2af75b…](https://explorer-studio.genlayer.com/tx/0x5c2af75b56d8e4b35d8e6b2858f227589e6bdae07ba2b8b456d3bea69d525659) | Two authenticated members accepted |
| Activate | [0xfc039096…](https://explorer-studio.genlayer.com/tx/0xfc0390967cd366c44c8833b85f34fbcb279cc100c9859417c5577ffc4869b601) | `ACTIVE` |
| Propose additive reviewer role | [0xd88e408b…](https://explorer-studio.genlayer.com/tx/0xd88e408b75ebdca13c25d5120ee6e98140aa2926c6dbc9c516269f52825d889b) | Bound to charter version 0 |
| Member B votes YES | [0x62db3cf4…](https://explorer-studio.genlayer.com/tx/0x62db3cf4862ff41deaef4123c22651956edfde1572e800f1e377df4fb3425a3a) | Immutable ballot |
| Founder votes YES | [0xea9868c4…](https://explorer-studio.genlayer.com/tx/0xea9868c4b4d78dee5297bf9edbd0ea795db1a09b572f57b56d66af9fb5923d9d) | 2/2 YES, quorum met |
| Ratify additive amendment | [0xef89d077…](https://explorer-studio.genlayer.com/tx/0xef89d077d3fba405e89c37dc1b9ece134b039e7265e865b83586c1673cf02a45) | `RATIFIED`; exact guard vector `PASS/PASS/PASS/PASS`; charter version 1; decision root `9b813911512eded49b8b40ef06bc574c141a278ee12b8d6c748460b24e87c385` |
| Propose founder capture | [0x0d866179…](https://explorer-studio.genlayer.com/tx/0x0d866179dc550c0fc24bc75056f36a104896d793c1bac3b222c90d8aeb77fdab) | Attempts to revoke equal votes and make ballots mutable/private |
| Founder votes YES | [0x0daf5f48…](https://explorer-studio.genlayer.com/tx/0x0daf5f4836797deb14bbfa673499483d6030d0ecbcc449855dd9cfe4051cb5ba) | Authenticated ballot |
| Member B votes YES | [0xe1c8e281…](https://explorer-studio.genlayer.com/tx/0xe1c8e2819ff852bde1ae5a454f47897ffd661bf39806100bdbb9880663c36ef4) | 2/2 YES, quorum met |
| Evaluate founder capture | [0x41618249…](https://explorer-studio.genlayer.com/tx/0x416182490f06ce3caf00d88c02aa951721644605c86bd9c18065e6fab8161984) | `VETOED` despite unanimous ballots; guard vector `FAIL/FAIL/FAIL/FAIL`; charter stays at version 1; decision root `1e8fc1774be466a86286666bfaced34b88ae51ca23561a2dc3be15e8ed3d601f` |

The decision-bearing records are readable via `get_record("add-reviewer")` and `get_record("founder-capture")`; `get_amendment` returns each terminal state and root. This demonstrates an onchain authenticated governance mechanism, not verification of offchain agent conduct or a claim that the constitutions have legal force.
