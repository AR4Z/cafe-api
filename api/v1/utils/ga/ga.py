from platypus.algorithms import NSGAIII
from platypus import Problem, Real
from .recolector import Recolector
from .lote import Lote
import random
import decimal


class GeneticAlgorithm():
    def __init__(self, rendimientos, pendientes, kgs):
        """
            Se encarga de crear los recolectores y los lotes para ejecutar el algoritmo.
            Primero, en self.recolectores creamos una lista de recolectores donde como atributos tenemos el rendimiento de ese recolector
            que es tomado al azar de self.range_rendimientos de la siguiente forma

            rendimiento bajo  -> 0 : [333, 1111]
            rendimiento medio -> 1 : [1122, 2777]
            rendimiento alto  -> 2 : [2788, 4000]

            dando el rendimiento obtenermos la cota inferior y superior de rendimiento y de ahí con random.randrange obtenermos un número al azar
            que es convertido a decimal.

            La lista de lotes self.lotes se encarga de almacenar los lotes cada lote tiene como atributo su pendiente y la cantidad de café en kilogramos
            a ser recolectados.

            En self.problem creamos el problema que tiene como atributos:
            1. El número de variables: éste número esta dado por el producto de la cantiad de recolectores y de lotes
            2. El número de objetivos: éste esta dado por el número de lotes
            3. La cantidad de reglas: éste es el doble del número de recolectores

            Luego, definimos que vamos a trabajar con número Reales en el intervalo cerrado[0, 40].
            éste número representa la cantidad de horas que un determinado recolector le va a dedicar a un determinado lote

            Luego, pasamos las funciones objetivo y reglas a optimizar que han sido encapsuladas en el metodo self.schaffer.
            El siguiente paso será definir las reglas, deben ser >= 40 y <= 45.
            Finalmente creamos el algoritmo a donde enviamos y almacenamos como cambian los rendimientos según la pendiente

            0 -> 20 - 100 % : aumeto en 3.4 el rendimiento de cada recolector
            1 -> 101 - 200 % : no aumenta el rendimiento de cada recolector
            2 -> mayor a 200% : Disminuye en 2.5 el rendimiento de cada recolector


        """
        self.range_rendimientos = [[333, 1111], [1122, 2777], [2788, 4000]]
        self.recolectores = list(map(lambda id_recolector: Recolector(
            float(decimal.Decimal(random.randrange(self.range_rendimientos[rendimientos[id_recolector]][0], self.range_rendimientos[rendimientos[id_recolector]][1])) / 100)), range(len(rendimientos))))
        self.lotes = list(map(lambda id_lote: Lote(
            kgs[id_lote], pendientes[id_lote]), range(len(pendientes))))
        self.problem = Problem(len(self.recolectores) *
                               len(pendientes), len(self.lotes), len(rendimientos)*2)
        self.problem.types[:] = Real(0, 40)
        self.problem.function = self.schaffer
        for rule in range(len(rendimientos) * 2):
            if rule % 2 == 0:
                self.problem.constraints[rule] = ">=40"
            else:
                self.problem.constraints[rule] = "<=45"

        self.solutions = []
        self.algorithm = NSGAIII(self.problem, 2, 1)
        self.change_rendimientos_per_pendiente = [3.4, 0, -2.25]

    def run(self):
        """
            Arrancará el algoritmo hasta la n=10000 iteración
        """
        self.algorithm.run(10000)

    def get_solutions(self):
        """
            Devuelve las soluciones que sean factibles del resultado devuelto por el algoritmo.
        """
        return list(filter(lambda solution: solution.feasible, self.algorithm.result))

    def get_solution_for_humans(self):
        """
            Se encarga de "decodificar" la mejor solución.
            Toma el vector solución ejemplo:

            [26, 21, 0, 2, 3, 24, 12, 15, 16]

                            Lote1  Lote2 Lote3
            Recolector 1 ->  26     2     12
            Recolector 2 ->  21     3     15
            Recolector 3 ->   0     24    16

        """
        hours_per_recolector = []
        solutions = self.get_solutions()
        for solution in solutions:
            print(solution)
        try:
            best_solution = solutions[-1]
        except IndexError as _:
            return 'No hemos encontrado una asignación óptima, revisa el número de recolectores y las características de los lotes.'
        
        hours = []
        num_lote = 1
        for num_recolector in range(len(self.recolectores)):
            for index_hours in range(num_recolector, len(best_solution.variables), len(self.recolectores)):
                hours.append({
                    'name': f'lote_{num_lote}',
                    'hours': int(best_solution.variables[index_hours]),
                    'cafe': int(best_solution.variables[index_hours]) * self.recolectores[num_recolector].get_rendimiento()
                })
                num_lote += 1
            num_lote = 1
            hours_per_recolector.append({
                'name': f'Recolector {num_recolector+1}',
                'lotes': hours
            })
            hours = []

        return hours_per_recolector

    def schaffer(self, x):
        """
            Se definen las funciones objetivo y las reglas

            Funciones objetivo:
            minimizar la sumatoria del producto del rendimiento de un recolector por las horas (x_1, x_2, ..., x_r)
            por cada uno de los lotes.
            Por ejemplo:
            Número de lotes: 3
            Número de recolectores 3
            [26, 21, 0, 2, 3, 24, 12, 15, 16]
            Lote1: min(26 * r1 + 21 * r2 + 0 * r3)
            Lote2: min(2 * r1 + 3 * r2 + 24 * r3)
            Lote3: min(12 * r1 + 15* r2 + 16 * r3)

            Reglas:
            Por cada recolector se define una regla. La sumatoria de las horas de este recolector a trabajar en todos los lotes debe ser
            40 <= h_1 + h_2 + h_3 + ... h_l <= 45

        """
        functions = []
        rules = []
        num_lote = 0
        num_recolector = 0
        for _ in range(len(self.recolectores)):
            hours = 0
            for recolector in range(num_recolector, len(self.recolectores) * len(self.lotes), len(self.recolectores)):
                hours += x[recolector]
            num_recolector += 1
            rules.append(hours)
            rules.append(hours)

        for _ in range(len(self.lotes)):
            recolectado = 0
            for recolector in range(num_lote, len(self.recolectores) + num_lote):
                recolectado += x[recolector] * \
                    (self.recolectores[recolector - num_lote].get_rendimiento() + (
                        self.change_rendimientos_per_pendiente[self.lotes[num_lote // len(self.recolectores)].get_pendiente()]))
            functions.append(recolectado)
            num_lote += len(self.recolectores)

        return functions, rules

