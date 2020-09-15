from typing import Union


class PlayerResources:
    """ Structure that hold information about player resources """


    def __init__(self, resources: int, income: int, income_increase=0):
        self.__resources = resources
        self.__income = income
        self.__income_increase = income_increase


    def add_resources(self, amount: int) -> None:
        """ Add amount of resources """
        self.__resources += amount


    def remove_resources(self, amount: int) -> None:
        """ Remove amount of resources """
        self.__resources -= amount


    @property
    def resources(self) -> int:
        return self.__resources


    @property
    def income(self) -> int:
        return self.__income


    @property
    def income_increase(self) -> Union[int, float]:
        return self.__income_increase


    def increase_income(self, value: int) -> None:
        self.__income += value
