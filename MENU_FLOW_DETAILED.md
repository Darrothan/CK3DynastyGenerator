## Menu Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│         MAIN MENU (After Dynasty Generation)                │
│  1) Save  2) Regen Same  3) Regen Diff  4) Exit             │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
        ┌──────┘              │              │
        │                     │              │
        ▼                     ▼              ▼
    [Save GEDCOM]      [Regen Same]   [Regen Diff]
         │                  │              │
         │                  │              │
         ▼                  │              │
    [Show Post Menu]        │              │
         │                  │              │
         ├──────────────────┘              │
         │                                 │
         ▼                                 ▼
    ┌─────────────────────────────┐   [Ask All Settings Again]
    │   POST-GEDCOM MENU          │       │
    │ 1) Save CK3                 │       │
    │ 2) Regen Same               │       │
    │ 3) Regen Diff               │       │
    │ 4) Exit                     │       │
    └──┬──────────┬──────────┬────┘       │
       │          │          │            │
       ▼          ▼          ▼            │
   [Save CK3] [Regen]  [Regen]          │
       │       Same      Diff             │
       │        │         │               │
       └────────┴─────────┴───────────────┤
                                         │
                      ┌──────────────────┘
                      │
                      ▼
         ┌──────────────────────────┐
         │   Back to Main Menu      │
         │ (with same dynasty data) │
         └──────────────────────────┘
```

---

## User Journey Examples

### Path A: Save Both Exports
```
Main Menu: 1 (Save)
  ↓
GEDCOM saved
  ↓
Post-GEDCOM Menu: 1 (Save CK3)
  ↓
CK3 saved
  ↓
Post-GEDCOM Menu: 4 (Exit)
  ↓
Program exits
```

### Path B: Generate Variants Quickly
```
Main Menu: 1 (Save)
  ↓
GEDCOM saved
  ↓
Post-GEDCOM Menu: 2 (Regen Same)
  ↓
New dynasty (same settings) generated
  ↓
Main Menu: 2 (Regen Same) 
  ↓
Another new dynasty generated
  ↓
Main Menu: 4 (Exit)
```

### Path C: Modify Settings
```
Main Menu: 3 (Regen Diff)
  ↓
Ask all settings again
  ↓
User enters NEW settings
  ↓
New dynasty (different settings) generated
  ↓
Main Menu: 1 (Save)
  ↓
GEDCOM saved
  ↓
Post-GEDCOM Menu: 4 (Exit)
```

### Path D: Just Export, No Regen
```
Main Menu: 1 (Save)
  ↓
GEDCOM saved
  ↓
Post-GEDCOM Menu: 1 (Save CK3)
  ↓
CK3 saved
  ↓
Post-GEDCOM Menu: 4 (Exit)
```

---

## Key Implementation Details

### Parameter Reuse Dictionary
```python
params_for_reuse = {
    'cfg': cfg,                        # Mortality/fertility config
    'culture': culture,                # Dynasty culture
    'dynasty_name': dynasty_name,      # Dynasty name
    'start_day_absolute': start_day_absolute,  # CK3 start date (absolute days)
    'start_year': start_year,          # CK3 start date (year)
    'birth_year': birth_year,          # Founder birth year
    'male_only_start': male_only_start,  # Male-only strategy start year
    'normal_start': normal_start,      # Normal strategy start year
}
```

### Loop Control
- **`continue`**: Re-runs the outer loop with new/same parameters
- **`break`**: Exits the program
- **Parameter reassignment**: When regenerating with same settings, values are restored from dict

### Menu Validation
- Both `main_menu_prompt()` and `post_gedcom_prompt()` validate input
- Invalid choices loop back with error message
- Choices are numbered 1-4 for clarity
