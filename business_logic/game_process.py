import math_operations
from math_operations.models.human import Human
from math_operations.models.world import World
from math_operations.physics_formulae import PhysicsFormulae


class GameProcess:
    def __init__(self, human:Human, world:World, time_step:float):
        self.human:Human = human
        self.world:World = world
        self.collision = False
        self.time_step = time_step

    ### Privatni metoda pro urceni zda nastala kolize
    def __is_collision(self):
        for o in self.world.obstacles:
            if self.human.center_X + self.human.width / 2 - o.centerX - o.width / 2 < 0 or self.human.center_Y + self.human.height / 2 - o.centerY - o.height / 2 < 0:
                self.collision = True
            else:
                self.collision = False

    ### Pridani nebo odebrani rychlosti pri vodorovne zmene
    def change_velocity(self, change_velocity):
        self.human.velocity_X += change_velocity

    ### Pohyb za kazdou elementarni jednotku casu vodorovne, pravidelne se updatuje s kazdym zobrazenim
    def moving(self):
        self.human.center_X += self.human.velocity_X * self.time_step
        self.__is_collision()

    ###Vyskok. Pri vyskoku se pro dany cas zacne provadet funkce jump, dokud hrac nesestoupi na uroven zeme kdy se zastavi
    def jump(self, jump_velocity: float):
        self.human.velocity_Y += jump_velocity
        self.flying(jump_velocity)

    ###Pohyb svisle. Provadi se neustale v kazdem kroku zobrazeni od spusteni, dokud hrac neprotne zem
    def flying(self, initial_velocity:float):
        self.human.center_Y += PhysicsFormulae.return_height(initial_velocity=initial_velocity, time=self.time_step)
        self.__is_collision()
        if self.human.center_Y < 0:
            self.human.velocity_Y = 0

