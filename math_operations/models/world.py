from typing import List

from business_logic.obstacle import Obstacle

class World:

    def __init__(self, elasticity_coeff, ground, velocity):
        self.elasticity_coeff = elasticity_coeff
        self.ground = ground
        self.velocity = velocity
        self.obstacles:List[Obstacle] = []

    #def create_world(self):
