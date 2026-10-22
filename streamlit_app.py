# pip install streamlit plotly
# run in a terminal do:
# 1. conda activate alicia (to open python envi)
# 2. cd to folder
# 3. streamlit run 01_hello.py [or whatever the file name is]

# ------ pt. 1------

#import streamlit as st
#import plotly.express as px

#st.title("Global Development Explorer")
#st.write("Life expectency and income for 142 countries, 1952-2007")

#df = px.data.gapminder()
#st.dataframe(df)

# ----- part 2: -----
#import streamlit as st
#import plotly.express as px
#st.title("Global Development Explorer")
#st.write("Life expectancy and income for 142 countries, 1952–2007.")
#df = px.data.gapminder()
#df_2007 = df[df["year"] == 2007]
#fig = px.scatter(
#df_2007, x="gdpPercap", y="lifeExp",
#hover_name="country", color="continent", size="pop", log_x=True,
#)
#st.plotly_chart(fig)

# ---- part 3: ----
# CHECKPOINT 3: widgets (where is the callback?)
#import streamlit as st
#import plotly.express as px

#st.title("Global Development Explorer")
#df = px.data.gapminder()

#continent = st.selectbox("Continent", ["All"] + sorted(df["continent"].unique()))
#year = st.slider("Year", 1952, 2007, 2007, step=5)

#filtered = df[df["year"] == year]
#if continent != "All":
#    filtered = filtered[filtered["continent"] == continent]

#fig = px.scatter(
#    filtered, x="gdpPercap", y="lifeExp",
#    hover_name="country", color="continent", size="pop",
#    log_x=True, size_max=50, range_y=[25, 90],
#    )
#st.plotly_chart(fig)

# -------- part 4: ----
# CHECKPOINT 4: sidebar + KPI metrics in columns
#import streamlit as st
#import plotly.express as px

#st.title("Global Development Explorer")

#df = px.data.gapminder()
#continent = st.sidebar.selectbox("Continent", ["All"] + sorted(df["continent"].unique()))

#year = st.sidebar.slider("Year", 1952, 2007, 2007, step=5)

#filtered = df[df["year"] == year]
#if continent != "All":
#    filtered = filtered[filtered["continent"] == continent]

#col1, col2, col3 = st.columns(3)
#col1.metric("Countries", len(filtered))
#col2.metric("Avg life expectancy", f"{filtered['lifeExp'].mean():.1f} yrs")
#col3.metric("Median GDP per capita", f"${filtered['gdpPercap'].median():,.0f}")

#fig = px.scatter(filtered, x="gdpPercap", y="lifeExp", hover_name="country",
#    color="continent", size="pop", log_x=True, size_max=50, range_y=[25, 90])
#st.plotly_chart(fig)

# ------- demo pt 4:
# DEMO: caching. Move the slider with and without @st.cache_data
#import time
#import streamlit as st
#import plotly.express as px

#@st.cache_data # try commenting this line out
#def load_data():
#        time.sleep(3) # pretend this is a slow database
#        return px.data.gapminder()

#df = load_data()
#year = st.slider("Year", 1952, 2007, 2007, step=5)
#st.write(f"{len(df[df['year'] == year])} countries in {year}")

# ------------ PART 5: --------------
# CHECKPOINT 5: a Story tab (author-driven) + an Explore tab (reader-driven)
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Global Development Explorer", layout="wide")
@st.cache_data

def load_data():
    return px.data.gapminder()

df = load_data()
st.title("Asia gained 24 years of life expectancy since 1952")
story, explore = st.tabs(["The story", "Explore it yourself"])

with story:
    by_continent = df.groupby(["continent", "year"], as_index=False)["lifeExp"].mean()
    fig = px.line(by_continent, x="year", y="lifeExp", color="continent",
        labels={"lifeExp": "Average life expectancy (years)", "year": ""})
    st.plotly_chart(fig)
    st.markdown("Every continent improved, but **Asia** rose fastest: "
                "from **46.3** years in 1952 to **70.7** in 2007.")
    st.caption("Source: Gapminder, via plotly.express. Unweighted country averages.")

with explore:
    left, right = st.columns([1, 3])
    continent = left.selectbox("Continent", ["All"] + sorted(df["continent"].unique()))
    year = left.slider("Year", 1952, 2007, 2007, step=5)
    
    filtered = df[df["year"] == year]
    if continent != "All":
        filtered = filtered[filtered["continent"] == continent]
    place = "the world" if continent == "All" else continent

    left.metric("Avg life expectancy", f"{filtered['lifeExp'].mean():.1f} yrs")
    right.markdown(f"In **{year}**, the **{len(filtered)}** countries in **{place}** "
                    f"had an average life expectancy of **{filtered['lifeExp'].mean():.1f} years**.")
    fig = px.scatter(filtered, x="gdpPercap", y="lifeExp", hover_name="country",
                    color="continent", size="pop", log_x=True, size_max=50, range_y=[25, 90])
    right.plotly_chart(fig)

# still indented inside "with explore:"
with st.expander("See the data behind this chart"):
    st.dataframe(filtered, hide_index=True)
    st.download_button(
        "Download as CSV",
        data=filtered.to_csv(index=False),
        file_name=f"gapminder_{place}_{year}.csv",
        mime="text/csv",
    )