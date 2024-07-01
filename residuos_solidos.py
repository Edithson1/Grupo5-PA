import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image

# Configurar la página titulo, icono 
st.set_page_config(page_title="Residuos Municipales", page_icon="🚮", layout="wide")

# Título de la aplicación
st.title('***RESIDUOS MUNICIPALES GENERADOS ANUALMENTE***')
st.subheader("Residuos municipales generados por periodo y región")
st.write("En el Perú, la gestión eficiente de los residuos sólidos municipales es un desafío prioritario. Esta página web presenta los datos de generación anual de residuos municipales para las 24 regiones del país, información fundamental para desarrollar políticas y estrategias de recolección, transporte, tratamiento y disposición final adecuados. Los datos provienen de informes técnicos y estadísticas oficiales del Ministerio del Ambiente y otras entidades, y serán actualizados periódicamente para brindar un panorama confiable sobre la situación de los residuos sólidos a nivel regional y nacional.")

# Mostrar una imagen 
image_path = 'imagen.jpg' 
try:
    image = Image.open(image_path)
    st.image(image, caption='Imagen 1: Residuos sólidos, Problema global', use_column_width=True)
except FileNotFoundError:
    st.error(f"Error de ruta: {image_path}")

# Cargar el archivo CSV con el encoding latin1 y separador ;
#try controlador de errores
file_path = 'data.csv'
try:
    df = pd.read_csv(file_path, encoding='latin1', sep=';')
except UnicodeDecodeError:
    st.error("Error al subir el archivo.")
    st.stop()
except Exception as e:
    st.error(f"Error al cargar el archivo CSV: {str(e)}")
    st.stop()

# Mostrar el DataFrame en Streamlit
st.subheader('Datos del archivo CSV')
st.dataframe(df)

#seleccionar opcion de configuracion
configuracion = st.selectbox('Selecciona configuracion del grafico', ['Simple', 'Avanzado'])
if configuracion == "Simple":
    # Selecconar el tipo de gráfico
    tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Circular', 'Barras'])
    
    # Selección de columna para visualizar
    columna_grafico = st.selectbox('Selecciona una columna para visualizar', df.columns[7:14])

else:
    region = st.selectbox('Selecciona la region', list(df['REG_NAT'].unique())+['ALL'])
    df_filtrado = df[df['REG_NAT'] == region]
    departamento = st.selectbox('Selecciona el departamento', list(df_filtrado['DEPARTAMENTO'].unique())+['ALL'])
    df_filtrado1 = df_filtrado[df_filtrado['DEPARTAMENTO'] == departamento]
    provincia = st.selectbox('Selecciona la provincia', list(df_filtrado1['PROVINCIA'].unique())+['ALL'])
    df_filtrado2 = df_filtrado1[df_filtrado1['PROVINCIA'] == provincia]
    distrito = st.selectbox('Selecciona el distrito', list(df_filtrado2['DISTRITO'].unique())+['ALL'])
    df_filtrado3 = df_filtrado2[df_filtrado2['DISTRITO'] == distrito]

if st.button('Generar gráfico'):
    sizes = df[columna_grafico].value_counts()
    if tipo_grafico == 'Circular':
        # Gráfico circular interactivo con plotly
        st.subheader(f'Diagrama circular para {columna_grafico}')
        fig = px.pie(df, names=columna_grafico, title=f'Distribución de {columna_grafico}', hole=0.3)
        st.plotly_chart(fig)
    elif tipo_grafico == 'Barras':
        # Gráfico de barras interactivo con plotly
        st.subheader(f'Gráfico de barras para {columna_grafico}')
        fig = px.bar(sizes, x=sizes.index, y=sizes.values, labels={'x': columna_grafico, 'y': 'Frecuencia'}, title=f'Distribución de {columna_grafico}')
        fig.update_layout(xaxis_title=columna_grafico, yaxis_title='Frecuencia')
        st.plotly_chart(fig)

        # Información adicional sobre el elemento seleccionado
        st.subheader('Detalles adicionales')
        selected_value = st.selectbox('Selecciona un valor para ver detalles', sizes.index)
        df_seleccionado = df[df[columna_grafico] == selected_value]
        st.dataframe(df_seleccionado)

        # Mostrar información específica de distrito si aplica
        if 'DISTRITO' in df_seleccionado.columns:
            distrito_info = df_seleccionado[['DISTRITO', 'DEPARTAMENTO']].drop_duplicates()
            st.write('Información de distritos y sus ubicaciones:')
            st.dataframe(distrito_info)

# Información general sobre los datos
st.subheader('Resumen estadístico')
st.write(df.describe())

# Notas adicionales o información relevante
st.sidebar.subheader('Notas:')
st.sidebar.write('Visualizar datos de residuos municipales anuales.')

# Código fuente y contacto
st.sidebar.subheader('Contacto:')
st.sidebar.write('Para más información, contactar a:')
st.sidebar.write('Grupo 4')
st.sidebar.write('correo electronico')
