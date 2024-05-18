import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os

df = pd.read_csv('Data boq.csv', encoding='utf-8')

df['vendor_name'] = df['vendor_name'].replace({
    'PT. Berca Engineering': 'PT Berca Engineering',
    'PT. Fadil Jaya abadi' : 'PT Fadil Jaya abadi',
    'PT. JAYA ABADI' : 'PT Jaya Abadi',
    'PT. Kaliraya Sari' : 'PT Kaliraya Sari',
    'PT. Yaop yaya op op ' : 'PT Yaop Yaya Op Op',
    'Universal export' : 'Universal Export',
    'pt yes' : 'PT Yes'})
    
boq_df = df.groupby(['vendor_name', 'month']).agg({
    'plan_cost': 'sum',
    'actual_cost': 'sum'
}).reset_index()
boq_df['month'] = pd.to_datetime(boq_df['month'])
boq_df['month'] = boq_df['month'].dt.strftime('%B %Y')

output_dir = 'output_graphs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def create_and_save_figure(vendor_name, output_filename):
    vendor_data = boq_df[boq_df['vendor_name'] == vendor_name]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=vendor_data['month'],
        y=vendor_data['plan_cost'],
        mode='markers',
        marker=dict(color='blue'),
        name='Plan Cost'))
    fig.add_trace(go.Scatter(
        x=vendor_data['month'],
        y=vendor_data['actual_cost'],
        mode='markers',
        marker=dict(color='green'),
        name='Actual Cost'))
    total_plan_per_month = vendor_data.groupby('month')['plan_cost'].sum()
    total_actual_per_month = vendor_data.groupby('month')['actual_cost'].sum()
    max_threshold = (total_plan_per_month.max() + total_actual_per_month.max()) / 2
    fig.add_hline(y=max_threshold, line=dict(color='red', dash='dash'), name='Max Threshold')
    fig.update_layout(
        title=f'{vendor_name} Performance Analysis',
        xaxis_title='Time',
        yaxis_title='Cost',
        yaxis=dict(tickprefix='IDR '),
        legend_title='Legend')
    
    fig_html = pio.to_html(fig, full_html=False)
    with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as f:
        f.write(fig_html)

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

for vendor, filename in vendors:
    create_and_save_figure(vendor, filename)