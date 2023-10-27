from datetime import datetime
import numpy as np, pandas as pd
from random import randint, sample
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto import Random

def encriptar(message):
    iv = Random.new().read(AES.block_size)
    key = input("La llave es: ")
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    ciphertext = iv+cipher.encrypt(padded_message)
    encriptado= ciphertext.hex().upper()
    return ' '.join([encriptado[i:i + 4] for i in range(0, 64, 4)])
    
class Bloque:
    def __init__(self, índice, saldos, código_previo):
        self.índice = índice
        self.saldos = saldos
        self.código_previo = código_previo
        self.código = None
        self.transacciones = pd.DataFrame(columns=['Fecha', 'De','Para', 'Cantidad'])
        self.fecha_hora = datetime.now()

    def encriptar_bloque(self):
        datos = ['índice', 'saldos', 'código_previo','transacciones', 'fecha_hora']
        contenido = ''.join(str(getattr(self,campo)) for campo in datos)
        self.código = encriptar(contenido)

    def actualizar_transacciones(self, de, para, cantidad):
        T = self.transacciones.shape[0]
        self.transacciones.loc[T] = [datetime.now(), de, para, cantidad]
        
class BlockChain(list):
    def __init__(self):
        saldo_original = pd.Series([0], index=['Banco Central'])
        bloque_original = Bloque(0, saldo_original, None)
        self.append(bloque_original)

    @property
    def bloque_actual(self):
        return self[-1]

    @property
    def saldos(self):
        return self.bloque_actual.saldos

    @property
    def transacciones(self):
        return pd.concat([bloque.transacciones for bloque in self],
        keys=[f'Bloque{k}' for k in range(len(self))])

    def emitir_Cocoins(self, cantidad):
        if cantidad < -self.bloque_actual.saldos['Banco Central']:
            print("No pueden destruirse más Cocoins que los que posee el Banco Central")
        else:
            self.bloque_actual.saldos['Banco Central'] += cantidad
            self.bloque_actual.actualizar_transacciones('Imprimiendo nuevos Cocoins', 'Banco Central', cantidad)

    def pagar(self, cuenta_origen, cuenta_destino, cantidad):
        cb = self.bloque_actual
        if cantidad < 0:
            print("El monto del pago no puede ser negativo.")
        elif cb.saldos[cuenta_origen] < cantidad:
            print(f"La cuenta {cuenta_origen} no tiene fondos suficientes!")
        else:
            if cuenta_destino not in cb.saldos.keys():
                cb.saldos[cuenta_destino] = 0
            cb.saldos[cuenta_origen] -= cantidad
            cb.saldos[cuenta_destino] += cantidad

            cb.actualizar_transacciones(cuenta_origen, cuenta_destino, cantidad)
            msg = '%12s le pagó %6.2f Cocoins a %s.'
            print(msg % (cuenta_origen, cantidad, cuenta_destino))
    
    def crear_siguiente_bloque(self):
        cb = self.bloque_actual
        cb.encriptar_bloque()
        self.append(Bloque(cb.índice + 1, cb.saldos.copy(), cb.código))
        
    def verificar_integridad(self):
        anterior = self.bloque_actual.código_previo
        for bloque in self[-2::-1]:
            print(f'\nVerificando bloque{bloque.índice}', anterior, sep='\n')
            bloque.encriptar_bloque()
            print(bloque.código)
        
            if bloque.código != anterior:
                print('ADVERTENCIA: LA CADENA DE BLOQUES FUE ADULTERADA EN EL BLOQUE %d!!!' % bloque.índice)
                return
            else:
                anterior = bloque.código_previo
        
        print('LA CADENA DE BLOQUES ESTÁ BIEN!')
        
    def nuevo_desafio(self, p):
        code = randint(0,10**p - 1)
        self.desafio = encriptar(str(code))
        print(f'\nNuevo desafío (dificultad = {p}): {self.desafio}')
        
    def verificar_solucion(self, propuesta, proponente):
        if encriptar(str(propuesta)) == self.desafio:
            COCOIN.emitir_Cocoins(20)
            self.pagar('Banco Central', proponente, 20)
            self.crear_siguiente_bloque()
            self.nuevo_desafio(p)
            
            
#cambio manual de las cuentas            
COCOIN = BlockChain()
COCOIN.emitir_Cocoins(5000)
print(COCOIN.saldos)

for nombre in ['Ana', 'Beto', 'Carlos', 'Diana']:
    COCOIN.pagar('Banco Central', nombre, 600)
print(COCOIN.saldos)
print(COCOIN.transacciones)

np.random.seed(2019)
NUMERO_DE_BLOQUES = 5

for i in range(0, NUMERO_DE_BLOQUES):
    COCOIN.crear_siguiente_bloque()
    print('\n', '='*60)
    print(f"El código del bloque {COCOIN[-2].índice} es:\n{COCOIN[-2].código}")
    print(f"El bloque #{COCOIN.bloque_actual.índice} ha sido agregado a la cadena del Cocoin!")

    NÚMERO_DE_PAGOS = np.random.randint(2,12)

    for k in range(NÚMERO_DE_PAGOS):
        DE, PARA = sample(list(COCOIN.saldos.index), 2)
        CANTIDAD = 10 * np.random.randint(1, 12)
        COCOIN.pagar(DE, PARA, CANTIDAD)
print(COCOIN.saldos)
print(COCOIN.transacciones)
COCOIN.verificar_integridad()

COCOIN[3].saldos['LADRON'] = 900
print(COCOIN[3].saldos)

COCOIN.verificar_integridad()

#Minado bitcoins
p = 4
COCOIN.nuevo_desafio(p)

def adivinar(p, nombre):
    for numero in range(10**p):
        codigo = encriptar(str(numero))
        if codigo == COCOIN.desafio:
            print(f'{nombre} adivinó {numero}')
            COCOIN.verificar_solucion(numero, nombre)
            break
        
adivinar(p, 'Ana')