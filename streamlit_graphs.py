
import plotly.express as px
import streamlit as st
import pandas as pd

def hbar_spends(data,start_date,end_date,selected_options,categories,**kwargs)->None:
    mask = (
        (data['date'].dt.date >= start_date)&
        (data['date'].dt.date <= end_date)&
        (data['price']<0)&
        (data['name'].isin(selected_options))&
        (data['category'].isin(categories))
    )
    data = data[mask]
    data['price'] = data['price'] * -1

    data = data[['price','category']]
    grouped_data = data.groupby('category').sum().reset_index()

        
    fig = px.bar(
        grouped_data,
        x = 'price',
        y = 'category',
        title='Затраты по категориям',
    )
    # Sort the data by price
    fig.update_layout(yaxis={'categoryorder':'total ascending'}) # add only this line
    st.write(fig)

def bar_income_spend_compare(data,start_date,end_date,selected_options,**kwargs)->None:
    mask = (
        (data['date'].dt.date >= start_date)&
        (data['date'].dt.date <= end_date)&
        (data['name'].isin(selected_options))&
        (~data['category'].isin(['С KASPI ДЕПОЗИТА','НА KASPI ДЕПОЗИТ']))
    )
    data = data[mask]
    spends = data[data['price']<0]['price'].sum()
    spends = spends * -1
    incomes = data[data['category']=='ЗАРПЛАТА']['price'].sum()

    data = pd.DataFrame({
        'Категория':['Затраты','Прибыль'],
        'Сумма':[spends,incomes]
        })
    fig = px.bar(data, x = 'Категория', y = 'Сумма',title= 'Соотношение доходов и расходов')
    
    st.write(fig)

def line_catspends_by_months(data,selected_options,categories,**kwargs)->None:
    subcontainer = st.container()
    selected_category = subcontainer.selectbox(
            "Select one or more options:",
            categories,
    )
    mask = (
        (data['name'].isin(selected_options))&
        (data['category'] == selected_category)
    )
    data = data[mask]
    data['price'] = data['price'] * -1
    data['month'] = data['date'].dt.strftime('%Y-%m')
    
    data = data[['month','price']].groupby('month').sum()['price']
    data = data.reset_index()
    data['price_thousands'] = (data['price']/1000).round().astype(str).str[:-2] + " тыс."
    fig = px.bar(data, x = 'month', y = 'price', title= 'Затраты по категории по месяцам, тыс. тг', text = 'price_thousands')

    st.write(fig)


def line_spends(data:pd.DataFrame ,start_date,end_date,selected_options,**kwargs)->None:

    mask = (
        (data['date'].dt.date >= start_date)&
        (data['date'].dt.date <= end_date)&
        (data['name'].isin(selected_options))&
        (~data['category'].isin(['С KASPI ДЕПОЗИТА','НА KASPI ДЕПОЗИТ']))
    )
    data = data[mask]
    incomes = data[data['category']=='ЗАРПЛАТА']['price'].sum()
    
    data['spends'] = (data[data['price']<0]['price'] * -1).cumsum()
    data['spends'] = data['spends'].fillna(method="backfill")
    st.dataframe(data)
    data['spends_thousands'] = (data['spends']/1000).round().astype(str).str[:-2] + " тыс."
    fig = px.line(data, x = 'date', y = 'spends', title= 'Затраты', markers='-*')
    fig.add_hrect(y0=incomes,y1=data['spends'].max(),  line_width=0, fillcolor="red", opacity=0.2)
    fig.add_vline(x = data[data['spends'] > incomes].iloc[0].date, line_width=3, line_dash="dash", line_color="green")

    st.write(fig)


GRAPH_DICT = {
    "Траты за месяц":line_spends,
    'Затраты по категориям':hbar_spends, 
    'Соотношение доходов и расходов':bar_income_spend_compare, 
    'Затраты по категории по месяцам':line_catspends_by_months,   
    }