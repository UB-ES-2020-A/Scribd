# Scribd
![GitHub release](https://img.shields.io/github/v/release/UB-ES-2020/Scribd)
[![GitHub issues](https://img.shields.io/github/issues/UB-ES-2020/Scribd)](https://github.com/UB-ES-2020/Scribd/issues) 
![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/UB-ES-2020/Scribd/Demo2) 
[![Build Status](https://travis-ci.com/UB-ES-2020/Scribd.svg?branch=main)](https://travis-ci.com/UB-ES-2020/Scribd) 
[![CodeFactor](https://www.codefactor.io/repository/github/ub-es-2020/scribd/badge)](https://www.codefactor.io/repository/github/ub-es-2020/scribd) 
[![Coverage Status](https://coveralls.io/repos/github/UB-ES-2020/Scribd/badge.svg)](https://coveralls.io/github/UB-ES-2020/Scribd) 
[![deepcode](https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6IlVCLUVTLTIwMjAiLCJyZXBvMSI6IlNjcmliZCIsImluY2x1ZGVMaW50IjpmYWxzZSwiYXV0aG9ySWQiOjE4MDMwLCJpYXQiOjE2MDU4MDMzMDB9.tYymiV4SWNBmk00ot3n5S-LzPFzsulyE6tC-8_m3NG8)](https://www.deepcode.ai/app/gh/UB-ES-2020/Scribd/_/dashboard?utm_content=gh%2FUB-ES-2020%2FScribd)

# Enginyeria del Software

Este Repositorio es de la asignatura de Enginyeria del Software, Ultima asignatura la carrera de Ingenieria Informatica de la Universidad de Barcelona.
Se basa en trabajo en equipo basado en métodos ágiles: Utilizamos Scrum, Trello, Kanban, XP...

## Comenzando 🚀

Para utilizar este proyecto necesitaras Pycharm

Mira **Deployment** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

1. Installing Django <br>
`pip install -r requirements.txt`  

2. Creating a project <br>
`django-admin startproject Scribd` <br>

### Importante! <br>
- Podemos crear un archivo json para exportar nuestra base de datos   
`python manage.py dumpdata > <nombre de archivo>.json`   
 
### Instalación 🔧

Python 3.8.6

## Ejecutando las pruebas ⚙️  

#### Development server localhost  🚀
`cd Scribd`  
`python manage.py makemigrations`  
`python manage.py migrate`  
`python manage.py loaddata fixtures/ebooks.json`  
`python manage.py runserver`  
- Podemos pasar test con:  
`python manage.py test`
- Podemos pasar test con **coverage**:  
`coverage run --source='.' manage.py test Scribd`


## Deployment CI/CD 📦  
- AutoDeployment:  
    * [**Travis**](https://travis-ci.com/)   
- Heroku:  
    * **Staging**: https://es-scribd-staging.herokuapp.com/  
    * **Production**: https://es-scribd.herokuapp.com/  

## Software analytics: 👩🏽‍💻🧑🏽‍💻
- [DeepCode](https://www.deepcode.ai/)  
- [Codefactor](https://codefactor.io)  
- [Coveralls](https://coveralls.io/)  

## Construido con 🛠️

* [PyCharm Professional](https://www.jetbrains.com/pycharm/) - Herramienta Practica 2

## Wiki 📖

No disponemos de wiki(actualmente)

## Versionado 📌

Usamos [Django](https://www.djangoproject.com/) Concretamente la versión 3.1.3

## Autores ✒️

* [Ester](https://github.com/esterSeguraUB) - Estudiante de Universidad de Barcelona 
* [Johnny](https://github.com/johnnync13) - Estudiante de Universidad de Barcelona
* [Marcos](https://github.com/marcosPlaza) - Estudiante de Universidad de Barcelona 
* [Xavi](https://github.com/XaviVal) - Estudiante de Universidad de Barcelona
* [Iker](https://github.com/IkerHonorato) - Estudiante de Universidad de Barcelona
* [**Eduardo**](https://github.com/eduardou-ub) - *Tutor practicas*
* [**Eloi Puertas**](https://github.com/eloipuertas) - *Documentación Teoría*

También puedes mirar la lista de todos los [contribuyentes](https://github.com/UB-ES-2020/Scribd/contributors) quíenes han participado en este proyecto. 

## Licencia 📄

## Expresiones de Gratitud 🎁

* Agradecimientos a los profesores de la asignatura.
