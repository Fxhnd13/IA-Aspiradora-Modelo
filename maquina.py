import random
import time
import threading
import keyboard

estado_actual_aspiradora = 'espera'
accion_actual_aspiradora = 'esperar'
cuadranteIzquierdoLimpio = True
cuadranteDerechoLimpio = True
posicionAspiradora = 1

#Si está en la izquierda, si está en la derecha, si está limpiando o si está esperando
estados_aspiradora = ['izquierda', 'derecha', 'limpiando', 'espera']

"""
La aspiradora en sí no tiene percepciones, pero vamos a simular entonces que la aspiradora, tiene internamente un registro que le envía percepciones artificiales que le indican según el modelo qué hacer
"""
percepciones_aspiradora = ['limpia','movio-izquierda','movio-derecha']

#Si está en la izquierda, moverse a la derecha, limpiar o esperar
reglas_aspiradora = {
    'izquierda': 'mover-derecha',
    'derecha': 'mover-izquierda',
    'limpiando': 'esperar',
    'espera': random.choice(['limpiar','mover-izquierda','mover-derecha'])
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
    global modelo_aspiradora

    if (estado, accion, percepcion) in modelo_aspiradora:
        return modelo_aspiradora[(estado, accion, percepcion)]
    else:
        return 'espera'

def aspirar():
    global estado_actual_aspiradora
    global accion_actual_aspiradora
    global acciones_aspiradora
    global percepciones_aspiradora
    global reglas_aspiradora

    for i in range(1,30):
        print(acciones_aspiradora[estado_actual_aspiradora])
        imprimir_estado_aspiradora()
        percepcion_aspiradora = random.choice(percepciones_aspiradora)
        """ print("-----------------------------------------------------------------------------")
        print("PERCEPCIÓN:> ", percepcion_aspiradora)
        print("ESTADO:> ", estado_actual_aspiradora)
        print("ACCION:> ", accion_actual_aspiradora)
        print("-----------------------------------------------------------------------------") """
        estado_actual_aspiradora = actualizar_estado_aspiradora(estado_actual_aspiradora, accion_actual_aspiradora, percepcion_aspiradora)
        verificar_estado_cuadrante()
        accion_actual_aspiradora = reglas_aspiradora[estado_actual_aspiradora]
        time.sleep(1)

def verificar_estado_cuadrante():
    global cuadranteIzquierdoLimpio
    global cuadranteDerechoLimpio
    global posicionAspiradora
    global estado_actual_aspiradora

    if(estado_actual_aspiradora == 'limpiando'): 
        if(posicionAspiradora==1):
            cuadranteIzquierdoLimpio=True
        elif(posicionAspiradora==2):
            cuadranteDerechoLimpio=True
    elif(estado_actual_aspiradora == 'izquierda'):
        posicionAspiradora=1
    elif(estado_actual_aspiradora == 'derecha'):
        posicionAspiradora=2

def imprimir_estado_aspiradora():
        global posicionAspiradora
        global cuadranteIzquierdoLimpio
        global cuadranteDerechoLimpio

        print("-----------------------------------------------------------------------------")
        print("ESTADO:> La aspiradora está en el cuadrante: ", ("A" if posicionAspiradora == 1 else "B"))
        print("ESTADO:> El cuadrante A está: ", ("Limpio" if cuadranteIzquierdoLimpio else "Sucio"))
        print("ESTADO:> El cuadrante B está: ", ("Limpio" if cuadranteDerechoLimpio else "Sucio"))
        print("-----------------------------------------------------------------------------")

def teclado_escucha(exit_event):
    def on_key_event(e):
        global cuadranteIzquierdoLimpio
        global cuadranteDerechoLimpio

        if e.event_type == keyboard.KEY_DOWN:
            if e.name == 'a':
                print("ACCION:> Se ensució el cuadrante izquierdo")
                cuadranteIzquierdoLimpio=False
            elif e.name == 's':
                print("ACCION:> Se ensució el cuadrante derecho")
                cuadranteDerechoLimpio=False
            elif e.name == 'd':
                print("Finalizando el hilo de interacción")
                exit_event.set()

    # Configurar el manejador de eventos de teclado
    keyboard.hook(on_key_event)

    # Mantener el hilo en ejecución hasta que se establezca la señal de salida
    while not exit_event.is_set():
        time.sleep(0.1)

    # Limpiar el manejador de eventos al finalizar el hilo
    keyboard.unhook_all()

if __name__ == "__main__":
    # Crear un evento para señalizar la salida del hilo
    exit_event = threading.Event()

    # Crear un hilo para la escucha de teclas
    hilo_interaccion = threading.Thread(target=teclado_escucha, args=(exit_event,))
    hilo_aspiradora = threading.Thread(target=aspirar)

    # Iniciar el hilo
    hilo_aspiradora.start()
    hilo_interaccion.start()

    # Esperar a que el hilo termine (no bloquea el hilo principal)
    hilo_interaccion.join()
    hilo_aspiradora.join()

    print("Programa principal finalizado")