# Wind Table Generator

This repository includes a small helper script for generating wind tables that
match the column structure of `wind_m060`. The script converts user inputs to
CGS units, computes the requested wind quantities, writes the output table, and
saves a diagnostic plot for verification.

## Usage

Run the script and provide inputs interactively:

```bash
python generate_wind_table.py
```

Or supply inputs on the command line:

```bash
python generate_wind_table.py \
  --t-f 5.0 \
  --t-ej 1.0 \
  --m-ej 0.1 \
  --v-ej 3000 \
  --n-steps 1000 \
  --output wind_generated \
  --plot wind_generated.png
```

### Inputs

* `t_f` (years): Final time of data generation.
* `t_ej` (years): Ejection time scale.
* `M_ej` (solar masses): Ejected mass.
* `v_ej` (km/s): Ejection velocity.

### Outputs

* Table file (default: `wind_generated`) with 63 columns matching `wind_m060`:
  * Column 1: time in seconds.
  * Column 2 (LSC): `Lw`.
  * Column 4: constant `v_ej` (cm/s).
* Plot image (default: `wind_generated.png`) showing `Lw` vs time.
