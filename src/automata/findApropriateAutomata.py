from typing import Callable
from automata.ArithmeticOperatorAutomata import ArithmeticOperatorAutomata
from automata.CommentAutomata import CommentAutomata
from automata.DelimiterAutomata import DelimiterAutomata
from automata.ErrorAutomata import ErrorAutomata
from automata.IdentifierAutomata import IdendifierAutomata
from automata.LogicalOperatorAutomata import LogicalOperatorAutomata
from automata.NumbertAutomata import NumbertAutomata
from automata.RelationalOperatorAutomata import RelationalOperatorAutomata
from automata.StringAutomata import StringAutomata


Automata = Callable[[str, str], str];

def findApropriateAutomata(state: str) -> Automata:
    if ('Identifier' in state):
        return IdendifierAutomata;
    elif ('Delimiter' in state):
        return DelimiterAutomata;
    elif ('String' in state):
        return StringAutomata;
    elif ('Comment' in state):
        return CommentAutomata;
    elif ('Logical' in state):
        return LogicalOperatorAutomata;
    elif ('Relational' in state):
        return RelationalOperatorAutomata;
    elif ('Arithmetic' in state):
        return ArithmeticOperatorAutomata;
    elif ('Number' in state):
        return NumbertAutomata;
    return ErrorAutomata;
