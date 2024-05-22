import pandas as pd 
import plotly.express as px
import os

def process_data_and_generate_plots():
    df = pd.read_csv('Data boq.csv', encoding='utf-8')

    vendor_mapping = {
        'PT. Berca Engineering': 'PT Berca Engineering',
        'PT. Fadil Jaya abadi': 'PT Fadil Jaya abadi',
        'PT. JAYA ABADI': 'PT Jaya Abadi',
        'PT. Kaliraya Sari': 'PT Kaliraya Sari',
        'PT. Yaop yaya op op ': 'PT Yaop Yaya Op Op',
        'Universal export': 'Universal Export',
        'pt yes': 'PT Yes'
    }
    df['vendor_name'] = df['vendor_name'].replace(vendor_mapping)

    boq_df = df.groupby(['vendor_name', 'month']).agg({
        'plan_cost': 'sum',
        'actual_cost': 'sum'
    }).reset_index()
    boq_df['month'] = pd.to_datetime(boq_df['month'])
    boq_df['month'] = boq_df['month'].dt.strftime('%B %Y')
    
    output_dir = 'output_graphs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for vendor_name, filename in vendors:
        vendor_data = boq_df[boq_df['vendor_name'] == vendor_name]
        fig = px.scatter(vendor_data, x='month', y=['plan_cost', 'actual_cost'], 
                         color_discrete_map={'plan_cost': 'blue', 'actual_cost': 'green'},
                         title=f'{vendor_name} Performance Analysis',
                         labels={'month': 'Time', 'value': 'Cost'},
                         hover_name='vendor_name')
        fig.update_yaxes(tickprefix='IDR ')
        fig.add_hline(y=(vendor_data['plan_cost'].max() + vendor_data['actual_cost'].max()) / 2, 
                      line=dict(color='red', dash='dash'), name='Max Threshold')
        fig.write_html(os.path.join(output_dir, filename))
        
vendors = [
    ('PT Vendor Al Fatih', 'fig_al_fatih.html'),
    ('PT Vendor Sejati', 'fig_sejati.html'),
    ('PT Berca Engineering', 'fig_berca.html'),
    ('PT Fadil Jaya abadi', 'fig_fadiljaya.html'),
    ('PT Jaya Abadi', 'fig_jayaabadi.html'),
    ('PT Kaliraya Sari', 'fig_kalirayasari.html'),
    ('PT Yaop Yaya Op Op', 'fig_yaopyaya.html'),
    ('SCM', 'fig_scm.html'),
    ('Universal Export', 'fig_universal.html'),
    ('PT Yes', 'fig_yes.html')
]

if __name__ == "__main__":
    process_data_and_generate_plots()