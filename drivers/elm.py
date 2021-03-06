from pytocl.driver import Driver
from pytocl.car import State, Command

from config import *
from utils.data import *
from disciples.elm import ExtremeLearningMachine


class ELMDriver(Driver):

    def __init__(self, model_path):
        super().__init__()
        self.epoch = 0
        self.jesus = ExtremeLearningMachine()
        self.jesus.restore(model_path)

    def calc_gear(self, command, carstate):
        acceleration = command.accelerator
        if acceleration > 0:
            if carstate.rpm > 8000:
                command.gear = carstate.gear + 1
        if carstate.rpm < 2500 and carstate.gear != 0:
            command.gear = carstate.gear - 1
        if not command.gear:
            command.gear = carstate.gear or 1

    def drive(self, carstate: State) -> Command:
        command = Command()
        current_state = state_to_vector(carstate)
        command_vector = self.jesus.take_wheel(current_state)
        command = vector_to_command(command_vector)
        self.calc_gear(command, carstate)
        if self.epoch%100 == 0:
            print(command_vector)
        self.epoch += 1
        return command
