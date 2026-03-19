# Vedabase Original Edition - Plan de Publicación

## Estado Actual: Interior Template en progreso

---

## FASE 1: DISEÑO Y TEMPLATES (En progreso)

### Portadas (Covers)
- [x] Definir paleta de colores por categoría
- [x] Crear generate_covers.py (portadas minimalistas)
- [x] Crear generate_back_covers.py (contraportadas)
- [x] Obtener portada BG 1972 original
- [x] Upscaling IA de portada BG (1838x2775 KDP ready)
- [ ] Procesar otras portadas pequeñas con upscaling:
  - [ ] Isopanisad (1556x2332 → 1838x2775)
  - [ ] Raja-vidya (1290x2147 → 1838x2775)
  - [ ] NOI (1418x2111 → 1838x2775)
  - [ ] PQPA (1255x2108 → 1838x2775)
- [ ] Generar portadas minimalistas para libros sin portada original

### Interior (6x9 Print)
- [x] Crear interior_specs.yaml (especificaciones KDP)
- [x] Crear interior.css (estilos completos)
- [x] Crear book_template.html (Jinja2)
- [x] Crear generate_interior.py (generador PDF)
- [ ] Instalar dependencias (weasyprint, jinja2, markdown)
- [ ] Probar generación con libro sample
- [ ] Ajustar estilos según resultado

### Contenido Legal
- [x] Definir modelo de licencia KBI
- [x] Crear publisher's note EN/ES
- [x] Crear pricing_guide.md
- [x] Crear amazon_kdp_metadata.yaml

---

## FASE 2: OBTENER CONTENIDO

### Fuentes de Contenido
- [ ] Descargar todos los ZIPs de vedabase.bhaktiyoga.es
- [ ] Extraer contenido MD/HTML de cada libro
- [ ] Verificar integridad del contenido
- [ ] Crear word count por libro

### Libros Introductory (I-01 a I-12)
| ID | Título | Estado |
|----|--------|--------|
| I-01 | Raja-vidya | Pendiente |
| I-02 | Path of Perfection | Pendiente |
| I-03 | Perfect Questions | Pendiente |
| I-04 | Perfection of Yoga | Pendiente |
| I-05 | Beyond Birth and Death | Pendiente |
| I-06 | Easy Journey | Pendiente |
| I-07 | Elevation | Pendiente |
| I-08 | Life Comes from Life | Pendiente |
| I-09 | Light of Bhagavata | Pendiente |
| I-10 | On the Way | Pendiente |
| I-11 | Reservoir of Pleasure | Pendiente |
| I-12 | Topmost Yoga | Pendiente |

### Libros Essential (ET-01 a ET-04)
| ID | Título | Estado |
|----|--------|--------|
| ET-01 | Nectar of Devotion | Pendiente |
| ET-02 | Nectar of Instruction | Pendiente |
| ET-03 | Sri Isopanisad | Pendiente |
| ET-04 | Teachings Lord Caitanya | Pendiente |

### Libros Teachings (T-01 a T-04)
| ID | Título | Estado |
|----|--------|--------|
| T-01 | Teachings of Lord Kapila | Pendiente |
| T-02 | Teachings of Queen Kunti | Pendiente |
| T-03 | Teachings of Prahlada | Pendiente |
| T-04 | Science of Self-Realization | Pendiente |

### Major Works (MW-01 a MW-04)
| ID | Título | Estado |
|----|--------|--------|
| MW-01 | Bhagavad-gita As It Is | Pendiente |
| MW-02 | Srimad-Bhagavatam | Multi-volumen |
| MW-03 | Sri Caitanya-caritamrta | Multi-volumen |
| MW-04 | Krsna Book | 2 volúmenes |

---

## FASE 3: PRODUCCIÓN (Libro por libro)

### Para cada libro:
1. [ ] Descargar/extraer contenido
2. [ ] Crear metadata.yaml con info del libro
3. [ ] Formatear contenido a MD estructurado
4. [ ] Generar interior PDF con generate_interior.py
5. [ ] Verificar en KDP Previewer
6. [ ] Generar portada específica
7. [ ] Generar contraportada
8. [ ] Crear ePub con Calibre/Pandoc
9. [ ] Validar ePub con epubcheck

### Libro de Prueba: Raja-vidya (I-01)
- [ ] Descargar de vedabase.bhaktiyoga.es
- [ ] Crear estructura de carpetas
- [ ] Formatear contenido
- [ ] Generar PDF interior
- [ ] Revisar y ajustar estilos
- [ ] Crear portada final
- [ ] Subir a KDP como prueba

---

## FASE 4: PUBLICACIÓN EN AMAZON KDP

### Configuración de Cuenta
- [ ] Verificar cuenta KDP activa
- [ ] Configurar información fiscal
- [ ] Crear Series en Amazon

### Subida de Libros
- [ ] Empezar con libros Introductory (menor riesgo)
- [ ] Subir 1-2 libros primero como prueba
- [ ] Esperar aprobación
- [ ] Si OK, continuar con resto

### Por cada libro subido:
- [ ] Upload interior PDF
- [ ] Upload cover PDF
- [ ] Completar metadata (título, descripción, keywords)
- [ ] Configurar precio según pricing_guide.md
- [ ] Seleccionar categorías
- [ ] Enviar a revisión

---

## FASE 5: ARCHIVE.ORG (Distribución Gratuita)

### Subida a Archive.org
- [ ] Crear cuenta/verificar cuenta en archive.org
- [ ] Crear colección "Vedabase Original Edition"
- [ ] Subir ePubs de todos los libros (gratuito)
- [ ] Subir PDFs de interiores (gratuito)
- [ ] Añadir metadata completa (autor, fecha original, licencia)
- [ ] Enlazar desde vedabase.bhaktiyoga.es

### Beneficios:
- Distribución gratuita mundial
- Preservación permanente
- Sin riesgo de DMCA (ya hay ediciones originales en Archive)
- Complementa venta en Amazon (gratis vs. físico)

---

## FASE 6: MARKETING

### Assets de Marketing
- [ ] Landing page vedabase.bhaktiyoga.es/amazon
- [ ] Descripciones A+ Content
- [ ] Imágenes promocionales
- [ ] Keywords optimizados

### Lanzamiento
- [ ] Email a lista existente
- [ ] Post en redes (sin FB)
- [ ] Amazon Ads (opcional)
- [ ] Enlazar Archive.org como opción gratuita

---

## ARCHIVOS CLAVE DEL PROYECTO

```
/amazon_books/
├── tasks.md                  # Este archivo
├── pricing_guide.md          # Precios y royalties
├── amazon_kdp_metadata.yaml  # Metadata para KDP
├── generate_covers.py        # Generador de portadas
├── generate_back_covers.py   # Generador contraportadas
├── generate_interior.py      # Generador PDF interior
├── templates/
│   ├── interior.css          # Estilos interior
│   ├── interior_specs.yaml   # Specs KDP
│   └── book_template.html    # Template Jinja2
├── covers/
│   └── originals/
│       ├── FINAL_BG_1972.jpg # Portada BG lista
│       └── BG_1972_KDP_READY.jpg
└── books/
    └── [por crear]
```

---

## DECISIONES TOMADAS

1. **Licencia**: Publicar bajo licencia KBI (como Gita español)
2. **Portada BG**: Usar versión upscaled con IA de KrishnaStore
3. **Precios**: ePub $0.99, Print mínimo + 30% profit
4. **Formato**: 6x9 KDP standard
5. **Tipografía**: Garamond 11pt
6. **Colores por categoría**:
   - Major Works: Azul #1a365d
   - Essential: Borgoña #722f37
   - Teachings: Verde #2d5016
   - Introductory: Naranja #c65d07
   - Lectures: Púrpura #4a1a6b

---

## RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Mitigación |
|--------|--------------|------------|
| DMCA takedown | Media | Empezar con libros pequeños, tener respuesta KBI lista |
| Cierre cuenta | Baja | No subir todo de golpe, mantener perfil bajo |
| Rechazo KDP | Baja | Usar KDP Previewer antes de subir |

---

## PRÓXIMA SESIÓN

1. Instalar dependencias Python (weasyprint, jinja2, markdown)
2. Probar generación de PDF con libro sample
3. Descargar Raja-vidya de vedabase
4. Procesar Raja-vidya completo como prueba

---

*Última actualización: 2026-03-19*
