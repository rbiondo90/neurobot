class Generation:
    # @classmethod
    # def from_json(cls, number):
    #     dir = cls.gen_dir_from_number(number)
    #     with open(os.path.join(dir,str(number) + ".json")) as file:
    #         data = json.load(file)
    #         individuals = [super.Individual]

    def __init__(self, number, individuals):
        self.number = number
        self.individuals = individuals
        self.current_individual = 0

    def advance(self):
        if not self.ended():
            print("Generazione %d - avviando l'individuo %d..." % (self.number, self.current_individual + 1))
            self.individuals[self.current_individual].live()
            self.current_individual += 1
        else:
            print("Generazione %d - non ci sono piu' individui da eseguire." % self.number)

    def execute(self):
        while not self.ended():
            self.advance()

    def get_best_n_individuals(self, n):
        self.individuals.sort(key=lambda individual: individual.fitness, reverse=True)
        return self.individuals[0:n]

    def ended(self):
        return self.current_individual == len(self.individuals)

