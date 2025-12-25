import streamlit as st
import pandas as pd
from pdf_export import generate_menu_dinner_pdf, generate_menu_lunch_pdf


#############################################################################
############ CONSTANTS ######################################################
SAVE_MENU_DIR = 'menu'
ss = st.session_state
MENU_COL = [ 'FL_ON_LUNCH', 'FL_ON_DINNER'
            , 'LB_CATEGORY', 'LB_DISH_NAME'
            , 'LB_DISH_SHORT_DESC', 'LB_DISH_LONG_DESC'
            , 'NBR_DISH_PRICE']
LS_DISH_TYPE = ['Cocktail', 'Dessert', 'Entrée', 'Plats', 'Suggestions du chef']


#############################################################################
############ Easter Eggs ####################################################

#############################################################################
############ FUNCTIONS ######################################################
############ FUNCTIONS - SS ######################################################
def initialize_ss() -> None:
    #TAB MENU MIDI
    if 'menu_midi' not in ss:
        ss['menu_midi'] = None
    if 'suggestion_midi' not in ss:
        ss['suggestion_midi'] = None
    if 'entree_midi' not in ss:
        ss['entree_midi'] = None
    if 'plat_midi' not in ss:
        ss['plat_midi'] = None
    if 'dessert_midi' not in ss:
        ss['dessert_midi'] = None

    #TAB MENU SOIR
    if 'menu_soir' not in ss:
        ss['menu_soir'] = None
    if 'suggestion_soir' not in ss:
        ss['suggestion_soir'] = None
    if 'cocktail_soir' not in ss:
        ss['cocktail_soir'] = None
    if 'dessert_soir' not in ss:
        ss['dessert_soir'] = None

    #TAB MENU COMPLET
    if 'entree_choix' not in ss:
        ss['entree_choix'] = None
    if 'plat_choix' not in ss:
        ss['plat_choix'] = None
    if 'suggestion_choix' not in ss:
        ss['suggestion_choix'] = None
    if 'dessert_choix' not in ss:
        ss['dessert_choix'] = None
    if 'cocktail_choix' not in ss:
        ss['cocktail_choix'] = None

    if 'df_full' not in ss:
        ss['df_full'] = None   
    if 'selected_category' not in ss:
        ss['selected_category'] = None
    if 'selected_category_selectbox' not in ss:
        ss['selected_category_selectbox'] = None

    #TECHNICAL
    if 'debug_mode' not in ss:
        ss['debug_mode'] = False


############ FUNCTIONS - DATA LOAD AND TRANSFORMATION  ######################################################
def concat_columns(ss_name) -> None:
    """" Create a new column - For data editor dropdown"""
    df = ss[ss_name]
    df['LB_FULL_DESC'] = df.apply(
        lambda row: f"{row['LB_DISH_NAME']} - {row['LB_DISH_SHORT_DESC']} - {row['NBR_DISH_PRICE']}",
        axis=1 )

def unconcat_columns(df) -> None:
    """" Update data according to user selection"""
    df['LB_DISH_NAME'] = df.apply(
        lambda row: f"{row['LB_FULL_DESC'].split(' - ')[0]}",
        axis=1 )
    df['LB_DISH_SHORT_DESC'] = df.apply(
        lambda row: f"{row['LB_FULL_DESC'].split(' - ')[1]}",
        axis=1 )
    df['NBR_DISH_PRICE'] = df.apply(
        lambda row: f"{row['LB_FULL_DESC'].split(' - ')[2]}",
        axis=1 )
    return (df)
    
def load_data(file_path) -> None:
    try:
        ss['menu'] = pd.read_csv(file_path
                                , sep=';'
                                , header=0)
        ss['menu'].sort_values(by=['LB_CATEGORY', 'LB_DISH_NAME']
                                             , axis=0
                                             , ascending=True
                                             , inplace=True)
    except Exception as e:
        st.error(f"Error loading file: {e}")    

def create_df_midi_soir():
    menu = ss['menu']
    ss['menu_midi'] = menu[(menu['FL_ON_LUNCH']==1)] #affichage du menu midi précédent
    menu_midi_prec = ss['menu_midi']
    ss['suggestion_midi'] = menu_midi_prec[menu_midi_prec['LB_CATEGORY'] == 'Suggestions du chef'].reset_index(drop=True)
    ss['entree_midi']   = menu_midi_prec[menu_midi_prec['LB_CATEGORY'] == 'Entrée'].reset_index(drop=True)
    ss['plat_midi']   = menu_midi_prec[menu_midi_prec['LB_CATEGORY'] == 'Plats'].reset_index(drop=True)
    ss['dessert_midi']    = menu_midi_prec[menu_midi_prec['LB_CATEGORY'] == 'Dessert'].reset_index(drop=True)
    
    ss['menu_soir'] = menu[(menu['FL_ON_DINNER']==1)]
    menu_soir_prec = ss['menu_soir']
    ss['suggestion_soir'] = menu_soir_prec[menu_soir_prec['LB_CATEGORY'] == 'Suggestions du chef'].reset_index(drop=True)
    ss['dessert_soir']    = menu_soir_prec[menu_soir_prec['LB_CATEGORY'] == 'Dessert'].reset_index(drop=True)
    ss['cocktail_soir']   = menu_soir_prec[menu_soir_prec['LB_CATEGORY'] == 'Cocktail'].reset_index(drop=True)

def get_list_choices():
    menu = ss['menu']
    ss['suggestion_choix'] = menu[menu['LB_CATEGORY'] == 'Suggestions du chef']['LB_FULL_DESC'].unique().tolist()
    ss['entree_choix']     = menu[menu['LB_CATEGORY'] == 'Entrée']['LB_FULL_DESC'].unique().tolist()
    ss['plat_choix']       = menu[menu['LB_CATEGORY'] == 'Plats']['LB_FULL_DESC'].unique().tolist()
    ss['dessert_choix']    = menu[menu['LB_CATEGORY'] == 'Dessert']['LB_FULL_DESC'].unique().tolist()
    ss['cocktail_choix']    = menu[menu['LB_CATEGORY'] == 'Cocktail']['LB_FULL_DESC'].unique().tolist()
    
############ FUNCTIONS - TECHNICAL ######################################################
def switch_debug_mode():
    ss['debug_mode'] = not(ss['debug_mode'])      

def update_db(df :pd.DataFrame, save_path :str) -> None:
    COL_TO_EXPORT = MENU_COL
    df[COL_TO_EXPORT].to_csv(path_or_buf=save_path
                    , sep=';'
                    , encoding='utf-8')
    st.success("Données mises à jour!", icon="✅")
    ss.clear()

def get_key():
    changes = ss["df_suggestion_soir_key"].get("edited_rows", {})
    #unconcat
    st.write("changes", changes)

############ FUNCTIONS - CALLBACK ######################################################
def full_call_back_midi(df1, df2, df3, df4):
    df1=unconcat_columns(df1)
    df2=unconcat_columns(df2)
    df3=unconcat_columns(df3)
    df4=unconcat_columns(df4)
    generate_menu_lunch_pdf(df1, df2, df3, df4)
    st.success("Menu midi exported", icon="✅")

def full_call_back_soir(df1, df2, df3):
    df1=unconcat_columns(df1)
    df2=unconcat_columns(df2)
    df3=unconcat_columns(df3)
    generate_menu_dinner_pdf(df1, df2, df3)
    st.success("Menu soir exported", icon="✅")


#############################################################################
############ PAGE CONFIG ####################################################
st.set_page_config(layout='wide')
st.title('Création du menu')

# st.checkbox(label='Debug mode'
#             , on_change=switch_debug_mode)

#############################################################################
############ CODE      ######################################################

def main() -> None:
    initialize_ss()
    load_data('files/menu.csv')
    concat_columns('menu')
    create_df_midi_soir()
    get_list_choices()

    tab_midi, tab_soir, tab_modif = st.tabs(["Menu_midi", "Menu_soir", "Modifier/Ajouter/Supprimer"])

    with tab_midi:
        st.title('☀️ MENU DU MIDI')
        st.header('Suggestions du chef')

        df_suggestion_midi = st.data_editor(
                            data=ss['suggestion_midi']
                            , key = 'df_suggestion_midi'
                            , column_order=['LB_FULL_DESC']
                            , column_config={
                                "LB_FULL_DESC": st.column_config.SelectboxColumn(
                                    "Suggestions",
                                    width="medium",
                                    options=ss['suggestion_choix'],
                                    required=True,
                                )}
                            # , hide_index=True
                            , num_rows="dynamic"
                        )

        st.header('Entrée')
        df_entree_midi = st.data_editor(
                            data=ss['entree_midi']
                            , key = 'df_entree_midi'
                            , column_order=['LB_FULL_DESC']
                            , column_config={
                                "LB_FULL_DESC": st.column_config.SelectboxColumn(
                                    "Desserts",
                                    width="medium",
                                    options=ss['entree_choix'],
                                    required=True,
                                )}
                            # , hide_index=True
                            , num_rows="dynamic"
                        )
        
        st.header('Plat du jour')
        df_plat_midi = st.data_editor(
                            data=ss['plat_midi']
                            , key = 'df_plat_midi'
                            , column_order=['LB_FULL_DESC']
                            , column_config={
                                "LB_FULL_DESC": st.column_config.SelectboxColumn(
                                    "Desserts",
                                    width="medium",
                                    options=ss['plat_choix'],
                                    required=True,
                                )}
                            # , hide_index=True
                            , num_rows="dynamic"
                        )
        
        st.header('Desserts maison')
        df_dessert_midi = st.data_editor(
                            data=ss['dessert_midi']
                            , key = 'df_dessert_midi'
                            , column_order=['LB_FULL_DESC']
                            , column_config={
                                "LB_FULL_DESC": st.column_config.SelectboxColumn(
                                    "Desserts",
                                    width="medium",
                                    options=ss['dessert_choix'],
                                    required=True,
                                )}
                            # , hide_index=True
                            , num_rows="dynamic"
                        )

        st.button(
                    label='Créer le menu du midi'
                    , on_click=full_call_back_midi
                    , args=( df_suggestion_midi
                            , df_entree_midi
                            , df_plat_midi
                            , df_dessert_midi)
                )

        if ss['debug_mode']:
            st.write(df_suggestion_soir) # 👈 Show the value in Session State










    with tab_soir:
        st.title('🌙 MENU DU SOIR')
        st.header('Suggestions du chef')

        df_suggestion_soir = st.data_editor(
                            data=ss['suggestion_soir']
                            , column_order=['LB_FULL_DESC']
                            , column_config={
                                "LB_FULL_DESC": st.column_config.SelectboxColumn(
                                    "Suggestions",
                                    width="medium",
                                    options=ss['suggestion_choix'],
                                    required=True,
                                )}
                            # , hide_index=True
                            , num_rows="dynamic"
                            # , on_change=update_columns
                        )

        st.header('Desserts maison')
        df_dessert_soir = st.data_editor(
                            data=ss['dessert_soir']
                            , column_order=['LB_FULL_DESC']
                            , column_config={
                                "LB_FULL_DESC": st.column_config.SelectboxColumn(
                                    "Desserts",
                                    width="medium",
                                    options=ss['dessert_choix'],
                                    required=True,
                                )}
                            # , hide_index=True
                            , num_rows="dynamic"
                        )
        
        st.header('Cocktails du moment')
        df_cocktail_soir = st.data_editor(
                            data=ss['cocktail_soir']
                            , column_order=['LB_FULL_DESC']
                            , column_config={
                                "LB_FULL_DESC": st.column_config.SelectboxColumn(
                                    "Cocktails",
                                    width="medium",
                                    options=ss['cocktail_choix'],
                                    required=True,
                                )}
                            # , hide_index=True
                            , num_rows="dynamic"
                        )

        st.button(
                    label='Créer le menu du soir'
                    , on_click=full_call_back_soir
                    , args=( df_suggestion_soir
                            , df_dessert_soir
                            , df_cocktail_soir)
                )

        if ss['debug_mode']:
            st.write(df_suggestion_soir) # 👈 Show the value in Session State
        

    with tab_modif:
        st.title('🔧 MODIFIER LA CARTE')
        st.header('')

        # choose_dish_type = st.selectbox(
        #     label='Choisir la catégorie'
        #     , options=LS_DISH_TYPE
        # )

        df_full = st.data_editor(
                data=ss['menu']
                , column_order=MENU_COL
                # , hide_index=True
                , num_rows="dynamic"
        )

        st.button(
                label='Sauvegarder'
                , on_click=update_db
                , args=(
                    df_full
                    , 'files/menu.csv')
            )

if __name__ == '__main__':
    main()
