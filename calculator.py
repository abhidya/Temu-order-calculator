"""Small CLI for estimating Temu order totals from a CSV export."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path


@dataclass(frozen=True)
class OrderLine:
    item: str
    quantity: int
    unit_price: Decimal
    discount: Decimal
    tax: Decimal

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity

    @property
    def total(self) -> Decimal:
        return self.subtotal - self.discount + self.tax


def money(value: str) -> Decimal:
    return Decimal(value.strip().replace("$", "") or "0").quantize(Decimal("0.01"))


def load_order(path: Path) -> list[OrderLine]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [
            OrderLine(
                item=row["item"],
                quantity=int(row["quantity"]),
                unit_price=money(row["unit_price"]),
                discount=money(row.get("discount", "0")),
                tax=money(row.get("tax", "0")),
            )
            for row in reader
        ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate an order total from a CSV file.")
    parser.add_argument("csv_path", nargs="?", type=Path, default=Path("sample_order.csv"))
    args = parser.parse_args()

    lines = load_order(args.csv_path)
    total = sum((line.total for line in lines), Decimal("0.00"))
    for line in lines:
        print(f"{line.item}: qty={line.quantity} subtotal=${line.subtotal} total=${line.total}")
    print(f"order_total=${total.quantize(Decimal('0.01'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
