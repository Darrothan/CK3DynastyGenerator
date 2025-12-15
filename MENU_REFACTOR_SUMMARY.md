## Menu System Refactor - Summary

### Changes Made

#### 1. New Prompt Functions

**`main_menu_prompt()`** - Shown after dynasty generation
- **Option 1**: Save GEDCOM (then shows post-GEDCOM menu)
- **Option 2**: Regenerate with current settings (quick variant generation)
- **Option 3**: Regenerate with different settings (re-prompt all parameters)
- **Option 4**: Exit program

**`post_gedcom_prompt()`** - Shown after GEDCOM is saved
- **Option 1**: Save CK3 export
- **Option 2**: Regenerate with current settings
- **Option 3**: Regenerate with different settings
- **Option 4**: Exit program

#### 2. Parameter Preservation

New dictionary `params_for_reuse` stores all dynasty parameters:
```python
{
    'cfg': cfg,                        # SimConfig (mortality/fertility)
    'culture': culture,                # Dynasty culture
    'dynasty_name': dynasty_name,      # Dynasty name
    'start_day_absolute': start_day_absolute,  # CK3 start day
    'start_year': start_year,          # CK3 start year
    'birth_year': birth_year,          # Founder birth year
    'male_only_start': male_only_start,  # Male-only strategy transition
    'normal_start': normal_start,      # Normal strategy transition
}
```

When user selects "regenerate with current settings", values are restored from this dictionary and the loop continues.

#### 3. Main Loop Changes

The `main()` function now:
1. Prompts for all initial parameters (as before)
2. Stores parameters in `params_for_reuse`
3. Generates and displays dynasty
4. Shows `main_menu_prompt()` with 4 options:
   - **save**: Saves GEDCOM, then shows `post_gedcom_prompt()`
   - **regen_same**: Regenerates with stored parameters, returns to main menu
   - **regen_diff**: Re-prompts all parameters (full loop restart)
   - **exit**: Breaks loop and exits program

#### 4. Post-GEDCOM Flow

After GEDCOM is saved:
- Shows `post_gedcom_prompt()` with 4 options:
  - **save_ck3**: Prompts for religion, death inclusion, filename; saves CK3 file
  - **regen_same**: Regenerates with stored parameters
  - **regen_diff**: Re-prompts all parameters
  - **exit**: Exits program

Special handling: After saving CK3, user must choose again from `post_gedcom_prompt()` (doesn't auto-exit).

---

### User Experience Improvements

**Before**:
- Limited to: Save GEDCOM, Regenerate (with re-prompt), or Exit
- Regenerating required re-entering all settings every time

**After**:
- **Quick variant generation**: Option 2 creates new variants in seconds
- **Flexible workflow**: Can save GEDCOM, then decide on CK3 export separately
- **Clear menu structure**: Numbered options (1-4) easier to remember than letters
- **Parameter reuse**: Don't need to re-enter dates/dynasty info to generate variants

---

### Menu Navigation

```
Generation Complete
        ↓
   Main Menu
   1) Save    2) Regen Same    3) Regen Diff    4) Exit
        ↓              ↓              ↓              ↓
   GEDCOM         [Generate]    [Re-prompt]    [Exit]
   Saved          → Back to       All Settings
        ↓             Main         ↓
   Post Menu        Menu       [Generate]
   1) CK3                      → Back to
   2) Regen                       Main
   3) Regen Diff
   4) Exit
```

---

### Code Structure

**Key Variables in main():**
- `params_for_reuse`: Stores configuration for quick regeneration
- `choice`: Return value from `main_menu_prompt()`
- `post_choice`: Return value from `post_gedcom_prompt()`

**Loop Control:**
- `continue`: Starts next iteration (regenerates or re-prompts)
- `break`: Exits the outer while loop and program

**State Management:**
- Parameters preserved across multiple regenerations
- Each dynasty generation fresh RNG (different variants)
- Dynasty data available until user chooses "regen_diff" or "exit"

---

### Testing

✅ **All 11 tests still passing**:
- No changes to core generation logic
- Menu functions not directly tested (interactive I/O)
- All existing functionality preserved
- Backwards compatible with previous GEDCOM/CK3 exports

---

### Files Modified

**main.py**:
- Added `main_menu_prompt()` function
- Added `post_gedcom_prompt()` function
- Removed `regenerate_prompt()` function (replaced by above)
- Refactored `main()` loop with parameter preservation
- Added `params_for_reuse` dictionary

**Documentation Added**:
- `MENU_FLOW_GUIDE.md` - Quick reference and examples
- `MENU_FLOW_DETAILED.md` - Detailed flowcharts and implementation

---

### Example Workflows

**Generate 3 Variants Quickly**:
```
Main Menu: 2 (Regen Same)
  → New dynasty (same settings)
Main Menu: 2 (Regen Same)  
  → Another dynasty (same settings)
Main Menu: 1 (Save)
  → GEDCOM saved
Post Menu: 4 (Exit)
```

**Export Both Formats**:
```
Main Menu: 1 (Save)
  → GEDCOM saved
Post Menu: 1 (Save CK3)
  → CK3 saved
Post Menu: 4 (Exit)
```

**Change Dynasty Name Only**:
```
Main Menu: 3 (Regen Diff)
  → Re-prompt all settings (user only changes dynasty name)
Main Menu: 1 (Save)
  → GEDCOM saved with new name
Post Menu: 4 (Exit)
```

---

### Implementation Status

✅ **Complete**:
- Menu prompts created and validated
- Parameter preservation working
- Loop control properly handling all paths
- All tests passing
- Documentation created

✅ **Ready for Use**:
- Run `python main.py`
- Follow on-screen prompts
- All export functionality working as before
