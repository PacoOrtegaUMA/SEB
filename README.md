**Descripción del Proyecto**

Este repositorio contiene materiales, scripts y documentación para la configuración y gestión de exámenes seguros mediante Safe Exam Browser (SEB) y máquinas virtuales (VirtualBox) en el Campus Virtual de la Universidad de Málaga.

El proyecto proporciona un marco completo para crear entornos de evaluación controlados, reproducibles y adaptables a distintos niveles de seguridad, desde exámenes básicos hasta escenarios avanzados con máquinas virtuales aisladas o con conectividad limitada.

Incluye:

- Guía detallada de configuración de SEB.
- Diferentes niveles de seguridad para exámenes.
- Scripts para automatizar tareas.
- Herramientas para generación de URLs permitidas.
- Automatización de configuraciones SEB.
- Control de conectividad en máquinas virtuales.
- Recomendaciones de seguridad y buenas prácticas.

**Niveles de Seguridad**

El sistema contempla cuatro niveles progresivos:

Nivel 1 – Examen básico con SEB
Navegación y aplicaciones restringidas desde el Campus Virtual.

Nivel 2 – SEB con acceso a contenidos de la asignatura
Acceso controlado a los recursos internos mediante generación automática de URLs.

Nivel 3 – Entorno aislado sin Internet
Uso de máquinas virtuales sin conectividad externa para exámenes técnicos.

Nivel 4 – Entorno con Internet controlado
Acceso limitado a servicios específicos bajo supervisión estricta.

**Herramientas Incluidas**

Generar_Urls_Asig.py
Extrae automáticamente las URLs de una asignatura del Campus Virtual.

Generar_Seb.py
Genera archivos .seb con URLs integradas de forma automática.

Scripts de control de red
Permiten habilitar o bloquear el acceso a Internet en máquinas virtuales.

Scripts de configuración de VirtualBox
Refuerzan el aislamiento del entorno de examen.

**Objetivo**

El objetivo principal de este proyecto es:

Facilitar la creación de entornos de evaluación seguros, flexibles y fiables, reduciendo el fraude académico y garantizando condiciones homogéneas para todo el alumnado.

Está especialmente orientado a exámenes técnicos que requieren el uso de herramientas informáticas, programación, redes o entornos virtualizados.

**Autor**

Francisco Ortega Zamorano
Departamento de Lenguajes y Ciencias de la Computación
Universidad de Málaga
Curso 2025–2026
