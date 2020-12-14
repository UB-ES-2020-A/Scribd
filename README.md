# Scribd
![GitHub release](https://img.shields.io/github/v/release/UB-ES-2020-A/Scribd)
[![GitHub issues](https://img.shields.io/github/issues/UB-ES-2020-A/Scribd)](https://github.com/UB-ES-2020-A/Scribd/issues) 
![GitHub milestones](https://img.shields.io/github/milestones/open/UB-ES-2020-A/Scribd)
![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/UB-ES-2020-A/Scribd/Demo2) 
[![Build Status](https://travis-ci.com/UB-ES-2020-A/Scribd.svg?branch=main)](https://travis-ci.com/UB-ES-2020-A/Scribd) 
[![CodeFactor](https://www.codefactor.io/repository/github/ub-es-2020-a/scribd/badge)](https://www.codefactor.io/repository/github/ub-es-2020-a/scribd)
[![Coverage Status](https://coveralls.io/repos/github/UB-ES-2020-A/Scribd/badge.svg?branch=main)](https://coveralls.io/github/UB-ES-2020-A/Scribd?branch=main)
[![deepcode](https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6IlVCLUVTLTIwMjAtQSIsInJlcG8xIjoiU2NyaWJkIiwiaW5jbHVkZUxpbnQiOmZhbHNlLCJhdXRob3JJZCI6MTgwMzAsImlhdCI6MTYwNjczOTMwMH0.0I3DrhQ1w89rXdEFHF0VXhjMFk7XDrtzqixBPX_dztA)](https://www.deepcode.ai/app/gh/UB-ES-2020-A/Scribd/_/dashboard?utm_content=gh%2FUB-ES-2020-A%2FScribd)

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
