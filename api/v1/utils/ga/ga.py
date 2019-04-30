from platypus.algorithms import NSGAIII
from platypus import Problem, Real
from recolector import Recolector
from lote import Lote


class GeneticAlgorithm():
    def __init__(self, rendimientos, pendientes, kgs):
        self.recolectores = list(map(lambda id_recolector: Recolector(
            rendimientos[id_recolector]), range(len(rendimientos))))
        self.lotes = list(map(lambda id_lote: Lote(
            kgs[id_lote], pendientes[id_lote]), range(len(pendientes))))
        self.problem = Problem(len(self.recolectores) *
                               len(pendientes), len(pendientes))
        self.problem.types[:] = Real(0, 40)
        self.problem.function = self.schaffer
        self.solutions = []
        self.algorithm = NSGAIII(self.problem, 12)

    def run(self):
        self.algorithm.run(10000)

    def get_solutions(self):
        return list(filter(lambda solution: solution.feasible, self.algorithm.result))

    def schaffer(self, x):
        functions = []
        num_lote = 0

        for lote in range(len(self.lotes)):
            recolectado = 0
            for recolector in range(num_lote, len(self.recolectores) + num_lote):
                recolectado += x[recolector] * \
                    self.recolectores[recolector - num_lote].get_rendimiento()

            functions.append(
                abs(self.lotes[num_lote // len(self.recolectores)].get_kg() - recolectado))
            num_lote += len(self.recolectores)

        return functions


ga = GeneticAlgorithm([21.32, 25.04, 10.56], [1, 2, 1], [7000, 4000, 3000])
ga.run()
print(ga.get_solutions())
