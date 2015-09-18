from enum import Enum

import logging

"""
    Behavioral Neuron which will treat element
    and return a result of a prices role
"""
class       Neuron:

    identifiers = []

    def     __init__(self, identifier):

        self.connections = {}
        self.identifier = identifier
        self.marked = False

    """
        Connection management
    """
    def     release_connection(self, oneuron):

        oidentifier = oneuron.identifier
        connection = self.connections.get(oidentifier, None)
        if connection:
            del self.connections[oidentifier]
            del connection

    def     add_or_update_connection(self, oneuron, weight=1):

        oidentifier = oneuron.identifier
        connection = self.connections.get(oidentifier)
        if connection:
            connection.weight = weight
        else:
            self.connections[oidentifier] = Connection(self, oneuron, weight)

    """
        Representation
    """
    def     __str__(self):

        return "{}:{}".format(self.identifier, list(self.connections.keys()))

    def     display(self):

        print("+ Node {}".format(self.identifier))
        for identifier, connection in self.connections.items():
            print("  => {} (weight {})".format(connection.next.identifier, connection.weight))

    """
        Perception Input / Output
        To reimplement to each type of neuron
    """
    def     perception(self, *args, **kwargs):
        return args, kwargs

    """
        Properties
    """
    @property
    def     identifier(self):
        """ Unique identifier of the Neuron """

        return self._identifier

    @identifier.setter
    def     identifier(self, iidentifier):

        if iidentifier in self.identifiers:
            raise AttributeError(
                "Neuron with identifier {} is already instanciated"
                )
        self._identifier = iidentifier

    @identifier.deleter
    def     identifier(self):

        del self._identifier

    @property
    def     marked(self):
        """ State of the Neuron """

        return self._marked

    @marked.setter
    def     marked(self, imarked):

        if not isinstance(imarked, bool):
            raise TypeError("marked value for Neuron should be a boolean")
        self._marked = imarked

    @marked.deleter
    def     marked(self):

        del self._marked

"""
    This is a representation of a connection between two neurons
    This one is always oriented and is it is a double side connection,
    it should be instanciated for the two way of reading (left to right
    and right to left)
"""
class       Connection:

    """
        Life Time
    """

    def     __init__(
            self, ineuron, oneuron, weight
            ):

        self._previous = ineuron
        self._next = oneuron

        self.weight = weight

    """
        Representation
    """
    def     __str__(self):

        return "{} --{}--> {}".format(
            self._previous.identifier,
            self.weight,
            self._next.identifier)

    """
        Properties
    """

    @property
    def     weight(self):
        """ To share weights with othe Neuron"""

        return self._weight

    @weight.setter
    def     weight(self, iweight):

        if (type(iweight) not in [ int, float ]
            or iweight < 0
            or iweight > 1):
            raise TypeError(
                "Weight should be a float somewhere between 0 and 1 included"
                )
        self._weight = iweight

    @weight.deleter
    def     weight(self):

        del self._weight

    @property
    def     previous(self):
        """ To share orientations with othe Neuron"""

        return self._previous

    @property
    def     next(self):
        """ To share orientations with othe Neuron"""

        return self._next
