Configurar entorno para generar el HTML / PDF
---------------------------------------------

Hay un script (`install_dependencies.sh`) que instala las
dependencias necesarias para generar el tutorial en todos sus
formatos.

*Abrir el archivo ANTES de ejecutarlo para estar SEGUROS que hace lo
 que queremos...*

1. Crear las version HTML, eBook y PDF (para crear esta version es necesario
   tener instalado `pdftk` 2.01):

```
fab create_html
fab create_ebook
fab create_pdf
```

1. Verificar que el PDF y eBook se abre correctamente con Evince y Firefox
(preview)
