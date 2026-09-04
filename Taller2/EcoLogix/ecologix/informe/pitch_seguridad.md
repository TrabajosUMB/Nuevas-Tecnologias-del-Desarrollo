# Pitch de Seguridad — EcoLogix

**Base de Datos Centralizada vs. Blockchain para Trazabilidad de Residuos Electrónicos**

---

## 1. ¿Cómo se aseguró que los datos lleguen correctamente a Firebase?

EcoLogix aplica tres capas de protección antes y durante la escritura en Firestore:

**Validación en el cliente (UI):** El formulario de registro usa `Form` con `validator` en cada campo. Ningún dato llega al servicio si el formulario no pasa todas las reglas: tipo de material debe estar en el catálogo definido, peso debe ser un número `> 0` y `< 1000 kg`, y la ubicación debe tener mínimo 3 caracteres no vacíos.

**Validación en el servicio (`FirebaseService._validar`):** Aunque el cliente ya validó, el servicio repite las reglas de negocio de forma independiente. Esto impide que llamadas directas a la capa de servicio (por ejemplo, desde pruebas o integraciones futuras) omitan la validación.

**Manejo explícito de errores en el async:** La llamada `await docRef.set(...)` está envuelta en `try/on FirebaseException catch`. Los errores se relanzán con un mensaje contextualizado hacia la UI, que los muestra en un `SnackBar` rojo. Nunca se silencia un error (`catch` vacío). Adicionalmente, `context.mounted` se verifica después de cada `await` antes de actualizar la interfaz, evitando excepciones de widgets desvinculados.

---

## 2. ¿Por qué una base de datos centralizada es vulnerable?

Firebase Firestore —como cualquier base de datos centralizada— presenta riesgos estructurales que son importantes en un sistema de trazabilidad:

| Vulnerabilidad | Descripción |
|---|---|
| **Single point of failure** | Si los servidores de Firebase presentan una interrupción, toda la app deja de funcionar. No hay réplica independiente fuera del control del proveedor. |
| **Acceso con privilegios root** | La cuenta administradora del proyecto Firebase tiene acceso irrestricto a todos los datos. Una credencial comprometida puede modificar o borrar el historial completo de recolecciones sin dejar rastro. |
| **Sin auditoría inmutable** | Aunque Firestore registra fechas de escritura, un administrador con permisos puede alterar o eliminar documentos. No existe un mecanismo nativo que garantice que el registro nunca fue modificado después de su creación. |
| **Reglas de seguridad mal configuradas** | Si las `Security Rules` de Firestore se configuran de forma permisiva (por ejemplo, `allow read, write: if true`), cualquier usuario con la API key puede leer y escribir todos los datos. |
| **Dependencia de terceros** | Se depende de la disponibilidad, las políticas de precios y las decisiones corporativas de Google. Un cambio en los términos del servicio afecta directamente la operación. |

---

## 3. ¿Qué ofrece Blockchain como alternativa?

Blockchain proporciona propiedades criptográficas que resuelven precisamente las vulnerabilidades anteriores:

**Registro inmutable:** Una vez que una transacción se confirma en la cadena, no puede modificarse ni eliminarse sin invalidar todos los bloques posteriores. En trazabilidad de residuos, esto significa que cada recolección queda sellada para siempre.

**Descentralización:** La cadena se replica en múltiples nodos independientes. No existe un servidor central que pueda caer o ser comprometido. Un atacante tendría que controlar más del 50 % de la red simultáneamente (ataque del 51 %), lo cual es económicamente inviable en cadenas públicas.

**Trazabilidad criptográfica:** Cada registro incluye el hash del bloque anterior, creando una cadena de custodia verificable matemáticamente. Cualquier auditor externo puede verificar la integridad del historial sin necesitar credenciales de administrador.

**Transparencia con privacidad selectiva:** Redes como Hyperledger Fabric permiten canales privados donde solo las partes autorizadas (empresa recicladora, regulador ambiental) pueden leer los datos, mientras que la inmutabilidad es pública y verificable.

**Smart contracts:** Las reglas de validación (peso mínimo, tipos de material aceptados) pueden codificarse como contratos autoejecutables. Ninguna entidad central puede omitir las reglas después del despliegue.

---

## 4. Conclusión: ¿cuándo usar base de datos tradicional vs. Blockchain?

| Criterio | Base de Datos Centralizada | Blockchain |
|---|---|---|
| **Costo operativo** | Bajo (Firebase tiene capa gratuita) | Alto (gas fees, infraestructura de nodos) |
| **Velocidad de desarrollo** | Rápida | Lenta (curva de aprendizaje alta) |
| **Confianza requerida** | Depositada en el proveedor | Distribuida matemáticamente |
| **Escala** | Millones de operaciones/segundo | Cientos a miles por segundo (según red) |
| **Auditoría externa** | Requiere acceso a la BD del proveedor | Cualquier nodo puede verificar |
| **Adecuado para** | MVPs, apps de consumo, datos no críticos | Cadenas de custodia, activos de valor, compliance regulatorio |

**Recomendación para EcoLogix:** En la etapa de startup con recursos limitados, Firebase es la elección correcta para validar el producto. A medida que la empresa deba cumplir regulaciones ambientales que exijan auditorías externas e independientes del historial de recolecciones, migrar los registros confirmados a una red Blockchain (por ejemplo, un registro público en Polygon o una red privada en Hyperledger) añadiría la capa de inmutabilidad regulatoria sin reemplazar Firebase como capa operacional de la app.

---

*EcoLogix — Taller de Nuevas Tecnologías del Desarrollo · 2026-02*
