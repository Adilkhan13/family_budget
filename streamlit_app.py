import streamlit as st

from transform import get_categories
from load_data import transfer_data_from_drive
from streamlit_func import set_dtype, hbar_spends, bar_income_spend_compare
from google_drive import SpreadSheet



def app():
    categories = get_categories()

    main_sheet = SpreadSheet('main')
    data = main_sheet.get_df()
    data = set_dtype(data)
    max_date = data['date'].max()
    min_date = data['date'].min()

    st.button("Update data!", on_click=transfer_data_from_drive)
    # Create the date range widget
    start_date = st.date_input("Start date:",min_date,min_value=min_date, max_value=max_date)
    end_date = st.date_input("End date:",max_date,min_value=min_date, max_value=max_date)

    # Get the selected dates
    container = st.container()
    all = st.checkbox("Select all", value=True)

    if all:
        selected_options = container.multiselect(
            "Select one or more options:",
            data['name'].unique().tolist(),
            data['name'].unique().tolist(),
        )
    else:
        selected_options = container.multiselect(
            "Select one or more options:", data['name'].unique().tolist()
        )


    fig = hbar_spends(data,start_date,end_date,selected_options,categories)
    st.write(fig)

    fig = bar_income_spend_compare(data,start_date,end_date,selected_options)
    st.write(fig)

if __name__=='__main__':
    app()
