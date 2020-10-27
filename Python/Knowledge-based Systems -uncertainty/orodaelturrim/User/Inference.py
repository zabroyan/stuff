from typing import List
from random import randrange

from ExpertSystem.Business.UserFramework import IInference, ActionBaseCaller
from ExpertSystem.Structure.Enums import LogicalOperator, Operator
from ExpertSystem.Structure.RuleBase import Rule, Fact, ExpressionNode, Expression


class Inference(IInference):
    """
    | User definition of the inference. You can define here you inference method (forward or backward).
      You can have here as many functions as you want, but you must implement interfere with same signature

    |
    | `def interfere(self, knowledge_base: List[Fact], rules: List[Rule], action_base: ActionBase):`
    |

    | Method `interfere` will be called each turn or manually with `Inference` button.
    | Class have no class parameters, you can use only inference parameters

    """
    knowledge_base: List[Fact]
    action_base: ActionBaseCaller

    def infere(self, knowledge_base: List[Fact], rules: List[Rule], action_base: ActionBaseCaller) -> None:
        """
        User defined inference

        :param knowledge_base: - list of Fact classes defined in  KnowledgeBase.create_knowledge_base()
        :param rules:  - list of rules trees defined in rules file.
        :param action_base: - instance of ActionBaseCaller for executing conclusions

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!    TODO: Write implementation of your inference mechanism definition HERE    !!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        self.knowledge_base = knowledge_base
        self.action_base = action_base
        uncert_rules = dict()
        for rule in rules:
            condition, uncertainty = self.rule_evaluation(rule.condition)
            if condition:
                if rule.conclusion.value is not None and rule.conclusion.value in self.action_base:
                    # print("concl: ", rule.conclusion.value, rule.uncertainty)
                    if uncertainty is not None and rule.uncertainty is not None:
                        uncert_rules[rule.conclusion.value] = rule, uncertainty + rule.uncertainty - uncertainty * rule.uncertainty
                    elif rule.uncertainty is not None:
                        uncert_rules[rule.conclusion.value] = rule, rule.uncertainty
                    elif uncertainty is not None:
                        uncert_rules[rule.conclusion.value] = rule, uncertainty
                    else:
                        self.conclusion_evaluation(rule.conclusion)
                else:
                    conclusion = self.rule_concl(rule.conclusion)
                    for c in conclusion:
                        if c in self.action_base:
                            if uncertainty is not None and rule.uncertainty is not None:
                                uncert_rules[c] = rule, uncertainty + rule.uncertainty - uncertainty * rule.uncertainty
                            elif rule.uncertainty is not None:
                                uncert_rules[c] = rule, rule.uncertainty
                            elif uncertainty is not None:
                                uncert_rules[c] = rule, uncertainty
                            else:
                                self.conclusion_evaluation(c)
        # print("UNC_RULER: ", sorted(uncert_rules.items(), key=lambda x: x[1][1])[::-1])

        self.infere_2(knowledge_base, sorted(uncert_rules.items(), key=lambda x: x[1][1])[::-1], action_base)

    def infere_2(self, knowledge_base: List[Fact], rules, action_base: ActionBaseCaller) -> None:
        self.knowledge_base = knowledge_base
        self.action_base = action_base
        for conclusion, rule in rules:
            rule, unc = rule
            for concl, r in rules:
                if str(concl) == str(conclusion) and concl != conclusion:
                    # print(unc, r[1])
                    unc = unc + r[1] - unc * r[1]
                    # print(unc)
                    rules.remove((concl, r))
            if unc * 100 < 30:
                continue
            condition, _ = self.rule_evaluation(rule.condition)
            if condition:
                # print(conclusion, unc * 100, rule, chance)
                if rule.conclusion.value is not None and rule.conclusion.value in self.action_base:
                    self.conclusion_evaluation(rule.conclusion)
                else:
                    conclusion = self.rule_concl(rule.conclusion)
                    for c in conclusion:
                        if c in self.action_base:
                            self.conclusion_evaluation(c)

    def rule_concl(self, root_node: ExpressionNode):
        if root_node.value != None:
            # print("concl: ", root_node.value, root_node.value.uncertainty)
            return root_node.value
        else:
            return self.rule_concl(root_node.left), self.rule_concl(root_node.right)

    def rule_evaluation(self, root_node: ExpressionNode, op=None):
        """
        Example of rule tree evaluation. This implementation did not check comparision operators and uncertainty.
        For usage in inference extend this function

        :param root_node: root node of the rule tree
        :return: True if rules is satisfiable, False in case of not satisfiable or missing Facts
        """
        # print("__root: ", root_node)
        if root_node.operator == LogicalOperator.AND:
            res1, unc1 = self.rule_evaluation(root_node.left, 1)
            res2, unc2 = self.rule_evaluation(root_node.right, 1)
            res = res1 and res2
            unc = None
            if unc1 is not None and unc2 is not None:
                unc = min(unc1, unc2)
            elif unc1 is not None:
                unc = unc1
            elif unc2 is not None:
                unc = unc2
            # print("AND: ", res1, unc1, res2, unc2, unc)
            return res, unc

        elif root_node.operator == LogicalOperator.OR:
            res1, unc1 = self.rule_evaluation(root_node.left, 0)
            res2, unc2 = self.rule_evaluation(root_node.right, 0)
            res = res1 or res2
            unc = None
            if unc1 is not None and unc2 is not None:
                unc = max(unc1, unc2)
            elif unc1 is not None:
                unc = unc1
            elif unc2 is not None:
                unc = unc2
            return res, unc

        elif isinstance(root_node.value, Expression):
            # print("CONDITION: ", root_node.value, root_node.value.uncertainty)
            if root_node.value.comparator == Operator.LESS_THEN:
                res = self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) < float(root_node.value.value)
                if not res:
                    root_node.value.uncertainty = None
                return res, root_node.value.uncertainty

            elif root_node.value.comparator == Operator.EQUAL:
                res = self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) == float(root_node.value.value)
                if not res:
                    root_node.value.uncertainty = None
                return res, root_node.value.uncertainty

            elif root_node.value.comparator == Operator.LESS_EQUAL:
                res = self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) <= float(root_node.value.value)
                if not res:
                    root_node.value.uncertainty = None
                return res, root_node.value.uncertainty

            elif root_node.value.comparator == Operator.MORE_EQUAL:
                res = self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) >= float(root_node.value.value)
                if not res:
                    root_node.value.uncertainty = None
                return res, root_node.value.uncertainty

            elif root_node.value.comparator == Operator.MORE_THEN:
                res = self.knowledge_base[self.knowledge_base.index(root_node.value.name)](
                    *root_node.value.args) > float(root_node.value.value)
                if not res:
                    root_node.value.uncertainty = None
                return res, root_node.value.uncertainty

            try:
                res = self.knowledge_base[self.knowledge_base.index(root_node.value.name)](*root_node.value.args)
                if not res:
                    root_node.value.uncertainty = None
                return res, root_node.value.uncertainty

            except ValueError:

                return False, 0

        else:
            res = bool(root_node.value)
            if not res:
                root_node.value.uncertainty = None
            return res, root_node.value.uncertainty

    def conclusion_evaluation(self, root_node: ExpressionNode):
        if self.action_base.has_method(root_node.value):
            self.action_base.call(root_node.value)
