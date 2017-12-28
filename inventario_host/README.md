# inventariohost
Para utilizar el projecto se debe instalar los modulos descritos en el archivo **requirements.txt** después de haber instalado [Python 3.6.3](https://www.python.org/downloads/):

```python
python -m pip install -r requirements.txt
```

Para ejecutar el projecto previamente instalado los requirements :  

```python
python manage.py runserver
```
o
```python
python manage.py runserver 127.0.0.1:8000
```

Ejecutar sitio en el navegador url:
```python
http://127.0.0.1:8000/
```
Ejecutar api en el navegador url:
```python
http://127.0.0.1:8000/api/
```
Ejecutar sitio administrador en el navegador url:
```python
http://127.0.0.1:8000/admin/
```

# Docker

Ejecutar comandos Docker como usuario no root, agregar usuario al grupo Docker:

```bash
su -l root -c 'usermod -aG docker mi_usuario_name'
```
