# Auto Shop no-OCR Design

## Objective

Replace the current per-item image search and stock OCR flow with a fast,
deterministic Gold Shop sweep. The automation must make no OCR calls and must
never issue a purchase click unless it has verified both the shop layout and
the item card that owns the click target.

This design applies to the existing Gold Shop only. Future shops can add their
own layout manifest without changing the Gold Shop rules.

## Confirmed purchase semantics

- A numeric target `N` means: attempt to buy up to `N` units once during the
  current UTC day. The game may clamp the entered value to the remaining stock.
- `Max` means: select the modal's Max action and purchase the remaining stock
  once during the current UTC day.
- Manual purchases are intentionally not subtracted from numeric targets. No
  screen number is read to infer them.
- A closed purchase modal after the macro clicked the final Buy is sufficient
  confirmation that the single daily purchase attempt was accepted.
- The UI must describe a successful numeric action as executed today, not as
  an exact total owned or an exact number confirmed from stock.

This deliberately trades exact manual-purchase reconciliation for speed and
predictability. Without reading a game number, it is impossible to calculate
the difference between a daily target and manual purchases.

## Gold Shop layout manifest

The docked game uses the normalized 1152x756 reference viewport already used
by `core.vision`. All card and button rectangles remain in that coordinate
space, then existing coordinate conversion maps clicks to the actual window.

The Gold Shop is treated as three verified list positions, not eleven separate
scroll destinations:

| Position | Fully actionable cards |
| --- | --- |
| Top | Cursed Boba, Red Flower, Frown Fruit, Delicious Pie |
| Middle | Mana Flask, Trait Crystal, Sprite (Grey), Equipment Reroll |
| Bottom | Equipment Lock, Stat Reroll, Stat Lock |

Every entry has a fixed card slot within its verified position. A slot holds:

- the expected item key;
- a bounded identity region;
- the initial Buy region;
- the terminal-label region;
- a requirement that the Buy region is fully inside the list viewport.

The identity region is an RGBA-masked reference made from the stable card
parts: item icon, item name, and fixed border details. It excludes the stock
label, dynamic price, button state, and animated card areas. A literal full
card screenshot is not used because those dynamic parts would make it fail
after an item sells out or changes state.

Existing reference screenshots can supply these masked identity references;
new manual screenshots are optional, not a prerequisite.

## Session and alignment flow

1. Navigate to Areas, Shop, Gold Shop, tilt the camera, press E, and select
   the Gold Shop tab as today.
2. Reset the item list upward once. Confirm the top position with one or two
   top sentinel identities before processing any card.
3. Process enabled Top cards in slot order.
4. Move down in bounded pulses. After each pulse, examine only the fixed list
   viewport and accept the Middle position only when its sentinel identities
   match their slots.
5. Process enabled Middle cards in slot order.
6. Move down in bounded pulses while inspecting the list scrollbar handle.
   The absolute bottom is reached only when the handle's lower edge rests at
   the lower end of its rail; it does not rely on a precomputed wheel count
   or a full-frame pixel comparison affected by card animation.
7. Confirm the Bottom sentinels and require the Stat Lock Buy region to be
   fully visible before processing Bottom cards.
8. Process Equipment Lock, Stat Reroll, then Stat Lock.

Stat Lock has a stricter bottom rule than the other items. Its card identity
alone is insufficient: the list must be at its physical end and its complete
Buy area must be visible. Otherwise the macro stops the Bottom pass without
clicking it.

If a sentinel or expected card does not match after the bounded alignment
attempt, the entire affected position is skipped. The macro never guesses a
slot or reuses coordinates from another list position.

## Per-card purchase flow

For each enabled, identity-confirmed slot:

1. Search the terminal-label region for `Out of Stock` and `Max Inventory`.
   Either label completes the item for the UTC day without opening a modal.
2. Inspect the known Buy rectangle by its green button-face pixel fraction.
   This is a color and geometry check, not a price-template search.
3. If the region is green, click its calculated center and wait briefly for
   the Cancel anchor in the purchase modal.
4. If the modal opens:
   - for `Max`, click the Max control derived from Cancel, then immediately
     click the final Buy control derived from Cancel;
   - for a numeric target, focus the input derived from Cancel, enter the
     number, then click the final Buy control.
5. Treat disappearance of Cancel after the final Buy as success and persist a
   one-time executed-today state. Do not reread the card or scan stock.
6. If Cancel remains, click the required far-right point inside Cancel and
   mark the action uncertain. It must not receive another automatic Buy click
   in the same UTC day without a user reset.

A non-green Buy rectangle without a terminal label is not interpreted as Out
of Stock. It can mean insufficient Gold or an unexpected render. The item is
left actionable for a future safe pass, with no purchase recorded and no
dangerous retry in the current shop visit.

## Safety invariants

- No OCR function is imported or called by the Gold Shop runtime path.
- At most one final Buy click is issued for an item in one UTC period.
- An ambiguous card identity, scroll position, button state, or modal state
  always results in no Buy click.
- The macro does not reset the list to the top between cards.
- Buy coordinates are valid only for the current verified slot and are never
  carried across a scroll.
- Disabled Buy, missing modal, and unknown layout states never become an
  Out-of-Stock result by inference.

## Expected performance

The common nine-item run should use three layout alignments, a maximum of
three list transitions, and one modal interaction per enabled purchasable
item. It should be dominated by Roblox's modal animation rather than visual
search or OCR. The target is roughly 20 to 40 seconds for a full enabled
store, subject to Roblox rendering and input latency.

## Implementation boundaries

- `core/runner_shop.py` becomes a session-oriented sweep rather than calling
  an item finder that resets and scrolls for every item.
- `core/auto_shop_vision.py` owns fixed slot geometry, masked identity checks,
  green-button classification, viewport-change detection, and modal-relative
  geometry.
- `core/auto_shop.py` owns the no-OCR purchase state semantics and UTC reset
  normalization.
- The pywebview settings bridge and Resource UI preserve existing enabled and
  target settings. They only change labels/statuses needed to distinguish
  executed today, terminal labels, blocked, and uncertain actions.

No generic shop abstraction or unrelated runner refactor is included.

## Verification

- Unit tests prove that the runtime flow cannot call stock OCR.
- Offline visual tests cover each top, middle, and bottom slot using the
  supplied Gold Shop screenshots, including terminal labels and dynamic Buy
  prices.
- Alignment tests prove that an unmatched sentinel causes no click.
- A bottom-alignment test proves Stat Lock is not processed until both the
  viewport is stationary at the end and its full Buy region is visible.
- Modal tests cover numeric, Max, successful closing, and non-closing Cancel
  recovery.
- Tests cover a disabled Buy with no terminal label and confirm it never
  becomes an Out-of-Stock completion.
- Run Ruff, the full pytest suite, Python compilation, and `node --check
  ui/app.js` before a live run.
- The first live validation uses one cheap numeric item, then one Max item,
  then a Bottom run containing Stat Lock.
