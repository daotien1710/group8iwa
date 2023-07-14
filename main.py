import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import urllib.parse
import plotly.graph_objects as go

# Read the data from CSV
data = pd.read_csv('archive.csv')

# Set the page configuration
st.set_page_config(page_title = "Project Python 2", page_icon = ":tada:", layout="wide")

# HEADER SECTION
with st.container():
    st.subheader("Hi:wave: we're from group 4 class Business IT2")
    st.title("What is there more to know about Nobel Prize Winners?")
    st.write("Apart from their achievements, join us today on this app to get to know the Laureates' Birth Countries and Average Lifespan!" ) 

# OUR DATASET
url = "https://www.kaggle.com/datasets/nobelfoundation/nobel-laureates?resource=download"
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column: st.header("Our dataset :sparkles:")
    st.markdown(f"[Click here to see the original dataset]({url})")
    st.write("##")
    st.write(
        """ Our refined data frame contains 4 main variables as follows:
        \n - *Category*: A factor with levels of Medicine, Physics, Peace, Literature, Chemistry, and Economics (Categories of the Nobel Prize)
        \n - *Number of Prizes*: A vector that counts the number of Prizes received
        \n - *Birth Country*: A factor that notes the birth countries of Nobel Laureates
        \n - *Age*: A vector that illustrates the age of Nobel Prize Winners using the subtraction of Death Year to Birth Year """)

st.divider()
st.header("Top Birth Countries and Life Span Chart")
st.write("Discover these two graphs below with us")


# Add Sidebar
st.sidebar.write('**:bulb: Reporting to Dr. Tan Duc Do**')
st.sidebar.write('**:bulb: Group 4 Business IT 2 Members:**')

# Add content to the main area
with st.sidebar:
    st.write('Ta Nguyen Minh Hang')
    st.write('Doan Minh Ngoc')
    st.write('Nguyen Hong Bao Ngoc')
    st.write('Pham Dan Thao')
    st.write('Nguyen Ai Nhi')

# Initial 2 tabs for each interactive graph
tab1, tab2 = st.tabs(["Bar Chart", "Boxplot Chart"])

### TAB 1: BAR CHART

# Calculate the value counts of Birth_Country
df = data['Birth_Country'].value_counts()

# Set the initial value for the slider
value = 5

# Get the top N countries with the most prizes
df1 = df.nlargest(n=value, keep='all')

# Define color palette for the bars
color1 = ["#19376D", "#576CBC", "#A5D7E8", "#66347F", "#9E4784", "#D27685", "#D4ADFC", "#F2F7A1", "#FB2576", "#E94560"]

# Add the slider
value = tab1.slider("Number of Countries", min_value=1, max_value=10, step=1, value=value)

# Update the top N countries based on the slider value
df1 = df.nlargest(n=value, keep='all')
color1 = color1[:len(df1)]

# Update the title of the plot
tab1.subheader("Top {} Countries That Had The Most Nobel Prize Winners".format(value))

# Create the bar chart using Altair
bar_data = pd.DataFrame({"Country": df1.index, "Number of Prizes": df1.values, "Color": color1})
bars = alt.Chart(bar_data).mark_bar().encode(
x=alt.X('Country', sort=None),
y=alt.Y('Number of Prizes'),
color=alt.Color('Color', scale=None),
tooltip=['Country', 'Number of Prizes']
       ).properties(width=1400)

# Rotate x-axis labels for better readability
bars = bars.configure_axisX(labelAngle=0)

# Display the chart using Streamlit
tab1.altair_chart(bars, use_container_width=True)

### TAB 2: BOXPLOT CHART
  
data[['Birth_Year', 'Birth_Month', 'Birth_Day']] = data['Birth_Date'].str.split("-", expand=True)
data[['Death_Day', 'Death_Month', 'Death_Year']] = data['Death_Date'].str.split("/", expand=True)
data["Birth_Year"] = pd.to_numeric(data["Birth_Year"], errors='coerce')
data["Death_Year"] = pd.to_numeric(data["Death_Year"], errors='coerce')
data["Year"] = pd.to_numeric(data["Year"], errors='coerce')
data['Age'] = data['Death_Year'] - data['Birth_Year']

 
# Sort the data by Age in ascending order
data_sorted = data.sort_values(by='Age', ascending=True)
# Create a subset of data for Physics, Medicine, and Chemistry categories
nat = data_sorted[data_sorted['Category'].isin(['Chemistry', 'Physics', 'Medicine'])]
# Create a subset of data for Literature, Peace, and Economics categories
soc = data_sorted[data_sorted['Category'].isin(['Literature', 'Peace', 'Economics'])]

# Create a palette color for categories
category_colors = {
    'Physics': '#7DEFA1',
    'Chemistry': '#FF2B2B',
    'Medicine': '#A5D7E8',
    'Literature': '#0068C9',
    'Peace': '#D4ADFC',
    'Economics': '#29B09D'
}

# Add the title of the plot
tab2.subheader("Lifespan of Nobel Winners")

# Store the initial value of widgets in session state
if "disabled" not in st.session_state:
    st.session_state.disabled = False

col1, col2, col3 = tab2.columns([2,2,3])
with col1:
    overview = st.checkbox("Overview of all categories", key="disabled")
    age_type = st.radio("Choose a value you want to look for 👇",
                        ["Oldest age", "Median age", "Youngest age"],
                        key="visibility",
                        # label_visibility= "visible",
                        disabled= st.session_state.disabled)
with col2:
    rank = st.selectbox("Rank", ("Maximum", "Minimum"), key="rank",
                        # label_visibility= "visible",
                        disabled= st.session_state.disabled)
with col3:
    if overview:
        st.write("Below is all categories.")
    else:
        st.write("Below is the category with")
        st.write("the {} value of the {} in each group.".format(rank.lower(), age_type.lower()))
        st.write(":green[**Note: Outlier values are accepted.**]")

# Create a container for displaying the boxplots
with tab2.container():
    
    # define a function to find the category as requested
    def find_category(data, age_type, rank):
        if age_type == "Oldest age":
            if rank == "Maximum":
                category = data.groupby('Category')['Age'].max().idxmax()
            else:
                category = data.groupby('Category')['Age'].max().idxmin()
        elif age_type == "Median age":
            if rank == "Maximum":
                category = data.groupby('Category')['Age'].median().idxmax()
            else:
                category = data.groupby('Category')['Age'].median().idxmin()
        elif age_type == "Youngest age":
            if rank == "Maximum":
                category = data.groupby('Category')['Age'].min().idxmax()
            else:
                category = data.groupby('Category')['Age'].min().idxmin()
        return category
    
   # Create two columns for displaying the boxplots
    box1, box2 = tab2.columns(2)
    with box1:
        # Add label above the first boxplot
        st.subheader("Natural Sciences")
        
        # Display the first boxplot
        if overview:
            fig1 = px.box(nat, y="Age", x="Category", color="Category", color_discrete_map=category_colors)
            fig1.update_layout(showlegend=False)  # Remove legend from the first plot
        else:
            nat_cat = find_category(nat, age_type, rank)
            nat_display_cat = nat[nat['Category'].isin([nat_cat])]
            fig1 = px.box(nat_display_cat, y="Age", x="Category", color="Category", color_discrete_map=category_colors)
            fig1.update_layout(showlegend=False)  # Remove legend from the first plot

        st.plotly_chart(fig1, use_container_width=True)


    with box2:
        # Add label above the second boxplot
        st.subheader("Social Sciences")

        # Display the second boxplot
        if overview:
            fig2 = px.box(soc, y="Age", x="Category", color="Category", color_discrete_map=category_colors)
            fig2.update_layout(showlegend=False)  # Remove legend from the second plot
        else:
            soc_cat = find_category(soc, age_type, rank)
            soc_display_cat = soc[soc['Category'].isin([soc_cat])]
            fig2 = px.box(soc_display_cat, y="Age", x="Category", color="Category", color_discrete_map=category_colors)
            fig2.update_layout(showlegend=False)  # Remove legend from the second plot

        st.plotly_chart(fig2, use_container_width=True)
