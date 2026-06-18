# Disentangling Biological Signal from Sampling Bias: A Machine Learning Investigation of Genus Survival Across the Permian–Triassic Mass Extinction

## Overview

This project investigates which biological and ecological traits are genuinely associated with genus-level survival across the Permian–Triassic (P-T) boundary (~252 million years ago), using fossil occurrence data from the [Paleobiology Database](https://paleobiodb.org). The central question is not "what predicts extinction" in a causal sense — occurrence data cannot support that claim directly — but rather: **which traits correlate with survival once the confounding effect of uneven fossil sampling is explicitly controlled for?**

Four well-preserved marine invertebrate groups are used: Bivalvia, Brachiopoda, Gastropoda, and Ammonoidea.

## Why this matters

Raw fossil occurrence counts conflate two signals: genuine biological/ecological change, and sampling intensity (how much rock from a given time period has been studied, how many collections exist, how much outcrop area is exposed). A model trained naively on occurrence-derived features risks learning "genera that happen to be in well-sampled rocks survive" rather than anything biological. This project builds two parallel models — one naive, one with explicit sampling-bias controls — and compares them directly, rather than reporting a single black-box result.

## Key finding

Stratigraphic **duration** retained essentially identical SHAP feature importance (≈0.20) whether or not sampling-bias controls were included in the model. In contrast, **occurrence count** and **environmental breadth** lost roughly half their apparent importance once sampling-control features (collection count, sampling intensity, formation breadth) were added — indicating these two features were partly tracking preservation bias rather than pure biological signal in the naive model.

| Feature | Naive model (mean \|SHAP\|) | Corrected model (mean \|SHAP\|) | Change |
|---|---|---|---|
| Duration | 0.2003 | 0.2003 | Unchanged — robust signal |
| Occurrence count | 0.0744 | 0.0328 | ↓ ~56% |
| Lazarus flag | 0.0480 | 0.0437 | Roughly stable |
| Latitudinal range | 0.0481 | 0.0322 | ↓ ~33% |
| Longitudinal range | 0.0513 | 0.0283 | ↓ ~45% |
| Environmental breadth | 0.0236 | 0.0098 | ↓ ~58% |

This pattern — duration surviving correction while several other features partly collapse — is consistent with longstanding palaeobiological observations on taxon longevity and extinction risk, and is discussed further in the project report.

## Repository structure

```
permian-triassic-survival-ml/
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── raw/                  (PBDB downloads — excluded from version control, see Setup)
│   └── processed/            (cleaned, binned, feature-engineered tables)
├── notebooks/
│   ├── 01_data_acquisition_cleaning.ipynb
│   ├── 02_sampling_corrected_diversity.ipynb
│   ├── 03_survival_labels.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_naive_vs_corrected_models.ipynb
│   ├── 06_shap_explainability.ipynb
│   └── 07_visualization_dashboard.ipynb
├── src/
│   ├── pbdb_download.py
│   ├── subsampling.py         (rarefaction implementation)
│   ├── survival_labels.py
│   ├── features.py
│   ├── models.py
│   ├── utils.py
│   └── dashboard_app.py       (standalone interactive Dash app)
└── results/
    ├── figures/                (final static + interactive visual outputs)
    ├── processed/              (saved diversity curves, SHAP summaries)
    └── rarefaction_summary.csv
```

## Methods summary

**Data.** Occurrence and collection-level records for Bivalvia, Brachiopoda, Gastropoda, and Ammonoidea, spanning the Late Permian (Changhsingian) through Middle Triassic, downloaded from the PBDB API.

**Sampling correction.** Raw genus richness per time interval is compared against rarefied (subsampled) richness to assess how much of the apparent Permian–Triassic diversity collapse is attributable to reduced sampling effort near the boundary, rather than purely biological turnover.

**Survival labels.** A genus is labeled as surviving if it appears in the subsequent time interval. Lazarus taxa (genera that disappear for one interval and reappear later) are flagged explicitly via a `lazarus` indicator rather than silently mislabeled as extinct.

**Features.** Each biological feature (occurrence count, geographic range, environmental breadth, stratigraphic duration, Lazarus flag) is paired with a sampling-control feature (collection count, sampling intensity, formation breadth) so that the contribution of preservation bias can be isolated.

**Models.** Two Random Forest classifiers are trained on identical train/test splits: a naive model (biological features only) and a corrected model (biological + sampling-control features). SHAP values are computed for both, and feature importance is compared directly to identify which biological signals are robust to sampling-bias correction.

**Limitations.** Coordinates used in the occurrence map (`results/figures/paleogeographic_map.html`) are modern present-day latitude/longitude, not plate-tectonic-reconstructed paleocoordinates — true paleogeographic positions were not available in this data pull. The sampling-effort proxy used in the diversity comparison is occurrence count rather than strict collection count, though both serve the same diagnostic purpose. These are discussed further in the full report.

## Setup

```bash
git clone https://github.com/dheerajtingilikar-hash/permian-triassic-survival-ml.git
cd permian-triassic-survival-ml

python -m venv .venv
.venv\Scripts\activate        # Windows PowerShell
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Raw PBDB downloads are not included in this repository (see `.gitignore`) since they are large and freely re-downloadable. Run `notebooks/01_data_acquisition_cleaning.ipynb` first to regenerate `data/raw/` and `data/processed/occurrences_clean.csv` from the PBDB API directly.

## How to run

Run the notebooks **in order** — each depends on outputs saved by the previous one:

```
01_data_acquisition_cleaning.ipynb     → cleans and saves occurrence data
02_sampling_corrected_diversity.ipynb  → builds rarefaction-corrected diversity curves
03_survival_labels.ipynb               → constructs genus-level survival labels
04_feature_engineering.ipynb           → builds paired biological + sampling-control features
05_naive_vs_corrected_models.ipynb     → trains both Random Forest models
06_shap_explainability.ipynb           → computes and saves SHAP feature importance
07_visualization_dashboard.ipynb       → generates all final figures
```

For each notebook, use **Restart & Run All** to ensure a clean, reproducible execution from a fresh kernel.

### Viewing results without re-running anything

Static figures are already saved in `results/figures/`:
- `diversity_raw_vs_corrected.png`
- `shap_naive_vs_corrected.png`
- `paleogeographic_map.html` (open directly in a browser — GitHub does not render interactive HTML inline)

### Running the interactive dashboard

```bash
python src/dashboard_app.py
```

Then open `http://127.0.0.1:8050` in a browser. Press `Ctrl+C` in the terminal to stop the server.

## Data source

[Paleobiology Database](https://paleobiodb.org) (PBDB) — occurrence and collection-level data accessed via the public Data Service API.

## License

See [LICENSE](LICENSE).
