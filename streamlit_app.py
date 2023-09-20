import streamlit as st
from transform import get_categories, get_main_df, resubmit_category_column
from load_data import transfer_data_from_drive
from streamlit_func import GRAPH_DICT



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
        st.button("Load data", on_click = transfer_data_from_drive)
        st.button('Update data', on_click = resubmit_category_column)
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
    
    st.title("Select the graph")
    selected_page = st.selectbox(
        label="выберите график",
        options=GRAPH_DICT.keys(),
    )

    GRAPH_DICT[selected_page](
        data = data,
        start_date = start_date,
        end_date = end_date,
        selected_options = selected_options,
        categories = categories
    )
    
if __name__=='__main__':
    app()
