import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Inicializar o aplicativo Dash
app = Dash(__name__)

server = app.server

# Ler o arquivo Excel
file_path = 'Planilha Geral - Índice Trilema Brasil.xlsx'
df = pd.read_excel(file_path, sheet_name='Trilema energético')

# Derreter os dados filtrados para Equidade, Segurança e Ambiental
df_equidade = pd.melt(
    df,
    id_vars=['Região', 'Estado'],
    value_vars=['Equidade 2018', 'Equidade 2019', 'Equidade 2020', 'Equidade 2021', 'Equidade 2022'],
    var_name='Dimensão',
    value_name='Escala'
)

df_seguranca = pd.melt(
    df,
    id_vars=['Região', 'Estado'],
    value_vars=['Segurança 2018', 'Segurança 2019', 'Segurança 2020', 'Segurança 2021', 'Segurança 2022'],
    var_name='Dimensão',
    value_name='Escala'
)

df_ambiental = pd.melt(
    df,
    id_vars=['Região', 'Estado'],
    value_vars=['Ambiental 2018', 'Ambiental 2019', 'Ambiental 2020', 'Ambiental 2021', 'Ambiental 2022'],
    var_name='Dimensão',
    value_name='Escala'
)

df_ambiental['Ano'] = df_ambiental['Dimensão'].str.slice(-4)
df_equidade['Ano'] = df_equidade['Dimensão'].str.slice(-4)
df_seguranca['Ano'] = df_seguranca['Dimensão'].str.slice(-4)

# Obter todas as regiões únicas
estado = df_ambiental['Estado'].unique()
ano = df_ambiental['Ano'].unique()

# Layout do aplicativo
app.layout = html.Div(
    style={
        'height' : '800px',
        'width': '1600px',  # Definindo a largura da Div
        'margin': '0 auto',  # Centraliza a Div
        'padding': '20px',  # Espaçamento interno
        'border': '2px solid #000',  # Borda para visualizar a Div
        'display': 'flex',  # Usar flexbox
        'flexDirection': 'row',  # Colocar os itens em linha
        'alignItems': 'flex-start',  # Alinha os itens no topo
    },
    children=[
        html.Div(
            style={
                'display': 'flex', 
                'flexDirection': 'column',  # Coloca dropdowns em coluna
                'marginRight': '20px'  # Espaçamento à direita
            },
            children=[
                html.H1("Vetores 3D Interativos", style={'fontFamily' : 'Helvetica'}),
                dcc.Dropdown(
                    id='estado-dropdown',
                    options=[{'label': estado, 'value': estado} for estado in estado],
                    value=estado[0],  # Valor padrão
                    clearable=False,
                    style={
                        'fontFamily' : 'Helvetica',
                        'fontSize' : '16px',
                        'color' : 'black',
                    }
                ),
                dcc.Dropdown(
                    id='ano-dropdown',
                    options=[{'label': ano, 'value': ano} for ano in ano],
                    value=ano[0],  # Valor padrão
                    clearable=False,
                    style={
                        'fontFamily' : 'Helvetica',
                        'fontSize' : '16px',
                        'color' : 'black',
                    }
                ),
            ]
        ),
        # Div para o gráfico
        html.Div(
            dcc.Graph(
                id='vetor-grafico',
                config={'displayModeBar': True},  # Exibe a barra de controle do gráfico
                style={'height': '600px', 'width': '800px'}  # Tamanho da figura
            ),
            style={
                'flex': '1',

                }  # Ocupa o espaço restante
        ),
        # div para os angulos de inclinação
        html.Div(
            id = 'angulos-div',
            style={
                'width' : '300px',
                'padding' : '10px',
                'border' : '1px solid #ddd',
                'backgroundColor' : '#f9f9f9'
            },
            children=[
                html.H3("Ângulos de Inclinação"),
                html.Hr(),
                html.P("Comparação entre cada um dos eixos com o vetor ideal "),
                html.P(id='angulo-ideal-x'),
                html.P(id='angulo-ideal-y'),
                html.P(id='angulo-ideal-z'),
                html.Hr(),
                html.P("Comparação entre cada um dos eixos com o vetor generico "),
                html.P(id='angulo-generico-x'),
                html.P(id='angulo-generico-y'),
                html.P(id='angulo-generico-z'),
                html.Hr(),
                html.P(id='angulo-generico-ideal'),
                html.Hr(),
                html.P("Comparação das dimensões entre si"),
                html.P(id='angulo-ambiental-seguranca'),
                html.P(id='angulo-ambiental-equidade'),
                html.P(id='angulo-seguranca-equidade'),
            ]
        )
    ]
)

# Callback para atualizar o gráfico com base na seleção do dropdown
@app.callback(
    [Output('vetor-grafico', 'figure'),
     Output('angulo-ideal-x', 'children'),
     Output('angulo-ideal-y', 'children'),
     Output('angulo-ideal-z', 'children'),
     Output('angulo-generico-x', 'children'),
     Output('angulo-generico-y', 'children'),
     Output('angulo-generico-z', 'children'),
     Output('angulo-generico-ideal', 'children'),
     Output('angulo-ambiental-seguranca', 'children'),
     Output('angulo-ambiental-equidade', 'children'),
     Output('angulo-seguranca-equidade', 'children')],
    [Input('estado-dropdown', 'value'),
     Input('ano-dropdown', 'value')]
)
def atualizar_grafico(estado_selecionado, ano_selecionado):
    # Filtrar os dados pela região selecionada
    df_ambiental_filtrado = df_ambiental[(df_ambiental['Estado'] == estado_selecionado) &
                                         (df_ambiental['Ano'] == ano_selecionado)]
    
    df_seguranca_filtrado = df_seguranca[(df_seguranca['Estado'] == estado_selecionado) &
                                         (df_seguranca['Ano'] == ano_selecionado)]
    
    df_equidade_filtrado = df_equidade[(df_equidade['Estado'] == estado_selecionado) &
                                        (df_equidade['Ano'] == ano_selecionado)]

    # Somar os elementos
    equidade = df_equidade_filtrado['Escala'].sum()
    ambiental = df_ambiental_filtrado['Escala'].sum()
    seguranca = df_seguranca_filtrado['Escala'].sum()

    # Ponto de origem
    start = [0, 0, 0]

    # Vetor ideal
    ideal = [10, 10, 10]

    # Criar a figura
    fig = go.Figure()

    # Vetor genérico
    fig.add_trace(go.Scatter3d(
        x=[start[0], equidade], y=[start[1], seguranca], z=[start[2], ambiental],
        mode='lines+markers',
        line=dict(color='red', width=5),
        marker=dict(size=4),
        name='Vetor genérico'
    ))

    # Vetor ideal
    fig.add_trace(go.Scatter3d(
        x=[start[0], ideal[0]], y=[start[1], ideal[1]], z=[start[2], ideal[2]],
        mode='lines+markers',
        line=dict(color='blue', width=5),
        marker=dict(size=4),
        name='Vetor ideal'
    ))

    # calculando os angulo
    
    # Calcular os ângulos de inclinação em relação aos eixos
    def calcular_angulo_eixo(vetor, eixo):
        return np.degrees(np.arccos(np.clip(np.dot(vetor, eixo) / (np.linalg.norm(vetor) * np.linalg.norm(eixo)), -1.0, 1.0)))

    def angulo_entre_eixos(cod1, cod2):
        return np.degrees(np.arctan(cod1 / cod2)) 

    # Vetores de referência dos eixos
    eixo_x = [1, 0, 0]
    eixo_y = [0, 1, 0]
    eixo_z = [0, 0, 1]

    angulo_yz = angulo_entre_eixos(ambiental, seguranca)
    angulo_xz = angulo_entre_eixos(ambiental, equidade)
    angulo_xy = angulo_entre_eixos(seguranca, equidade)

    # Calcular ângulos de inclinação
    angulo_ideal_x = calcular_angulo_eixo(ideal, eixo_x)
    angulo_ideal_y = calcular_angulo_eixo(ideal, eixo_y)
    angulo_ideal_z = calcular_angulo_eixo(ideal, eixo_z)

    angulo_generico_x = calcular_angulo_eixo([equidade, seguranca, ambiental], eixo_x)
    angulo_generico_y = calcular_angulo_eixo([equidade, seguranca, ambiental], eixo_y)
    angulo_generico_z = calcular_angulo_eixo([equidade, seguranca, ambiental], eixo_z)

    angulo_ideal_generico = calcular_angulo_eixo(ideal, [equidade, seguranca, ambiental])

    # Ajustar limites dos eixos
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 10], title='Equidade Energética - x'),
            yaxis=dict(range=[0, 10], title='Segurança Energética - y'),
            zaxis=dict(range=[0, 10], title='Ambiental - z')
        ),
        title=f"Vetores 3D Interativos - Estado: {estado_selecionado}",
        height=800,
        width=900,
    )

    return (fig,
            f"Vetor Ideal com Eixo X: {angulo_ideal_x:.2f}°",
            f"Vetor Ideal com Eixo Y: {angulo_ideal_y:.2f}°",
            f"Vetor Ideal com Eixo Z: {angulo_ideal_z:.2f}°",
            f"Vetor Genérico com Eixo X: {angulo_generico_x:.2f}°",
            f"Vetor Genérico com Eixo Y: {angulo_generico_y:.2f}°",
            f"Vetor Genérico com Eixo Z: {angulo_generico_z:.2f}°",
            f"Angulo entre vetor genérico e ideal: {angulo_ideal_generico:.2f}°",
            f"Angulo entre ambiental e segurança: {angulo_yz:.2f}°",
            f"Angulo entre ambiental e equidade: {angulo_xz:.2f}°",
            f"Angulo entre segurança e equidade: {angulo_xy:.2f}°")

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
