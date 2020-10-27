from typing import List

from ExpertSystem.Business.UserFramework import IInference, ActionBaseCaller
from ExpertSystem.Structure.Enums import LogicalOperator, Operator
from ExpertSystem.Structure.RuleBase import Rule, Fact, ExpressionNode, Expression


class Inference(IInference):
    """
    | User definition of the inference. You can define here you interference method (forward or backward).
      You can have here as many functions as you want, but you must implement interfere with same signature

    |
    | `def interfere(self, knowledge_base: List[Fact], rules: List[Rule], action_base: ActionBase):`
    |

    | Method `interfere` will be called each turn or manually with `Interference` button.
    | Class have no class parameters, you can use only interference parameters

    """

    knowledge_base: List[Fact]
    action_base: ActionBaseCaller

    spawn_distance = {
        "closest": {'a': 0, 'b': 0, 'c': 3.5, 'd': 4},
        "close": {'a': 3, 'b': 4, 'c': 5, 'd': 6},
        "medium": {'a': 5, 'b': 6, 'c': 7, 'd': 8},
        "far": {'a': 7, 'b': 8, 'c': 16, 'd': 16}
    }

    fuzzy_sets = {'lives', 'enemy_distance'}
    defuzz = dict()

    def infere(self, knowledge_base: List[Fact], rules: List[Rule], action_base: ActionBaseCaller, fuzzification=True) -> None:
        """
        User defined interference

        :param fuzzification:
        :param knowledge_base: - list of Fact classes defined in  KnowledgeBase.create_knowledge_base()
        :param rules:  - list of rules trees defined in rules file. def __init__(self):
        self.knowledge_base = None
        self.action_base = None
        :param action_base: - instance of user action base for executing conclusions

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!    TODO: Write implementation of your inference mechanism definition HERE    !!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        fuzzy_rules = {}
        self.knowledge_base = knowledge_base
        self.action_base = action_base
        do_fuzzification = False
        for rule in rules:
            condition, fz = self.rule_evaluation(rule.condition)
            # print(rule, fz)
            if fz is not None and fz > 0 and fuzzification is True:
                self.defuzz[rule.conclusion.value.args[0]] = fz
                fuzzy_rules[rule.conclusion.value.name]= rule
                do_fuzzification = True
                continue
            if condition:
                if rule.conclusion.value is not None and rule.conclusion.value in self.action_base:
                    self.conclusion_evaluation(rule.conclusion)
                else:
                    conclusion = self.rule_concl(rule.conclusion)
                    for c in conclusion:
                        if c in self.action_base:
                            self.conclusion_evaluation(c)
        if do_fuzzification:
            result = self.defuzzification()
            # print(fuzzy_rules)
            for r in fuzzy_rules:
                fuzzy_rules[r].conclusion.value.args[0] = str(result)
            f_rules = fuzzy_rules.values()
            self.infere(knowledge_base, f_rules, action_base, False)
            self.defuzz.clear()

    def defuzzification(self):
        mu = {}
        for i in range(17):
            for x in self.spawn_distance:
                a = self.spawn_distance[x]['a']
                b = self.spawn_distance[x]['b']
                c = self.spawn_distance[x]['c']
                d = self.spawn_distance[x]['d']
                if a < i < d and x in self.defuzz:
                    if a < i < b:
                        res = (i - a) / (b - a)
                        mu[i] = (max(res, self.defuzz[x]))
                    elif b <= i <= c:
                        mu[i] = (self.defuzz[x])
                    elif c < i <= d:
                        res = (d - i) / (d - c)
                        mu[i] = (max(res, self.defuzz[x]))
                    continue
        result = 0
        # print(self.defuzz)
        # print("mu = ", mu)
        for i in mu:
            result += i * mu[i]
        result /= sum(mu.values())
        return result

    def rule_concl(self, root_node: ExpressionNode):
        if root_node.value is not None:
            return root_node.value
        else:
            return self.rule_concl(root_node.left), self.rule_concl(root_node.right)

    def rule_evaluation(self, root_node: ExpressionNode):
        """
        Example of rule tree evaluation. This implementation did not check comparision operators and uncertainty.
        For usage in interference extend this function

        :param root_node: root node of the rule tree
        :return: True if rules is satisfiable, False in case of not satisfiable or missing Facts
        """

        if root_node.operator == LogicalOperator.AND:
            res1, fz1 = self.rule_evaluation(root_node.left)
            res2, fz2 = self.rule_evaluation(root_node.right)
            res = res1 and res2
            fz = None
            if fz1 is not None and fz2 is not None:
                fz = min(fz1, fz2)
            elif fz1 is not None:
                fz = fz1
            elif fz2 is not None:
                fz = fz2
            return res, fz


        elif root_node.operator == LogicalOperator.OR:
            res1, fz1 = self.rule_evaluation(root_node.left)
            res2, fz2 = self.rule_evaluation(root_node.right)
            res = res1 or res2
            fz = None
            if fz1 is not None and fz2 is not None:
                fz = max(fz1, fz2)
            elif fz1 is not None:
                fz = fz1
            elif fz2 is not None:
                fz = fz2
            return res, fz

        elif isinstance(root_node.value, Expression):
            if root_node.value.comparator == Operator.LESS_THEN:
                return self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) < int(root_node.value.value), None
            elif root_node.value.comparator == Operator.EQUAL:
                return self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) == int(root_node.value.value), None
            elif root_node.value.comparator == Operator.LESS_EQUAL:
                return self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) <= int(root_node.value.value), None
            elif root_node.value.comparator == Operator.MORE_EQUAL:
                return self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) >= int(root_node.value.value), None
            elif root_node.value.comparator == Operator.MORE_THEN:
                return self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) > int(root_node.value.value), None
            try:
                if root_node.value.name in self.fuzzy_sets:
                    res = self.knowledge_base[self.knowledge_base.index(root_node.value.name)](*root_node.value.args)
                    # self.defuzz[root_node.value.args.pop()] = res
                    return res, res
                return self.knowledge_base[self.knowledge_base.index(root_node.value.name)](*root_node.value.args), None
            except ValueError:
                return False, None

        else:
            return bool(root_node.value), None

    def conclusion_evaluation(self, root_node: ExpressionNode):
        if self.action_base.has_method(root_node.value):
            self.action_base.call(root_node.value)
