# Generated from Rules.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .RulesParser import RulesParser
else:
    from RulesParser import RulesParser

# This class defines a complete listener for a parse tree produced by RulesParser.
class RulesListener(ParseTreeListener):

    # Enter a parse tree produced by RulesParser#rules_set.
    def enterRules_set(self, ctx:RulesParser.Rules_setContext):
        pass

    # Exit a parse tree produced by RulesParser#rules_set.
    def exitRules_set(self, ctx:RulesParser.Rules_setContext):
        pass


    # Enter a parse tree produced by RulesParser#single_rule.
    def enterSingle_rule(self, ctx:RulesParser.Single_ruleContext):
        pass

    # Exit a parse tree produced by RulesParser#single_rule.
    def exitSingle_rule(self, ctx:RulesParser.Single_ruleContext):
        pass


    # Enter a parse tree produced by RulesParser#condition.
    def enterCondition(self, ctx:RulesParser.ConditionContext):
        pass

    # Exit a parse tree produced by RulesParser#condition.
    def exitCondition(self, ctx:RulesParser.ConditionContext):
        pass


    # Enter a parse tree produced by RulesParser#conclusion.
    def enterConclusion(self, ctx:RulesParser.ConclusionContext):
        pass

    # Exit a parse tree produced by RulesParser#conclusion.
    def exitConclusion(self, ctx:RulesParser.ConclusionContext):
        pass


    # Enter a parse tree produced by RulesParser#ComparisonExpression.
    def enterComparisonExpression(self, ctx:RulesParser.ComparisonExpressionContext):
        pass

    # Exit a parse tree produced by RulesParser#ComparisonExpression.
    def exitComparisonExpression(self, ctx:RulesParser.ComparisonExpressionContext):
        pass


    # Enter a parse tree produced by RulesParser#LogicalExpressionInParen.
    def enterLogicalExpressionInParen(self, ctx:RulesParser.LogicalExpressionInParenContext):
        pass

    # Exit a parse tree produced by RulesParser#LogicalExpressionInParen.
    def exitLogicalExpressionInParen(self, ctx:RulesParser.LogicalExpressionInParenContext):
        pass


    # Enter a parse tree produced by RulesParser#LogicalExpressionAnd.
    def enterLogicalExpressionAnd(self, ctx:RulesParser.LogicalExpressionAndContext):
        pass

    # Exit a parse tree produced by RulesParser#LogicalExpressionAnd.
    def exitLogicalExpressionAnd(self, ctx:RulesParser.LogicalExpressionAndContext):
        pass


    # Enter a parse tree produced by RulesParser#LogicalExpressionOr.
    def enterLogicalExpressionOr(self, ctx:RulesParser.LogicalExpressionOrContext):
        pass

    # Exit a parse tree produced by RulesParser#LogicalExpressionOr.
    def exitLogicalExpressionOr(self, ctx:RulesParser.LogicalExpressionOrContext):
        pass


    # Enter a parse tree produced by RulesParser#function_expr.
    def enterFunction_expr(self, ctx:RulesParser.Function_exprContext):
        pass

    # Exit a parse tree produced by RulesParser#function_expr.
    def exitFunction_expr(self, ctx:RulesParser.Function_exprContext):
        pass


    # Enter a parse tree produced by RulesParser#args.
    def enterArgs(self, ctx:RulesParser.ArgsContext):
        pass

    # Exit a parse tree produced by RulesParser#args.
    def exitArgs(self, ctx:RulesParser.ArgsContext):
        pass


    # Enter a parse tree produced by RulesParser#arg.
    def enterArg(self, ctx:RulesParser.ArgContext):
        pass

    # Exit a parse tree produced by RulesParser#arg.
    def exitArg(self, ctx:RulesParser.ArgContext):
        pass


    # Enter a parse tree produced by RulesParser#comp_operator.
    def enterComp_operator(self, ctx:RulesParser.Comp_operatorContext):
        pass

    # Exit a parse tree produced by RulesParser#comp_operator.
    def exitComp_operator(self, ctx:RulesParser.Comp_operatorContext):
        pass


    # Enter a parse tree produced by RulesParser#RLogicalExpression.
    def enterRLogicalExpression(self, ctx:RulesParser.RLogicalExpressionContext):
        pass

    # Exit a parse tree produced by RulesParser#RLogicalExpression.
    def exitRLogicalExpression(self, ctx:RulesParser.RLogicalExpressionContext):
        pass


    # Enter a parse tree produced by RulesParser#RLogicalExpressionAnd.
    def enterRLogicalExpressionAnd(self, ctx:RulesParser.RLogicalExpressionAndContext):
        pass

    # Exit a parse tree produced by RulesParser#RLogicalExpressionAnd.
    def exitRLogicalExpressionAnd(self, ctx:RulesParser.RLogicalExpressionAndContext):
        pass


    # Enter a parse tree produced by RulesParser#RLogicalExpressionInParen.
    def enterRLogicalExpressionInParen(self, ctx:RulesParser.RLogicalExpressionInParenContext):
        pass

    # Exit a parse tree produced by RulesParser#RLogicalExpressionInParen.
    def exitRLogicalExpressionInParen(self, ctx:RulesParser.RLogicalExpressionInParenContext):
        pass


    # Enter a parse tree produced by RulesParser#r_function_expr.
    def enterR_function_expr(self, ctx:RulesParser.R_function_exprContext):
        pass

    # Exit a parse tree produced by RulesParser#r_function_expr.
    def exitR_function_expr(self, ctx:RulesParser.R_function_exprContext):
        pass


