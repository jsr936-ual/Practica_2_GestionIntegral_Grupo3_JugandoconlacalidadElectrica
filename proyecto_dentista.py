# %% [markdown]
# # Ejecución Interactiva en VS Code
# Haz clic en "Run Cell" (Ejecutar celda) justo encima de este texto o del bloque de abajo para iniciar el simulador.

# %%
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import IntSlider, ToggleButton, HTML, Tab, VBox, HBox, Dropdown, interactive_output
from IPython.display import display

# Esto le dice a VS Code que los gráficos van incrustados en su panel interactivo


# ==========================================
# 1. FUNCIÓN DEL SIMULADOR
# ==========================================
def plot_simulador(p_autoclave, n_leds_box, compresor_on, disparo_rx):
    t = np.linspace(0, 0.04, 1000)
    V_peak = 230 * np.sqrt(2)
    
    drop = 0.85 if disparo_rx else 1.0
    v1 = V_peak * np.sin(2 * np.pi * 50 * t) * drop
    
    i_r = (p_autoclave / 230) * np.sin(2 * np.pi * 50 * t)
    i_l = 2.5 * np.sin(2 * np.pi * 50 * t - np.pi/4) if compresor_on else 0
    i_nl = (n_leds_box * 0.5) * (np.abs(v1) > (V_peak * 0.9)) * np.sign(v1)
    
    i_total = i_r + i_l + i_nl

    # IMPORTANTE: Forzar el cierre de figuras previas para evitar lag o duplicados
    plt.close('all') 
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))
    
    ax1.plot(t, v1, color='#00ACC1', linewidth=2)
    ax1.set_title(f"Tensión en Box Principal (V) - Estado: {'⚠️ HUECO DETECTADO' if disparo_rx else '✅ Estable'}")
    ax1.grid(True, linestyle=':', alpha=0.7)
    
    ax2.plot(t, i_total, color='#D84315', linewidth=2)
    ax2.fill_between(t, i_total, color='#FFAB91', alpha=0.3)
    ax2.set_title("Demanda de Corriente (A) - Distorsión visible")
    ax2.grid(True, linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

# ==========================================
# 2. INTERFAZ VISUAL: TEMÁTICA DENTISTA
# ==========================================
header = HTML("""
<div style='background-color: #E0F7FA; padding: 15px; border-radius: 10px; border-left: 5px solid #00ACC1;'>
    <h2 style='margin-top: 0;'>🦷 Clínica Dental "Sonrisa Segura"</h2>
    <b>Dashboard Pericial: Monitorización de Calidad de Suministro para TAC</b>
</div><br>
""")

w_autoclave = IntSlider(min=0, max=3000, step=100, value=1500, description='♨️ Esterilizador:')
w_leds = IntSlider(min=0, max=6, step=1, value=2, description='💺 Sillones LED:')
w_compresor = ToggleButton(value=False, description='⚙️ Compresor Aire', button_style='warning', icon='cogs')
w_rx = ToggleButton(value=False, description='☢️ Disparo Rayos X', button_style='danger', icon='bolt')

out_grafico = interactive_output(plot_simulador, {
    'p_autoclave': w_autoclave, 'n_leds_box': w_leds, 
    'compresor_on': w_compresor, 'disparo_rx': w_rx
})

panel_controles = HBox([
    VBox([HTML("<b>Cargas Permanentes</b>"), w_autoclave, w_leds]),
    VBox([HTML("<b>Eventos Dinámicos</b>"), w_compresor, w_rx])
])
tab_simulador = VBox([panel_controles, HTML("<hr>"), out_grafico])

# ==========================================
# 3. MENÚ DE CONSULTA
# ==========================================
w_dropdown = Dropdown(
    options=['Seleccione un problema para investigar...', 
             '☢️ Hueco de Tensión (Disparo RX)', 
             '💺 Distorsión Armónica (Fuentes Sillones)', 
             '⚙️ Desequilibrio (Motor Compresor)'],
    value='Seleccione un problema para investigar...',
    layout={'width': 'max-content'}
)

out_diagnostico = HTML("<div style='padding: 20px; border: 1px solid #ccc; border-radius: 5px;'><i>Selecciona un error en el menú superior para desplegar el dictamen técnico.</i></div>")

def actualizar_diccionario(change):
    estilo_caja = "<div style='padding: 20px; background-color: #fcfcfc; border: 1px solid #ccc; border-radius: 5px;'>"
    if change.new == '☢️ Hueco de Tensión (Disparo RX)':
        texto = "<h4>📉 Hueco de Tensión (Voltage Dip)</h4><p><b>Origen:</b> Disparo de RX demanda corriente extrema en milisegundos.</p><p><b>Riesgo:</b> Reinicio del TAC y pérdida de tomografías.</p>"
    elif change.new == '💺 Distorsión Armónica (Fuentes Sillones)':
        texto = "<h4>🌊 Distorsión Armónica Total (THD > 5%)</h4><p><b>Origen:</b> Fuentes conmutadas de LEDs y motores de sillones.</p><p><b>Riesgo:</b> Armónicos de 3º y 5º orden sobrecalientan el neutro.</p>"
    elif change.new == '⚙️ Desequilibrio (Motor Compresor)':
        texto = "<h4>⚖️ Desequilibrio Trifásico (> 2%)</h4><p><b>Origen:</b> Motor monofásico inductivo conectado a una sola fase.</p><p><b>Riesgo:</b> Asimetría daña rectificadores del TAC (Pérdida de garantía).</p>"
    else:
        texto = "<i>Selecciona un error en el menú superior para desplegar el dictamen técnico.</i>"
    out_diagnostico.value = estilo_caja + texto + "</div>"

w_dropdown.observe(actualizar_diccionario, names='value')
tab_diccionario = VBox([HTML("<h3>📖 Guía de Diagnóstico de Red</h3>"), w_dropdown, out_diagnostico])

# ==========================================
# 4. MOSTRAR INTERFAZ
# ==========================================
interfaz_final = Tab(children=[tab_simulador, tab_diccionario])
interfaz_final.set_title(0, '🖥️ Simulador TAC en Vivo')
interfaz_final.set_title(1, '📋 Diccionario Pericial')

display(header, interfaz_final)
