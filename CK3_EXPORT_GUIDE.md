# CK3 Dynasty Export - Quick Reference

## Using the CK3 Export Feature

### Basic Steps
1. Run the main program:
   ```bash
   python main.py
   ```

2. Follow the interactive prompts to set up your dynasty:
   - Select configuration preset (Normal/Generous/Realistic)
   - Choose start date (CK3 bookmarks or custom)
   - Set patriarch birth year and dynasty expansion dates
   - Optionally show detailed statistics

3. When asked "What would you like to do?", enter `c` for CK3 export

4. Follow the CK3 export prompts:
   - Enter religion code (e.g., `jingxue`, `daoxue`, `catholic`, `tengrian`)
   - Choose whether to include death dates for living characters
   - Enter filename (default: `{DynastyName}_history.txt`)

5. File saves to `ck3_exports/` directory

### CK3 Religion Codes
Common examples for testing:
- Chinese religions: `jingxue`, `daoxue`, `wuism`
- Western religions: `catholic`, `orthodox`, `protestant`
- Islamic: `sunni`, `shia`
- Other: `tengrian`, `jewish`, `zoroastrian`

### CK3 Export Format

Each character entry follows this structure:
```
{dynasty_name}_character_{N} = {
    name = "{given_name}"
    dynasty = {dynasty_name}      # Only if part of dynasty
    religion = {religion_code}
    culture = {culture_name}
    father = {parent_character_id} # If applicable
    mother = {parent_character_id} # If applicable
    female = yes                    # Only for females
    
    {YYYY.M.D} = {                 # Birth date
        birth = yes
        effect = { ... }           # May include playable flag
    }
    
    {YYYY.M.D} = {                 # Marriage date
        add_spouse = {spouse_id}
    }
    
    {YYYY.M.D} = {                 # Death date
        death = yes
    }
}
```

### Key Features
- **Character IDs**: Auto-generated as `{dynasty_name}_character_1`, `{dynasty_name}_character_2`, etc.
- **Dates**: CK3 format (YYYY.M.D) with no leading zeros
- **Playable Flag**: Males under 30 at birth get `do_not_generate_starting_family` effect
- **Living Characters**: Can optionally include death dates (end_date + 1 day)
- **Marriages**: Both spouses linked with mutual `add_spouse` pointers

### Testing
Run the test suite:
```bash
python -m pytest test_ck3_export.py -v
```

Run the demo:
```bash
python demo_ck3_export.py
```

### File Locations
- **Generated files**: `ck3_exports/` directory
- **Export module**: `exporters/export_to_ck3.py`
- **Tests**: `test_ck3_export.py`
- **Demo**: `demo_ck3_export.py`

### Troubleshooting

**Q: Character IDs use capital letters (e.g., `Zhu_character_1`)**
A: This is correct behavior. CK3 handles both cases fine, and capitals match the dynasty name casing.

**Q: Dates look wrong in the output**
A: Make sure they follow YYYY.M.D format (no leading zeros). Example: `867.1.1` not `867.01.01`

**Q: Unicode characters in names are garbled when viewing in Windows**
A: The file is encoded correctly in UTF-8. Open with a modern editor or CK3 will handle it properly.

**Q: Marriage entries showing spouses twice**
A: This is correct - each marriage event appears twice (once for each spouse) so they're mutually linked.

### All Tests Passing ✅
- test_ck3_export_basic: File creation and basic format
- test_ck3_export_character_format: Format specification compliance
- All 9 existing tests: Still passing (no regressions)

### Next Steps
1. Export your dynasty to CK3 format
2. Import the file into Crusader Kings 3 history folder
3. Start a game with your generated dynasty
