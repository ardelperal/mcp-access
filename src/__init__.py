"""
MCP Access Database Server

Servidor MCP para gestión de bases de datos Microsoft Access con soporte para contraseñas.
"""

__version__ = "1.1.0"
__author__ = "ardelperal"
__description__ = "Servidor MCP para gestión de bases de datos Microsoft Access"

from .mcp_access_server import AccessDatabaseManager

__all__ = ["AccessDatabaseManager"]