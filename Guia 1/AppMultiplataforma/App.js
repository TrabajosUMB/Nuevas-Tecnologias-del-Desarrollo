// useState: hook de React que permite guardar y actualizar valores en el componente
import { useState } from 'react';

// StatusBar: controla la barra de estado del dispositivo (hora, batería, etc.)
import { StatusBar } from 'expo-status-bar';

// Componentes nativos de React Native:
import {
  StyleSheet,       // permite crear objetos de estilos optimizados
  Text,             // muestra texto en pantalla
  View,             // contenedor genérico (equivalente a <div> en web)
  TextInput,        // campo de entrada de texto/números
  TouchableOpacity, // botón con efecto de opacidad al presionar
  Alert,            // muestra ventanas emergentes de alerta nativas
  ScrollView,       // contenedor que permite hacer scroll si el contenido es largo
  SafeAreaView,     // evita que el contenido quede tapado por el notch o la barra del sistema
} from 'react-native';

// ─── Paleta de colores de la app ──────────────────────────────────────────────
// Centralizar los colores aquí evita repetirlos en cada estilo
const COLORS = {
  cf: '#f97316',      // naranja fuego — identifica la conversión Celsius → Fahrenheit
  fc: '#06b6d4',      // azul hielo    — identifica la conversión Fahrenheit → Celsius
  ck: '#8b5cf6',      // púrpura       — identifica la conversión Celsius → Kelvin
  clear: '#334155',   // gris azulado  — color del botón limpiar
  bg: '#111827',      // fondo principal de la pantalla (casi negro)
  surface: '#1f2937', // superficie de tarjetas y bordes sutiles
  surfaceAlt: '#0f172a', // superficie más oscura para inputs y botones
  textPrimary: '#f1f5f9', // texto principal (blanco suave)
  textDim: '#64748b',     // texto secundario (gris medio)
  textMuted: '#374151',   // texto muy apagado (placeholders y footer)
};

// Devuelve el color de acento para la conversión activa.
// Si no hay conversión activa (''), devuelve el gris por defecto.
const accentFor = (unit) => COLORS[unit] || COLORS.textDim;

// ─── Componente principal de la app ───────────────────────────────────────────
export default function App() {

  // valor: lo que el usuario escribe en el campo de entrada
  const [valor, setValor] = useState('');

  // resultado: el número convertido que se muestra en la tarjeta de resultado
  const [resultado, setResultado] = useState('');

  // etiqueta: texto descriptivo de la conversión, ej. "100 °C  →  Fahrenheit"
  const [etiqueta, setEtiqueta] = useState('');

  // activeUnit: clave de la conversión activa ('cf', 'fc', 'ck' o '').
  // Controla qué color de acento se usa en toda la UI.
  const [activeUnit, setActiveUnit] = useState('');

  // ─── Función: Celsius → Fahrenheit ──────────────────────────────────────────
  const convertirCF = () => {
    // Valida que el campo no esté vacío y que sea un número
    if (!valor || isNaN(valor)) {
      Alert.alert('Error', 'Ingresa un número válido');
      return;
    }
    // Fórmula: °F = (°C × 9/5) + 32
    const r = (parseFloat(valor) * 9) / 5 + 32;
    setResultado(r.toFixed(2) + ' °F'); // guarda el resultado con 2 decimales
    setEtiqueta(valor + ' °C  →  Fahrenheit'); // texto descriptivo
    setActiveUnit('cf'); // activa el tema naranja
  };

  // ─── Función: Fahrenheit → Celsius ──────────────────────────────────────────
  const convertirFC = () => {
    if (!valor || isNaN(valor)) {
      Alert.alert('Error', 'Ingresa un número válido');
      return;
    }
    // Fórmula: °C = (°F - 32) × 5/9
    const r = ((parseFloat(valor) - 32) * 5) / 9;
    setResultado(r.toFixed(2) + ' °C');
    setEtiqueta(valor + ' °F  →  Celsius');
    setActiveUnit('fc'); // activa el tema azul
  };

  // ─── Función: Celsius → Kelvin ───────────────────────────────────────────────
  const convertirCK = () => {
    if (!valor || isNaN(valor)) {
      Alert.alert('Error', 'Ingresa un número válido');
      return;
    }
    // Fórmula: K = °C + 273.15
    const r = parseFloat(valor) + 273.15;
    setResultado(r.toFixed(2) + ' K');
    setEtiqueta(valor + ' °C  →  Kelvin');
    setActiveUnit('ck'); // activa el tema púrpura
  };

  // ─── Función: Limpiar ────────────────────────────────────────────────────────
  // Resetea todos los estados al valor vacío inicial
  const limpiar = () => {
    setValor('');
    setResultado('');
    setEtiqueta('');
    setActiveUnit(''); // vuelve al color gris por defecto
  };

  // Color de acento calculado a partir de la conversión activa.
  // Se recalcula automáticamente cada vez que activeUnit cambia.
  const accent = accentFor(activeUnit);

  // ─── Interfaz visual (JSX) ───────────────────────────────────────────────────
  return (
    // SafeAreaView: respeta el área segura del dispositivo (notch, barra inferior)
    <SafeAreaView style={styles.root}>

      {/* StatusBar en modo "light": iconos blancos sobre fondo oscuro */}
      <StatusBar style="light" />

      {/* ScrollView: permite desplazar la pantalla si el contenido no cabe */}
      <ScrollView
        contentContainerStyle={styles.scroll}
        keyboardShouldPersistTaps="handled"  // permite tocar botones sin cerrar el teclado
        showsVerticalScrollIndicator={false}  // oculta la barra de scroll
      >

        {/* ── ENCABEZADO ──────────────────────────────────────────────────── */}
        <View style={styles.header}>

          {/* Círculo decorativo en la esquina superior derecha (efecto de brillo) */}
          <View style={styles.headerGlow} />

          {/* Badge pequeño con la etiqueta "CONVERSOR" */}
          <View style={styles.headerBadge}>
            <Text style={styles.headerBadgeText}>CONVERSOR</Text>
          </View>

          {/* Título principal de la app */}
          <Text style={styles.titulo}>Temperatura</Text>
        </View>

        {/* ── SECCIÓN DE ENTRADA ──────────────────────────────────────────── */}
        <View style={styles.inputSection}>
          <Text style={styles.inputLabel}>Ingresa el valor</Text>

          {/* Campo numérico donde el usuario escribe la temperatura.
              El borde cambia de color según la conversión activa. */}
          <TextInput
            style={[
              styles.input,
              activeUnit
                ? { borderColor: accent, borderWidth: 2 } // borde coloreado si hay conversión activa
                : { borderColor: COLORS.surface, borderWidth: 2 }, // borde gris si no hay nada
            ]}
            value={valor}
            onChangeText={setValor}  // actualiza 'valor' en cada tecla presionada
            keyboardType="numeric"   // muestra teclado numérico en móvil
            placeholder="0.00"
            placeholderTextColor={COLORS.textMuted}
          />

          {/* Línea de acento debajo del input — solo visible cuando hay conversión activa */}
          {activeUnit !== '' && (
            <View style={[styles.inputAccentLine, { backgroundColor: accent }]} />
          )}
        </View>

        {/* ── GRILLA DE BOTONES DE CONVERSIÓN ─────────────────────────────── */}
        <Text style={styles.sectionLabel}>Selecciona conversión</Text>
        <View style={styles.btnGrid}>

          {/* Botón: Celsius → Fahrenheit */}
          <TouchableOpacity
            style={[styles.convBtn, { borderColor: COLORS.cf }]} // borde naranja
            onPress={convertirCF}
            activeOpacity={0.75} // reduce opacidad al 75% al presionar
          >
            {/* Barra de color en la parte superior del botón */}
            <View style={[styles.convBtnTopBar, { backgroundColor: COLORS.cf }]} />
            {/* Unidad destino (a qué se convierte) */}
            <Text style={[styles.convBtnUnit, { color: COLORS.cf }]}>°F</Text>
            {/* Unidad origen (desde qué se convierte) */}
            <Text style={styles.convBtnSub}>desde °C</Text>
          </TouchableOpacity>

          {/* Botón: Fahrenheit → Celsius */}
          <TouchableOpacity
            style={[styles.convBtn, { borderColor: COLORS.fc }]} // borde azul
            onPress={convertirFC}
            activeOpacity={0.75}
          >
            <View style={[styles.convBtnTopBar, { backgroundColor: COLORS.fc }]} />
            <Text style={[styles.convBtnUnit, { color: COLORS.fc }]}>°C</Text>
            <Text style={styles.convBtnSub}>desde °F</Text>
          </TouchableOpacity>

          {/* Botón: Celsius → Kelvin */}
          <TouchableOpacity
            style={[styles.convBtn, { borderColor: COLORS.ck }]} // borde púrpura
            onPress={convertirCK}
            activeOpacity={0.75}
          >
            <View style={[styles.convBtnTopBar, { backgroundColor: COLORS.ck }]} />
            <Text style={[styles.convBtnUnit, { color: COLORS.ck }]}>K</Text>
            <Text style={styles.convBtnSub}>desde °C</Text>
          </TouchableOpacity>

        </View>

        {/* ── BOTÓN LIMPIAR ────────────────────────────────────────────────── */}
        {/* Sin fondo ni borde — visualmente subordinado a los botones principales */}
        <TouchableOpacity style={styles.clearBtn} onPress={limpiar} activeOpacity={0.6}>
          <Text style={styles.clearBtnText}>Limpiar</Text>
        </TouchableOpacity>

        {/* ── TARJETA DE RESULTADO ─────────────────────────────────────────── */}
        {/* Solo se renderiza cuando hay un resultado calculado */}
        {resultado !== '' && (
          <View style={[styles.resultCard, { borderLeftColor: accent }]}>

            {/* Franja de brillo en la parte superior de la tarjeta */}
            <View style={[styles.resultGlowStrip, { backgroundColor: accent }]} />

            {/* Texto descriptivo: ej. "100 °C  →  Fahrenheit" */}
            <Text style={styles.resultLabel}>{etiqueta}</Text>

            {/* Fila con el número y la unidad alineados en la base */}
            <View style={styles.resultValueRow}>
              {/* Número grande: extrae solo el valor numérico del resultado */}
              <Text
                style={[styles.resultNumber, { color: accent }]}
                numberOfLines={1}
                adjustsFontSizeToFit
              >
                {resultado.split(' ')[0]}
              </Text>
              {/* Unidad: extrae el símbolo (ej. "°F", "°C", "K") */}
              <Text style={[styles.resultUnit, { color: accent }]}>
                {' '}{resultado.split(' ').slice(1).join(' ')}
              </Text>
            </View>

            {/* Pill (etiqueta redondeada) con el nombre completo de la conversión.
                El color de fondo usa el acento con opacidad reducida (sufijo hex '22' = ~13%). */}
            <View style={[styles.resultPill, { backgroundColor: accent + '22', borderColor: accent + '55' }]}>
              <Text style={[styles.resultPillText, { color: accent }]}>
                {activeUnit === 'cf' ? 'Celsius → Fahrenheit'
                  : activeUnit === 'fc' ? 'Fahrenheit → Celsius'
                  : 'Celsius → Kelvin'}
              </Text>
            </View>
          </View>
        )}


      </ScrollView>
    </SafeAreaView>
  );
}

// ─── Estilos ──────────────────────────────────────────────────────────────────
// StyleSheet.create() optimiza los estilos para el renderizado nativo
const styles = StyleSheet.create({

  // Contenedor raíz: ocupa toda la pantalla con el color de fondo oscuro
  root: {
    flex: 1,                        // ocupa todo el espacio disponible
    backgroundColor: COLORS.bg,    // fondo casi negro (#111827)
  },

  // Espaciado inferior del ScrollView para que el footer no quede pegado al borde
  scroll: {
    paddingBottom: 48,
  },

  // ── Encabezado ──────────────────────────────────────────────────────────────
  header: {
    paddingTop: 52,              // espacio desde la parte superior
    paddingBottom: 36,
    paddingHorizontal: 28,
    alignItems: 'flex-start',   // alinea contenido a la izquierda
    overflow: 'hidden',         // recorta el círculo decorativo que se sale del borde
  },

  // Círculo semitransparente en la esquina superior derecha — solo decorativo
  headerGlow: {
    position: 'absolute',   // se posiciona sobre los demás elementos
    top: -60,
    right: -60,
    width: 220,
    height: 220,
    borderRadius: 110,      // la mitad del ancho/alto = círculo perfecto
    backgroundColor: COLORS.cf, // color naranja del tema C→F
    opacity: 0.07,          // muy transparente para no distraer
  },

  // Pequeña caja con borde que contiene el texto "CONVERSOR"
  headerBadge: {
    backgroundColor: COLORS.surfaceAlt,
    borderRadius: 6,
    paddingVertical: 4,
    paddingHorizontal: 10,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: COLORS.surface,
  },

  // Texto dentro del badge: pequeño, en mayúsculas con espaciado entre letras
  headerBadgeText: {
    color: COLORS.textDim,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 2,       // espaciado extra entre letras para efecto de etiqueta
  },

  // Título principal grande y bold
  titulo: {
    fontSize: 40,
    fontWeight: '800',          // extra bold
    color: COLORS.textPrimary,
    letterSpacing: -0.5,        // letras ligeramente más juntas para look editorial
    lineHeight: 44,
    marginBottom: 6,
  },

  // ── Sección del campo de entrada ────────────────────────────────────────────
  inputSection: {
    marginHorizontal: 20,
    marginBottom: 28,
  },

  // Etiqueta sobre el input: pequeña, en mayúsculas, con mucho espaciado
  inputLabel: {
    color: COLORS.textDim,
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 1.5,
    textTransform: 'uppercase', // transforma el texto a MAYÚSCULAS
    marginBottom: 10,
  },

  // Campo de texto donde se escribe la temperatura
  input: {
    backgroundColor: COLORS.surfaceAlt,
    color: COLORS.textPrimary,
    borderRadius: 16,
    paddingVertical: 18,
    paddingHorizontal: 22,
    fontSize: 28,         // texto grande para que el número sea legible
    fontWeight: '300',    // thin — contrasta con los títulos bold
    letterSpacing: 1,
  },

  // Línea delgada de color debajo del input — refuerza la conversión activa
  inputAccentLine: {
    height: 3,
    borderRadius: 2,
    marginTop: 6,
    marginHorizontal: 6,
  },

  // ── Etiqueta de sección ─────────────────────────────────────────────────────
  // Mismo estilo que inputLabel — texto pequeño en mayúsculas sobre los botones
  sectionLabel: {
    color: COLORS.textDim,
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 1.5,
    textTransform: 'uppercase',
    marginHorizontal: 20,
    marginBottom: 12,
  },

  // ── Grilla de botones de conversión ─────────────────────────────────────────
  // Fila horizontal con 3 columnas iguales
  btnGrid: {
    flexDirection: 'row',   // coloca los hijos en fila horizontal
    marginHorizontal: 20,
    gap: 10,                // espacio entre botones
    marginBottom: 16,
  },

  // Cada botón de conversión: flex:1 hace que los tres compartan el espacio igualmente
  convBtn: {
    flex: 1,
    backgroundColor: COLORS.surfaceAlt,
    borderRadius: 20,
    paddingVertical: 28,
    alignItems: 'center',   // centra el texto horizontalmente
    borderWidth: 1,
    overflow: 'hidden',     // necesario para que la barra superior quede recortada
  },

  // Barra de color de 4px en la parte superior de cada botón
  convBtnTopBar: {
    position: 'absolute',   // se posiciona en la parte superior del botón
    top: 0,
    left: 0,
    right: 0,
    height: 4,
  },

  // Unidad destino (°F, °C, K) — texto grande y bold
  convBtnUnit: {
    fontSize: 26,
    fontWeight: '800',
    letterSpacing: -0.5,
    marginBottom: 6,
  },

  // Texto secundario del botón: "desde °C" o "desde °F"
  convBtnSub: {
    color: COLORS.textDim,
    fontSize: 11,
    fontWeight: '500',
  },

  // ── Botón limpiar ────────────────────────────────────────────────────────────
  // Sin fondo — parece un enlace de texto para no competir con los botones principales
  clearBtn: {
    alignSelf: 'center',    // se centra horizontalmente
    paddingVertical: 10,
    paddingHorizontal: 24,
    marginBottom: 28,
  },

  clearBtnText: {
    color: COLORS.textDim,
    fontSize: 13,
    fontWeight: '500',
    letterSpacing: 0.5,
  },

  // ── Tarjeta de resultado ─────────────────────────────────────────────────────
  resultCard: {
    backgroundColor: COLORS.surfaceAlt,
    marginHorizontal: 20,
    borderRadius: 20,
    padding: 20,
    marginBottom: 32,
    borderLeftWidth: 4,   // borde izquierdo grueso — su color se asigna dinámicamente
    overflow: 'hidden',
  },

  // Franja horizontal en la parte superior de la tarjeta (sutil efecto de brillo)
  resultGlowStrip: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 2,
    opacity: 0.6,
  },

  // Texto de la etiqueta descriptiva: ej. "100 °C  →  Fahrenheit"
  resultLabel: {
    color: COLORS.textDim,
    fontSize: 12,
    fontWeight: '500',
    letterSpacing: 0.5,
    marginBottom: 14,
  },

  // Fila que contiene el número y la unidad alineados por la base
  resultValueRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    flexWrap: 'wrap',        // permite que la unidad baje de línea si el número es muy ancho
    marginBottom: 18,
  },


  resultNumber: {
    fontSize: 52,
    fontWeight: '800',
    letterSpacing: -1,
    lineHeight: 56,
    flexShrink: 1,           // se encoge en vez de desbordar la tarjeta en pantallas angostas
  },

  // Símbolo de unidad al lado del número
  resultUnit: {
    fontSize: 28,
    fontWeight: '600',
    paddingBottom: 6,
    flexShrink: 1,
  },

  // Pill (pastilla) con el nombre completo de la conversión
  resultPill: {
    alignSelf: 'flex-start',  
    borderRadius: 20,
    borderWidth: 1,
    paddingVertical: 5,
    paddingHorizontal: 12,
  },

  resultPillText: {
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 0.3,
  },
});
