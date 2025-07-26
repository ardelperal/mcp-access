# 📝 Ejemplos de Prompts para MCP Access Database

Esta guía contiene ejemplos prácticos de prompts que puedes usar con el servidor MCP de Access Database en Trae AI o cualquier cliente MCP compatible.

## 🔗 Conexión y Configuración Inicial

### Conectar a una base de datos sin contraseña
```
Conéctate a la base de datos Access ubicada en C:\Datos\MiEmpresa.accdb
```

### Conectar a una base de datos con contraseña
```
Conéctate a la base de datos C:\Proyectos\Ventas.accdb usando la contraseña "admin123"
```

### Conectar y explorar estructura
```
Conéctate a la base de datos C:\Datos\Inventario.accdb y muéstrame todas las tablas disponibles con sus esquemas
```

## 📊 Exploración y Análisis de Datos

### Listar todas las tablas
```
Muéstrame todas las tablas que hay en la base de datos actual
```

### Obtener esquema de una tabla específica
```
Muéstrame la estructura completa de la tabla "Empleados" incluyendo tipos de datos y restricciones
```

### Analizar relaciones entre tablas
```
Analiza todas las relaciones entre tablas en esta base de datos y muéstrame un diagrama de las conexiones
```

### Contar registros en todas las tablas
```
Dame un resumen con el número de registros que tiene cada tabla en la base de datos
```

## 🔍 Consultas de Datos

### Consultas básicas
```
Muéstrame todos los registros de la tabla "Clientes"
```

```
Obtén los primeros 10 registros de la tabla "Productos" ordenados por precio descendente
```

### Consultas con filtros
```
Busca todos los empleados del departamento "Ventas" que tengan un salario mayor a 50000
```

```
Muéstrame todos los pedidos realizados en el último mes desde la tabla "Pedidos"
```

### Consultas con JOIN
```
Muéstrame una lista de todos los pedidos con el nombre del cliente correspondiente, uniendo las tablas "Pedidos" y "Clientes"
```

```
Crea un reporte que muestre el nombre del producto, categoría y proveedor para todos los productos en stock
```

### Consultas de agregación
```
Calcula el total de ventas por mes del año actual desde la tabla "Ventas"
```

```
Muéstrame el salario promedio por departamento de la tabla "Empleados"
```

## ✏️ Modificación de Datos

### Insertar nuevos registros
```
Agrega un nuevo empleado a la tabla "Empleados" con los siguientes datos:
- Nombre: Juan Pérez
- Departamento: IT
- Salario: 55000
- Fecha de ingreso: hoy
```

```
Inserta 3 nuevos productos en la tabla "Productos" con datos de ejemplo realistas
```

### Actualizar registros existentes
```
Actualiza el salario del empleado con ID 123 a 60000 en la tabla "Empleados"
```

```
Cambia el estado de todos los pedidos pendientes a "En proceso" en la tabla "Pedidos"
```

### Eliminar registros
```
Elimina todos los productos descontinuados de la tabla "Productos"
```

```
Borra el cliente con ID 456 y todos sus pedidos relacionados
```

## 🏗️ Gestión de Estructura

### Crear nuevas tablas
```
Crea una nueva tabla llamada "Proveedores" con los siguientes campos:
- ID (clave primaria, autoincremental)
- Nombre (texto, obligatorio)
- Email (texto)
- Teléfono (texto)
- Dirección (texto)
- Fecha_registro (fecha, valor por defecto hoy)
```

### Modificar estructura existente
```
Agrega una nueva columna "Descuento" de tipo decimal a la tabla "Productos"
```

### Eliminar tablas
```
Elimina la tabla "TablaTemporal" si existe
```

## 📈 Análisis y Reportes

### Generar documentación automática
```
Genera una documentación completa de toda la base de datos incluyendo esquemas, relaciones y estadísticas
```

### Análisis de calidad de datos
```
Analiza la calidad de los datos en la tabla "Clientes" y reporta campos vacíos, duplicados o inconsistencias
```

### Crear reportes personalizados
```
Crea un reporte de ventas mensual que incluya:
- Total de ventas por mes
- Producto más vendido
- Cliente con mayor compra
- Tendencia de crecimiento
```

## 🔧 Operaciones Avanzadas

### Consultas complejas con múltiples condiciones
```
Encuentra todos los empleados que:
- Trabajen en el departamento "Ventas" o "Marketing"
- Tengan un salario entre 40000 y 70000
- Hayan sido contratados en los últimos 2 años
- Ordénalos por salario descendente
```

### Operaciones de limpieza de datos
```
Identifica y limpia todos los registros duplicados en la tabla "Clientes" basándose en email
```

### Migración de datos
```
Copia todos los datos de la tabla "ProductosViejos" a "Productos" pero solo los registros activos
```

## 🎯 Casos de Uso Específicos por Industria

### Gestión de Inventario
```
Crea un sistema de alertas que me muestre todos los productos con stock menor a 10 unidades
```

### Recursos Humanos
```
Genera un reporte de cumpleaños de empleados para este mes y calcula la antigüedad de cada uno
```

### Ventas y CRM
```
Identifica los 10 clientes más valiosos basándose en el total de compras históricas
```

### Contabilidad
```
Calcula el balance total de ingresos vs gastos por trimestre del año actual
```

## 🚨 Manejo de Errores y Troubleshooting

### Verificar conectividad
```
Verifica si la conexión a la base de datos está activa y funcionando correctamente
```

### Diagnosticar problemas de datos
```
Revisa la tabla "Pedidos" y reporta cualquier inconsistencia en fechas o valores nulos en campos críticos
```

### Backup y recuperación
```
Exporta toda la estructura y datos de la tabla "Clientes" a un formato que pueda ser restaurado
```

## 💡 Tips para Prompts Efectivos

### 1. Sé específico con las rutas
```
✅ Bueno: "Conéctate a C:\Datos\Empresa\Ventas2024.accdb"
❌ Malo: "Conéctate a la base de datos de ventas"
```

### 2. Especifica el formato de salida deseado
```
✅ Bueno: "Muéstrame los datos en formato tabla con totales al final"
❌ Malo: "Muéstrame los datos"
```

### 3. Incluye contexto cuando sea necesario
```
✅ Bueno: "Busca empleados del departamento IT contratados este año para el reporte mensual"
❌ Malo: "Busca empleados"
```

### 4. Usa nombres exactos de tablas y campos
```
✅ Bueno: "Actualiza el campo 'Precio_Unitario' en la tabla 'Productos'"
❌ Malo: "Actualiza el precio en productos"
```

## 🔄 Prompts de Flujo de Trabajo Completo

### Análisis completo de una nueva base de datos
```
Acabo de recibir una nueva base de datos en C:\Nuevos\Sistema.accdb. 
Por favor:
1. Conéctate a ella
2. Analiza su estructura completa
3. Genera documentación
4. Identifica posibles problemas de calidad de datos
5. Sugiere optimizaciones
```

### Migración de datos entre tablas
```
Necesito migrar datos de una tabla antigua a una nueva estructura:
1. Crea una tabla "ClientesNuevo" con campos mejorados
2. Migra todos los datos válidos de "ClientesViejo"
3. Verifica la integridad de los datos migrados
4. Genera un reporte de la migración
```

### Automatización de reportes periódicos
```
Configura un reporte automático que cada mes me proporcione:
- Resumen de ventas por producto
- Análisis de tendencias
- Clientes más activos
- Productos con bajo stock
- Recomendaciones basadas en los datos
```

---

## 📞 Soporte y Recursos Adicionales

Si necesitas ayuda adicional:
- Revisa la documentación técnica en `/docs/`
- Ejecuta los scripts de prueba en `/tests/`
- Consulta los ejemplos en `/examples/`

¡Estos prompts te ayudarán a aprovechar al máximo el poder del MCP Access Database Server! 🚀