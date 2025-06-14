import math
import constants

class PhysicsFormulae:

    def __init__(self, human, cave):
        self.human = human
        self.cave = cave

    @staticmethod
    def return_height(time, initial_velocity):
        return  initial_velocity * time - 0.5 * constants.GRAVITY_ACCELERATION * time * time

    def return_break_force(self, velocity):
        return 0.5 * self.human.width * self.human.width * constants.COEFFICIENT * velocity * velocity

    def return_initial_velocity_on_jump(self, jumps, initial_velocity):
        return self.cave.coeff ** jumps * initial_velocity

    def return_fall_velocity(self,time):
        return math.sqrt(constants.GRAVITY_ACCELERATION / (0.5 * constants.COEFFICIENT * self.human.width * self.human.width)) * (math.tanh(math.sqrt(constants.GRAVITY_ACCELERATION * (0.5 * constants.COEFFICIENT * self.human.width * self.human.width) / self.human.mass ** 2)) * time)

    def return_fall_position(self, initial_height, time):
        velocity = self.return_fall_velocity(time)
        return initial_height - 0.5 * (constants.GRAVITY_ACCELERATION * self.human.mass - self.return_break_force(velocity)) * time * time
