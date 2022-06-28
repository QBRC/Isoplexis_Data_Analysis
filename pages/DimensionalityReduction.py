import dash
dash.register_page(__name__, title = "Dimensionality Reduction")
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from dash import no_update
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from sklearn.manifold import TSNE


#methods for PCA and TSNE
method_pcatsne = ["Standard Scalar Normalized", "Not Normalized"]
#values neccessary for tsne function
iterations = [250, 300, 400, 500, 600, 700, 800, 900, 1000]
perplexity = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
plot_types = ['2D', '3D']


centerStyle = {'textAlign': 'center'}

layout = html.Div(
    [   html.H2("Dimensionality Reduction"),
        html.H4("PCA is a linear dimensionality reduction technique and TSNE is a non-linear dimensionality reduction technique."),
        html.H5("Note: TSNE might take a minute to reload since this is calculated in real-time."),
        html.H4("Select whether or not to normalize dimensionality reduction plots."),
        html.P("Data is normally normalized before performing dimensionality reduction."),
        dcc.RadioItems(
                    id="method_radio",
                    options=method_pcatsne,
                    value="Standard Scalar Normalized",
                    inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                    style=centerStyle),
        html.H4("Select to visualize the plot in 2D or 3D."),  
        dcc.RadioItems(
                id="plot_types",
                options=plot_types,
                value="3D",
                inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                style=centerStyle),

        dbc.Row([dbc.Col(html.Div( 
                html.Div(dcc.Graph(id='dim_red_fig')),  
                )), 
        dbc.Col(html.Div([  
                html.Div(dcc.Graph(id='ts_dim_red_fig')),  
                html.H5("Select Perplexity of Nearest Neighbors: ", style=centerStyle),
                html.P("Perplexity is the balance between local and global aspects of the data."), 
                dcc.RadioItems(
                    id="perplexity_radio",
                    options=perplexity,
                    value=30,
                    inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                    style=centerStyle),
                html.H5("Select Number of TSNE Iterations: ", style=centerStyle),
                html.P("Note: The more iterations performed, the slower the algorithm runs."), 
                dcc.RadioItems(
                    id="iterations_radio",
                    options=iterations,
                    value=500,
                    inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                    style=centerStyle)
                ]))])
    ], style = centerStyle
)

#callback: pca function
@callback(Output('dim_red_fig', 'figure'),
            Input('analysis-button','n_clicks'),
            Input('method_radio', 'value'),
            Input('plot_types', 'value'),
            Input('cyto_list', 'data'),
            State ('stored-data-reordered', 'data'), 
            State ('color_discrete_map', 'data'),
            )

def pca_func(n, method, plot_type, cytokines, df, color_discrete_map):
    try:
        if n is None: 
            return no_update
        else:
            df = pd.DataFrame(df)
            Y = df.loc[:,['Treatment Conditions']].values
            x = df.loc[:, cytokines].values
            # # Separating out the target
            if method == "Standard Scalar Normalized":
                x = StandardScaler().fit_transform(x)
            pca = PCA(n_components=3)
            principalComponents = pca.fit_transform(x)
            df = pd.DataFrame(principalComponents)
            df2 = df.rename({0: "PCA 1", 1: "PCA 2", 2: "PCA 3"}, axis=1) 
            df2['Treatment Conditions'] = Y
            if plot_type == "2D":
                fig = px.scatter(df2, x="PCA 1", y="PCA 2", color="Treatment Conditions", color_discrete_map = color_discrete_map)
            else:
                fig = px.scatter_3d(df2, x="PCA 1", y="PCA 2", z="PCA 3", color="Treatment Conditions", color_discrete_map = color_discrete_map)
            fig.update_layout(title_text = method+" PCA", title_x=0.5, )
            fig.update_layout(plot_bgcolor='rgb(255,255,255)')
            fig.update_traces(marker={'size': 5}) 
            return(fig)
    except:
        return no_update


#callback: tsne function
@callback(Output('ts_dim_red_fig', 'figure'),
            Input('analysis-button','n_clicks'),
            Input('method_radio', 'value'),
            Input('plot_types', 'value'),
            Input('perplexity_radio', 'value'),
            Input('iterations_radio', 'value'),
            Input('cyto_list', 'data'),
            State ('stored-data-reordered', 'data'), 
            State ('color_discrete_map', 'data'),
           )

def tsne_func(n, method, plot_type, perplexity, iterations, cytokines, df , color_discrete_map):
    try:
        if n is None: 
            return no_update

        else:
            df = pd.DataFrame(df)
            Y = df.loc[:,['Treatment Conditions']].values
            x = df.loc[:, cytokines].values
            # # Separating out the target
            if method == "Standard Scalar Normalized":
                x = StandardScaler().fit_transform(x)
            pca = PCA()
            principalComponents = pca.fit_transform(x)
            tsne = TSNE(n_components=3, perplexity=perplexity, n_iter=iterations).fit_transform(principalComponents)
            df = pd.DataFrame(tsne)
            df2 = df.rename({0: "TSNE 1", 1: "TSNE 2", 2: "TSNE 3"}, axis=1) 
            df2['Treatment Conditions'] = Y
            if plot_type == "2D":
                fig = px.scatter(df2, x="TSNE 1", y= "TSNE 2", color="Treatment Conditions", color_discrete_map = color_discrete_map)
            else:
                fig = px.scatter_3d(df2, x="TSNE 1", y="TSNE 2", z="TSNE 3", color="Treatment Conditions", color_discrete_map = color_discrete_map)      
            fig.update_layout(title_text = method + " TSNE", title_x=0.5, )
            fig.update_layout(plot_bgcolor='rgb(255,255,255)')
            fig.update_traces(marker={'size': 5})
            return(fig)
    except:
        return no_update
