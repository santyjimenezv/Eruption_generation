#!/usr/bin/env python3
"""Generate a wind table matching the column structure of wind_m060."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SECONDS_PER_YEAR = 365.25 * 24 * 3600
MSUN_CGS = 1.98847e33
KM_TO_CM = 1.0e5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a wind table with times, Lw (LSC), and constant v_ej "
            "in the fourth column."
        )
    )
    parser.add_argument("--t-f", type=float, help="Final time in years.")
    parser.add_argument("--t-ej", type=float, help="Ejection time scale in years.")
    parser.add_argument("--m-ej", type=float, help="Ejected mass in solar masses.")
    parser.add_argument("--v-ej", type=float, help="Ejection velocity in km/s.")
    parser.add_argument(
        "--n-steps",
        type=int,
        default=1000,
        help="Number of time samples between 0 and t_f (inclusive).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("wind_generated"),
        help="Output filename for the wind table.",
    )
    parser.add_argument(
        "--plot",
        type=Path,
        default=Path("wind_generated.png"),
        help="Output filename for the diagnostic plot.",
    )
    return parser.parse_args()


def prompt_if_missing(value: float | None, prompt: str) -> float:
    if value is not None:
        return value
    return float(input(prompt))


def compute_wind_table(
    t_f_years: float,
    t_ej_years: float,
    m_ej_msun: float,
    v_ej_km_s: float,
    n_steps: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    t_f = t_f_years * SECONDS_PER_YEAR
    t_ej = t_ej_years * SECONDS_PER_YEAR
    m_ej = m_ej_msun * MSUN_CGS
    v_ej = v_ej_km_s * KM_TO_CM

    times = np.linspace(0.0, t_f, n_steps)
    ratio = np.divide(times, t_ej, out=np.zeros_like(times), where=t_ej != 0)

    mw = np.zeros_like(times)
    valid = ratio != 0
    mw[valid] = (
        m_ej
        * (1.0 - np.exp(ratio[valid] ** 2))
        * ratio[valid] ** -2
        / (math.sqrt(math.pi) * t_ej)
    )

    lw = mw * v_ej**2
    return times, lw, np.full_like(times, v_ej)


def write_wind_table(
    output_path: Path, times: np.ndarray, lw: np.ndarray, v_ej: np.ndarray
) -> None:
    columns = 63
    data = np.zeros((times.size, columns))
    data[:, 0] = times
    data[:, 1] = lw
    data[:, 3] = v_ej
    fmt = " ".join(["% .8e"] * columns)
    output_path.write_text("\n".join(fmt % tuple(row) for row in data))


def plot_wind(output_path: Path, times: np.ndarray, lw: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(times, lw, label="Lw")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Lw [erg/s]")
    ax.set_title("Wind luminosity over time")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)


def main() -> None:
    args = parse_args()
    t_f = prompt_if_missing(args.t_f, "t_f [y]: ")
    t_ej = prompt_if_missing(args.t_ej, "t_ej [y]: ")
    m_ej = prompt_if_missing(args.m_ej, "M_ej [Msun]: ")
    v_ej = prompt_if_missing(args.v_ej, "v_ej [km/s]: ")

    times, lw, v_ej_values = compute_wind_table(
        t_f, t_ej, m_ej, v_ej, args.n_steps
    )
    write_wind_table(args.output, times, lw, v_ej_values)
    plot_wind(args.plot, times, lw)

    print(f"Wrote wind table to {args.output}")
    print(f"Saved plot to {args.plot}")


if __name__ == "__main__":
    main()
