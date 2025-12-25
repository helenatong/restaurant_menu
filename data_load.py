import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, landscape
from datetime import date
import pandas as pd
import streamlit as st

"""
y1-----y2
|      |
|      |
x1-----x2
"""

def generate_section_block(menu_pdf, df, section_title, dict_dim, end_line=True)-> int:
    #suggestions   
    menu_pdf.setFont("Helvetica-Bold", 16)
    menu_pdf.drawCentredString(dict_dim["width"]/2, dict_dim["y_current"]
                        , section_title) 
    dict_dim["y_current"] += dict_dim["y_inter_title_dish"]

    for index, row in df.iterrows():
        dish_name = str(row["LB_DISH_NAME"])
        dish_desc = ", " + str(row["LB_DISH_DESC"])
        if dish_desc==', nan': #pas de description
            dish_desc=''
        dish_price = f"{row['NBR_DISH_PRICE']}€"

        menu_pdf.setFont("Helvetica-Bold", 10) #nom du plat
        width_dish = menu_pdf.stringWidth(dish_name , "Helvetica-Bold", 10)
        menu_pdf.setFont("Helvetica-Oblique", 8) #nom du plat
        width_desc = menu_pdf.stringWidth(dish_desc , "Helvetica-Oblique", 8)
        total_text_width = width_dish + width_desc
        x_start = (dict_dim["width"] - total_text_width) / 2

        menu_pdf.setFont("Helvetica-Bold", 10) #nom du plat
        menu_pdf.drawString(x_start, dict_dim["y_current"], dish_name)

        menu_pdf.setFont("Helvetica-Oblique", 8) #accompagnement
        menu_pdf.drawString(x_start + width_dish, dict_dim["y_current"], dish_desc)

        menu_pdf.setFont("Helvetica", 8) #prix
        menu_pdf.drawRightString(dict_dim["x_right_price"], dict_dim["y_current"], dish_price) 
        dict_dim["y_current"] += dict_dim["y_inter_row"]

    if end_line:
        dict_dim["y_current"] += dict_dim["y_inter_line"]
        menu_pdf.line(x1=dict_dim["width"]/2-100, y1=dict_dim["y_current"], x2=dict_dim["width"]/2+100, y2=dict_dim["y_current"]) 
    dict_dim["y_current"] += dict_dim["y_inter_section"]
    return(dict_dim)


def generate_menu_dinner_pdf(df_suggestion:pd.DataFrame, df_dessert:pd.DataFrame, df_cocktail:pd.DataFrame) -> None:
    #file settings
    filename = f"menu_soir_{date.today().isoformat()}.pdf"
    menu_pdf = canvas.Canvas(filename
                            , pagesize=landscape(A5))
    menu_pdf.setTitle("menu_soir")

    #dimension settings
    width, height = landscape(A5)
    menu_pdf.translate(dx=0, dy=height) #move the origin from bottom left to upper left

    DIM = {
        "width": width
        ,"height": height
        ,"x_left" : 30
        ,"x_right_price" : width-75
        ,"y_start" : -30
        ,"y_current" : -30
        ,"y_inter_section" : -20        
        ,"y_inter_row" : -10
        ,"y_inter_line" : -10
        ,"y_inter_title_dish" : -15
    }

    #header Menu du jour 
    # menu_pdf.setFont("Helvetica-Bold", 16)
    # menu_pdf.drawCentredString(width/2
    #                             , DIM['y_start']
    #                             , 'Menu du jour') 
    # DIM["y_current"] += DIM["y_inter_line"]
    # menu_pdf.line(x1=width/2-100, y1=DIM["y_current"]
    #               , x2=width/2+100, y2=DIM["y_current"]) 
    # DIM["y_current"] += DIM["y_inter_section"]*1.5

    DIM = generate_section_block(menu_pdf, df_suggestion, section_title="Suggestions du chef", dict_dim=DIM, end_line=True)
    DIM = generate_section_block(menu_pdf, df_dessert, section_title="Desserts maison", dict_dim=DIM, end_line=True)
    DIM = generate_section_block(menu_pdf, df_cocktail, section_title="Cocktails du moment", dict_dim=DIM, end_line=False)

    menu_pdf.save()
    st.success("OK ! ")





def generate_section_lunch_menu(menu_pdf, df, section_title, dict_dim, end_line=True)-> int:
    #suggestions   
    menu_pdf.setFont("Helvetica-Bold", 14)
    menu_pdf.drawCentredString(dict_dim["width"]/2, dict_dim["y_current"]
                        , section_title) 
    dict_dim["y_current"] += dict_dim["y_inter_title_dish"]

    for index, row in df.iterrows():
        dish_name = str(row["LB_DISH_NAME"])
        dish_desc = ", " + str(row["LB_DISH_DESC"])
        if dish_desc==', nan': #pas de description
            dish_desc=''
        dish_price = f"{row['NBR_DISH_PRICE']}€"

        menu_pdf.setFont("Helvetica-Bold", 10) #nom du plat
        width_dish = menu_pdf.stringWidth(dish_name , "Helvetica-Bold", 10)
        menu_pdf.setFont("Helvetica-Oblique", 8) #nom du plat
        width_desc = menu_pdf.stringWidth(dish_desc , "Helvetica-Oblique", 8)
        total_text_width = width_dish + width_desc
        x_start = (dict_dim["width"] - total_text_width) / 2

        menu_pdf.setFont("Helvetica-Bold", 10) #nom du plat
        menu_pdf.drawString(x_start, dict_dim["y_current"], dish_name)

        menu_pdf.setFont("Helvetica-Oblique", 8) #accompagnement
        menu_pdf.drawString(x_start + width_dish, dict_dim["y_current"], dish_desc)

        menu_pdf.setFont("Helvetica", 8) #prix
        menu_pdf.drawRightString(dict_dim["x_right_price"], dict_dim["y_current"], dish_price) 
        dict_dim["y_current"] += dict_dim["y_inter_row"]

    if end_line:
        dict_dim["y_current"] += dict_dim["y_inter_line"]
        menu_pdf.line(x1=dict_dim["width"]/2-100, y1=dict_dim["y_current"], x2=dict_dim["width"]/2+100, y2=dict_dim["y_current"]) 
    dict_dim["y_current"] += dict_dim["y_inter_section"]
    return(dict_dim)


def generate_menu_lunch_pdf(df_suggestion:pd.DataFrame, df_entree:pd.DataFrame, df_plat:pd.DataFrame, df_dessert:pd.DataFrame) -> None:
    #file settings
    filename = f"menu_midi_{date.today().isoformat()}.pdf"
    menu_pdf = canvas.Canvas(filename
                            , pagesize=landscape(A5))
    menu_pdf.setTitle("menu_midi")

    #dimension settings
    width, height = landscape(A5)
    menu_pdf.translate(dx=0, dy=height) #move the origin from bottom left to upper left

    DIM = {
        "width": width
        ,"height": height
        ,"x_left" : 30
        ,"x_right_price" : width-75
        ,"y_start" : -30
        ,"y_current" : -30
        ,"y_inter_section" : -20        
        ,"y_inter_row" : -10
        ,"y_inter_line" : -10
        ,"y_inter_title_dish" : -15
    }

    DIM = generate_section_block(menu_pdf, df_suggestion, section_title="Suggestions", dict_dim=DIM, end_line=True)

    #header Menu du jour 
    menu_pdf.setFont("Helvetica-Bold", 16)
    menu_pdf.drawCentredString(width/2
                                , DIM['y_start']
                                , 'Suggestions du chef') 
    DIM["y_current"] += DIM["y_inter_line"]
    menu_pdf.line(x1=width/2-100, y1=DIM["y_current"]
                  , x2=width/2+100, y2=DIM["y_current"]) 
    DIM["y_current"] += DIM["y_inter_section"]*1.5

    DIM = generate_section_lunch_menu(menu_pdf, df_entree, section_title="Entrée", dict_dim=DIM, end_line=True)
    DIM = generate_section_lunch_menu(menu_pdf, df_plat, section_title="Plat", dict_dim=DIM, end_line=True)
    DIM = generate_section_lunch_menu(menu_pdf, df_dessert, section_title="Dessert", dict_dim=DIM, end_line=False)

    menu_pdf.save()
    st.success("OK ! ")