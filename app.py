from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Variable global para almacenar los datos procesados
df_global = None


@app.route("/", methods=["GET", "POST"])
def index():
    global df_global

    if request.method == "POST":
        file = request.files['file']

        if file:
            # Leer el archivo Excel y guardarlo en un DataFrame
            df_global = pd.read_excel(file, sheet_name='Comparación')

          

            # Redirigir a la página principal después de cargar el archivo
            return redirect(url_for('index'))

    return render_template("index.html", zonas=df_global['ZONA'].unique() if df_global is not None else [])

@app.route("/filter", methods=["POST"])
def filter():
    global df_global

    if df_global is None:
        return redirect(url_for('index'))

    # Obtener la zona seleccionada del formulario
    zona_seleccionada = request.form.get("zona")

    if zona_seleccionada:
        # Filtrar los datos por la zona seleccionada
        df_filtrado = df_global[df_global['ZONA'] == zona_seleccionada]
    else:
        # Si no se selecciona ninguna zona, usar todo el DataFrame
        df_filtrado = df_global

    # Pivotar los datos para mostrar los productos como columnas y terminales/proveedores como filas
    df_descuentos_pivot = df_filtrado.pivot_table(index=['TERMINAL', 'PROVEEDOR'], columns='PRODUCTO', values='DESCUENTO', aggfunc='first').reset_index()
    df_precios_pivot = df_filtrado.pivot_table(index=['TERMINAL', 'PROVEEDOR'], columns='PRODUCTO', values='PRECIO VENTA INCL. IGV + PERCEPCION', aggfunc='first').reset_index()

    productos = df_filtrado['PRODUCTO'].unique()

    max_descuentos = df_descuentos_pivot.drop(columns=['TERMINAL', 'PROVEEDOR']).max().to_dict()
    min_descuentos = df_descuentos_pivot.drop(columns=['TERMINAL', 'PROVEEDOR']).min().to_dict()
    max_precios = df_precios_pivot.drop(columns=['TERMINAL', 'PROVEEDOR']).min().to_dict()
    min_precios = df_precios_pivot.drop(columns=['TERMINAL', 'PROVEEDOR']).max().to_dict()

    # Renderizar la plantilla con los datos filtrados y pivotados
    return render_template("index.html", 
                           zonas=df_global['ZONA'].unique(),
                           descuentos=df_descuentos_pivot.to_dict(orient='records'), 
                           precios=df_precios_pivot.to_dict(orient='records'),
                           productos=productos,
                            max_descuentos=max_descuentos,
                           min_descuentos=min_descuentos,
                           max_precios=max_precios,
                           min_precios=min_precios)

if __name__ == "__main__":
    app.run(debug=True)
