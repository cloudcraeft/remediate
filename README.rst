REMEDIATE
========================
remediate is a wrapper to fire independent runbooks which were originally 
python code create for aws lambdas. Without touching them they have been
repurposed as a target for a Demisto integration. 

There is a layer of indirection in the calling. Plus the feedback from the
individual runbooks were meant for running in a serverless environment.

Therefore some interesting strategies are used to capture the needed info.
Mainly string processing.

.. image:: remediate.png
