# app.py
import streamlit as st
import altair as alt
import pydytuesday
import pandas as pd

# Read country visa datasets
pydytuesday.get_date('2025-09-09')
country_lists = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-09-09/country_lists.csv')
rank_by_year = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-09-09/rank_by_year.csv')

# See how the information is given
print(country_lists.info())

import json
json_data = country_lists['visa_free_access'].apply(lambda x: json.loads(x)[0])

country_lists = pd.read_csv("country_lists.csv").rename(
    columns={"code": "origin_code", "country": "origin_country"}
)

import gdown

# Access to my datasets (population)
url = 'https://drive.google.com/file/d/1vUfW1osY_yzNiaBI2vf2FUG8KHf3Fmvi/view?usp=sharing'

# Download file content as bytes
content = gdown.download(url, quiet=False, fuzzy=True)
# If gdown returns the filename, you can read directly
population = pd.read_csv(content)

# Access to my datasets (population)
url2 = 'https://drive.google.com/file/d/19I_DOB0Mv3pJpjopHqzhG9jkA63xeCGF/view?usp=drive_link'

# Download file content as bytes
content = gdown.download(url2, quiet=False, fuzzy=True)
# If gdown returns the filename, you can read directly
gdp = pd.read_csv(content)

"""Problem with different datasets is that they do not have the same country names nor country codes, so let me first do some operations to be able to combine them properly:"""

# Lets normalize country names form my datasets
def normalize_country_name(name):
    if isinstance(name, str):
        return (
            name.strip()          # remove leading/trailing spaces
                .lower()           # make lowercase
                .replace(" ", "_") # unify spacing
                .replace("-", "_") # unify hyphens and underscores
        )
    return name

country_lists["origin_country_norm"] = country_lists["origin_country"].apply(normalize_country_name)
country_map = dict(zip(country_lists["origin_code"], country_lists["origin_country_norm"]))
population["origin_country_norm"] = population["Country Name"].apply(normalize_country_name)
gdp["origin_country_norm"] = gdp["Country Name"].apply(normalize_country_name)

print(country_lists["origin_country_norm"])
print(population["origin_country_norm"])

# As we can see we even have more countries in one dataset than in the other,
# fotunately the one with less is the one from which we are gathering the visa
# information

set1 = set(country_lists["origin_country_norm"])
set2 = set(population["origin_country_norm"])

set3 = set(gdp["origin_country_norm"])

only_in_1 = set1 - set2
only_in_2 = set2 - set1
print("Countries only in dataset 1:", only_in_1)
print("Countries only in dataset 2:", only_in_2)

# Now we can look at these names from the set 2 and normalize them in both
manual_corrections = {
    "the_gambia": "gambia,_the",
    "iran": "iran,_islamic_rep.",
    "somalia": "somalia,_fed._rep.",
    "congo_(rep.)": "congo,_rep.",
    "congo_(dem._rep.)": "congo,_dem._rep.",
    "taiwan_(chinese_taipei)": "taiwan",
    "türkiye": "turkiye",
    "vietnam": "viet_nam",
    "laos": "lao_pdr",
    "palau_islands": "palau",
    "kyrgyzstan": "kyrgyz_republic",
    "macao_(sar_china)": "macao_sar,_china",
    "north_korea": "korea,_dem._people's_rep.",
    "south_korea": "korea,_rep.",
    "vatican_city": "holy_see",
    "yemen": "yemen,_rep.",
    "palestinian_territory": "west_bank_and_gaza",
    "micronesia": "micronesia,_fed._sts.",
    "brunei": "brunei_darussalam",
    "cape_verde_islands": "cabo_verde",
    "venezuela": "venezuela,_rb",
    "syria": "syrian_arab_republic",
    "slovakia": "slovak_republic",
    "bahamas": "bahamas,_the",
    "comoro_islands": "comoros",
    "hong_kong_(sar_china)": "hong_kong_sar,_china",
    "egypt": "egypt,_arab_rep."
}

def apply_manual_corrections(name):
    return manual_corrections.get(name, name)

country_lists["origin_country_norm"] = country_lists["origin_country_norm"].apply(apply_manual_corrections)

set1 = set(country_lists["origin_country_norm"])
set2 = set(population["origin_country_norm"])

only_in_1 = set1 - set2
only_in_2 = set2 - set1
print("Countries only in dataset 1:", only_in_1)

# And if we look at our population dataset we see that we are missing Taiwan nor
# Vatican City information. As Vatican City has roughtly 800 people of which 450
# are citizends, we will omit this group and clean it from the dataset.
country_lists = country_lists[country_lists["origin_country"] != "Vatican City"]

# As we cannot do the same with taiwan being a fairly big country, even tho it
# might not be considered one by many other countries we will add its information
# about the population to not delete it.

taiwan_row = pd.DataFrame([{
    "Country Name": "Taiwan",
    "Country Code": "TWN",
    "Indicator Name": "Population, total",
    "Indicator Code": "SP.POP.TOTL",
    "2006": 22790000,
    "2007": 22876000,
    "2008": 22973000,
    "2009": 23062000,
    "2010": 23162000,
    "2011": 23257000,
    "2012": 23268000,
    "2013": 23349000,
    "2014": 23441000,
    "2015": 23473000,
    "2016": 23540000,
    "2017": 23572000,
    "2018": 23589000,
    "2019": 23603000,
    "2020": 23561000,
    "2021": 23359000,
    "origin_country_norm": "taiwan"
}])

population = pd.concat([population, taiwan_row], ignore_index=True)
population[population["origin_country_norm"] == "taiwan"]

set1 = set(country_lists["origin_country_norm"])
set2 = set(population["origin_country_norm"])

only_in_1 = set1 - set2
only_in_2 = set2 - set1
print("Countries only in dataset 1:", only_in_1)

taiwan_gdp_pc_row = pd.DataFrame([{
    "Country Name": "Taiwan",
    "Country Code": "TWN",
    "Indicator Name": "GDP per capita (current US$)",
    "Indicator Code": "NY.GDP.PCAP.CD",
    "2006": 17013.0,
    "2007": 18630.0,
    "2008": 18620.0,
    "2009": 17360.0,
    "2010": 19630.0,
    "2011": 20950.0,
    "2012": 21270.0,
    "2013": 21910.0,
    "2014": 22610.0,
    "2015": 22330.0,
    "2016": 22820.0,
    "2017": 24570.0,
    "2018": 25850.0,
    "2019": 25960.0,
    "2020": 28490.0,
    "2021": 32600.0,
    "origin_country_norm": "taiwan"
}])

gdp = pd.concat([gdp, taiwan_gdp_pc_row], ignore_index=True)
gdp[gdp["origin_country_norm"] == "taiwan"]

set1 = set(country_lists["origin_country_norm"])
set2 = set(gdp["origin_country_norm"])

only_in_1 = set1 - set2
only_in_2 = set2 - set1
print("Countries only in dataset 1:", only_in_1)

"""## **Question 1**

Which continent has the most visa-free destinations? How does this vary when
considering population size?
"""

# 2) Columns that contain JSON text
visa_cols = [
    "visa_required",
    "visa_online",
    "visa_on_arrival",
    "visa_free_access",
    "electronic_travel_authorisation",
]

# 3) Safe parser that accepts JSON or Python-literal strings and unwraps [[...]]
def parse_cell(x):
    if pd.isna(x):
        return []
    if isinstance(x, str):
        try:
            # try JSON first
            v = json.loads(x)
        except Exception:
            try:
                # some CSV exporters save as Python literal
                v = literal_eval(x)
            except Exception:
                return []
    else:
        v = x

    # unwrap double brackets [[...]]
    if isinstance(v, list) and len(v) == 1 and isinstance(v[0], list):
        v = v[0]
    return v if isinstance(v, list) else []

# 4) Melt → parse → explode once
long = (
    country_lists
    .melt(
        id_vars=["origin_code", "origin_country"],
        value_vars=visa_cols,
        var_name="visa_type",
        value_name="entries"
    )
    .assign(entries=lambda d: d["entries"].apply(parse_cell))
    .explode("entries", ignore_index=True)
    .dropna(subset=["entries"])
)

# 5) Expand destination dict and finalize columns
normalized = (
    pd.concat([long.drop(columns=["entries"]),
               pd.json_normalize(long["entries"])], axis=1)
    .rename(columns={"code": "dest_code", "name": "dest_name"})
)

# 6) Optional: nicer labels
label_map = {
    "visa_required": "Visa required",
    "visa_online": "E-visa",
    "visa_on_arrival": "Visa on arrival",
    "visa_free_access": "Visa-free",
    "electronic_travel_authorisation": "Electronic travel authorisation",
}
normalized["visa_type"] = normalized["visa_type"].map(label_map)

# 7) Keep only rows with valid origin
normalized = normalized[normalized["origin_code"].notna()].reset_index(drop=True)

print(normalized.head(10))

origin_dest_counts = (
    normalized[normalized["visa_type"] == "Visa-free"]                # filter rows
    .groupby(["origin_code", "origin_country"])                       # group by origin
    ["dest_code"]
    .nunique()                                                        # count unique destinations
    .reset_index(name="num_visa_free_destinations")                   # rename count column
)

print(origin_dest_counts.head(100))

import pycountry_convert as pc

# Continent code -> pretty name
CONTINENT_NAME = {
    "AF": "Africa", "AS": "Asia", "EU": "Europe",
    "NA": "North America", "SA": "South America", "OC": "Oceania"
}

# Overrides for non-ISO / tricky codes
OVERRIDES = {
    "PS": "AS",  # Palestinian Territory -> Asia
    "XK": "EU",  # Kosovo -> Europe
    "CW": "NA",  # Curaçao
    "SX": "NA",  # Sint Maarten
    "BQ": "NA",  # Bonaire, Sint Eustatius & Saba
    "GG": "EU", "JE": "EU", "IM": "EU",
    "TL": "AS",  # Timor-Leste sometimes shows as TL
    "MF": "NA",  # Saint Martin -> North America
    "SS": "AF",  # South Sudan -> Africa
    "EH": "AF",  # Western Sahara -> Africa
    "PN": "OC",  # Pitcairn Islands -> Oceania
    "VA": "EU",  # Vatican City -> Europe
}

def a2_to_continent_name(a2):
    if pd.isna(a2):
        return None
    code = str(a2).strip().upper()
    # Try overrides first
    if code in OVERRIDES:
        return CONTINENT_NAME.get(OVERRIDES[code])
    # Try pycountry_convert
    try:
        cont_code = pc.country_alpha2_to_continent_code(code)
        return CONTINENT_NAME.get(cont_code)
    except Exception:
        return None

# Add continent name and normalized name to data
origin_dest_counts["origin_continent"] = origin_dest_counts["origin_code"].apply(a2_to_continent_name)
origin_dest_counts["origin_country_norm"] = origin_dest_counts["origin_code"].map(country_map)

# See how many mapped vs not mapped
print(origin_dest_counts.head(10))
#print(normalized["origin_continent"].value_counts(dropna=False))

print(population.head(10))

pop_2024 = population[["origin_country_norm", "2024"]].copy()
pop_2024 = pop_2024.rename(columns={"2024": "population_2024"})

origin_dest_counts = origin_dest_counts.merge(
    pop_2024,
    left_on="origin_country_norm",   # from origin_dest_counts
    right_on="origin_country_norm",    # from population
    how="left"                       # keep all countries, even if no population match
)
print(origin_dest_counts.head(10))

import altair as alt
import pandas as pd

df = origin_dest_counts.copy()

# Keep only complete rows
df = df.dropna(subset=[
    "origin_continent",
    "num_visa_free_destinations",
    "population_2024"
])

# Optional: define a logical continent order
continent_order = ["Africa", "Asia", "Europe", "North America", "South America", "Oceania"]

chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x=alt.X(
            "origin_continent:N",
            title="Continent",
            sort=continent_order,
            axis=alt.Axis(labelAngle=0, labelPadding=3, labelFontSize=11)

        ),
        y=alt.Y(
            "num_visa_free_destinations:Q",
            title="Visa-free destinations",
            scale=alt.Scale(zero=False)
        ),
        size=alt.Size(
            "population_2024:Q",
            title="Population (2024)",
            legend=None,
            scale=alt.Scale(type="sqrt", range=[10, 1000])
        ),
        color=alt.Color(
            "origin_continent:N",
            title="Continent",
            legend=None
        ),
        tooltip=[
            alt.Tooltip("origin_country:N", title="Country"),
            alt.Tooltip("num_visa_free_destinations:Q", title="Visa-free"),
            alt.Tooltip("population_2024:Q", title="Population", format=",.0f"),
        ]
    )
    .properties(
        title="Visa-Free Destinations by Country and Continent (Bubble size = Population 2024)",
        width=400,
        height=400
    )
)

chart

df = origin_dest_counts.copy()

# Keep only complete rows
df = df.dropna(subset=[
    "origin_continent",
    "num_visa_free_destinations",
    "population_2024"
])

# Optional: define a logical continent order
continent_order = ["Africa", "Asia", "Europe", "North America", "South America", "Oceania"]

chart1 = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x=alt.X(
            "num_visa_free_destinations:Q",
            title="Visa-free destinations",
            scale=alt.Scale(zero=False)
        ),
        y=alt.Y(
            "origin_continent:N",
            title="Continent",
            sort=continent_order,
            axis=alt.Axis(labelAngle=0, labelPadding=3, labelFontSize=11)

        ),
        size=alt.Size(
            "population_2024:Q",
            title="Population (2024)",
            legend=None,
            scale=alt.Scale(range=[10, 1000]) # treure el sqrt
        ),
        color=alt.Color(
            "origin_continent:N",
            title="Continent",
            legend=None
        ),
        tooltip=[
            alt.Tooltip("origin_country:N", title="Country"),
            alt.Tooltip("num_visa_free_destinations:Q", title="Visa-free"),
            alt.Tooltip("population_2024:Q", title="Population", format=",.0f"),
        ]
    )
    .properties(
        title="Visa-Free Destinations by Country and Continent (Bubble size = Population 2024)",
        width=600,
        height=250
    )
)

chart1

import altair as alt
import pandas as pd

df = origin_dest_counts.copy().dropna(subset=[
    "origin_continent", "num_visa_free_destinations", "population_2024"
])

# Wrap long names for readability
df["origin_continent_wrapped"] = df["origin_continent"].replace({
    "North America": "North\nAmerica",
    "South America": "South\nAmerica"
})

continent_order = ["Africa", "Asia", "Europe", "North\nAmerica", "South\nAmerica", "Oceania"]

# --- Main bubble chart ---
bubbles = (
    alt.Chart(df)
    .mark_circle(tooltip=False)
    .encode(
        x=alt.X("num_visa_free_destinations:Q",
                title="Visa-free destinations",
                scale=alt.Scale(zero=False)),
        y=alt.Y("origin_continent_wrapped:N",
                title="Continent",
                sort=continent_order,
                axis=alt.Axis(labelAngle=0)),
        size=alt.Size("population_2024:Q",
                      scale=alt.Scale( range=[10, 600]),
                      legend=None),
        color=alt.Color("origin_continent:N", legend=None)
    )
    .properties(width=600, height=350)
)

# --- Population distribution line (approximation via binning) ---
density = (
    alt.Chart(df)
    .transform_bin(
        "binned_destinations", "num_visa_free_destinations", bin=alt.Bin(maxbins=40)
    )
    .transform_aggregate(
        total_population="sum(population_2024)",
        groupby=["binned_destinations"]
    )
    .mark_line(color="gray", opacity=0.7)
    .encode(
        x=alt.X("binned_destinations:Q", title="Visa-free destinations"),
        y=alt.Y("total_population:Q", title="Total population (2024)",
                axis=alt.Axis(format=".2s"))
    )
    .properties(width=600, height=100)
)

# --- Combine vertically with shared X-axis ---
chart = alt.vconcat(
    bubbles,
    density
).resolve_scale(x="shared")

chart.properties(
    title="Visa-Free Destinations by Country and Continent (Bubble size = Population 2024)"
)

"""Which countries have experienced the greatest changes as visa-free countries between 2006 and 2021?"""

print(rank_by_year.info())

print(rank_by_year['year'].unique())

"""We do have more information that we want so we can remove >2021"""

rank_by_year_subset = rank_by_year[(rank_by_year['year'] >= 2006) & (rank_by_year['year'] <= 2021)]
print(rank_by_year_subset['year'].unique())
print(len(rank_by_year_subset))

japan_data = rank_by_year_subset[rank_by_year_subset['country'] == 'Japan']
print(japan_data[['year', 'visa_free_count']])

# Sort so diff() compares the correct previous year
rank_by_year_subset = rank_by_year_subset.sort_values(["country", "year"])

# Δ vs previous year (NaN for the first available year of each country)
rank_by_year_subset["delta_vs_prev"] = rank_by_year_subset.groupby("country")["visa_free_count"].diff()

# If you prefer 0 instead of NaN for the first year:
# df["delta_vs_prev"] = df.groupby("country")["visa_free_count"].diff().fillna(0)
print(rank_by_year_subset.head(100))

# Start with sorted data
df2 = rank_by_year_subset.sort_values(["country", "year"]).copy()

# Compute a flag indicating whether previous year's data exists
df2["has_prev_year"] = df2.groupby("country")["year"].diff() == 1

# Compute valid_delta based on data and continuity
df2["valid_delta"] = df2["has_prev_year"] & df2["delta_vs_prev"].notna()

# 🔧 Hardcode years that should never be considered valid
df2.loc[df2["year"].isin([2008, 2010]), "valid_delta"] = False

print(df2[["country", "year", "visa_free_count", "delta_vs_prev", "valid_delta"]].head(20))

import numpy as np
import pandas as pd
# --- Start from your dataset ---
rank_delta = rank_by_year_subset.sort_values(["country", "year"]).copy()
rank_delta["year"] = rank_delta["year"].astype(int)
# --- 1) Compute continuity and base valid flag ---
rank_delta["has_prev_year"] = rank_delta.groupby("country")["year"].diff().eq(1)
rank_delta["valid_delta"] = rank_delta["has_prev_year"] & rank_delta["delta_vs_prev"].notna()
# --- 2) Hardcoded invalid years ---
INVALID_YEARS = [2008, 2010]
rank_delta.loc[rank_delta["year"].isin(INVALID_YEARS), "valid_delta"] = False
# --- 3) Countries that start with 0 visa-free in 2006 ---
start_zero = ( rank_delta[rank_delta["year"] == 2006][["country", "visa_free_count"]] .assign(start_zero=lambda d: d["visa_free_count"].fillna(0).eq(0)) .set_index("country")["start_zero"] )
rank_delta["start_zero_2006"] = rank_delta["country"].map(start_zero).fillna(False)
# --- 4) Keep valid_delta=False until first non-zero appears (for zero-start countries) ---
rank_delta["ever_nonzero"] = rank_delta.groupby("country")["visa_free_count"].transform( lambda s: s.ne(0).cummax() )
mask_override = rank_delta["start_zero_2006"] & ~rank_delta["ever_nonzero"]
rank_delta.loc[mask_override, "valid_delta"] = False
# --- 5) Mark the first True after a False as "NEW" --- # Previous valid flag within each country (False for the first row)
rank_delta["prev_valid_delta"] = rank_delta.groupby("country")["valid_delta"].shift(fill_value=False)
# NEW when: this row is valid AND the previous row (same country) was NOT valid
rank_delta["is_new"] = rank_delta["valid_delta"] & (~rank_delta["prev_valid_delta"])
# (Optional) If you want NEW only for countries that started at 0 in 2006, use:
# rank_delta["is_new"] = rank_delta["is_new"] & rank_delta["start_zero_2006"]
# --- 6) Human-readable status column ---
rank_delta["delta_status"] = np.where( rank_delta["is_new"], "NEW", np.where(rank_delta["valid_delta"], "VALID", "INVALID") )
# (Optional) If you don't want to use NEW years in calculations, uncomment:
# rank_delta.loc[rank_delta["is_new"], "valid_delta"] = False
# --- (Optional) cleanup helpers ---
# rank_delta = rank_delta.drop(columns=["has_prev_year", "start_zero_2006", "ever_nonzero", "prev_valid_delta"])
# --- Quick sanity check ---
print( rank_delta.loc[:, ["country", "year", "visa_free_count", "delta_vs_prev", "valid_delta", "delta_status"]] .head(20) )

def compute_updated_diff(df):
    df = df.copy()
    df["updated_diff"] = df["delta_vs_prev"]  # start with original values

    # Sort for safety
    df = df.sort_values(["country", "year"])

    # Process each country separately
    for country, group in df.groupby("country"):
        group = group.copy()
        year_to_value = group.set_index("year")["visa_free_count"].to_dict()

        # Compute your specific differences
        diff_2008 = year_to_value.get(2008, 0) - year_to_value.get(2006, 0)
        diff_2010 = year_to_value.get(2010, 0) - year_to_value.get(2008, 0)

        # Apply to updated_diff
        df.loc[(df["country"] == country) & (df["year"] == 2008), "updated_diff"] = diff_2008
        df.loc[(df["country"] == country) & (df["year"] == 2010), "updated_diff"] = diff_2010

        # Set 2006, 2007, 2009 to 0
        df.loc[(df["country"] == country) & (df["year"].isin([2006, 2007, 2009])), "updated_diff"] = 0

    return df

# Apply the transformation
rank_delta = compute_updated_diff(rank_delta)

# Sanity check
print(rank_delta.loc[rank_delta["country"].isin(["Afghanistan", "Albania"]),
                     ["country", "year", "visa_free_count", "delta_vs_prev", "updated_diff"]])

import altair as alt
from vega_datasets import data
import pandas as pd

# Load world map topology
countries = alt.topo_feature(data.world_110m.url, 'countries')

# Example data (country ISO numeric id + value)
values = pd.DataFrame({
    'id': [4, 8, 12, 32, 36, 40, 50, 56, 68, 76],  # ISO numeric codes
    'country': ['Afghanistan', 'Albania', 'Algeria', 'Argentina', 'Australia',
                'Austria', 'Bangladesh', 'Belgium', 'Bolivia', 'Brazil'],
    'gdp_per_capita': [1800, 12000, 4000, 9500, 55000, 53000, 1900, 46000, 7200, 8700]
})

# Dropdown for projection type
input_dropdown = alt.binding_select(options=[
    "albers", "albersUsa", "azimuthalEqualArea", "azimuthalEquidistant",
    "conicEqualArea", "conicEquidistant", "equalEarth", "equirectangular",
    "gnomonic", "mercator", "naturalEarth1", "orthographic",
    "stereographic", "transverseMercator"
], name='Projection ')
param_projection = alt.param(value="equalEarth", bind=input_dropdown)

# Create the chart
chart = (
    alt.Chart(countries, width=700, height=400)
    .mark_geoshape(stroke='black', strokeWidth=0.3)
    .encode(
        color=alt.Color(
            'gdp_per_capita:Q',
            scale=alt.Scale(scheme='blues'),
            title='GDP per capita'
        ),
        tooltip=[
            alt.Tooltip('country:N', title='Country'),
            alt.Tooltip('gdp_per_capita:Q', title='GDP per capita', format=',.0f')
        ]
    )
    .transform_lookup(
        lookup='id',
        from_=alt.LookupData(values, 'id', ['country', 'gdp_per_capita'])
    )
    .project(type=alt.expr(param_projection.name))
    .add_params(param_projection)
)

chart

from vega_datasets import data


def iso_to_numeric(code):
    """Convert ISO alpha-2 (e.g. 'AF') or alpha-3 ('AFG') to ISO numeric (int)."""
    if not isinstance(code, str) or not code:
        return None
    code = code.strip().upper()
    c = None
    if len(code) == 2:
        c = pycountry.countries.get(alpha_2=code)
    elif len(code) == 3:
        c = pycountry.countries.get(alpha_3=code)
    return int(c.numeric) if c and getattr(c, "numeric", None) else None

# 2) Prepare your data: add a numeric 'id' to match the topojson
rank_delta = rank_delta.copy()
rank_delta["id"] = rank_delta["code"].apply(iso_to_numeric)

# (optional) see which codes didn’t map (e.g., XK for Kosovo)
unmapped = rank_delta[rank_delta["id"].isna()]["code"].unique()
# print("Unmapped codes:", unmapped)

# 3) Build the map (base + data layer)
world = alt.topo_feature(data.world_110m.url, "countries")

# Projection control (optional)
input_dropdown = alt.binding_select(options=[
    "albers","albersUsa","azimuthalEqualArea","azimuthalEquidistant",
    "conicEqualArea","conicEquidistant","equalEarth","equirectangular",
    "gnomonic","mercator","naturalEarth1","orthographic",
    "stereographic","transverseMercator"
], name='Projection ')
param_projection = alt.param(value="equalEarth", bind=input_dropdown)

base = (
    alt.Chart(world, width=700, height=420)
      .mark_geoshape(fill="#eee", stroke="#bbb", strokeWidth=0.4)
      .project(type=alt.expr(param_projection.name))
)

choropleth = (
    alt.Chart(world)
      .mark_geoshape(stroke="#555", strokeWidth=0.2)
      .transform_lookup(
          lookup="id",  # Natural Earth 'id' == ISO numeric code
          from_=alt.LookupData(
              rank_delta.dropna(subset=["id"]),
              key="id",
              fields=["country", "updated_diff", "visa_free_count", "year"]
          )
      )
      .encode(
          color=alt.Color(
              "updated_diff:Q",
              title="Updated Diff",
              scale=alt.Scale(scheme="redblue", domainMid=0)
          ),
          tooltip=[
              alt.Tooltip("country:N",          title="Country (data)"),
              alt.Tooltip("updated_diff:Q",     title="Updated Diff", format=".2f"),
              alt.Tooltip("visa_free_count:Q",  title="Visa-free Count"),
              alt.Tooltip("year:O",             title="Year")
          ]
      )
      .project(type=alt.expr(param_projection.name))
)

(base + choropleth).add_params(param_projection)

def iso_to_numeric(code):
    """Convert ISO alpha-2 (e.g. 'AF') or alpha-3 ('AFG') to ISO numeric (int)."""
    if not isinstance(code, str) or not code:
        return None
    code = code.strip().upper()
    c = None
    if len(code) == 2:
        c = pycountry.countries.get(alpha_2=code)
    elif len(code) == 3:
        c = pycountry.countries.get(alpha_3=code)
    return int(c.numeric) if c and getattr(c, "numeric", None) else None

# 2) Prep your data: make 'id' and *composite* 'id_year' used by the Vega lookup
rank_delta = rank_delta.copy()

# map ISO to numeric id (Natural Earth 'id')
rank_delta["id"] = rank_delta["code"].apply(iso_to_numeric)

# make sure 'year' is integer, drop rows where id/year missing
rank_delta["year"] = pd.to_numeric(rank_delta["year"], errors="coerce").astype("Int64")
rank_delta = rank_delta.dropna(subset=["id", "year"])

# build composite join key used by the chart ("<id>_<YearParamValue>")
rank_delta["id_year"] = (
    rank_delta["id"].astype(int).astype(str)
    + "_"
    + rank_delta["year"].astype(int).astype(str)
)

# 3) World topojson + projection chooser (same as code1)
world = alt.topo_feature(data.world_110m.url, "countries")

input_dropdown = alt.binding_select(
    options=[
        "albers","albersUsa","azimuthalEqualArea","azimuthalEquidistant",
        "conicEqualArea","conicEquidistant","equalEarth","equirectangular",
        "gnomonic","mercator","naturalEarth1","orthographic",
        "stereographic","transverseMercator"
    ],
    name='Projection '
)
param_projection = alt.param(value="equalEarth", bind=input_dropdown)

base = (
    alt.Chart(world, width=700, height=420)
      .mark_geoshape(fill="#eee", stroke="#bbb", strokeWidth=0.4)
      .project(type=alt.expr(param_projection.name))
)

# 4) Year slider param (as in your code2)
years = sorted(int(y) for y in rank_delta["year"].dropna().unique())
year_param = alt.param(
    name="Year",
    value=years[0],
    bind=alt.binding_range(min=min(years), max=max(years), step=1, name="Year ")
)

# 5) Choropleth with composite key lookup & signed log color
#    Note: include origin_country in fields if you have it; it’s typed as :N below.
lookup_fields = ["country", "updated_diff", "visa_free_count", "year"]
if "origin_country" in rank_delta.columns:
    lookup_fields.append("origin_country")

choropleth = (
    alt.Chart(world)
      .mark_geoshape(stroke="#555", strokeWidth=0.2)
      # Build the same key the DataFrame uses: "<id>_<YearParamValue>"
      .transform_calculate(id_year="toString(datum.id) + '_' + toString(Year)")
      # Lookup by id_year
      .transform_lookup(
          lookup="id_year",
          from_=alt.LookupData(
              # Important: use the frame that already has 'id_year'
              rank_delta[["id_year"] + lookup_fields],
              key="id_year",
              fields=lookup_fields
          )
      )
      # signed log transform for diverging color (works in Vega expression)
      .transform_calculate(
          signed_log_diff="(datum.updated_diff == 0 ? 0 : "
                          "(datum.updated_diff > 0 ? 1 : -1) * log(abs(datum.updated_diff) + 1))"
      )
      .encode(
          color=alt.Color(
              "signed_log_diff:Q",
              title="Updated Diff (log-scaled)",
              scale=alt.Scale(scheme="redblue", domainMid=0)
          ),
          tooltip=[
              alt.Tooltip("country:N",          title="Country"),
              alt.Tooltip("updated_diff:Q",     title="Changed", format=".2f"),
              alt.Tooltip("visa_free_count:Q",  title="Visa-free Count"),
              alt.Tooltip("year:O",             title="Year")
          ]
      )
      .project(type=alt.expr(param_projection.name))
)

# 6) Compose, add params, title
map_chart = (
    (base + choropleth)
    .add_params(param_projection, year_param)
    .properties(
        title=alt.TitleParams(
            text="Change in Visa-free Access per Country (Δ vs Previous Year)",
            subtitle="Log-scaled color; red = decrease, blue = increase",
            anchor="middle",
            fontSize=18,
            subtitleFontSize=12
        )
    )
)

map_chart

import pandas as pd
import altair as alt

def top_list_card(title, order):
    # Header drawn INSIDE the chart — avoids external title offset
    header = (
        alt.Chart(pd.DataFrame({"label": [title], "row": [0]}))
          .mark_text(align="left", baseline="bottom", fontWeight="bold")
          .encode(
              y=alt.Y("row:O", axis=None),
              text="label:N",
              x=alt.value(0)   # flush left
          )
    )

    # Top 5 rows as plain text, directly under the header
    rows = (
        alt.Chart(rank_delta)
          .transform_filter("datum.year == Year")
          .transform_window(
              rank="row_number()",
              sort=[{"field": "updated_diff", "order": order}]  # 'descending' or 'ascending'
          )
          .transform_filter("datum.rank <= 5")
          .transform_calculate(
              label="toString(datum.rank) + '. ' + datum.country + ' (' + "
                    "(datum.updated_diff >= 0 ? '+' : '') + "
                    "format(datum.updated_diff, '.0f') + ')'",
              row="datum.rank + 0.8"  # place items just below header
          )
          .mark_text(align="left", baseline="top")
          .encode(
              y=alt.Y("row:O", axis=None),
              text="label:N",
              x=alt.value(0)  # flush left
          )
    )

    # Layer header + rows; small, tight card
    return (header + rows).properties(width=260, height=130)

# Build both cards
card_up   = top_list_card("Top 5 Increases", "descending")
card_down = top_list_card("Top 5 Decreases", "ascending")

# Stack cards vertically
sidebar_cards = alt.vconcat(card_up, card_down, spacing=10)

# Optional: widen the map slightly to balance the layout
pretty_map = map_chart.properties(width=820)

# Final composition — configs only at top level
chart2 = (
    alt.hconcat(pretty_map, sidebar_cards, spacing=24)
      .add_params(year_param, param_projection)
      .resolve_legend(color="independent")
      .configure_view(stroke=None)            # remove borders
      #.configure_concat(spacing=12)           # tidy spacing
)

chart2

"""Do countries that belong to certain global alliances, or have stronger economies, tend to enjoy greater visa-free access?"""

# Filter only entries where destination is the United States
usa_visas = normalized[normalized["dest_code"] == "US"]

# Count how many of each visa_type exist
visa_type_counts = usa_visas["visa_type"].value_counts()

print(visa_type_counts)

# Filter for visa-free entries to the United States
usa_visa_free = normalized[
    (normalized["dest_code"] == "US") &
    (normalized["visa_type"] == "Visa-free")
]
usa_electronic_auth = normalized[
    (normalized["dest_code"] == "US") &
    (normalized["visa_type"] == "Electronic travel authorisation")
]

# Show only the origin countries (unique ones)
usa_visa_free_countries = usa_visa_free[["origin_code", "origin_country"]].drop_duplicates()
usa_electronic_auth_countries = usa_electronic_auth[["origin_code", "origin_country"]].drop_duplicates()

print(usa_visa_free_countries)
print(usa_electronic_auth_countries)

"""If we look we can see that only 4 countries have visa-free access to the USA where one is canada which has had a log-standing reciprocal agreement built on close economic ties, shared border and political alliances. And the other three are part of the Trust Territory of the Pacific Islands and each signed a special tretay, Compact of Free Association (COFA)."""

#Some military/defense alliances
nato = [
    "US", "CA", "GB", "FR", "DE", "IT", "ES", "PL", "TR", "GR",
    "NO", "SE", "FI", "PT", "NL", "BE", "DK", "CZ", "SK", "RO",
    "BG", "HU", "LT", "LV", "EE", "HR", "SI", "AL", "ME", "MK"
]
csto = ["RU", "BY", "AM", "KZ", "KG", "TJ"]
aukus = ["US", "GB", "AU"]
five_eyes = ["US", "GB", "CA", "AU", "NZ"]
quad = ["US", "IN", "JP", "AU"]

from vega_datasets import data as vega_data

# --- ISO conversion helpers ---
SPECIAL_NUMERIC = {
    "XK": -99,  # Kosovo
    "TW": 158,  # Taiwan
    "HK": 344,  # Hong Kong
    "MO": 446,  # Macao
    "PS": 275,  # Palestine
}

# --- Prepare visa data ---
visa_df = (
    usa_visas.loc[:, ["origin_code", "origin_country", "visa_type"]]
    .dropna(subset=["origin_code", "visa_type"])
    .drop_duplicates(subset=["origin_code"])
    .copy()
)
visa_df["id"] = visa_df["origin_code"].apply(iso_to_numeric)

# --- World geometry ---
world = alt.topo_feature(vega_data.world_110m.url, "countries")

# --- Color scale ---
visa_order = ["Visa required", "Electronic travel authorisation", "Visa-free"]
visa_scale = alt.Scale(domain=visa_order, range=["#d73027", "#ffd24a", "#1a9850"])

# --- Choropleth (Equal Earth projection 🌎) ---
chart = (
    alt.Chart(world)
    .mark_geoshape(stroke="#aaaaaa", strokeWidth=0.3)
    .encode(
        color=alt.Color("visa_type:N", title="Visa to US", sort=visa_order, scale=visa_scale),
        tooltip=[
            alt.Tooltip("origin_country:N", title="Country"),
            alt.Tooltip("visa_type:N", title="Visa type"),
        ],
    )
    .transform_lookup(
        lookup="id",
        from_=alt.LookupData(visa_df, key="id", fields=["origin_country", "visa_type"])
    )
    .properties(
        width=950,
        height=520,
        title="Visa status for travel to the United States (Equal Earth Projection)"
    )
    .project(type="equalEarth")
)

chart

# --- Alliance lists ---
nato = [
    "US", "CA", "GB", "FR", "DE", "IT", "ES", "PL", "TR", "GR",
    "NO", "SE", "FI", "PT", "NL", "BE", "DK", "CZ", "SK", "RO",
    "BG", "HU", "LT", "LV", "EE", "HR", "SI", "AL", "ME", "MK"
]
csto = ["RU", "BY", "AM", "KZ", "KG", "TJ"]
aukus = ["US", "GB", "AU"]
five_eyes = ["US", "GB", "CA", "AU", "NZ"]
quad = ["US", "IN", "JP", "AU"]

# --- ISO conversion helper ---
SPECIAL_NUMERIC = {"XK": -99, "TW": 158, "HK": 344, "MO": 446, "PS": 275}

def iso_to_numeric(code: str):
    """Convert ISO alpha-2 (e.g., 'AF') or alpha-3 ('AFG') -> numeric iso_n3 (int)."""
    if not isinstance(code, str) or not code:
        return None
    code = code.strip().upper()
    if code in SPECIAL_NUMERIC:
        return SPECIAL_NUMERIC[code]
    c = None
    if len(code) == 2:
        c = pycountry.countries.get(alpha_2=code)
    elif len(code) == 3:
        c = pycountry.countries.get(alpha_3=code)
    return int(c.numeric) if c and getattr(c, "numeric", None) else None

# --- Prepare visa data ---
visa_df = (
    usa_visas.loc[:, ["origin_code", "origin_country", "visa_type"]]
    .dropna(subset=["origin_code", "visa_type"])
    .drop_duplicates(subset=["origin_code"])
    .copy()
)
visa_df["id"] = visa_df["origin_code"].apply(iso_to_numeric)

# --- Alliance ID lists ---
def get_ids(codes):
    return [iso_to_numeric(c) for c in codes if iso_to_numeric(c) is not None]

nato_ids = get_ids(nato)
csto_ids = get_ids(csto)
aukus_ids = get_ids(aukus)
five_ids = get_ids(five_eyes)
quad_ids = get_ids(quad)

# --- World geometry ---
world = alt.topo_feature(vega_data.world_110m.url, "countries")

# --- Visa color scale ---
visa_order = ["Visa required", "Electronic travel authorisation", "Visa-free"]
visa_scale = alt.Scale(domain=visa_order, range=["#d73027", "#ffd24a", "#1a9850"])

# --- Base choropleth ---
base = (
    alt.Chart(world)
    .mark_geoshape(stroke="#aaaaaa", strokeWidth=0.3)
    .encode(
        color=alt.Color("visa_type:N", title="Visa to US", sort=visa_order, scale=visa_scale),
        tooltip=[
            alt.Tooltip("origin_country:N", title="Country"),
            alt.Tooltip("visa_type:N", title="Visa type"),
        ],
    )
    .transform_lookup(
        lookup="id",
        from_=alt.LookupData(visa_df, key="id", fields=["origin_country", "visa_type"])
    )
    .properties(width=950, height=520, title="Visa status for travel to the United States (Equal Earth)")
    .project(type="equalEarth")
)

# --- Checkbox parameters (names without spaces) ---
p_nato = alt.param(name="showNATO", value=False, bind=alt.binding_checkbox(name="NATO"))
p_csto = alt.param(name="showCSTO", value=False, bind=alt.binding_checkbox(name="CSTO"))
p_aukus = alt.param(name="showAUKUS", value=False, bind=alt.binding_checkbox(name="AUKUS"))
p_five = alt.param(name="showFiveEyes", value=False, bind=alt.binding_checkbox(name="Five Eyes"))
p_quad = alt.param(name="showQuad", value=False, bind=alt.binding_checkbox(name="Quad"))

# --- Function for alliance overlay ---
def alliance_overlay(ids, stroke_color, param_obj, label):
    return (
        alt.Chart(world)
        .mark_geoshape(fillOpacity=0, stroke=stroke_color, strokeWidth=1.6)
        # join visa info just like in the base layer
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(visa_df, key="id", fields=["origin_country", "visa_type"])
        )
        .transform_filter(alt.FieldOneOfPredicate(field="id", oneOf=ids))
        .encode(
            strokeOpacity=alt.condition(param_obj, alt.value(1.0), alt.value(0.0)),
            tooltip=[
                alt.Tooltip("origin_country:N", title="Country"),
                alt.Tooltip("visa_type:N", title="Visa type"),
            ]
        )
    )

# --- Overlays for each alliance ---
overlay_nato       = alliance_overlay(nato_ids,        "#0033cc", p_nato, "NATO")        # deep blue
overlay_csto       = alliance_overlay(csto_ids,        "#7a001f", p_csto, "CSTO")        # deep crimson (separates from base red)
overlay_aukus      = alliance_overlay(aukus_ids,       "#9933ff", p_aukus, "AUKUS")      # vivid violet
overlay_five       = alliance_overlay(five_ids,        "#007a99", p_five, "Five Eyes")   # teal (contrasts with visa green)
overlay_quad       = alliance_overlay(quad_ids,        "#b35900", p_quad, "Quad")        # dark amber (reads on yellow)

# --- Combine all layers + add params ---
chart = (
    base
    + overlay_nato
    + overlay_csto
    + overlay_aukus
    + overlay_five
    + overlay_quad
).add_params(p_nato, p_csto, p_aukus, p_five, p_quad)

chart

# --- extract the relevant columns ---
gdp_2021 = gdp.loc[:, ["origin_country_norm", "2021"]].rename(columns={"2021": "gdp_per_capita"})
pop_2021 = population.loc[:, ["origin_country_norm", "2021"]].rename(columns={"2021": "population"})

# --- base: every country in your country list ---
out = country_lists.loc[:, ["origin_country_norm", "origin_code", "origin_country"]].drop_duplicates()

# --- merge GDP per capita + population ---
out = (out
       .merge(gdp_2021, on="origin_country_norm", how="left")
       .merge(pop_2021, on="origin_country_norm", how="left"))

out["gdp_total"] = out["gdp_per_capita"] * out["population"]

# Optional: make the column order tidy
out = out[["origin_country_norm", "origin_code", "origin_country",
           "gdp_per_capita", "population", "gdp_total"]]

# Optional: sort and reset
out = out.sort_values("origin_country_norm").reset_index(drop=True)

# --- Top 15 by GDP per capita ---
top15_gdp_per_capita = (
    out.sort_values("gdp_per_capita", ascending=False)
       .head(15)
       .reset_index(drop=True)
)

# --- Top 15 by total GDP ---
top15_gdp_total = (
    out.sort_values("gdp_total", ascending=False)
       .head(15)
       .reset_index(drop=True)
)

# Optional: show just the key columns for readability
print("Top 15 by GDP per capita:")
print(top15_gdp_per_capita[["origin_code", "origin_country", "gdp_per_capita"]])

print("\nTop 15 by total GDP:")
print(top15_gdp_total[["origin_code", "origin_country", "gdp_total"]])

# --- Top-15 ID lists (pick the right code column from your dataframes) ---
code_col = "origin_code" if "origin_code" in top15_gdp_per_capita.columns else "country_code"
top15_pc_ids    = get_ids(top15_gdp_per_capita[code_col].dropna().astype(str).tolist())
code_col_total  = "origin_code" if "origin_code" in top15_gdp_total.columns else "country_code"
top15_total_ids = get_ids(top15_gdp_total[code_col_total].dropna().astype(str).tolist())

# --- Checkbox params for Top-15 overlays ---
p_top_pc    = alt.param(name="showTopGDPpc",    value=False,
                        bind=alt.binding_checkbox(name="Top 15 GDP/capita"))
p_top_total = alt.param(name="showTopGDPtotal", value=False,
                        bind=alt.binding_checkbox(name="Top 15 GDP total"))

# --- Reusable overlay helper (same tooltip as base) ---
def id_outline_overlay(ids, stroke_color, param_obj):
    return (
        alt.Chart(world)
        .mark_geoshape(fillOpacity=0, stroke=stroke_color, strokeWidth=1.6)
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(visa_df, key="id", fields=["origin_country", "visa_type"])
        )
        .transform_filter(alt.FieldOneOfPredicate(field="id", oneOf=ids))
        .encode(
            strokeOpacity=alt.condition(param_obj, alt.value(1.0), alt.value(0.0)),
            tooltip=[
                alt.Tooltip("origin_country:N", title="Country"),
                alt.Tooltip("visa_type:N",      title="Visa type"),
            ],
        )
    )

# --- Top-15 overlays ---
overlay_top_pc     = id_outline_overlay(top15_pc_ids,    "#333333", p_top_pc)            # charcoal gray
overlay_top_total  = id_outline_overlay(top15_total_ids, "#cc00cc", p_top_total)         # magenta (not close to NATO blue)

chart4 = (
    base
    + overlay_nato + overlay_csto + overlay_aukus + overlay_five + overlay_quad
    + overlay_top_pc + overlay_top_total `
).add_params(p_nato, p_csto, p_aukus, p_five, p_quad, p_top_pc, p_top_total)

chart4

st.set_page_config(page_title="Altair Chart Host", layout="wide")
st.title("Altair Chart Host")

chart = None
error_text = None

# Try to import a function from your own script that returns an Altair chart
# Create a file called chart_module.py with a function `build_chart()` that returns alt.Chart
try:
    from chart_module import build_chart  # <- you provide this
    chart = build_chart()
except Exception as e:
    error_text = str(e)

if chart is None:
    import pandas as pd
    st.info(
        "Couldn’t import your chart from `chart_module.build_chart()`.\n"
        "Showing a small demo chart instead."
        + (f"\n\nDetails: {error_text}" if error_text else "")
    )
    # --- Demo chart ---
    df = pd.DataFrame({"x": list(range(30))})
    df["y"] = (df["x"] * 1.3).round(2)
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("x:Q", title="X"),
            y=alt.Y("y:Q", title="Y"),
            tooltip=["x", "y"],
        )
        .properties(height=400)
        .interactive()
    )

# Render your Altair chart
st.altair_chart(chart1, use_container_width=True)

# Optional: show the Vega-Lite spec (helps debug)
with st.expander("View Vega-Lite spec"):
    st.json(chart.to_dict())

