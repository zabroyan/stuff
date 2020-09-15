Rules definition language
===========================

For defining expert system rules there is prepared language. This language should be universal enough for
defining all your rules needs. If something missing in the language, please let me know through GIT
issue in the repository.

Language is processed with parser and lexer based on antlr4, which gives you many advantages like:

   - Syntax controlling
   - Error messages with bad rules format
   - No need to write own Python parser
   - Create expression tree for easy evaluation of each rule

So when you try to write some rules with bad syntax, you don't need to check it by yourself, parser will tell you
about it. Language is described with grammar. In the grammar you should find out, what you can write.
Grammar definition is written in atnrl4 language.

.. _grammar:

Grammar
-----------

.. literalinclude:: _static/Rules.g4
   :language: antlr


Examples
-----------
Here you can find some examples, about what can be written in the language. It is make no sense to write all
possibilities, because there are infinity number of possibilities. It is recommended to look at grammar definition
and lear what is possible by that. Here you can find some inspiration. All examples are correct so you can copy them
to ``rule`` file and execute inference, but you probably don't get any output, because of missing action definition.


**Rule with no condition**

.. code-block:: none

   IF TRUE THEN build_base_random;

**Rule with simple condition**

.. code-block:: none

   IF player_dont_have_base THEN build_base_random;

**Parametrized expressions**

.. code-block:: none

   IF player_dont_have_base THEN build_base 2 2;

**Expression with comparision**

.. code-block:: none

   IF base_count == 0 THEN build_base 2 2;

**Expression with comparision and arguments**

.. code-block:: none

   IF object_count base == 0 THEN build_base 2 2;

**Expression with data holder mark and arguments**

.. code-block:: none

   IF free_position* mountain THAT build_archer free_position;

**Logical operators in condition**

.. code-block:: none

   IF object_count base == 0 AND terrain 2 2 == forest THEN build base 2 2;
   IF object_count archer < 2 OR object_count knight < 2 THEN spawn_archer 1 3;

**Logical operators in conclusion**

.. code-block:: none

   IF object_count archer < 2 THEN spawn_archer 1 3 AND spawn_archer 5 5;

**Parentheses for logical operators order**

.. code-block:: none

   IF player_have_base AND ( object_count archer < 2 OR object_count knight < 2 ) THEN spawn_archer 1 3;

**Defining value in conclusion**

.. code-block:: none

   IF object_count archer > 10 THEN strength := 10;
   IF object_count archer > 10 THEN strength := high;

**Probability of whole rule**

.. code-block:: none

   IF object_count archer > 10 THEN strength := 10 WITH 0.50;

**Probability of condition expressions**

.. code-block:: none

   IF object_count archer > 10 [0.25] AND object_count knight > 5 [0.8] THEN strength := 10;