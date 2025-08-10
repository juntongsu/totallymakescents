# -------------------------------------------------------------------------
# Import libraries
# -------------------------------------------------------------------------
import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    "flowers":    "#E8C1D1",
    "natural and synthetic, popular and weird":  "#B0C4DE",
    "greens, herbs and fougeres":"#228B22",
    "fruits, vegetables and nuts":"#FF6EB4",
    "sweets and gourmand smells":"#D2B48C",
    "woods and mosses":"#556B2F",
    "beverages": "#FFB6C1",
    "spices":    "#D2691E",
    "musk, amber, animalic smells":"#8B0000",
    "citrus smells":"#FFF44F", 
    "resins and balsams":"#FFBF00",
    "white flowers":"#F5F5F5",
    "uncategorized":"#E0FFFF",
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
    accords = data.index.to_list()[:5]
    values = data.values[:5]
    
    colors = [get_accord_color(a) for a in accords]
    # sys_bg_color = '#FFFFFF'
    # sys_fr_color = '#0e1117'
    if st.context.theme.type == 'dark':
        sys_bg_color = '#0e1117'
        sys_fr_color = '#FFFFFF'
    else:
        sys_bg_color = '#FFFFFF'
        sys_fr_color = '#0e1117'
    
    fig, ax = plt.subplots(figsize=(6, 3), facecolor=sys_bg_color)
    ax.set_facecolor(sys_bg_color)

    y_pos = np.arange(len(accords))
    ax.barh(y_pos, values, color=colors, height=1)
    for i in range(min(len(values), 5)):
        accord = accords[i]
        val = values[i]
        bg = colors[i]
        if (val >= values[0] / 2):
            text_color = get_text_color(bg)
            ax.text(val / 2, i, accord, va='center', ha='center', color=text_color, fontsize=10)
        else:
            ax.text((values[0]+val)/ 2, i, accord, va='center', ha='center', color=sys_fr_color, fontsize=10)
    ax.invert_yaxis()
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

def get_img_fragrantica(input_url):
    perfume_id = input_url.split('-')[-1].split('.')[0]
    return f'https://fimgs.net/mdimg/perfume-thumbs/375x500.{perfume_id}.jpg'