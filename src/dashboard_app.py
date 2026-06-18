"""
src/dashboard_app.py
Minimal Dash app combining diversity curve + paleogeographic map
for the Permian-Triassic survival modeling project.

Run with: python src/dashboard_app.py
Then open http://127.0.0.1:8050 in a browser.
"""

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

DIVERSITY_PATH = "results/processed/diversity_raw_vs_corrected.csv"
OCCURRENCE_PATH = "data/processed/occurrences_clean.csv"
SURVIVAL_PATH = "data/processed/survival_labels_genus.csv"

diversity_df = pd.read_csv(DIVERSITY_PATH)
diversity_df = diversity_df.rename(columns={"index": "interval"})

# --- Build occ_df the same way notebook 07 does: merge occurrence-level
# data with genus-level survival labels, since occurrences_clean.csv does
# not have survival info and survival_labels_genus.csv has no coordinates.
occ_raw = pd.read_csv(OCCURRENCE_PATH)
survival = pd.read_csv(SURVIVAL_PATH)

occ_raw = occ_raw.rename(columns={
    "accepted_name": "genus",
    "early_interval": "interval",
    "lat": "paleolat",   # NOTE: these are modern coordinates, not true
    "lng": "paleolng",   # paleocoordinates -- see project README/report
})

occ_df = occ_raw.merge(survival, on=["genus", "interval"], how="inner")

interval_order = ["Changhsingian", "Griesbachian", "Dienerian", "Smithian",
                   "Spathian", "Aegean", "Bithynian"]
intervals_present = [i for i in interval_order if i in occ_df["interval"].unique()]
extra_intervals = [i for i in occ_df["interval"].unique() if i not in intervals_present]
intervals_available = intervals_present + sorted(extra_intervals)

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Permian-Triassic Survival Modeling Dashboard"),

    html.Div([
        html.H4("Diversity Through Time (Raw vs. Sampling-Corrected)"),
        dcc.Graph(
            figure=px.line(
                diversity_df, x="interval",
                y=["raw_richness", "corrected_richness"],
                markers=True,
                labels={"value": "Genus richness", "interval": "Time interval"},
            )
        ),
    ]),

    html.Div([
        html.H4("Fossil Occurrence Map"),
        html.P("Note: coordinates shown are modern present-day positions, "
               "not plate-tectonic-reconstructed paleocoordinates.",
               style={"fontSize": "0.85em", "color": "#666"}),
        html.Label("Select time interval:"),
        dcc.Dropdown(
            id="interval-dropdown",
            options=[{"label": i, "value": i} for i in intervals_available],
            value=intervals_available[0] if intervals_available else None,
        ),
        dcc.Graph(id="occurrence-map"),
    ]),
])


@app.callback(
    Output("occurrence-map", "figure"),
    Input("interval-dropdown", "value"),
)
def update_map(selected_interval):
    filtered = occ_df[occ_df["interval"] == selected_interval]
    fig = px.scatter_geo(
        filtered, lat="paleolat", lon="paleolng",
        color="survived", hover_name="genus",
        projection="orthographic",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)