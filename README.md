# mercadolibre-bot 🤖
Un bot muy simple que se conecta con la api de mercado libre y actualiza un archivo xlsx.


## Instalación 📝

### Clonando el repo

```bash
$ git clone https://github.com/Scr44gr/mercadolibre-bot.git
```

### Instalando dependencias

**Tenemos que estar dentro de la carpeta del proyecto para poder instalar las dependencias.**
```bash
$ pip install -r requirements.txt
```

## Como usar 📓

Primero es necesario configurar nuestro archivo _settings.json_, para ello es necesario que entiendas su formato.

### Sheets 
Aquí ira la información de las hojas de cálculo.  Estan estructuradas en una lista, por lo cual si necesitas añadir una nueva tendras que hacerlo al final.




```javascript
        {
            "active": true,
            "name": "a",
            "path": "./example.xlsx",
            "output_path": "./myDocumentUpdated.xlsx",
            "hyperlink_in":"title",
            "column_date_value": "sales",
            "columns": [
                "title",
                "price",
                "sales",
                "nickname",
                "type_of_post",
                "date"
            ],
            "fetching_params": [
                "price",
                "sales"
            ]
        }
```

### Corriendo nuestro script 🤖

```python
python main.py
```
