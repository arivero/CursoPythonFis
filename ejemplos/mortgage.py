"""este es un ejemplo para calcular una hipoteca subvencionada via IRPF
   -las modificaciones a la cuota son locales, por tanto
   -hay que tener una temperatura no nula para que se pueda trasladar el efecto de pagar al principio
    y recortar cuota del final. Es una no localidad de hasta treinta años!
    """

    
import random
import matplotlib.pyplot as plt
import math
 
# Función para calcular el pago mensual de una hipoteca a interés fijo. Lo que dice chatGPT...
def calculate_monthly_payment(loan_amount, interest_rate, loan_term):
  monthly_payment = loan_amount * (interest_rate / 12) / (1 - (1 + interest_rate / 12) ** (-loan_term))
  return monthly_payment
 

def pagoDesgravado(pago):
  return pago * 0.85 if pago < 753.33 else pago - 113
   

# Función para minimizar la suma total de pagos. Colaboracion con copilot...
def propose_total_payments(T):
  # Selecciona al azar un mes y modifica ligeramente al azar el pago de ese mes
  random_month = random.randint(0, loan_term + 498)
  pagoActual = payments[random_month]
  #estp se va a rechazar casi siempre, el maximo deberia ser el que no produzca un segundo pago negativo
  #nuevoPago= random.uniform( 0, balance[random_month] * (1 + interest_rate / 12) )

  #si el segundo pago es cero, tendriamos que balance[random_month+2] = balance[random_month+1] * (1 + interest_rate / 12),
  #y por tanto este es el maximo balance que podemos amortizar. Dado que
  #balance[random_month+1] = balance[random_month] * (1 + interest_rate / 12) - payments[random_month]
  #el maximo payments[random_month] es:
  nuevoPago= random.uniform( 0, balance[random_month] * (1 + interest_rate / 12) - balance[random_month+2] / (1+ interest_rate/12) )
  #if nuevoPago > balance[random_month] * (1 + interest_rate / 12):
  #  nuevoPago = balance[random_month] * (1 + interest_rate / 12)
  # Calcula el pago del mes siguiente para mantener el balance inalterado
  balanceTrasPago = balance[random_month] * (1 + interest_rate / 12) - nuevoPago
  segundoPago = balanceTrasPago * (1 + interest_rate / 12) - balance[random_month+2]
  costeViejo = pagoDesgravado(payments[random_month]) + pagoDesgravado(payments[random_month+1])
  costeNuevo = pagoDesgravado(nuevoPago) + pagoDesgravado(segundoPago)
  #if segundoPago > 0 and random.random() < math.exp((costeViejo-costeNuevo)/T):
  if segundoPago > 0 and math.log(random.random()) < (costeViejo-costeNuevo)/T:
    #note that if diff is negative, we accept the new value, and if diff is positive, we accept it with probability $e^{-\frac{costeViejo-costeNuevo}{T}}$:
    payments[random_month] = nuevoPago
    payments[random_month+1] = segundoPago
    balance[random_month+1] = balanceTrasPago
    #balance[random_month+2] = balanceAEstablecer
    coste[random_month] = pagoDesgravado(nuevoPago)
    coste[random_month+1] = pagoDesgravado(segundoPago)
  # Devuelve el coste total de la hipoteca
  return sum(coste)

# Parámetros de la hipoteca
loan_amount = 80000
interest_rate = 0.040278
loan_term = int(12*4)
temperature = 10.0


  # Crea una lista con los pagos mensuales
payments = [calculate_monthly_payment(loan_amount, interest_rate, loan_term)] * loan_term + [0.0]*500

coste = [ pagoDesgravado(pago) for pago in payments ]

balance=[]
balance.append(loan_amount)
for i in range(loan_term+500):
        balance.append(balance[i] * (1 + interest_rate / 12) - payments[i])
        #print(payments[i], balance[i], balance[i+1])
# Ejecuta el código de Monte Carlo
num_iterations = 250000000000
min_payment = float("inf")
for i in range(num_iterations):
  total_payment = propose_total_payments(temperature) #T = 133
  if total_payment < min_payment:
    #print("Nuevo mínimo: " + str(total_payment))
    min_payment = total_payment
    mejorPagos = payments.copy()
    mejorCoste = coste.copy()
    mejorBalance = balance.copy()
    #print(mejorPagos[0:10])
  if i % 10000000 == 0:
     print(str(i) + "T=" + str(temperature) + " mejorCoste "+ str(min_payment)+ " Coste: " + str(total_payment), coste[0:10])
     temperature = temperature*0.95
     continue
     #plot it too:
     plt.yscale('log')
     plt.plot(payments)
     plt.plot(mejorPagos)
     #plt.plot(balance)
     plt.show()
