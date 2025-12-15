## Updated Menu Flow - Quick Reference

### Main Menu (After Dynasty Generation)
```
What would you like to do? (1 = save, 2 = regen same settings, 3 = regen diff settings, 4 = exit)
```

**Option 1: Save GEDCOM & Optional CK3**
- Prompts for GEDCOM filename and saves to `gedcom_exports/`
- After GEDCOM is saved, shows Post-GEDCOM menu

**Option 2: Regenerate with Current Settings**
- Immediately regenerates a new dynasty using the same parameters
- No prompts needed - just generates and shows new stats
- User is then returned to Main Menu

**Option 3: Regenerate with Different Settings**
- Goes back to the beginning to ask for all parameters again
- User can change config, dynasty name, dates, etc.

**Option 4: Exit**
- Exits the program

---

### Post-GEDCOM Menu (Only shown after saving GEDCOM)
```
What would you like to do? (1 = save CK3, 2 = regen same settings, 3 = regen diff settings, 4 = exit)
```

**Option 1: Save CK3**
- Prompts for religion code
- Prompts for living character death inclusion
- Prompts for CK3 filename and saves to `ck3_exports/`
- Returns to Main Menu with same dynasty (to optionally regen or exit)

**Option 2: Regenerate with Current Settings**
- Immediately regenerates a new dynasty using the same parameters
- Returns to Main Menu with new dynasty

**Option 3: Regenerate with Different Settings**
- Goes back to prompt for all parameters again

**Option 4: Exit**
- Exits the program

---

## Usage Examples

### Example 1: Save Both Formats
1. Generate dynasty
2. Choose option 1 (save) → GEDCOM saved
3. Choose option 1 (save CK3) → CK3 saved
4. Choose option 4 (exit) or option 2 (regen same)

### Example 2: Generate Multiple Variants
1. Generate dynasty
2. Choose option 2 (regen same) → New dynasty with same settings
3. Choose option 2 again (regen same) → Another variant
4. Choose option 4 (exit)

### Example 3: Change One Parameter
1. Generate dynasty
2. Choose option 3 (regen different) → Prompted for all settings
3. Keep most settings the same, only change dynasty name or dates
4. New dynasty generated with modified settings

---

## Implementation Notes

- **Parameters Preserved**: When regenerating with same settings, all parameters are stored in `params_for_reuse` dictionary
- **Menu State**: The main loop correctly handles each menu choice and transitions
- **Backwards Compatible**: GEDCOM and CK3 export functionality unchanged
- **Quick Regen**: Option 2 at main menu is the fastest way to generate variants without re-entering all settings

