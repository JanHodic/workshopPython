import math

class PhysicsFormulae:

    def __init__(self, human, cave, step):
        self.human = human
        self.cave = cave
        self.gravity_acceleration = 9.81
        self.air_density = 1.25
        self.coefficient = 1.05

    def return_height(self, time, initial_velocity):
        return  initial_velocity * time - 0.5 * self.gravity_acceleration * time * time

    def return_break_force(self, velocity):
        return 0.5 * self.human.width * self.human.width * self.coefficient * velocity * velocity

    def return_initial_velocity_on_jump(self, jumps, initial_velocity):
        return self.cave.coeff ** jumps * initial_velocity

    def return_fall_velocity(self, time):
        return math.sqrt(self.gravity_acceleration / (0.5 * self.coefficient * self.human.width * self.human.width)) * (math.tanh(math.sqrt(self.gravity_acceleration * (0.5 * self.coefficient * self.human.width * self.human.width) / self.human.mass ** 2)) * time)

    def return_fall_position(self, initial_height, time):
        velocity = self.return_fall_velocity(time)
        return initial_height - 0.5 * (self.gravity_acceleration * self.human.mass - self.return_break_force(velocity)) * time * time
