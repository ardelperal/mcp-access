"""
Módulo de Documentación Mejorada para MCP Access Database Server
================================================================

Este módulo proporciona funcionalidades avanzadas de documentación incluyendo:
- Generación de diagramas ER automáticos (Mermaid)
- Documentación de campos mejorada con descripciones y validaciones
- Historial de cambios de la base de datos
- Exportación a múltiples formatos (HTML, JSON, PDF)
- Análisis de calidad de datos
- Generación de reportes ejecutivos

Autor: MCP Access Team
Versión: 1.0.0
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib
import re

# Configurar logging
logger = logging.getLogger(__name__)

@dataclass
class FieldDocumentation:
    """Documentación detallada de un campo."""
    name: str
    data_type: str
    size: Optional[int]
    nullable: bool
    default_value: Optional[str]
    description: str = ""
    business_rules: List[str] = None
    validation_rules: List[str] = None
    sample_values: List[str] = None
    data_quality_score: float = 0.0
    
    def __post_init__(self):
        if self.business_rules is None:
            self.business_rules = []
        if self.validation_rules is None:
            self.validation_rules = []
        if self.sample_values is None:
            self.sample_values = []

@dataclass
class TableDocumentation:
    """Documentación detallada de una tabla."""
    name: str
    description: str = ""
    purpose: str = ""
    business_context: str = ""
    fields: List[FieldDocumentation] = None
    record_count: int = 0
    data_quality_score: float = 0.0
    last_modified: Optional[datetime] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.fields is None:
            self.fields = []
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class DatabaseChangeRecord:
    """Registro de cambio en la base de datos."""
    timestamp: datetime
    change_type: str  # 'schema', 'data', 'relationship'
    table_name: str
    field_name: Optional[str]
    old_value: Optional[str]
    new_value: Optional[str]
    description: str
    hash_signature: str

class EnhancedDocumentationGenerator:
    """Generador de documentación mejorada para bases de datos Access."""
    
    def __init__(self, db_manager):
        """
        Inicializar el generador de documentación.
        
        Args:
            db_manager: Instancia de AccessDatabaseManager
        """
        self.db_manager = db_manager
        self.change_history: List[DatabaseChangeRecord] = []
        self.field_descriptions: Dict[str, Dict[str, str]] = {}
        self.table_descriptions: Dict[str, str] = {}
        
    def analyze_data_quality(self, table_name: str, sample_size: int = 1000) -> Dict[str, Any]:
        """
        Analizar la calidad de datos de una tabla.
        
        Args:
            table_name: Nombre de la tabla
            sample_size: Tamaño de muestra para análisis
            
        Returns:
            Dict con métricas de calidad de datos
        """
        try:
            # Obtener esquema de la tabla
            schema = self.db_manager.get_table_schema(table_name)
            
            # Obtener muestra de datos
            query = f"SELECT TOP {sample_size} * FROM [{table_name}]"
            sample_data = self.db_manager.execute_query(query)
            
            if not sample_data:
                return {"error": "No hay datos para analizar"}
            
            quality_metrics = {
                "table_name": table_name,
                "sample_size": len(sample_data),
                "fields": {},
                "overall_score": 0.0,
                "issues": []
            }
            
            field_scores = []
            
            for field in schema:
                field_name = field["column_name"]
                field_metrics = {
                    "data_type": field["data_type"],
                    "null_count": 0,
                    "unique_count": 0,
                    "completeness": 0.0,
                    "uniqueness": 0.0,
                    "validity": 0.0,
                    "consistency": 0.0,
                    "sample_values": [],
                    "issues": []
                }
                
                # Extraer valores del campo
                values = [row.get(field_name) for row in sample_data]
                non_null_values = [v for v in values if v is not None and v != ""]
                
                # Calcular métricas
                field_metrics["null_count"] = len(values) - len(non_null_values)
                field_metrics["completeness"] = len(non_null_values) / len(values) if values else 0
                field_metrics["unique_count"] = len(set(non_null_values))
                field_metrics["uniqueness"] = len(set(non_null_values)) / len(non_null_values) if non_null_values else 0
                
                # Muestras de valores (primeros 5 únicos)
                unique_values = list(set(non_null_values))[:5]
                field_metrics["sample_values"] = [str(v) for v in unique_values]
                
                # Validez según tipo de dato
                validity_score = self._calculate_validity_score(field, non_null_values)
                field_metrics["validity"] = validity_score
                
                # Consistencia (patrones en strings)
                consistency_score = self._calculate_consistency_score(field, non_null_values)
                field_metrics["consistency"] = consistency_score
                
                # Score general del campo
                field_score = (field_metrics["completeness"] * 0.3 + 
                             field_metrics["validity"] * 0.4 + 
                             field_metrics["consistency"] * 0.3)
                
                field_scores.append(field_score)
                
                # Identificar problemas
                if field_metrics["completeness"] < 0.8:
                    field_metrics["issues"].append(f"Baja completitud: {field_metrics['completeness']:.1%}")
                if field_metrics["validity"] < 0.9:
                    field_metrics["issues"].append(f"Problemas de validez: {field_metrics['validity']:.1%}")
                
                quality_metrics["fields"][field_name] = field_metrics
            
            # Score general de la tabla
            quality_metrics["overall_score"] = sum(field_scores) / len(field_scores) if field_scores else 0
            
            # Problemas generales
            if quality_metrics["overall_score"] < 0.7:
                quality_metrics["issues"].append("Calidad general de datos baja")
            
            return quality_metrics
            
        except Exception as e:
            logger.error(f"Error analizando calidad de datos para {table_name}: {e}")
            return {"error": str(e)}
    
    def _calculate_validity_score(self, field: Dict, values: List) -> float:
        """Calcular score de validez según el tipo de dato."""
        if not values:
            return 0.0
            
        data_type = field["data_type"].upper()
        valid_count = 0
        
        for value in values:
            try:
                if "INT" in data_type or "LONG" in data_type:
                    int(value)
                    valid_count += 1
                elif "DOUBLE" in data_type or "SINGLE" in data_type or "CURRENCY" in data_type:
                    float(value)
                    valid_count += 1
                elif "DATE" in data_type:
                    # Verificar si es una fecha válida
                    if isinstance(value, datetime) or self._is_valid_date_string(str(value)):
                        valid_count += 1
                else:
                    # Para texto, considerar válido si no está vacío
                    if str(value).strip():
                        valid_count += 1
            except:
                continue
                
        return valid_count / len(values) if values else 0.0
    
    def _calculate_consistency_score(self, field: Dict, values: List) -> float:
        """Calcular score de consistencia basado en patrones."""
        if not values or len(values) < 2:
            return 1.0
            
        # Para campos de texto, analizar patrones
        if "TEXT" in field["data_type"].upper():
            patterns = {}
            for value in values:
                pattern = self._extract_pattern(str(value))
                patterns[pattern] = patterns.get(pattern, 0) + 1
            
            # Si hay un patrón dominante (>70%), alta consistencia
            max_pattern_count = max(patterns.values()) if patterns else 0
            return max_pattern_count / len(values)
        
        return 1.0  # Para otros tipos, asumir consistencia alta
    
    def _extract_pattern(self, text: str) -> str:
        """Extraer patrón de un texto (ej: 'ABC123' -> 'AAA999')."""
        pattern = ""
        for char in text:
            if char.isalpha():
                pattern += "A"
            elif char.isdigit():
                pattern += "9"
            elif char.isspace():
                pattern += " "
            else:
                pattern += char
        return pattern
    
    def _is_valid_date_string(self, date_str: str) -> bool:
        """Verificar si una cadena representa una fecha válida."""
        date_formats = [
            "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S", "%m/%d/%Y %H:%M:%S"
        ]
        
        for fmt in date_formats:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except:
                continue
        return False
    
    def generate_er_diagram_mermaid(self) -> str:
        """
        Generar diagrama ER en formato Mermaid.
        
        Returns:
            String con el código Mermaid del diagrama ER
        """
        try:
            # Obtener información de tablas y relaciones
            doc = self.db_manager.generate_database_documentation()
            
            mermaid_code = "erDiagram\n"
            
            # Definir entidades (tablas)
            for table_name, table_info in doc["tables"].items():
                mermaid_code += f"    {table_name} {{\n"
                
                # Agregar campos
                for field in table_info["schema"]:
                    field_name = field["column_name"]
                    data_type = field["data_type"]
                    
                    # Determinar tipo de clave
                    is_pk = any(pk.get("column_name", pk) == field_name 
                              for pk in table_info.get("primary_keys", []))
                    
                    if is_pk:
                        mermaid_code += f"        {data_type} {field_name} PK\n"
                    else:
                        mermaid_code += f"        {data_type} {field_name}\n"
                
                mermaid_code += "    }\n\n"
            
            # Agregar relaciones
            for rel in doc["relationships"]:
                parent_table = rel["parent_table"]
                child_table = rel["child_table"]
                
                # Determinar cardinalidad (por defecto 1:N)
                cardinality = "||--o{"
                
                # Agregar relación
                mermaid_code += f"    {parent_table} {cardinality} {child_table} : \"{rel['parent_column']} -> {rel['child_column']}\"\n"
            
            return mermaid_code
            
        except Exception as e:
            logger.error(f"Error generando diagrama ER: {e}")
            return f"Error generando diagrama: {e}"
    
    def generate_enhanced_documentation(self, include_quality_analysis: bool = True) -> Dict[str, Any]:
        """
        Generar documentación mejorada completa.
        
        Args:
            include_quality_analysis: Si incluir análisis de calidad de datos
            
        Returns:
            Dict con documentación completa mejorada
        """
        try:
            # Obtener documentación base
            base_doc = self.db_manager.generate_database_documentation()
            
            enhanced_doc = {
                "metadata": {
                    "database_path": base_doc["database_path"],
                    "generation_timestamp": datetime.now().isoformat(),
                    "generator_version": "1.0.0",
                    "analysis_type": "enhanced"
                },
                "executive_summary": {},
                "tables": {},
                "relationships": base_doc["relationships"],
                "er_diagram": self.generate_er_diagram_mermaid(),
                "data_quality": {},
                "recommendations": [],
                "change_history": [asdict(change) for change in self.change_history]
            }
            
            total_records = 0
            quality_scores = []
            
            # Procesar cada tabla
            for table_name, table_info in base_doc["tables"].items():
                enhanced_table = {
                    "basic_info": table_info,
                    "description": self.table_descriptions.get(table_name, ""),
                    "business_context": "",
                    "enhanced_fields": [],
                    "data_quality": {},
                    "recommendations": []
                }
                
                # Análisis de calidad si está habilitado
                if include_quality_analysis:
                    quality_analysis = self.analyze_data_quality(table_name)
                    enhanced_table["data_quality"] = quality_analysis
                    
                    if "overall_score" in quality_analysis:
                        quality_scores.append(quality_analysis["overall_score"])
                
                # Documentación mejorada de campos
                for field in table_info["schema"]:
                    field_name = field["column_name"]
                    enhanced_field = FieldDocumentation(
                        name=field_name,
                        data_type=field["data_type"],
                        size=field.get("size"),
                        nullable=field["nullable"],
                        default_value=field.get("default_value"),
                        description=self.field_descriptions.get(table_name, {}).get(field_name, "")
                    )
                    
                    # Agregar reglas de negocio inferidas
                    enhanced_field.business_rules = self._infer_business_rules(field, table_name)
                    
                    # Agregar validaciones inferidas
                    enhanced_field.validation_rules = self._infer_validation_rules(field)
                    
                    enhanced_table["enhanced_fields"].append(asdict(enhanced_field))
                
                # Contar registros
                if isinstance(table_info["record_count"], int):
                    total_records += table_info["record_count"]
                
                # Generar recomendaciones para la tabla
                enhanced_table["recommendations"] = self._generate_table_recommendations(
                    table_name, enhanced_table
                )
                
                enhanced_doc["tables"][table_name] = enhanced_table
            
            # Resumen ejecutivo
            enhanced_doc["executive_summary"] = {
                "total_tables": len(base_doc["tables"]),
                "total_relationships": len(base_doc["relationships"]),
                "total_records": total_records,
                "average_data_quality": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
                "database_complexity": self._calculate_complexity_score(base_doc),
                "health_status": self._determine_health_status(quality_scores),
                "key_insights": self._generate_key_insights(base_doc, quality_scores)
            }
            
            # Recomendaciones generales
            enhanced_doc["recommendations"] = self._generate_general_recommendations(enhanced_doc)
            
            return enhanced_doc
            
        except Exception as e:
            logger.error(f"Error generando documentación mejorada: {e}")
            raise
    
    def _infer_business_rules(self, field: Dict, table_name: str) -> List[str]:
        """Inferir reglas de negocio basadas en el campo y tabla."""
        rules = []
        field_name = field["column_name"].lower()
        data_type = field["data_type"].upper()
        
        # Reglas basadas en nombres de campos
        if "id" in field_name and field_name.endswith("id"):
            rules.append("Identificador único para referenciar registros")
        elif "fecha" in field_name or "date" in field_name:
            rules.append("Debe ser una fecha válida")
        elif "email" in field_name:
            rules.append("Debe tener formato de email válido")
        elif "telefono" in field_name or "phone" in field_name:
            rules.append("Debe tener formato de teléfono válido")
        elif "precio" in field_name or "price" in field_name or "CURRENCY" in data_type:
            rules.append("Debe ser un valor monetario positivo")
        
        # Reglas basadas en tipo de dato
        if not field["nullable"]:
            rules.append("Campo obligatorio - no puede estar vacío")
        
        return rules
    
    def _infer_validation_rules(self, field: Dict) -> List[str]:
        """Inferir reglas de validación basadas en el campo."""
        rules = []
        data_type = field["data_type"].upper()
        field_name = field["column_name"].lower()
        
        # Validaciones por tipo de dato
        if "INT" in data_type or "LONG" in data_type:
            rules.append("Debe ser un número entero")
        elif "DOUBLE" in data_type or "SINGLE" in data_type:
            rules.append("Debe ser un número decimal")
        elif "DATE" in data_type:
            rules.append("Debe ser una fecha válida")
        elif "TEXT" in data_type and field.get("size"):
            rules.append(f"Máximo {field['size']} caracteres")
        
        # Validaciones específicas por nombre
        if "email" in field_name:
            rules.append("Formato: usuario@dominio.com")
        elif "url" in field_name or "web" in field_name:
            rules.append("Debe ser una URL válida")
        
        return rules
    
    def _generate_table_recommendations(self, table_name: str, table_doc: Dict) -> List[str]:
        """Generar recomendaciones específicas para una tabla."""
        recommendations = []
        
        # Verificar calidad de datos
        if "data_quality" in table_doc and "overall_score" in table_doc["data_quality"]:
            score = table_doc["data_quality"]["overall_score"]
            if score < 0.7:
                recommendations.append("Mejorar la calidad de datos - score actual: {:.1%}".format(score))
        
        # Verificar documentación
        if not table_doc["description"]:
            recommendations.append("Agregar descripción de la tabla")
        
        # Verificar campos sin documentar
        undocumented_fields = [f for f in table_doc["enhanced_fields"] 
                             if not f["description"]]
        if undocumented_fields:
            recommendations.append(f"Documentar {len(undocumented_fields)} campos sin descripción")
        
        # Verificar índices
        if len(table_doc["basic_info"].get("indexes", [])) == 0:
            recommendations.append("Considerar agregar índices para mejorar rendimiento")
        
        return recommendations
    
    def _calculate_complexity_score(self, doc: Dict) -> str:
        """Calcular score de complejidad de la base de datos."""
        table_count = len(doc["tables"])
        relationship_count = len(doc["relationships"])
        
        # Calcular complejidad basada en tablas y relaciones
        complexity_score = (table_count * 0.3) + (relationship_count * 0.7)
        
        if complexity_score < 10:
            return "Baja"
        elif complexity_score < 25:
            return "Media"
        else:
            return "Alta"
    
    def _determine_health_status(self, quality_scores: List[float]) -> str:
        """Determinar el estado de salud de la base de datos."""
        if not quality_scores:
            return "Desconocido"
        
        avg_score = sum(quality_scores) / len(quality_scores)
        
        if avg_score >= 0.9:
            return "Excelente"
        elif avg_score >= 0.8:
            return "Bueno"
        elif avg_score >= 0.7:
            return "Regular"
        else:
            return "Necesita Atención"
    
    def _generate_key_insights(self, doc: Dict, quality_scores: List[float]) -> List[str]:
        """Generar insights clave sobre la base de datos."""
        insights = []
        
        # Insight sobre tablas
        table_count = len(doc["tables"])
        if table_count > 20:
            insights.append(f"Base de datos compleja con {table_count} tablas")
        elif table_count < 5:
            insights.append(f"Base de datos simple con {table_count} tablas")
        
        # Insight sobre relaciones
        rel_count = len(doc["relationships"])
        if rel_count == 0:
            insights.append("No se detectaron relaciones explícitas entre tablas")
        elif rel_count > table_count:
            insights.append("Base de datos bien estructurada con múltiples relaciones")
        
        # Insight sobre calidad
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            if avg_quality < 0.7:
                insights.append("Se requiere atención en la calidad de datos")
            elif avg_quality > 0.9:
                insights.append("Excelente calidad de datos en general")
        
        return insights
    
    def _generate_general_recommendations(self, doc: Dict) -> List[str]:
        """Generar recomendaciones generales para la base de datos."""
        recommendations = []
        
        # Recomendaciones basadas en el resumen ejecutivo
        summary = doc["executive_summary"]
        
        if summary["health_status"] in ["Regular", "Necesita Atención"]:
            recommendations.append("Implementar proceso de limpieza de datos")
        
        if summary["total_relationships"] == 0:
            recommendations.append("Definir relaciones explícitas entre tablas")
        
        if summary["database_complexity"] == "Alta":
            recommendations.append("Considerar normalización o particionamiento")
        
        # Recomendaciones basadas en tablas
        undocumented_tables = sum(1 for table in doc["tables"].values() 
                                if not table["description"])
        if undocumented_tables > 0:
            recommendations.append(f"Documentar {undocumented_tables} tablas sin descripción")
        
        return recommendations
    
    def export_to_html(self, doc: Dict, output_path: str) -> str:
        """
        Exportar documentación a formato HTML.
        
        Args:
            doc: Documentación generada
            output_path: Ruta del archivo de salida
            
        Returns:
            Ruta del archivo generado
        """
        try:
            html_content = self._generate_html_template(doc)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error exportando a HTML: {e}")
            raise
    
    def _generate_html_template(self, doc: Dict) -> str:
        """Generar template HTML para la documentación."""
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentación de Base de Datos</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .summary {{ background: #e8f5e8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .table-section {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }}
        .field-table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        .field-table th, .field-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .field-table th {{ background-color: #f2f2f2; }}
        .quality-score {{ padding: 5px 10px; border-radius: 3px; color: white; }}
        .score-excellent {{ background-color: #28a745; }}
        .score-good {{ background-color: #ffc107; }}
        .score-poor {{ background-color: #dc3545; }}
        .recommendations {{ background: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
        .mermaid {{ text-align: center; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Documentación de Base de Datos</h1>
        <p><strong>Archivo:</strong> {doc['metadata']['database_path']}</p>
        <p><strong>Generado:</strong> {doc['metadata']['generation_timestamp']}</p>
    </div>
    
    <div class="summary">
        <h2>📋 Resumen Ejecutivo</h2>
        <ul>
            <li><strong>Total de tablas:</strong> {doc['executive_summary']['total_tables']}</li>
            <li><strong>Total de relaciones:</strong> {doc['executive_summary']['total_relationships']}</li>
            <li><strong>Total de registros:</strong> {doc['executive_summary']['total_records']:,}</li>
            <li><strong>Calidad promedio:</strong> {doc['executive_summary']['average_data_quality']:.1%}</li>
            <li><strong>Estado de salud:</strong> {doc['executive_summary']['health_status']}</li>
            <li><strong>Complejidad:</strong> {doc['executive_summary']['database_complexity']}</li>
        </ul>
    </div>
    
    <h2>🔗 Diagrama de Relaciones</h2>
    <div class="mermaid">
{doc['er_diagram']}
    </div>
    
    <h2>📚 Tablas</h2>
"""
        
        # Agregar información de cada tabla
        for table_name, table_info in doc['tables'].items():
            quality_score = table_info.get('data_quality', {}).get('overall_score', 0)
            score_class = self._get_score_class(quality_score)
            
            html += f"""
    <div class="table-section">
        <h3>📋 {table_name}</h3>
        <p><strong>Descripción:</strong> {table_info.get('description', 'Sin descripción')}</p>
        <p><strong>Registros:</strong> {table_info['basic_info']['record_count']:,}</p>
        <p><strong>Calidad de datos:</strong> <span class="quality-score {score_class}">{quality_score:.1%}</span></p>
        
        <h4>Campos</h4>
        <table class="field-table">
            <tr>
                <th>Campo</th>
                <th>Tipo</th>
                <th>Nulo</th>
                <th>Descripción</th>
                <th>Reglas de Negocio</th>
            </tr>
"""
            
            for field in table_info['enhanced_fields']:
                nullable = "Sí" if field['nullable'] else "No"
                description = field.get('description', 'Sin descripción')
                business_rules = '; '.join(field.get('business_rules', []))
                
                html += f"""
            <tr>
                <td><strong>{field['name']}</strong></td>
                <td>{field['data_type']}</td>
                <td>{nullable}</td>
                <td>{description}</td>
                <td>{business_rules}</td>
            </tr>
"""
            
            html += """
        </table>
"""
            
            # Agregar recomendaciones si existen
            if table_info.get('recommendations'):
                html += """
        <div class="recommendations">
            <h4>💡 Recomendaciones</h4>
            <ul>
"""
                for rec in table_info['recommendations']:
                    html += f"                <li>{rec}</li>\n"
                
                html += """
            </ul>
        </div>
"""
            
            html += "    </div>\n"
        
        # Agregar recomendaciones generales
        if doc.get('recommendations'):
            html += """
    <div class="recommendations">
        <h2>💡 Recomendaciones Generales</h2>
        <ul>
"""
            for rec in doc['recommendations']:
                html += f"            <li>{rec}</li>\n"
            
            html += """
        </ul>
    </div>
"""
        
        html += """
    <script>
        mermaid.initialize({startOnLoad:true});
    </script>
</body>
</html>
"""
        
        return html
    
    def _get_score_class(self, score: float) -> str:
        """Obtener clase CSS para el score de calidad."""
        if score >= 0.8:
            return "score-excellent"
        elif score >= 0.6:
            return "score-good"
        else:
            return "score-poor"
    
    def export_to_json(self, doc: Dict, output_path: str) -> str:
        """
        Exportar documentación a formato JSON.
        
        Args:
            doc: Documentación generada
            output_path: Ruta del archivo de salida
            
        Returns:
            Ruta del archivo generado
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(doc, f, indent=2, ensure_ascii=False, default=str)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error exportando a JSON: {e}")
            raise
    
    def add_field_description(self, table_name: str, field_name: str, description: str):
        """Agregar descripción a un campo."""
        if table_name not in self.field_descriptions:
            self.field_descriptions[table_name] = {}
        self.field_descriptions[table_name][field_name] = description
    
    def add_table_description(self, table_name: str, description: str):
        """Agregar descripción a una tabla."""
        self.table_descriptions[table_name] = description
    
    def record_change(self, change_type: str, table_name: str, description: str, 
                     field_name: str = None, old_value: str = None, new_value: str = None):
        """Registrar un cambio en la base de datos."""
        change = DatabaseChangeRecord(
            timestamp=datetime.now(),
            change_type=change_type,
            table_name=table_name,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            description=description,
            hash_signature=hashlib.md5(f"{table_name}{field_name}{description}".encode()).hexdigest()
        )
        self.change_history.append(change)