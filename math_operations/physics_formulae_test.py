import unittest
import math_operations

from physics_formulae import PhysicsFormulae  # nahraď skutečným názvem modulu


class DummyHuman:
    def __init__(self, width, mass):
        self.width = width
        self.mass = mass


class DummyCave:
    def __init__(self, coeff):
        self.coeff = coeff


class physics_formulae_test(unittest.TestCase):

    def setUp(self):
        self.human = DummyHuman(width=0.5, mass=70)
        self.cave = DummyCave(coeff=0.9)
        self.physics = PhysicsFormulae(self.human, self.cave, step=0.1)

    def test_return_height(self):
        h = self.physics.return_height(time=2, initial_velocity=20)
        expected = 20 * 2 - 0.5 * 9.81 * 2 * 2
        self.assertAlmostEqual(h, expected, places=5)

    def test_return_break_force(self):
        velocity = 10
        expected = 0.5 * self.human.width ** 2 * self.physics.coefficient * velocity ** 2
        self.assertAlmostEqual(self.physics.return_break_force(velocity), expected, places=5)

    def test_return_initial_velocity_on_jump(self):
        v0 = 5
        jumps = 2
        expected = (self.cave.coeff ** jumps) * v0
        self.assertEqual(self.physics.return_initial_velocity_on_jump(jumps, v0), expected)

    def test_initial_velocity_after_jumps_with_damping(self):
        cave = DummyCave(coeff=0.5)
        human = DummyHuman(width=0.5, mass=70)
        physics = PhysicsFormulae(human, cave, step=0.1)

        initial_velocity = 10.0
        jumps = 3

        # Při každém odrazu se rychlost násobí 0.5 → (0.5^3) * 10 = 0.125 * 10 = 1.25
        expected_velocity = (0.5 ** 3) * initial_velocity
        actual_velocity = physics.return_initial_velocity_on_jump(jumps, initial_velocity)

        self.assertAlmostEqual(actual_velocity, expected_velocity, places=5)

    def test_return_fall_position(self):
        initial_height = 100
        time = 1
        pos = self.physics.return_fall_position(initial_height, time)
        self.assertTrue(pos < initial_height)

if __name__ == '__main__':
    unittest.main()
