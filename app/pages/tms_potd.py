# -------------------------------------------------------------------------
# Import libraries
# -------------------------------------------------------------------------
import streamlit as st
import numpy as np
import pandas as pd

import os
import sys
import pathlib
import datetime

# from app.pages.helper_funcs import *
# from recommender.version_epsilon.helper_funcs import *
from streamlit_extras.let_it_rain import rain

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import plotly.express as px
import plotly.graph_objects as go

from bs4 import BeautifulSoup
from selenium import webdriver
# import shutil
# import seleniumbase
import chromedriver_autoinstaller
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import re

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_data = path_total + 'data/'

# @st.cache_resource
# def install_chromium():
#   os.system('sbase get chromedriver')
#   os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/chromedriver /home/appuser/venv/bin/chromedriver')

# _ = install_chromium()
chromedriver_autoinstaller.install()

# -------------------------------------------------------------------------
# Scraping Function
# -------------------------------------------------------------------------
def scrape_perfume(website):
    # Visit specific perfume website and obtain html code

    # CHROME SCRAPING OPTIONS
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--remote-debugging-port=9222")
    opts.add_argument("--window-size=1920,1080")
    # Mild “stealth”:
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36")
    # In some Colab images, the binary path is needed explicitly:
    # opts.binary_location = shutil.which('chromium')
    # opts.binary_location = '/home/appuser/venv/chromedriver' # '/home/appuser/venv/chromium-browser' # "/usr/bin/chromium-browser"  # or "/usr/bin/chromium"
    # opts.setBrowserVersion("113.0.5672.126")
    # opts.add_argument("--browserVersion=113.0.5672.126")
    driver = webdriver.Chrome(options=opts)

    try:
        driver.get(website)
        WebDriverWait(driver, 40).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        perfume_soup = BeautifulSoup(driver.page_source, "html.parser")
        notes_are_categorized = perfume_soup.find("h2", string="Perfume Pyramid")
    finally:
        driver.quit()

    # Extract info from html

    pattern = r'([\d.]+)%'  # re pattern for searching

    accord_data = []

    # Rating (out of 5)
    try:
        rating = float(perfume_soup.find('span',itemprop='ratingValue').text)
        num_votes = int(perfume_soup.find('span',itemprop='ratingCount').text)
    except Exception:
        rating = 0.0
        num_votes = 0

    # User descriptions (longevity, sillage, gender, price)
    try:
        ratings = np.array([int(x.text) for x in perfume_soup.find_all('span',class_="vote-button-legend")[11:30]])
        longevity = (ratings[:5]/sum(ratings[:5])) if sum(ratings[:5])!=0 else np.zeros(5)
        sillage = (ratings[5:9]/sum(ratings[5:9])) if sum(ratings[5:9])!=0 else np.zeros(4)
        fem_masc = (ratings[9:14]/sum(ratings[9:14])) if sum(ratings[9:14])!=0 else np.zeros(5)
        price = (ratings[14:19]/sum(ratings[14:19])) if sum(ratings[14:19])!=0 else np.zeros(5)
    except Exception:
        longevity = np.zeros(5)
        sillage = np.zeros(4)
        fem_masc =  np.zeros(5)
        price = np.zeros(5)

    # Environment (seasons, day/night
    try:
        environment = perfume_soup.find_all('div',style="width: 100%; height: 0.3rem; border-radius: 0.2rem; background: rgba(204, 224, 239, 0.4);")[8:]
        environment = [str(tag.div) for tag in environment]
        environment = np.array([float(re.search(pattern, tag).group(1)) for tag in environment])
    except Exception:
        environment = np.zeros(6)

    return accord_data,rating,longevity,sillage,fem_masc,price,environment

# -------------------------------------------------------------------------
# Radar Chart for Perfume Stats
# -------------------------------------------------------------------------
def radar_chart(longevity_score,sillage_score,gender_score,price_score,rating_score):

    categories = ["Longevity", "Sillage", "Gender", "Affordability", "Rating"]
    values     = [longevity_score, sillage_score, gender_score, price_score, rating_score]

    # Close loop for plotting
    cats_loop = categories + categories[:1]
    vals_loop = values     + values[:1]

    # Build the Plotly radar chart
    fig = go.Figure()

    # Add concentric pentagons: 20%, 40%, 60%, 80%, 100%
    for r, col, w in zip([20,40,60,80,100],
                        ["lightgray"]*4 + ["black"],
                        [1]*4 + [2]):
        fig.add_trace(go.Scatterpolar(
            r    = [r]*len(cats_loop),
            theta= cats_loop,
            mode = "lines",
            line = dict(color=col, width=w),
            hoverinfo="none"
        ))

    # Add inner hover text
    hover_text = [f"{cat}: {val}%" for cat,val in zip(categories, values)]

    fig.add_trace(go.Scatterpolar(
        r        = vals_loop,
        theta    = cats_loop,
        mode     = "markers+lines",
        line     = dict(color="orange"),
        marker   = dict(size=8, color="orange"),
        hoverinfo= "text",
        fill      = "toself",
        hovertext= hover_text + [""]          # blank for the closing point
    ))
    fig.add_trace(go.Scatterpolar(
        r        = values,
        theta    = categories,
        mode     = "markers",
        marker   = dict(size=40, color="rgba(0,0,0,0)"),
        hoverinfo= "text",
        hovertext= hover_text,
        showlegend=False
    ))
    # Add outer hover text
    fig.add_trace(go.Scatterpolar(
        r        = [100]*len(categories),
        theta    = categories,
        mode     = "markers",
        marker   = dict(size=20, color="rgba(0,0,0,0)"),
        hoverinfo= "text",
        hovertext= ['0=short-lasting to 100=long-lasting',
                    '0=intimate radius to 100=large radius',
                    '0=feminine to 100=masculine',
                    '0=overpriced to 100=great value',
                    '0=poor ratings to 100=excellent ratings'],
        showlegend=False
    ))
    # Tidy layout
    fig.update_layout(
        polar = dict(
            radialaxis   = dict(visible=False, range=[0,100]),
            angularaxis  = dict(rotation=-90, direction="clockwise")
        ),
        showlegend=False,
        margin=dict(l=20,r=20,t=20,b=20)
    )
    # Display
    st.plotly_chart(fig, use_container_width=True)
    
# -------------------------------------------------------------------------
# Environment Pie Charts
# -------------------------------------------------------------------------
def environment_chart(environment):
    if st.context.theme.type == 'dark':
        sys_bg_color = '#0e1117'
        sys_fr_color = '#FFFFFF'
    else:
        sys_bg_color = '#FFFFFF'
        sys_fr_color = '#0e1117'
    # day_colors = ["#FFC300","#345492"]  # gold yellow, indigo blue
    season_colors = {
    "Winter": "#20A2D5",  # deep blue
    "Spring": "#229F56",  # forest green
    "Summer": "#E1BB23",  # warm gold
    "Fall":   "#BB392B"   # autumn brown
    }
    season_labels = ["Winter", "Spring", "Summer", "Fall"]

    # Create axes
    fig, ax = plt.subplots(figsize=(2, 1),facecolor=sys_bg_color)
    ax.set_facecolor(sys_bg_color)

    # Data for day/night slider
    day_pct, night_pct = environment[4], environment[5]
    ratio = night_pct / (day_pct + night_pct)
    # Gradient colormap from gold to blue
    cmap = LinearSegmentedColormap.from_list('daynight', ['#FFC300', "#0B4CD0"])
    # Horizontal gradient image
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    ax.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 100, 0, 1])
    # Draw the slider handle
    ax.axvline(ratio * 100, color=sys_fr_color, linewidth=3)
    # Add labels
    ax.text(0, 1.5, 'Day', color=sys_fr_color, ha='left', va='center', fontsize=8)
    ax.text(100, 1.5, 'Night', color=sys_fr_color, ha='right', va='center', fontsize=8)
    # Clean up axes
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    # Tree Map for Seasonality
    df = pd.DataFrame({
    "Season": season_labels,
    "Value":  environment[:4]
    })
    fig = px.treemap(
    df,
    path=["Season"],
    values="Value",
    color="Season",
    color_discrete_map=season_colors
    )
    fig.update_traces(
        textinfo="label+percent entry",
        textfont=dict(color="white", size=24)
    )
    fig.update_layout(
        autosize = False,
        width=380,height=300,
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor=sys_bg_color,
        plot_bgcolor=sys_bg_color
    )
    st.plotly_chart(fig, use_container_width=True)


# -------------------------------------------------------------------------
# Accord Colorizer and Plot
# -------------------------------------------------------------------------
accord_colors = {
    "honey":     "#FFC300", 
    "lemon":     "#FFF44F", 
    "citrus":    "#FFD966",  
    "orange":    "#FFA500",
    "berry":     "#8E4585",
    "grapefruit":"#FF5F1F",
    "rose":      "#FFC0CB", 
    "jasmine":   "#F8F4FF", 
    "tuberose":  "#F2E7FE",
    "floral":    "#E8C1D1",
    "white floral":"#F5F5F5",
    "yellow floral":"#FFF8DC",
    "woody":     "#8B5E3C", 
    "cedarwood": "#A0522D",
    "patchouli": "#70543E",
    "earthy":    "#6B4226",
    "moss":      "#556B2F",
    "mossy":     "#556B2F",
    "green":     "#228B22",
    "herbal":    "#6B8E23",
    "lavender":  "#967BB6",
    "violet":    "#7F00FF",
    "iris":      "#5A4FCF",
    "powdery":   "#EDE3E0",
    "vanilla":   "#F3E5AB",
    "coconut":   "#FFF5E1",
    "almond":    "#EED5B7",
    "caramel":   "#C68E17",
    "chocolate": "#5C4033",
    "cacao":     "#3B1F1F",
    "coffee":    "#4B3621",
    "tobacco":   "#5D3A1A",
    "smoke":     "#4F4F4F",
    "smoky":     "#4F4F4F",
    "leather":   "#59351F",
    "amber":     "#FFBF00",
    "warm spicy":"#C1440E",
    "spicy":     "#D2691E",
    "cinnamon":  "#A0522D",
    "fresh spicy":"#FF7F50",
    "sweet":     "#FFB6C1",
    "fruity":    "#FF6EB4",
    "tropical":  "#FFA07A",
    "aquatic":   "#00CED1",
    "marine":    "#4682B4",
    "ozonic":    "#E0FFFF",
    "metallic":  "#B0C4DE",
    "mineral":   "#A9A9A9",
    "rubber":    "#2F4F4F",
    "vinyl":     "#708090",
    "plastic":   "#A9A9A9",
    "balsamic":  "#8B4513",
    "oriental":  "#DEB887",
    "gourmand":  "#D2B48C",
    "animalic":  "#8B0000",
    "lactonic":  "#FFF8E7",
    }

def get_accord_color(accord):
    try:
        return accord_colors[accord]
    except KeyError:
        return "#888888"
    return "#888888"  

def get_text_color(bg_hex):
    bg_hex = bg_hex.lstrip('#')
    r, g, b = int(bg_hex[:2], 16), int(bg_hex[2:4], 16), int(bg_hex[4:6], 16)
    brightness = 0.299*r + 0.587*g + 0.114*b
    return 'black' if brightness > 186 else 'white'

def display_accords(data):
    # input: ['rose','woody',fruity,aromatic,floral]
    accords = data
    data = [(a,60.0) for a in accords]
    values = [60.0 for a in accords]
    colors = [get_accord_color(a) for a in accords]
    if st.context.theme.type == 'dark':
        sys_bg_color = '#0e1117'
    else:
        sys_bg_color = '#FFFFFF'
    
    fig, ax = plt.subplots(figsize=(6, 3), facecolor=sys_bg_color)
    ax.set_facecolor(sys_bg_color)

    y_pos = np.arange(len(accords))
    ax.barh(y_pos, values, color=colors, height=1)
    for i, (accord, val) in enumerate(data):
        bg = colors[i]
        text_color = get_text_color(bg)
        ax.text(val / 2, i, accord, va='center', ha='center', color=text_color, fontsize=10)
    ax.invert_yaxis()
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

def get_img_fragrantica(input_url):
    perfume_id = input_url.split('-')[-1].split('.')[0]
    return f'https://fimgs.net/mdimg/perfume-thumbs/375x500.{perfume_id}.jpg'

# -------------------------------------------------------------------------
# Title
# -------------------------------------------------------------------------
st.set_page_config(
    page_title='Perfume of the Day',
    layout="wide",                # ← uses the full width
    initial_sidebar_state="auto"  # optional
)

st.title('Perfume of the Day')

st.write(':material/calendar_today: ', datetime.date.today())

# -------------------------------------------------------------------------
# Load data and choose perfume of the day
# -------------------------------------------------------------------------
today = datetime.date.toordinal(datetime.date.today())
df_fra_standard = pd.read_csv(f'{path_data}fra_standard.csv')
index_potd = df_fra_standard.sample(1, random_state=today).index[0]
potd = df_fra_standard.iloc[index_potd]

# -------------------------------------------------------------------------
# Scrape perfume of the day
# -------------------------------------------------------------------------
accord_data, rating, longevity, sillage, fem_masc, price, environment = scrape_perfume(potd['url'])

accord_data = [ str(potd.get(f'mainaccord{i}', '')) for i in range(1, 6) ]
# e.g. ['rose', 'woody', fruity, aromatic, floral]

# Compute scores
longevity_score = (100*np.dot(longevity,range(5))/5).round(2)
sillage_score   = (100*np.dot(sillage,range(4))/4).round(2)
gender_score    = (100*np.dot(fem_masc,range(5))/5).round(2)
price_score     = (100*np.dot(price,range(5))/5).round(2)
rating_score    = round(100.0*rating/5,2)

col1, col2 = st.columns([1,10])
with col1:
    img = get_img_fragrantica(potd['url'])
    st.image(image = img,
            width = 100,
            use_container_width = False)
with col2:
    # Name, Brand, Link
    st.header(':material/fragrance: {name} by {brand}'.format(name=potd['Perfume'],brand=potd['Brand']))
    st.link_button(
        'Find more details and Reviews at Fragrantica.com :material/arrow_outward: ',
        f"{potd['url']}",
    )

col1, col2, col3 = st.columns([2, 2, 2])

# Radar Chart
with col1:
    radar_chart(longevity_score, sillage_score, gender_score, price_score, rating_score)

# Accords and Notes
with col2:
    st.subheader('𓏊 Notes')
    st.write(f":material/clock_loader_10: Top: {potd['Top']}")
    st.write(f":material/clock_loader_40: Middle: {potd['Middle']}")
    st.write(f":material/clock_loader_90: Base: {potd['Base']}")
    st.subheader(':material/ent: Accords')
    display_accords(accord_data)

# Environment Information
with col3:
    environment_chart(environment)