import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import whisper
import av

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(page_title="Lista de Inspección Químicos", layout="wide")

# ==============================
# CARGA DEL MODELO DE WHISPER
# ==============================
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

# ==============================
# ENCABEZADO DE DATOS BÁSICOS
# ==============================
st.title("📋 Formato de Inspección de Sustancias Químicas")

st.subheader("Datos de la Inspección")
empresa = st.text_input("🏢 Nombre de la empresa")
responsable = st.text_input("👤 Responsable que atiende la inspección")
fecha = st.date_input("📅 Fecha de la inspección", datetime.today())

st.markdown("---")

# ==============================
# LISTA DE ÍTEMS DE INSPECCIÓN
# ==============================
st.subheader("✅ Lista de Inspección")

items = [
    "1. Se tiene un inventario de las sustancias químicas presentes en el proceso.",
    "2. Se clasifican e identifican los peligros de las sustancias de acuerdo al SGA.",
    "3. El trabajador del área tiene acceso permanente a las fichas de datos de seguridad.",
    "4. Se cuenta con las fichas de datos de seguridad de las sustancias químicas que se utilizan en el área.",
    "5. Todo el trabajador involucrado en el área entiende y conoce la información de las fichas de datos de seguridad.",
    "6. Se etiquetan los productos intermedios, remanentes o transvasados de acuerdo con el SGA.",
    "7. Los trabajadores han sido capacitados en la utilización de sustancias químicas y conocen los riesgos.",
    "8. Existen y se conocen procedimientos escritos para la utilización y preparación de sustancias químicas.",
    "9. Los trabajadores cuentan con equipos de protección personal de acuerdo al peligro.",
    "10. Se evidencia la utilización de elementos de protección personal.",
    "11. Los trabajadores que manipulan químicos han sido capacitados en el uso y manejo de los mismos.",
    "12. Los trabajadores que manipulan químicos han sido capacitados en el uso de equipos de protección personal.",
    "13. Los trabajadores que manipulan químicos han sido capacitados en primeros auxilios.",
    "14. Se cuenta con procedimientos escritos de seguridad para la manipulación de sustancias químicas.",
    "15. Se cuenta con equipos para atender emergencias por derrames o fugas.",
    "16. Se cuenta con elementos absorbentes para la atención de derrames.",
    "17. Se tiene establecido un plan de contingencia para emergencias con químicos.",
    "18. Se cuenta con rutas de evacuación señalizadas.",
    "19. Se cuenta con extintores en el área de almacenamiento de químicos.",
    "20. Los extintores se encuentran señalizados y visibles.",
    "21. Se realiza mantenimiento preventivo a los extintores.",
    "22. Se cuenta con duchas de emergencia en áreas críticas.",
    "23. Se cuenta con lavaojos en áreas críticas.",
    "24. Los trabajadores conocen el manejo de duchas de emergencia y lavaojos.",
    "25. Se cuenta con ventilación natural o mecánica adecuada.",
    "26. Se cuenta con sistemas de extracción localizada en procesos con emisión de vapores o gases.",
    "27. Se controla la exposición de los trabajadores a químicos mediante mediciones ambientales.",
    "28. Se realizan evaluaciones médicas ocupacionales a los trabajadores expuestos.",
    "29. Se lleva registro de trabajadores expuestos a químicos.",
    "30. Se identifican incompatibilidades químicas en el almacenamiento.",
    "31. Se almacenan sustancias químicas incompatibles en lugares separados.",
    "32. Los recipientes de sustancias químicas se encuentran en buen estado.",
    "33. Los recipientes de sustancias químicas se encuentran debidamente cerrados.",
    "34. Los recipientes cuentan con etiquetas legibles y actualizadas.",
    "35. Se cuenta con señalización de seguridad en áreas de almacenamiento.",
    "36. Se dispone de ventilación adecuada en áreas de almacenamiento.",
    "37. El área de almacenamiento cuenta con piso impermeable.",
    "38. El área de almacenamiento cuenta con diques de contención.",
    "39. El área de almacenamiento cuenta con acceso restringido.",
    "40. Se dispone de iluminación adecuada en el área de almacenamiento.",
    "41. El área de almacenamiento se encuentra ordenada y limpia.",
    "42. Se dispone de un plan de mantenimiento de equipos y áreas donde se manipulan químicos.",
    "43. Se cuenta con procedimientos de disposición de residuos peligrosos.",
    "44. Se utilizan recipientes adecuados para residuos peligrosos.",
    "45. Los recipientes de residuos se encuentran identificados.",
    "46. Se cuenta con proveedor autorizado para la disposición final de residuos peligrosos.",
    "47. Se lleva registro de la disposición de residuos peligrosos.",
    "48. Los trabajadores han sido capacitados en el manejo de residuos peligrosos.",
    "49. Se prohíbe el consumo de alimentos en áreas donde se manipulan químicos.",
    "50. Se prohíbe fumar en áreas donde se manipulan químicos.",
    "51. Se prohíbe almacenar sustancias químicas en áreas no autorizadas.",
    "52. Los trabajadores conocen los procedimientos de emergencia por fugas o derrames.",
    "53. Se realizan simulacros de emergencia relacionados con sustancias químicas.",
    "54. Se dispone de botiquín de primeros auxilios en el área.",
    "55. Los botiquines cuentan con elementos actualizados y completos.",
    "56. Se dispone de números de emergencia visibles en el área.",
    "57. Se evalúan periódicamente las condiciones de seguridad en el manejo de químicos.",
    "58. Se implementan acciones correctivas frente a hallazgos en inspecciones.",
    "59. Se promueve la cultura de autocuidado en los trabajadores.",
    "60. Maquinaria, equipos, tanques y herramientas que se requieren para la manipulación de sustancias químicas se encuentran en buen estado."
]

opciones = [
    "NA - No aplica",
    "1 - No cumple",
    "3 - Cumple parcialmente",
    "5 - Cumple totalmente"
]

resultados = []

# ==============================
# LOOP DE ÍTEMS CON AUDIO
# ==============================
for item in items:
    st.markdown(f"**{item}**")

    col1, col2 = st.columns([1, 3])

    with col1:
        calificacion = st.selectbox(
            "Calificación",
            opciones,
            key=f"sel_{item}"
        )

    with col2:
        observacion = st.text_area(
            "Observaciones / Transcripción del hallazgo",
            key=f"obs_{item}"
        )

        # Grabación de voz y transcripción
        webrtc_ctx = webrtc_streamer(
            key=f"speech_{item}",
            mode=WebRtcMode.SENDONLY,
            audio_receiver_size=1024,
            media_stream_constraints={"audio": True, "video": False}
        )

        if webrtc_ctx.audio_receiver:
            audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
            if audio_frames:
                audio = audio_frames[0].to_ndarray().flatten()
                # Aquí puedes guardar temporalmente el audio y pasarlo a Whisper
                # Por simplicidad, simulamos con texto fijo
                st.info("🎤 Transcribiendo audio...")
                observacion = "Texto transcrito automáticamente"

    foto = st.file_uploader(
        "📷 Subir foto de evidencia",
        type=["jpg", "png", "jpeg"],
        key=f"foto_{item}"
    )

    resultados.append({
        "Ítem": item,
        "Calificación": calificacion,
        "Observación": observacion,
        "Foto": foto.name if foto else ""
    })

    st.markdown("---")

# ==============================
# BOTÓN DE GUARDADO
# ==============================
if st.button("💾 Guardar Resultados"):
    df = pd.DataFrame(resultados)
    df.insert(0, "Empresa", empresa)
    df.insert(1, "Responsable", responsable)
    df.insert(2, "Fecha", fecha)

    nombre_archivo = f"Inspeccion_{empresa}_{fecha}.xlsx"
    df.to_excel(nombre_archivo, index=False)

    st.success(f"✅ Resultados guardados en {nombre_archivo}")
    st.dataframe(df)
