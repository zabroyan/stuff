import pytest as pytest


def test_basic(utils, capsys):
    utils.parse_antlr_grammar('IF condition THEN conclusion;')

    captured = capsys.readouterr()
    assert 'no viable alternative' not in captured.err


@pytest.mark.parametrize('operator', ['<', '<=', '>', '>=', '==', '!='])
def test_comparators_numbers(utils, capsys, operator):
    result = utils.parse_antlr_grammar('IF condition {} 5 THEN conclusion;'.format(operator))

    captured = capsys.readouterr()
    assert 'no viable alternative' not in captured.err
    assert str(" ".join(str(result[0]).split())) == 'IF condition {} 5 THEN conclusion'.format(operator)


@pytest.mark.parametrize('operator', ['<', '<=', '>', '>=', '==', '!='])
def test_comparators_text(utils, capsys, operator):
    result = utils.parse_antlr_grammar('IF condition {} malo THEN conclusion;'.format(operator))

    captured = capsys.readouterr()
    assert 'no viable alternative' not in captured.err
    assert str(" ".join(str(result[0]).split())) == 'IF condition {} malo THEN conclusion'.format(operator)


@pytest.mark.parametrize('rule', [
    'IF condition 2 THEN conclusion;',
    'IF condition a THEN conclusion;',
    'IF condition 2 a THEN conclusion;',
    'IF condition 2 > 5 THEN conclusion;',
    'IF condition THEN conclusion 2;',
    'IF condition THEN conclusion a;',
    'IF condition THEN conclusion 2 a;',
])
def test_parameters(utils, capsys, rule):
    result = utils.parse_antlr_grammar(rule)

    captured = capsys.readouterr()
    assert 'no viable alternative' not in captured.err
    assert str(" ".join(str(result[0]).split())) == rule.replace(';', '')


@pytest.mark.parametrize('rule', [
    'IF condition AND condition THEN conclusion;',
    'IF condition OR condition THEN conclusion;',
    'IF condition AND condition THEN conclusion AND conclusion;',
])
def test_logical_operators(utils, capsys, rule):
    result = utils.parse_antlr_grammar(rule)

    captured = capsys.readouterr()
    assert 'no viable alternative' not in captured.err
    assert str(" ".join(str(result[0]).split())) == rule.replace(';', '')


@pytest.mark.parametrize('rule', [
    'IF (condition) THEN conclusion;',
    'IF (condition AND condition) THEN conclusion;',
    'IF (condition AND condition) OR condition THEN conclusion;',
    'IF (condition AND (condition)) OR condition THEN conclusion;',
    'IF (condition AND (condition OR condition)) OR condition THEN conclusion;',
])
def test_parenthesis(utils, capsys, rule):
    result = utils.parse_antlr_grammar(rule)

    captured = capsys.readouterr()
    assert 'no viable alternative' not in captured.err


@pytest.mark.parametrize('rule', [
    'IF condition THEN conclusion WITH 0.25;',
    'IF condition [0.25] THEN conclusion WITH 0.25;',
    'IF condition [0.25] AND condition [0.25] THEN conclusion WITH 0.25;',
])
def test_uncertainty_rule(utils, capsys, rule):
    result = utils.parse_antlr_grammar(rule)

    captured = capsys.readouterr()
    assert 'no viable alternative' not in captured.err
    assert str(" ".join(str(result[0]).split())) == rule.replace(';', '')


@pytest.mark.parametrize('rule', [
    'IF condition THEN conclusion',  # No semicolon on the end of rule
    'IF condition conclusion;',  # Missing THEN token
    'condition THEN conclusion;',  # Missing IF token
    'IF condition THEN conclusion WITH ;',  # Missing value for WITH token
    'IF condition [0.25 THEN conclusion ;',  # Missing R square bracket
    'IF condition 0.25 ] THEN conclusion ;',  # Missing L square bracket
    'IF condition  THEN conclusion OR conclusion;',  # OR operator in conclusion
    'IF condition < THEN conclusion;',  # Compare operator without identifier of number
    'IF condition THEN conclusion :=;',  # Assign operator without value
    'IF 05condition THEN conclusion;',  # Bad name of identifier (starting with number)
])
def test_bad_rules(utils, capsys, rule):
    utils.parse_antlr_grammar(rule)

    captured = capsys.readouterr()
    assert 'no viable alternative' in captured.err or 'expecting' in captured.err or 'missing' in captured.err
