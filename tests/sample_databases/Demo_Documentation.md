# Documentación de Base de Datos

**Archivo:** `sample_databases\Lanzadera_Datos.accdb`  
**Fecha de generación:** 2025-07-26 14:17:50

## Resumen

- **Total de tablas:** 35
- **Total de relaciones:** 0

## Tablas

### Errores de pegado

**Registros:** 1

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| F1 | VARCHAR | 255 | Sí | - |
| F2 | DOUBLE | 53 | Sí | - |
| F3 | VARCHAR | 255 | Sí | - |
| F4 | VARCHAR | 255 | Sí | - |
| F5 | VARCHAR | 255 | Sí | - |
| F6 | VARCHAR | 255 | Sí | - |
| F7 | VARCHAR | 255 | Sí | - |
| F8 | VARCHAR | 255 | Sí | - |
| F9 | VARCHAR | 255 | Sí | - |

---

### Tb0HerramientaDocAyuda

**Registros:** 4

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| NombreFormulario | VARCHAR | 255 | Sí | - |
| NombreArchivoAyuda | VARCHAR | 255 | Sí | - |

#### Índices
- **PrimaryKey**: NombreFormulario (ÚNICO)
- **PrimaryKey**: NombreArchivoAyuda (ÚNICO)

---

### TbAplicaciones

**Registros:** 19

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDAplicacion | INTEGER | 10 | Sí | - |
| NombreAplicacion | VARCHAR | 255 | Sí | - |
| NombreCorto | VARCHAR | 255 | Sí | - |
| NombreEjecutable | VARCHAR | 255 | Sí | - |
| NombreArchivoDatos | VARCHAR | 255 | Sí | - |
| Pass | VARCHAR | 255 | Sí | - |
| NombreCarpeta | VARCHAR | 255 | Sí | - |
| NombreFuncionPublicacion | VARCHAR | 255 | Sí | - |
| NombreCarpetaTemporal | VARCHAR | 255 | Sí | - |
| TituloAplicacion | VARCHAR | 255 | Sí | - |
| NombreIconoParaArbol | VARCHAR | 255 | Sí | - |
| NombreIcono | VARCHAR | 255 | Sí | - |
| NombreIconoLanzadera | VARCHAR | 255 | Sí | - |
| EjecucionEnOficina | VARCHAR | 2 | Sí | - |
| NombreCarpetaDocumentacion | VARCHAR | 255 | Sí | - |
| NombreDirectorioIconos | VARCHAR | 255 | Sí | - |
| NombreDirectorioAyuda | VARCHAR | 255 | Sí | - |
| NombreDirectorioRecursos | VARCHAR | 255 | Sí | - |
| URLDIrectorioIconoAplicacion | VARCHAR | 255 | Sí | - |
| EnPruebas | VARCHAR | 2 | Sí | - |
| ConIconoEnLanzadera | VARCHAR | 2 | Sí | - |
| Comando | LONGCHAR | 1073741823 | Sí | - |

#### Índices
- **NombreAplicacion**: NombreAplicacion (ÚNICO)
- **NombreAplicacion1**: NombreCorto (ÚNICO)
- **PrimaryKey**: IDAplicacion (ÚNICO)
- **IDAplicacion**: IDAplicacion

---

### TbAplicacionesAperturas

**Registros:** 1697

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDApertura | INTEGER | 10 | Sí | - |
| IDAplicacion | INTEGER | 10 | Sí | - |
| NombreUsuario | VARCHAR | 255 | Sí | - |
| FechaApertura | DATETIME | 19 | Sí | - |
| HoraApertura | DATETIME | 19 | Sí | - |
| FechaCierre | DATETIME | 19 | Sí | - |
| HoraCierre | DATETIME | 19 | Sí | - |
| NombreAplicacion | VARCHAR | 255 | Sí | - |
| FechaEnvioCorreoAdministrador | DATETIME | 19 | Sí | - |
| EnOficina | VARCHAR | 2 | Sí | - |
| UsuarioConectadoMaquina | VARCHAR | 255 | Sí | - |
| VersionAplicacion | VARCHAR | 255 | Sí | - |
| NombreMaquina | VARCHAR | 255 | Sí | - |
| UsuarioMaquina | VARCHAR | 255 | Sí | - |
| Observaciones | LONGCHAR | 1073741823 | Sí | - |

#### Índices
- **PrimaryKey**: IDApertura (ÚNICO)
- **IDApertura**: IDApertura
- **IDAplicacion**: IDAplicacion

---

### TbAplicacionesEdiciones

**Registros:** 1262

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDAplicacion | INTEGER | 10 | Sí | - |
| IDVersion | INTEGER | 10 | Sí | - |
| Version | VARCHAR | 255 | Sí | - |
| FechaPublicacion | DATETIME | 19 | Sí | - |
| ParaInforme | VARCHAR | 255 | Sí | - |

#### Índices
- **PrimaryKey**: IDAplicacion (ÚNICO)
- **PrimaryKey**: IDVersion (ÚNICO)

---

### TbAplicacionesEdicionesCambios

**Registros:** 1364

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDCambio | INTEGER | 10 | Sí | - |
| IDVersion | INTEGER | 10 | Sí | - |
| Cambio | VARCHAR | 255 | Sí | - |
| FechaCambio | DATETIME | 19 | Sí | - |
| DescripcionCambio | LONGCHAR | 1073741823 | Sí | - |

#### Índices
- **PrimaryKey**: IDCambio (ÚNICO)
- **IDCambio**: IDCambio
- **IDVersion**: IDVersion

---

### TbAplicacionesEstados

**Registros:** 6

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| PerfilAplicacion | VARCHAR | 255 | Sí | - |
| PerfilAplicacionEncriptado | VARCHAR | 255 | Sí | - |

#### Índices
- **PrimaryKey**: PerfilAplicacion (ÚNICO)

---

### TbAplicacionesParametros

**Registros:** 60

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDAplicacion | INTEGER | 10 | Sí | - |
| IDParametro | INTEGER | 10 | Sí | - |
| Valor | LONGCHAR | 1073741823 | Sí | - |

#### Índices
- **PrimaryKey**: IDAplicacion (ÚNICO)
- **PrimaryKey**: IDParametro (ÚNICO)
- **{456C66C0-8BFE-4156-BEF1-225B1B654B5A}**: IDParametro
- **{C312B6B3-587C-452F-8036-DC0E5866E679}**: IDAplicacion
- **IDAplicacion**: IDAplicacion
- **Parametro**: IDParametro

---

### TbAplicacionesPerfiles

**Registros:** 34

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDAplicacion | INTEGER | 10 | Sí | - |
| Perfil | VARCHAR | 255 | Sí | - |

#### Índices
- **PrimaryKey**: IDAplicacion (ÚNICO)
- **PrimaryKey**: Perfil (ÚNICO)
- **IDAplicacion**: IDAplicacion

---

### TbAplicacionesVideos

**Registros:** 0

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDAplicacionVideo | INTEGER | 10 | Sí | - |
| IDVideo | INTEGER | 10 | Sí | - |
| IDAplicacion | INTEGER | 10 | Sí | - |
| Descripcion | LONGCHAR | 1073741823 | Sí | - |
| NombreArchivo | VARCHAR | 255 | Sí | - |
| FechaCreacion | DATETIME | 19 | Sí | - |
| UsuarioCrea | VARCHAR | 255 | Sí | - |
| FechaModificacion | DATETIME | 19 | Sí | - |
| UsuarioModifica | VARCHAR | 255 | Sí | - |

#### Índices
- **IDAplicacionVideo**: IDAplicacionVideo (ÚNICO)
- **PrimaryKey**: IDAplicacionVideo (ÚNICO)
- **Secundario**: IDVideo (ÚNICO)
- **Secundario**: IDAplicacion (ÚNICO)
- **IDAplicacion**: IDAplicacion
- **IDVideo**: IDVideo

---

### TbCategorias

**Registros:** 2

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDCategoria | INTEGER | 10 | Sí | - |
| NombreCategoria | VARCHAR | 255 | Sí | - |

#### Índices
- **PrimaryKey**: IDCategoria (ÚNICO)
- **IDCategoria**: IDCategoria

---

### TbConexiones

**Registros:** 24

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| Usuario | VARCHAR | 255 | Sí | - |
| UltimaConexion | DATETIME | 19 | Sí | - |
| UltimaDesconexion | DATETIME | 19 | Sí | - |
| InstaladoFW3 | VARCHAR | 2 | Sí | - |
| InstaladoFW4 | VARCHAR | 2 | Sí | - |
| Exitoso | VARCHAR | 2 | Sí | - |

#### Índices
- **PrimaryKey**: Usuario (ÚNICO)

---

### TbConexionesRegistro

**Registros:** 10360

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDConexion | INTEGER | 10 | Sí | - |
| Usuario | VARCHAR | 255 | Sí | - |
| FechaConexion | DATETIME | 19 | Sí | - |
| FechaCierre | DATETIME | 19 | Sí | - |
| ConContraseña | BIT | 1 | No | - |
| UsuarioSSID | VARCHAR | 255 | Sí | - |
| EnOficina | BIT | 1 | No | - |
| Vertical | INTEGER | 10 | Sí | - |
| Horizontal | INTEGER | 10 | Sí | - |

**Claves Primarias:** UsuarioSSID

#### Índices
- **PrimaryKey**: IDConexion (ÚNICO)
- **IDConexion**: IDConexion
- **UsuarioSSID**: UsuarioSSID

---

### TbConexionUltimaAppAbierta

**Registros:** 1469

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDConexion | INTEGER | 10 | Sí | - |
| IDUltimaAplicacionAbierta | INTEGER | 10 | Sí | - |

#### Índices
- **PrimaryKey**: IDConexion (ÚNICO)
- **IDConexion**: IDConexion

---

### TbCuestionarioPreguntas

**Registros:** 0

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDPregunta | INTEGER | 10 | Sí | - |
| IDCuestionario | INTEGER | 10 | Sí | - |
| Texto | LONGCHAR | 1073741823 | Sí | - |

#### Índices
- **PrimaryKey**: IDPregunta (ÚNICO)
- **IDCuestionario**: IDCuestionario
- **IDPregunta**: IDPregunta

---

### TbCuestionarios

**Registros:** 0

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDCuestionario | INTEGER | 10 | Sí | - |
| FechaRealizado | DATETIME | 19 | Sí | - |
| IDUsuarioRealiza | INTEGER | 10 | Sí | - |
| IDAplicacion | INTEGER | 10 | Sí | - |
| IDRespuestaCorrecta | INTEGER | 10 | Sí | - |
| Observaciones | LONGCHAR | 1073741823 | Sí | - |

#### Índices
- **PrimaryKey**: IDCuestionario (ÚNICO)
- **IDAplicacion**: IDAplicacion
- **IDCuestionario**: IDCuestionario
- **IDRespuestaCorrecta**: IDRespuestaCorrecta

---

### TbCuestionaroRespuestas

**Registros:** 0

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDRespuesta | INTEGER | 10 | Sí | - |
| IDPregunta | INTEGER | 10 | Sí | - |
| Letra | VARCHAR | 255 | Sí | - |
| Texto | LONGCHAR | 1073741823 | Sí | - |

#### Índices
- **PrimaryKey**: IDRespuesta (ÚNICO)
- **Secundario**: IDPregunta (ÚNICO)
- **Secundario**: Letra (ÚNICO)
- **IDPregunta**: IDPregunta
- **IDRespuesta**: IDRespuesta

---

### TbDetalleVersiones

**Registros:** 28

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDAplicacion | INTEGER | 10 | Sí | - |
| IDVersion | INTEGER | 10 | Sí | - |
| IDDetalle | INTEGER | 10 | Sí | - |
| Detalle | LONGCHAR | 1073741823 | Sí | - |

#### Índices
- **PrimaryKey**: IDAplicacion (ÚNICO)
- **PrimaryKey**: IDVersion (ÚNICO)
- **PrimaryKey**: IDDetalle (ÚNICO)
- **IDAplicacion**: IDAplicacion
- **IDDetalle**: IDDetalle
- **IDVersion**: IDVersion

---

### TbParametros

**Registros:** 53

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDParametro | INTEGER | 10 | Sí | - |
| Parametro | VARCHAR | 255 | Sí | - |

#### Índices
- **IDParametro**: IDParametro (ÚNICO)
- **Parametro**: Parametro (ÚNICO)
- **PrimaryKey**: IDParametro (ÚNICO)

---

### TbPermisos

**Registros:** 205

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDAplicacion | INTEGER | 10 | Sí | - |
| Usuario | VARCHAR | 255 | Sí | - |
| F3 | VARCHAR | 255 | Sí | - |
| F4 | VARCHAR | 255 | Sí | - |
| F5 | VARCHAR | 255 | Sí | - |
| F6 | VARCHAR | 255 | Sí | - |
| F7 | VARCHAR | 255 | Sí | - |
| F8 | VARCHAR | 255 | Sí | - |
| F9 | VARCHAR | 255 | Sí | - |

#### Índices
- **PrimaryKey**: IDAplicacion (ÚNICO)
- **PrimaryKey**: Usuario (ÚNICO)

---

### TbTablasAVincular

**Registros:** 411

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDBBDD | INTEGER | 10 | Sí | - |
| IDAplicacion | INTEGER | 10 | Sí | - |
| NombreTabla | VARCHAR | 255 | Sí | - |
| NombreTablaEnLocal | VARCHAR | 255 | Sí | - |

#### Índices
- **IDBBDD**: IDBBDD
- **IDBBDD1**: IDAplicacion

---

### TbUbicaciones

**Registros:** 8

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| NombreUbicacion | VARCHAR | 255 | Sí | - |
| Sirdee | VARCHAR | 2 | Sí | - |
| Ubicacion | VARCHAR | 255 | Sí | - |

#### Índices
- **PrimaryKey**: NombreUbicacion (ÚNICO)
- **PrimaryKey**: Sirdee (ÚNICO)

---

### TbUsuarioAplicacionesSolicitud

**Registros:** 0

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| CorreoUsuario | TEXT | 255 | Sí | - |
| Password | TEXT | 255 | Sí | - |
| Nombre | TEXT | 255 | Sí | - |
| Matricula | TEXT | 255 | Sí | - |
| Telefono | TEXT | 255 | Sí | - |
| Movil | TEXT | 255 | Sí | - |
| FechaSolicitud | TEXT | 255 | Sí | - |

#### Índices
- **PrimaryKey**: CorreoUsuario (ÚNICO)

---

### TbUsuarioConfiguracion

**Registros:** 14

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| UsuarioDeRed | VARCHAR | 255 | Sí | - |
| MantenerLanzaderaAbierta | VARCHAR | 2 | Sí | - |

#### Índices
- **PrimaryKey**: UsuarioDeRed (ÚNICO)

---

### tbUsuarios

**Registros:** 156

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| Id | INTEGER | 10 | Sí | - |
| Nombre | VARCHAR | 50 | Sí | - |
| UsuarioRed | VARCHAR | 50 | Sí | - |
| DirCorreo | VARCHAR | 255 | Sí | - |
| Matricula_DNI | VARCHAR | 50 | Sí | - |
| Cargo | VARCHAR | 50 | Sí | - |
| telfijo | INTEGER | 10 | Sí | - |
| telmovil | INTEGER | 10 | Sí | - |
| JefeDelUsuario | VARCHAR | 50 | Sí | - |
| FechaAlta | DATETIME | 19 | Sí | - |
| FechaBaja | DATETIME | 19 | Sí | - |
| EmplazamientoExterno | VARCHAR | 2 | Sí | - |
| SeLogean | BIT | 1 | No | - |
| ParaTareasProgramadas | BIT | 1 | No | - |
| Autorizador | BIT | 1 | No | - |
| DiaEnvioTareas | BYTE | 3 | Sí | - |
| UsuarioDeGestionRiesgos | VARCHAR | 2 | Sí | - |
| UsuariosI3D | VARCHAR | 2 | Sí | - |

**Claves Primarias:** Id

#### Índices
- **Matricula_DNI**: Matricula_DNI (ÚNICO)
- **PrimaryKey**: Id (ÚNICO)
- **Id**: Id

---

### TbUsuariosAplicaciones

**Registros:** 174

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| CorreoUsuario | TEXT | 255 | Sí | - |
| Password | TEXT | 255 | Sí | - |
| UsuarioRed | TEXT | 255 | Sí | - |
| Nombre | TEXT | 255 | Sí | - |
| Matricula | TEXT | 255 | Sí | - |
| FechaAlta | TEXT | 255 | Sí | - |
| Activado | TEXT | 255 | Sí | - |
| FechaProximoCambioContrasenia | TEXT | 255 | Sí | - |
| FechaUltimaConexion | TEXT | 255 | Sí | - |
| TieneQueCambiarLaContrasenia | TEXT | 255 | Sí | - |
| Telefono | TEXT | 255 | Sí | - |
| Movil | TEXT | 255 | Sí | - |
| Observaciones | TEXT | 255 | Sí | - |
| UsuarioImborrable | TEXT | 255 | Sí | - |
| EsAdministrador | TEXT | 255 | Sí | - |
| PermisosAsignados | TEXT | 255 | Sí | - |
| FechaBaja | TEXT | 255 | Sí | - |
| PasswordNuncaCaduca | TEXT | 255 | Sí | - |
| MantenerLanzaderaAbierta | TEXT | 255 | Sí | - |
| PassIncialPlana | TEXT | 255 | Sí | - |
| UsuarioSSID | TEXT | 255 | Sí | - |
| Id | TEXT | 255 | Sí | - |
| JefeDelUsuario | TEXT | 255 | Sí | - |
| PermisoPruebas | TEXT | 255 | Sí | - |
| ParaTareasProgramadas | TEXT | 255 | Sí | - |
| FechaBloqueo | TEXT | 255 | Sí | - |

**Claves Primarias:** UsuarioSSID

#### Índices
- **Id**: Id (ÚNICO)
- **PrimaryKey**: CorreoUsuario (ÚNICO)
- **UsuarioSSID**: UsuarioSSID

---

### TbUsuariosAplicacionesPermisos

**Registros:** 526

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| CorreoUsuario | VARCHAR | 255 | Sí | - |
| IDAplicacion | INTEGER | 10 | Sí | - |
| EsUsuarioAdministrador | VARCHAR | 2 | Sí | - |
| EsUsuarioCalidad | VARCHAR | 2 | Sí | - |
| EsUsuarioEconomia | VARCHAR | 2 | Sí | - |
| EsUsuarioSecretaria | VARCHAR | 2 | Sí | - |
| EsUsuarioTecnico | VARCHAR | 2 | Sí | - |
| EsUsuarioSinAcceso | VARCHAR | 2 | Sí | - |
| EsUsuarioCalidadAvisos | VARCHAR | 2 | Sí | - |

#### Índices
- **PrimaryKey**: CorreoUsuario (ÚNICO)
- **PrimaryKey**: IDAplicacion (ÚNICO)
- **{CC570485-919B-4483-817F-22CC7ED23D6E}**: IDAplicacion
- **{D37B534E-7186-4341-95DE-C52BB833445F}**: CorreoUsuario
- **CorreoUsuario**: CorreoUsuario
- **IDAplicacion**: IDAplicacion

---

### TbUsuariosAplicacionesTareas

**Registros:** 7

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| CorreoUsuario | TEXT | 255 | Sí | - |
| EsAdministrador | TEXT | 255 | Sí | - |
| EsTecnico | TEXT | 255 | Sí | - |
| EsCalidad | TEXT | 255 | Sí | - |
| EsEconomia | TEXT | 255 | Sí | - |

#### Índices
- **PrimaryKey**: CorreoUsuario (ÚNICO)

---

### TbUsuariosCorreosEnvio

**Registros:** 1042

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDCorreo | INTEGER | 10 | Sí | - |
| Destinatarios | LONGCHAR | 1073741823 | Sí | - |
| DestinatariosConCopia | LONGCHAR | 1073741823 | Sí | - |
| DestinatariosConCopiaOculta | LONGCHAR | 1073741823 | Sí | - |
| Asunto | VARCHAR | 255 | Sí | - |
| Cuerpo | LONGCHAR | 1073741823 | Sí | - |
| FechaEnvio | DATETIME | 19 | Sí | - |
| FechaCreado | DATETIME | 19 | Sí | - |
| URLAdjunto | VARCHAR | 255 | Sí | - |

#### Índices
- **PrimaryKey**: IDCorreo (ÚNICO)
- **IDCorreo**: IDCorreo

---

### TbUsuariosHistoricoContrasenias

**Registros:** 428

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| Usuario | VARCHAR | 255 | Sí | - |
| PassAntigua | VARCHAR | 255 | Sí | - |
| FechaPass | DATETIME | 19 | Sí | - |

#### Índices
- **PrimaryKey**: Usuario (ÚNICO)
- **PrimaryKey**: PassAntigua (ÚNICO)
- **{C99BFE53-04C6-4580-B23B-BDB314F2DBA1}**: Usuario

---

### TbUsuariosTareasDiarias

**Registros:** 8

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| UsuarioRed | VARCHAR | 255 | Sí | - |

#### Índices
- **PrimaryKey**: UsuarioRed (ÚNICO)

---

### TbVideos

**Registros:** 16

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDVideo | INTEGER | 10 | Sí | - |
| Titulo | VARCHAR | 255 | Sí | - |
| NombreArchivo | VARCHAR | 255 | Sí | - |
| IDAplicacion | INTEGER | 10 | Sí | - |
| Observaciones | LONGCHAR | 1073741823 | Sí | - |
| Descripcion | LONGCHAR | 1073741823 | Sí | - |
| SubidoPor | VARCHAR | 255 | Sí | - |
| FechaSubido | DATETIME | 19 | Sí | - |
| ParaCalidad | VARCHAR | 2 | Sí | - |
| ParaAdministrador | VARCHAR | 2 | Sí | - |
| ParaTecnicos | VARCHAR | 2 | Sí | - |

#### Índices
- **PrimaryKey**: IDVideo (ÚNICO)
- **IDVideo**: IDVideo

---

### TbVideosCategorias

**Registros:** 15

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDCategoriaVideo | INTEGER | 10 | Sí | - |
| IDCategoria | INTEGER | 10 | Sí | - |
| IDVideo | INTEGER | 10 | Sí | - |

#### Índices
- **PrimaryKey**: IDCategoriaVideo (ÚNICO)
- **Segundo**: IDCategoria (ÚNICO)
- **Segundo**: IDVideo (ÚNICO)
- **IDCategoria**: IDCategoria
- **IDCategoriaVideo**: IDCategoriaVideo
- **IDVideo**: IDVideo

---

### TbVideosCuestionario

**Registros:** 0

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDVideoCuestionario | INTEGER | 10 | Sí | - |
| IDCuestionario | INTEGER | 10 | Sí | - |
| IDVideo | INTEGER | 10 | Sí | - |
| FechaRealizado | DATETIME | 19 | Sí | - |
| UsuarioRealiza | VARCHAR | 255 | Sí | - |
| Observaciones | LONGCHAR | 1073741823 | Sí | - |

#### Índices
- **PrimaryKey**: IDVideoCuestionario (ÚNICO)
- **Secundario**: IDCuestionario (ÚNICO)
- **Secundario**: IDVideoCuestionario (ÚNICO)
- **IDVideo**: IDVideo
- **IDVideoCuestionario**: IDVideoCuestionario
- **IDVisionado**: IDCuestionario

---

### TbVideosVisionados

**Registros:** 138

#### Estructura
| Columna | Tipo | Tamaño | Nulo | Valor por Defecto |
|---------|------|--------|------|-------------------|
| IDVisionado | INTEGER | 10 | Sí | - |
| IDVideo | INTEGER | 10 | Sí | - |
| TiempoVisionado | INTEGER | 10 | Sí | - |
| TiempoVideo | INTEGER | 10 | Sí | - |
| IDUsuario | INTEGER | 10 | Sí | - |
| FechaVisionado | DATETIME | 19 | Sí | - |

#### Índices
- **PrimaryKey**: IDVisionado (ÚNICO)
- **IDVideo**: IDVideo
- **IDVisionado**: IDVisionado

---

