# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import nibabel as nib
import plotly
from dash.dependencies import Input, Output
import plotly.express as px

img = nib.load("standard_mni152.nii.gz")
data_img = img.get_fdata()
img_rgb = data_img[:, ::-1, data_img.shape[-1]//2]

fig = px.imshow(data_img[:, ::-1, data_img.shape[-1]//2].T, color_continuous_scale="gray")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash()

app.layout = html.Div([
    html.Div(id='container'),
    html.Div(dcc.Slider(
        id='my-slider',
        min=0,
        max=data_img.shape[-1],
        #marks={i: '{}'.format(10**i) for i in range(data_img.shape[-1])},
        step=1,
        value=data_img.shape[-1]//2,
    )),
])

@app.callback(
    dash.dependencies.Output('container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
        fig = px.imshow(data_img[:, ::-1, value].T, color_continuous_scale="gray")
        fig.update_traces(hovertemplate="x: %{x} <br> y: %{y}")
        fig.add_annotation(
            x=0.5,
            y=0.0,
            text="Z={}".format(value-data_img.shape[-1]//2),
            xref="paper",
            yref="paper",
            showarrow=False,
            font_size=20, font_color='white')
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        graphs = dcc.Graph(
        id='brain',
        figure=fig,
        style={"width": "100%", "display": "inline-block"})
        return html.Div(graphs)

if __name__ == '__main__':
    app.run_server(debug=True)
