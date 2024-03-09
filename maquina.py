import random

#Si está en la izquierda, si está en la derecha, si está limpiando o si está esperando
estados_aspiradora = ['izquierda', 'derecha', 'limpiando', 'espera']

"""
La aspiradora en sí no tiene percepciones, pero vamos a simular entonces que la aspiradora, tiene internamente un registro que le envía percepciones artificiales que le indican según el modelo qué hacer
"""
percepciones_aspiradora = ['limpia','movio-izquierda','movio-derecha','espera']

#Si está en la izquierda, moverse a la derecha, limpiar o esperar
reglas_aspiradora = {
    'izquierda': 'mover-derecha',
    'derecha': 'mover-izquierda',
    'limpiando': 'esperar',
    'espera': random.choice['limpiar','mover-izquierda','mover-derecha']
}

#Esto en el ejemplo estaba con la parte derecha de las reglas, pero lo cambié por lo estados dado que son básicamente mensajes informativos y utilizando el estado, es más claro
acciones_aspiradora = {
    'izquierda':  "--------------- Se movió a la izquierda -----------------",
    'derecha':    "---------------- Se movió a la derecha ------------------",
    'limpiando':  "--------------------- Limpió ----------------------------",
    'espera':     "--------------------- Esperó ----------------------------"
}

modelo_aspiradora = {
    ('izquierda','mover-derecha','movio-derecha'): 'derecha',
    ('derecha','mover-izquierda','movio-izquierda'): 'izquierda',
    ('espera','limpiar','limpia'): 'limpiando',
    ('espera','mover-izquierda','movio-izquierda'): 'izquierda',
    ('espera','mover-derecha','movio-derecha'): 'derecha'
}

def actualizar_estado_aspiradora(estado, accion, percepcion):
    if (estado, accion, percepcion) in modelo_aspiradora:
        return modelo_aspiradora[(estado, accion, percepcion)]
    else:
        return 'espera'

estado_actual_aspiradora = 'espera'
accion_actual_aspiradora = 'limpiar'

while True:
    print(acciones_aspiradora[accion_actual_aspiradora])
    percepcion_aspiradora = random.choice(percepciones_aspiradora)
    estado_actual_aspiradora = actualizar_estado_aspiradora(estado_actual_aspiradora, accion_actual_aspiradora, percepcion_aspiradora)
    accion_actual_aspiradora = reglas_aspiradora[estado_actual_aspiradora]
