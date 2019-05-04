from platypus.algorithms import NSGAIII
from platypus import Problem, Real
from .recolector import Recolector
from .lote import Lote
import random
import decimal


class GeneticAlgorithm():
    def __init__(self, rendimientos, pendientes, kgs):
        self.range_rendimientos = [[333, 1111], [1122, 2777], [2788, 4000]]
        self.recolectores = list(map(lambda id_recolector: Recolector(
            float(decimal.Decimal(random.randrange(self.range_rendimientos[rendimientos[id_recolector]][0], self.range_rendimientos[rendimientos[id_recolector]][1])) / 100)), range(len(rendimientos))))
        self.lotes = list(map(lambda id_lote: Lote(
            kgs[id_lote], pendientes[id_lote]), range(len(pendientes))))
        self.problem = Problem(len(self.recolectores) *
                               len(pendientes), len(self.lotes), len(rendimientos)*2)
        self.problem.types[:] = Real(0, 40)
        self.problem.function = self.schaffer
        for rule in range(len(rendimientos)*2):
            if rule % 2 == 0:
                self.problem.constraints[rule] = ">=40"
            else:
                self.problem.constraints[rule] = "<=45"

        self.solutions = []
        self.algorithm = NSGAIII(self.problem, 2, 1)
        self.change_rendimientos_per_pendiente = [3.4, 0, -2.25]

    def run(self):
        self.algorithm.run(10000)

    def get_solutions(self):
        return list(filter(lambda solution: solution.feasible, self.algorithm.result))

    def get_solution_for_humans(self):
        hours_per_recolector = []
        solutions = self.get_solutions()
        for solution in solutions:
            print(solution)

        best_solution = solutions[-1]
        hours = []
        num_lote = 1
        for num_recolector in range(len(self.recolectores)):
            for index_hours in range(num_recolector, len(best_solution.variables), len(self.recolectores)):
                hours.append({
                    'name': f'lote_{num_lote}',
                    'hours': int(best_solution.variables[index_hours])
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
        functions = []
        rules = []
        num_lote = 0
        num_recolector = 0
        for rule in range(len(self.recolectores)):
            hours = 0
            for recolector in range(num_recolector, len(self.recolectores) * len(self.lotes), len(self.recolectores)):
                hours += x[recolector]
            num_recolector += 1
            rules.append(hours)
            rules.append(hours)

        for lote in range(len(self.lotes)):
            recolectado = 0
            for recolector in range(num_lote, len(self.recolectores) + num_lote):
                recolectado += x[recolector] * \
                    (self.recolectores[recolector - num_lote].get_rendimiento() + (
                        self.change_rendimientos_per_pendiente[self.lotes[num_lote // len(self.recolectores)].get_pendiente()]))
            functions.append(recolectado)
            num_lote += len(self.recolectores)

        return functions, rules

