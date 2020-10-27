Expert system
===================

The main module of Orodael Turrim is an expert system. Your task is to create your own planning expert system that will
plan defense against Rigor Mortis.  All behavior of the expert system is extracted to the ``User`` module, so you don't
need to change anything in the program code.

Also, it is forbidden to change anything in other parts of the code. Tests of the Expert system will be executed
with the original modules, only with you ``User`` module, so any other changes will be ignored.

Structure of the expert system is divided into 3 parts:

* ``KnowledgeBase.py`` - part of the module for creating knowledge based on game state
* ``Inference.py`` - part of the module for inference mechanism
* ``ActionBase.py`` - part of the module for defining conclusions and actions of conclusions

You need to implement all three parts to achieve a working expert system. As an example, there is already implemented
basic version of inference, but did not support all necessary function, so use that example only for
inspiration.

.. warning::

   When you are creating an expert system, there are few restrictions for implementation. If you violate these
   restrictions, your solution will not be accepted.



Knowledge base
-----------------

The first part that you should implement is ``KnowledgeBase``. In this part of the module you should get all the necessary
information from proxy and transform that information to ``Facts``. Those ``Facts`` you will use in the inference mechanism.

Fact
******

You must use the ``ExpertSystem.Structure.RuleBase.Fact`` class to represent facts, otherwise you can't use some functions.
Class ``Fact`` have 4 instance variables:

**name**

Represent the name of the fact. THe name should be always string. The same name is then used in rules file.

**eval_function**

Instance variable ``eval_function`` is used for evaluation of rules conditions. We want to decide
if the condition in the rule is satisfied or not. For basic use, when we assume that once a fact is
in the base than is True, we do not need to change this variable. By default ``eval_function`` is
True.

If we want to use operators (<, >, ==, ...), we need to set value to the fact. Also, the value of the
fact could depend on the given parameters. That is the reason, why ``eval_function`` is defined as
function (Callable). Easies way to define ``eval_function`` is with lambda functions.

The first option is very simple. We define a function, that always returns a number. There are no
additional parameters from the rules. This could be used for compare operators (<, >, ==, ...).

.. code-block:: python

   archer_count = 5
   Fact('archer_count', lambda : archer_count)


If you want to pass an argument from rules to the fact, you need to add arguments to the lambda function.

.. code-block:: python

   Fact('unit_count', lambda unit: get_num_unit(unit))


Also, you can call a function inside the lambda function. For example, if you want to have info about player money.

.. code-block:: python

   Fact('money', lambda : self.game_object_proxy.get_resources(self.player))


Using the lambda function is not that hard, so don't worry about that.

**probability**

The next instance variable is ``probability``. With this parameter, you can store the probability of your fact.
It using standard float numbers, so there is no magic.

**data**

The last instance variable is data. This variable is used for passing parameters from condition to conclusion.
If you mark fact in your rule file with data handle mark (*) then you must specify ``data`` variable of that fact.
TYpe of this variable is also callable (pointer to function). This function could return only a position or
list of positions. It is forbidden to return any other value types. If you didn't mark fact with handle mark,
you don't need to specify data variable. Example of usage:


.. code-block:: python

   # KnowledgeBase.py
   def free_tile():
      return self.map_proxy.get_player_visible_tiles()[0]

   Fact('free_tile', data=free_tile)

   # rules
   IF free_tile* THEN build_base free_tile;


Function defined by data variable will be evaluated when you call build_base from inference. So the result will be
up to date with the game state.

Framework also tries to pass arguments to data function. Evaluation tries pass all arguments to data function and if
there is conflict, the framework tries evaluate data function without parameters. So if your eval function needs
parameters but your data function not, it is no problem. Here is an example of data function with parameters


.. code-block:: python

   # KnowledgeBase.py
   def free_tile(terrain_type):
      tiles = self.map_proxy.get_player_visible_tiles()
        border_tiles = self.map_proxy.get_border_tiles()

        for position in tiles:
            terrain = self.map_proxy.get_terrain_type(position) == TerrainType.from_string(terrain_type)
            occupied = self.map_proxy.is_position_occupied(position)
            if terrain and not occupied and position not in border_tiles:
                return position
        return None

   Fact('free_tile', data=free_tile)

   # rules
   IF free_tile* mountain THEN build_base free_tile;





For creating knowledge base you could use 3 types of proxy:

* ``MapProxy`` - access information about map
* ``GameObjectProxy`` - access information about game objects
* ``GameUncertaintyProxy`` - access information about uncertainty spawns

You can read more about proxy methods at :ref:`proxy`

A list of the facts that you generate in ``KnowledgeBase.create_knowledge_base`` will be passed to inference method.
You need to return a list of facts from the method.

.. warning::

    For creating facts use only proxy! Don't try to get more information from the GameEngine itself!

Inference
--------------

In the inference part of the User module, you should define your inference method. You could use forward or backward
inference. Whole inference implementation is up to you. You must implement inference in ``interfere`` method
because this method will be executed each round in the game. Of course, you can implement other supported
functions for better code structure, but the entry point must be the ``interfere`` method. Don't change the signature
of the ``interfere`` method, you will never call inference directly. ``interfere`` method provides parameters:

* ``knowledge_base`` - list of facts from ``KnowledgeBase.create_knowledge_base``
* ``rules`` - list of rules from rules files in tree representation
* ``action_base`` - special class used to call functions that you define in ``ActionBase``

**Knowledge base**

Argument knowledge_base contains facts, that you prepare in the ``KnowledgeBase`` module. There is only one change,
all data variables are wiped out. The passing of data variables are described below.

**Rules structure**

Framework will parse rules file for you. You will get rules as a list of the ``ExpertSystem.Structure.RuleBase.Rule``
instances. Each list item represents one rule. You can read about rule structure at :ref:`rules`.

**Inference method**

In the ``User`` module you can find an example of basic inference method. This is a very simple and useless implementation of
inference. Use it only as an example. As a result of the inference, you should call some action from ``ActionBase``.

**Action base calls**

In the inference method, you have a ``ActionBaseCaller`` instance, that represent your action base.

If you want to call your function from ActionBase, you need to use the method ``call`` from ``ActionBaseCaller``.
Method call get parameter of type ``Expression`` (conclusion Expression node). You must use ``Expression`` class
from given rules, don't try to create a new one. If you call method ``call``, all parameters from ``Expression`` are
passed to ``ActionBase`` method and also all parameters from facts are injected. So basically you don't need
to worry about nothing. Just be sure, that you have a method in action base with the correct signature.

``ActionBaseCaller`` has also method ``has_method`` that check, if correspond method exist in ``ActionBase``.


**Recapitulation**

There are important things that need to be done. First, you need to mark your fact as a data holder with ``*`` in the rules file.
Otherwise, the data variables will not be injected. Your ActionBase method must contain an argument with the same name as the
fact name. There could be more than one data facts. You can combine this also with standard arguments, but data holder
arguments must be after positional arguments. Last thing, don't try to pass the data holder fact (parameter) manually.
Everything is done by dependency injection.

Example of usage

.. code-block:: python

   # KnowledgeBase.py
   target_position = OffsetPosition(0, 0)
   facts.append(Fact('free_tile', data=lambda: target_position))

   # rules
   IF free_tile* THEN build_base 1 1 free_tile;

   # ActionBase.py
   def build_base(self, position_x, position_y, free_tile):
      pass

   # Inference.py
   def conclusion_evaluation(self, root_node: ExpressionNode):
       if self.action_base.has_method(root_node.value):
             self.action_base.call(root_node.value)
          else:
             pass # Add to facts


Complex example with proxy call

.. code-block:: python

   # KnowledgeBase.py
   def visible_free_tile(self, terrain_type: str):
    """ Find random free tile with given terrain type """
    tiles = self.map_proxy.get_player_visible_tiles()
    border_tiles = self.map_proxy.get_border_tiles()

    for position in tiles:
        terrain = self.map_proxy.get_terrain_type(position) == TerrainType.from_string(terrain_type)
        occupied = self.map_proxy.is_position_occupied(position)
        if terrain and not occupied and position not in border_tiles:
            return position
    return None

   facts.append(Fact('free_tile', data=visible_free_tile, eval_function=visible_free_tile))

   # rules
   IF free_tile* mountain THEN build_base awesome_text free_tile;

   # ActionBase.py
   def build_base(self, log_text, free_tile):
      pass

   # Inference.py
   def conclusion_evaluation(self, root_node: ExpressionNode):
       if self.action_base.has_method(root_node.value):
             self.action_base.call(root_node.value)
          else:
             pass # Add to facts


As you can see in the example, same function is used for data and eval_function. That because our ``visible_free_tiles``
function returns None, if there is no such position. Boolean value of None is False and boolean value of position is True.
Of course, data function and eval_function could be different functions.

Action base
--------------

In the action base, you can specify your own conclusions with your own implementation. Just write new method to
``ActionBase``. Your methods could have as many parameters as you want, but you need to provide values of the
parameters in the inference. Your methods cannot start with underline, otherwise you cannot use them in inference.
Also, if you are using data holder parameters, don't forget about arguments with **same name** as fact with data.

``ActionBase`` class provides access to ``GameControlProxy`` and instance of ``PlayerTag`` that represent your
player (you need it because of identification).


.. _rules:

Rules file
--------------

In the file ``rules`` you can specify all your rules. You must use defined language, you can read about it at
:ref:`grammar`. Those rules will be automatically parsed and transformed to tree representation. Each rule have own tree.

Each rule is represented with ``ExpertSystem.Structure.RuleBase.Rule`` class. This class have 3 properties

* ``condition`` - tree representation of condition, root ``ExpressionNode``
* ``conclusion`` - tree representation of conclusion, root ``ExpressionNode``
* ``uncertainty`` - probability of whole rule


Each condition and conclusion tree is created with ``ExpressionNode`` classes for each node in the tree.
``ExpressionNode`` provides 6 properties:

* ``left`` - instance of left child node if exists, None if node don't have left child
* ``right`` - instance of right child node if exists, None if node don't have right child
* ``operator`` - if node have left and right child, there is specified operator between them (``LogicalOperator``)
* ``value`` - if node is leaf, there is specified expression ( ``Expression`` )
* ``parent`` - instance of node parent, None if node is root
* ``parentheses`` - True if current node is in parentheses in rule, False otherwise

Leafs are ``Expression`` classes. They represent one part of the rule. ``Expression`` class provides 5 properties:

* ``name`` - name of the identifier (fact)
* ``args`` - list of arguments provided to the fact
* ``comparator`` - comparator between fact and value (``Operator``)
* ``value`` - value on the right side of comparator
* ``uncertainty`` - probability of this part of rule
* ``data_holder_mark`` - True, if fact is marked as data holder

**Example of the tree**

.. code-block:: none

   IF player_have_base AND ( enemy_attack 2 2 > 5 OR enemy_attack 3 3 > 8 ) THEN spawn_archer 2 2 AND spawn_archer 3 3 WITH 0.25;


.. figure::  _static/principles/rule_parse.png
   :target: _static/principles/rule_parse.png

.. _custom_filters:

Custom filters
------------------

In the section :ref:`filters` you can read about move and attack filter system. Now talk about how to create own custom filters.
As a defender, you can use only attack filters, because your unit cannot move. But also some smart attack filters
could be really handy in some cases.

If you want to define you own filter, you need to create new class that inherit from
``OrodaelTurrim.Structure.Filter.FilterPattern.AttackFilter``. There are some restrictions for your filters:

 * Your filter class must be in ``AttackFilter.py`` file in ``User`` module
 * Your filter must inherit only ``OrodaelTurrim.Structure.Filter.FilterPattern.AttackFilter``
 * Your filter must overload ``filter`` method with same parameters
 * ``filter`` method must return List of tiles and tiles must be subset of given ``tiles`` List
 * You can overload ``__init__`` method but first two parameters must be same as in abstract class and you must
   call __init__ from inherited class
 * You can implement as many functions as you wont in filter class

If your class meets all requirements, you will see this filter in GUI and also you can instance your filter with
``FilterFactory`` (you can instance them directly but then you need to take care of initial parameters).

In the ``AttackFilter.py`` file you have example of custom filter.