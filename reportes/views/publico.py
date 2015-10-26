#encoding:utf-8
from django.shortcuts import render, redirect

def tipos(request):
    return render(request, 'publico/tipos.html', {
    })

#usado para visualizar datos en dos o cuatro dimensiones
#la primera columna es el nombre o identificador de la burbuja
#las segunda y tercera columna son los ejes(x e y), la cuarta el color y la quinta el tamaño de la burbuja
#el color o cuarta columna lo que indica es una manera de agrupar los datos y dependiendo de ese grupo toma un color
#las columnas  dos, tres y cinco deben ser numéricas, la columna cuatro(color) puede ser numérica o string
def ejemploBubble(request):
    #para especificar el nombre de las columnas use el formato nombreColumna:tipo donde tipo puede ser string o number
    columnas = ['ID:string','Life Expectancy:number', 'Fertility Rate:number', 'Region:string', 'Population:number']
    datos = [
        ['CAN',    80.66,              1.67,      'North America',  33739900],
        ['DEU',    79.84,              1.36,      'Europe',         81902307],
        ['DNK',    78.6,               1.84,      'Europe',         5523095],
        ['EGY',    72.73,              2.78,      'Middle East',    79716203],
        ['GBR',    80.05,              2,         'Europe',         61801570],
        ['IRN',    72.49,              1.7,       'Middle East',    73137148],
        ['IRQ',    68.09,              4.77,      'Middle East',    31090763],
        ['ISR',    81.55,              2.96,      'Middle East',    7485600],
        ['RUS',    68.6,               1.54,      'Europe',         141850000],
        ['USA',    78.09,              2.05,      'North America',  307007000]

      ]
    return render(request, 'ejemplos/bubble.html',
        {"datos": datos,
        "columnas":columnas,
        "titulo": "Correlation between life expectancy, fertility rate and population of some world countries (2010)",
        "div": "bubble_chart"})

#usado para visualizar cómo varios parámetros cambian con el tiempo
#usa flash
#la primera columna debe de ser de tipo String y representa el nombre de las entidades
#la segunda columna debe contener valores de tiempo. Se puede usar uno de los siguientes formatos
#* numéricas(number) si representan un año, ex. 2008
#* fecha(date) si es una fecha puntual, ex. 'new Date(2000,10,2)' -> OJO: se pasa como string
#las restantes columnas pueden ser numéricas o string

def ejemploMotion(request):
    #para especificar el nombre de las columnas use el formato nombreColumna:tipo donde tipo puede ser string, date o number
    #recuerde que la primera columna debe ser string y la segunda debe de ser date o number
    columnas = ['Fruit:string','Date:date','Sales:number','Expenses:number','Location:string']
    datos = [
          ['Apples', 'new Date (1988,0,1)', 1000, 300, 'East'],
          ['Oranges', 'new Date (1988,0,1)', 1150, 200, 'West'],
          ['Bananas', 'new Date (1988,0,1)', 300,  250, 'West'],
          ['Apples',  'new Date (1989,6,1)', 1200, 400, 'East'],
          ['Oranges', 'new Date (1989,6,1)', 750,  150, 'West'],
          ['Bananas', 'new Date (1989,6,1)', 788,  617, 'West']
        ]
    return render(request, 'ejemplos/motion.html',
        {"datos": datos,
        "columnas": columnas,
        "div": "motion_chart"})