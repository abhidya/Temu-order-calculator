# Temu Order Calculator

Small local CLI for estimating an order total from a CSV export.

## Demo

```bash
python3 calculator.py
```

The default command reads `sample_order.csv` and prints line totals plus the
final `order_total`.

## CSV format

Required columns:

- `item`
- `quantity`
- `unit_price`
- `discount`
- `tax`

## Portfolio framing

This is now a small utility demo, not a full Temu integration. It does not call
Temu or scrape order history.
