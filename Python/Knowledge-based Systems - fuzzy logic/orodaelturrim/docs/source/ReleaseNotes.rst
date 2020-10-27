Release Notes
==============
* **1.2.3**
   * Fix bug with fact at conclusion in rules
   * Update documentation based on unit balance
   * Update default rules files

* **1.2.2**
   * Implement bss units to AI player
   * Add ``get_current_turn`` to ``GameObjectProxy``

* **1.2.1**
   * Data variable in Fact change from variable to callable
   * Remove option to call actions from action base directly (you need to you call method)
   * Remove option to call actions from action base by string (you need to use Expression)
   * Add method ``get_inner_tiles`` to map proxy. Method returns all non border tiles
   * Documentation update
   * Extended example implementation

* **1.2.0**
    .. warning:: This version is incompatible with 1.1.* versions

   * **Implement variable passing from knowledge base to action base**
   * Change method, how to call ActionBase methods from inference
   * Removed MapProxy from ActionBase
   * Rename Interference.py to Inference.py in User module
   * Add more details and examples to User module documentation
   * Update documentation of proxy classes
   * Replace ``Player`` object with ``PlayerTag`` object in ``User`` module
   * Fix bug with console simulation works without base
   * Improve bug reports - add user implementation to report
   * Unit balancing
   * Add option to disable AI console output (AI_CONSOLE_OUTPUT)

* **1.1.8**
    * Fix bug with more than two arguments in rules (more arguments were squeezed)
    * Fix bug with bad definition of ``LEFT_LOWER`` constant for ``OffsetPosition``
    * Add some example implementation to ``User`` module
    * Fix random exception at operation with gui log widget
    * Some changes in documentation

* **1.1.7**
    * **Add** ``MapProxy`` **to** ``ActionBase``
    * Updated class doc in ``ActionBase``
    * Add console option -x / --log-output-xml for XML log output

* **1.1.6**
    * Rise max number in GUI for round simulation to 9999

* **1.1.5**
    * Fix bug with problem of using other position types in ``ActionBase``

* **1.1.4**
    * Fix bug in the example evaluation in ``Interference`` class

* **1.1.3**
   * Add bug reporting feature