import streamlit as st
from transform import get_categories, get_main_df
from load_data import transfer_data_from_drive
from streamlit_func import hbar_spends, bar_income_spend_compare,line_catspends_by_months

def app():
    categories = get_categories()
    data = get_main_df()
    max_date = data['date'].max()
    min_date = data['date'].min()
    default_start_date = max_date.replace(day=1)
    default_end_date = max_date

    with st.sidebar:
        st.header("Configuration")
        # Create the date range widget
        st.button("Update data!", on_click=transfer_data_from_drive)
        start_date = st.date_input("Start date:",default_start_date,min_value=min_date, max_value=max_date)
        end_date = st.date_input("End date:",default_end_date,min_value=min_date, max_value=max_date)
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
    
    # Get the selected dates

    fig = hbar_spends(data,start_date,end_date,selected_options,categories)
    st.write(fig)

    fig = bar_income_spend_compare(data,start_date,end_date,selected_options)
    st.write(fig)

    subcontainer = st.container()
    selected_category = subcontainer.selectbox(
            "Select one or more options:",
            categories,
        )
    
    
    fig = line_catspends_by_months(data,selected_options,selected_category)
    st.write(fig)

if __name__=='__main__':
    app()
