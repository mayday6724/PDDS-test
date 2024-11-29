# %%
import plotly.express as px
import pandas as pd
import numpy as np
from dash import dcc, Dash, html, Input, Output, callback

#data preprocessing - calculate raw data into data that can be used

df = pd.read_csv("/Users/iris.tsai/Desktop/PDDS/2.dataset/Sleep_health_and_lifestyle_dataset.csv")
df_3 = df[df["Stress Level"] == 3]
df_4 = df[df["Stress Level"] == 4]
df_5 = df[df["Stress Level"] == 5]
df_6 = df[df["Stress Level"] == 6]
df_7 = df[df["Stress Level"] == 7]
df_8 = df[df["Stress Level"] == 8]

stress_level = [i for i in range(3,9)]
count = df["Stress Level"].value_counts(sort=True).to_list()
activity_mins = []
disorder = []
for i in range(3,9):
    df_name = f"df_{i}"
    df_name = globals()[df_name]
    sum = round(df_name["Physical Activity Level"].mean(), 2)
    activity_mins.append(sum)
    sum_d = df_name[df_name["Sleep Disorder"].isin(["Sleep Apnea", "Insomnia"])].shape[0]
    disorder.append(sum_d)
disorder_prop = [round(i, 2) for i in (np.array(disorder) / np.array(count) * 100)]

results_dict = {"stress level": stress_level,
                "num": count,
                "activity times": activity_mins,
                "disorder num": disorder,
                "disorder rate(%)": disorder_prop}
results_df = pd.DataFrame(results_dict)


# fig = px.scatter(results_df, 
#                  x="activity times",
#                  y="stress level",
#                  size="disorder rate(%)",
#                  color="disorder rate(%)",
#                  hover_name="stress level",
#                  title="Stress Level vs. Average Activity Times to Disorder Rate"
#                  )

# fig.update_layout(
#     xaxis_title="Average Activity Times(mins)",
#     yaxis_title="Stress Level",
#     template="plotly_white"
# )

# fig.show()

# %%
# Dash
app = Dash(__name__) 
server = app.server

app.layout = html.Div(
    children=[
        html.H2('Stress Level vs. Average Activity Times to Disorder Rate'),
        dcc.RangeSlider(id='disorder_rate',
                        min=0,
                        max=100,
                        step=10,
                        marks={i: f"{i}%" for i in range(0, 101, 10)},
                        value=[0, 100]),
        dcc.Graph(id='bubble_map')
    ]
)

@app.callback(
    Output(component_id='bubble_map', component_property='figure'),
    Input(component_id='disorder_rate', component_property='value'))

def update_graph(input_value):
    df = results_df
    if input_value:
        filtered_df = df[(df['disorder rate(%)'] >= input_value[0]) & (df['disorder rate(%)'] < input_value[1])]
    
    fig = px.scatter(filtered_df, 
                 x="activity times",
                 y="stress level",
                 size="disorder rate(%)",
                 color="disorder rate(%)",
                 hover_name="stress level"
                 )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)


