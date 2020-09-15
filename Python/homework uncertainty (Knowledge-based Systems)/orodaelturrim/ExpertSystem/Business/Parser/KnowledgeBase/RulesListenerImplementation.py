from ExpertSystem.Business.Parser.KnowledgeBase.RulesListener import RulesListener
from ExpertSystem.Structure.Enums import LogicalOperator
from ExpertSystem.Structure.RuleBase import Rule, Expression, ExpressionNode

if __name__ is not None and "." in __name__:
    from .RulesParser import RulesParser
else:
    from RulesParser import RulesParser


# This class defines a complete listener for a parse tree produced by RulesParser.
class RulesListenerImplementation(RulesListener):
    """ Overload listener method to save rules to tree format """


    def __init__(self):
        super().__init__()
        self.rules = None
        self.rule = None
        self.expression = None
        self.context = None
        self.expression_uncertainty = None


    def enterRules_set(self, ctx: RulesParser.Rules_setContext):
        """ Enter list of single rules ending with EOF """
        self.rules = []


    def exitRules_set(self, ctx: RulesParser.Rules_setContext):
        pass


    def enterSingle_rule(self, ctx: RulesParser.Single_ruleContext):
        """
        Enter single rule -> one rule ending with semicolon

        ``IF condition THEN conclusion WITH DECIMAL;``
        """
        self.rule = Rule()
        if ctx.WITH() and ctx.DECIMAL() and 'missing' not in ctx.DECIMAL().getText():
            self.rule.uncertainty = float(ctx.DECIMAL().getText())


    def exitSingle_rule(self, ctx: RulesParser.Single_ruleContext):
        self.rules.append(self.rule)


    def enterCondition(self, ctx: RulesParser.ConditionContext):
        """ Enter condition. Prepare root Node and set context to this node"""
        self.context = ExpressionNode()
        self.rule.condition = self.context


    def exitCondition(self, ctx: RulesParser.ConditionContext):
        pass


    def enterConclusion(self, ctx: RulesParser.ConclusionContext):
        """ Enter conclusion. Prepare root Node and set context to this node"""
        self.context = ExpressionNode()
        self.rule.conclusion = self.context


    def exitConclusion(self, ctx: RulesParser.ConclusionContext):
        pass


    def enterComparisonExpression(self, ctx: RulesParser.ComparisonExpressionContext):
        """
        Condition rewrite to Comparison expression

        ``function_expr [ DECIMAL ]``
        """
        self.expression_uncertainty = ctx.DECIMAL()


    def exitComparisonExpression(self, ctx: RulesParser.ComparisonExpressionContext):
        self.expression_uncertainty = None


    def enterLogicalExpressionInParen(self, ctx: RulesParser.LogicalExpressionInParenContext):
        """ Exclude parentheses from rule and save info about parentheses """
        self.context.parentheses = True


    def exitLogicalExpressionInParen(self, ctx: RulesParser.LogicalExpressionInParenContext):
        pass


    def enterLogicalExpressionAnd(self, ctx: RulesParser.LogicalExpressionAndContext):
        """
        Enter left logical expresion with AND

        ``logical_expresion AND logical_expresion``
        """

        self.context.operator = LogicalOperator.AND
        self.context.left = ExpressionNode()
        self.context.left.parent = self.context
        self.context = self.context.left


    def exitLogicalExpressionAnd(self, ctx: RulesParser.LogicalExpressionAndContext):
        """ Exit left logical end -> check where to pass context (to parent or right child of parent) """
        if self.context.parent:
            if self.context.parent.right is None:
                self.context.parent.right = ExpressionNode()
                self.context.parent.right.parent = self.context.parent
                self.context = self.context.parent.right
            else:
                self.context = self.context.parent


    def enterLogicalExpressionOr(self, ctx: RulesParser.LogicalExpressionOrContext):
        """
        Enter left logical expresion with OR

        ``logical_expresion OR logical_expresion``
        """
        self.context.operator = LogicalOperator.OR
        self.context.left = ExpressionNode()
        self.context.left.parent = self.context
        self.context = self.context.left


    def exitLogicalExpressionOr(self, ctx: RulesParser.LogicalExpressionOrContext):
        """ Exit left logical end -> check where to pass context (to parent or right child of parent) """
        if self.context.parent:
            if self.context.parent.right is None:
                self.context.parent.right = ExpressionNode()
                self.context.parent.right.parent = self.context.parent
                self.context = self.context.parent.right
            else:
                self.context = self.context.parent


    def enterFunction_expr(self, ctx: RulesParser.Function_exprContext):
        """
        Parse function expression

        * ``IDENTIFIER args operator DECIMAL/IDENTIFIER``
        * ``TRUE/FALSE``
        """

        expression = Expression()
        if self.expression_uncertainty:
            expression.uncertainty = float(self.expression_uncertainty.getText())

        # Expression have identifier or only TRUE / FALSE
        if ctx.IDENTIFIER():
            expression.name = ctx.IDENTIFIER(0).getText()
        else:
            expression.name = 'TRUE' if ctx.TRUE() else 'FALSE'

        # Set data holder mark bool
        expression.data_holder_mark = True if ctx.DHM() else False

        # Expression have comparator (<,>,==,!=,<=,>=)
        if ctx.comp_operator():
            expression.comparator = ctx.comp_operator().getText()

        # Expression have number or string value after comparator
        if ctx.DECIMAL():
            expression.value = ctx.DECIMAL().getText()
        elif len(ctx.IDENTIFIER()) > 1:
            expression.value = ctx.IDENTIFIER(1).getText()

        self.context.value = expression


    def exitFunction_expr(self, ctx: RulesParser.Function_exprContext):
        """ Exit expression -> pass context to correct place (parent or parent right child)"""
        if self.context.parent:
            if self.context.parent.right is None:
                self.context.parent.right = ExpressionNode()
                self.context.parent.right.parent = self.context.parent
                self.context = self.context.parent.right
            else:
                self.context = self.context.parent


    def enterRLogicalExpression(self, ctx: RulesParser.RLogicalExpressionContext):
        """ Enter right logical expression """
        pass


    def exitRLogicalExpression(self, ctx: RulesParser.RLogicalExpressionContext):
        pass


    def enterRLogicalExpressionAnd(self, ctx: RulesParser.RLogicalExpressionAndContext):
        """ Parse logical operator AND in conclusion """
        self.context.operator = LogicalOperator.AND
        self.context.left = ExpressionNode()
        self.context.left.parent = self.context
        self.context = self.context.left


    def exitRLogicalExpressionAnd(self, ctx: RulesParser.RLogicalExpressionAndContext):
        """ Exit logical operator AND -> pass context to right place """
        if self.context.parent.parent:
            self.context.parent.parent.right = ExpressionNode()
            self.context.parent.parent.right.parent = self.context.parent.parent
            self.context = self.context.parent.parent.right


    def enterRLogicalExpressionInParen(self, ctx: RulesParser.RLogicalExpressionInParenContext):
        """ Parse parentheses from expression """
        self.context.parentheses = True


    def exitRLogicalExpressionInParen(self, ctx: RulesParser.RLogicalExpressionInParenContext):
        pass


    def enterR_function_expr(self, ctx: RulesParser.R_function_exprContext):
        """ Parse right expression """
        expression = Expression()

        # Get text of identifier
        expression.name = ctx.IDENTIFIER(0).getText()

        # Check if there is assign operator
        if ctx.ASSIGN():
            expression.comparator = ':='

        # Check if assign is number or identifier
        if ctx.DECIMAL():
            expression.value = ctx.DECIMAL().getText()

        if ctx.IDENTIFIER(1):
            expression.value = ctx.IDENTIFIER(1).getText()

        self.context.value = expression


    def exitR_function_expr(self, ctx: RulesParser.R_function_exprContext):
        """ Exit right expression -> pass context to right place"""
        if self.context.parent and self.context.parent.right is None:
            self.context.parent.right = ExpressionNode()
            self.context.parent.right.parent = self.context.parent
            self.context = self.context.parent.right


    def enterArg(self, ctx: RulesParser.ArgContext):
        """ Enter arg and add arg tu current context """
        self.context.value.args.append(ctx.getText())
