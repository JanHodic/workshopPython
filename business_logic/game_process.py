import math_operations
from math_operations.models.human import Human
from math_operations.models.world import World
from math_operations.physics_formulae import PhysicsFormulae
from math_operations.physics_formulae_test import physics_formulae_test


class GameProcess:
    def __init__(self, human, world):
        self.human:Human = human
        self.world:World = world
        self.collision = False

    ### Privatni metoda pro urceni zda nastala kolize
    def _is_collision(self):
        for o in self.world.obstacles:
            if self.human.center_X + self.human.width / 2 - o.centerX - o.width / 2 < 0 or self.human.center_Y + self.human.height / 2 - o.centerY - o.height / 2 < 0:
                self.collision = True
            else:
                self.collision = False

    ### Pridani nebo odebrani rychlosti
    def change_velocity(self, change_velocity):
        self.human.velocity_X += change_velocity

    ### Pohyb za kazdou elementarni jednotku casu vodorovne
    def moving(self):
        self.human.center_X += self.human.velocity_X * 0.001
        self._is_collision()

    ###Vyskok
    def jump(self, jump_velocity):
        self.human.velocity_Y += jump_velocity

    ###Pohyb svisle
    def flying(self, time, initial_velocity):
        self.human.velocity_Y += PhysicsFormulae.return_height(self.human,initial_velocity=initial_velocity, time=time)

