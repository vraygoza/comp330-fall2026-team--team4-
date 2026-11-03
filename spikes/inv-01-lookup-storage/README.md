# INV-01 Spike: Lookup and Storage

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun (Operations & Evidence Co-Lead) |
| Last updated | 2026-10-14 |

Throwaway investigation code for [INV-01](../../docs/architecture/investigations/inv-01-lookup-storage.md). It is not the Cycle 1 implementation and nothing in `/src/` imports it. Standard library only (Python 3.10 or later).

| File | Purpose |
|------|---------|
| `calorie_core.py` | Parsing, food resolution, quantity conversion, SQLite storage, Chicago day window |
| `run_investigation.py` | Runs 19 synthetic messages and prints a results table; `--live` queries FoodData Central |
| `test_investigation.py` | Never-save rules, restart persistence, two-tester and 15-tester isolation, midnight and daylight-saving checks |
| `fixtures/fdc_synthetic.json` | Invented records shaped like FDC data. Values are placeholders, not FDC data |
| `fixtures/food_map_synthetic.json` | Example curated food map (the real one is filled from T-13) |
| `results-2026-10-14.md` | Output of the offline run recorded for review |

## Run It

```bash
cd spikes/inv-01-lookup-storage
python3 run_investigation.py                 # offline, synthetic fixture
python3 -m unittest -v test_investigation.py # 14 checks
FDC_API_KEY=your_key python3 run_investigation.py --live   # live FDC search, stores nothing
```

Keep the FDC key in your shell or `.env`. USDA deactivates keys found in public repositories.
