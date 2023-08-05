# pylint: disable=E1120
from mySweetCache import use_par, use_pars


def test_use_par():
    """
    Test basic usage use_par.
    """
    variable = 'Knights Who Say "Ni!"'

    @use_par(variable)
    def testing_fun(variable):
        return variable

    assert variable == testing_fun()
    variable = "Green Knight"
    assert variable != testing_fun()


def test_use_pars():
    """
    Test basic usage use_par.
    """
    variable0 = 'Knights Who Say "Ni!"'
    variable1 = "Green Knight"

    @use_pars(variable0, variable1)
    def testing_fun(variable0, variable1):
        return variable0 + variable1

    assert variable0 + variable1 == testing_fun()
    variable0 = "Wenn ist das Nunstuck git und slotermeyer?"
    variable1 = "Ja, beiherhund das Oder Die Flipperwald gerstuck."

    assert variable0 + variable1 != testing_fun()
