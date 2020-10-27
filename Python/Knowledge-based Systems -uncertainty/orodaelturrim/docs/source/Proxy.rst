.. _proxy:

Proxy definition
===================

Map proxy
------------

.. autoclass:: OrodaelTurrim.Business.Proxy.MapProxy
   :noindex:
   :members:

Game Object Proxy
------------------

.. autoclass:: OrodaelTurrim.Business.Proxy.GameObjectProxy
   :members:
   :noindex:

Game Control Proxy
--------------------

.. autoclass:: OrodaelTurrim.Business.Proxy.GameControlProxy
   :members:
   :noindex:



Game Uncertainty Proxy
--------------------------

.. autoclass:: OrodaelTurrim.Business.Proxy.GameUncertaintyProxy
   :members:
   :noindex:


UncertaintySpawn:
   * **positions** - list of UncertaintyPositions, where unit could spawn
      * **position** - position of unit
      * **uncertainty** - uncertainty of spawn
   * **game_object_type** - GameObjectType enum that define unit type

