
import plotly.express as px
import pandas as pd

def hbar_spends(data,start_date,end_date,selected_options,categories):
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
    return fig

def bar_income_spend_compare(data,start_date,end_date,selected_options):
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
    
    return fig

def line_catspends_by_months(data,selected_options,selected_category):
    mask = (
        (data['name'].isin(selected_options))&
        (data['category'] == selected_category)
    )
    data = data[mask]
    data['price'] = data['price'] * -1
    data['month'] = data['date'].dt.strftime('%Y-%m')
    
    data = data[['month','price']].groupby('month').sum()['price']
    data = data.reset_index()
    fig = px.line(data, x = 'month', y = 'price', markers=True, title= 'Затраты по категории по месяцам')
    
    return fig