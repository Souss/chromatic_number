from enum import Enum

import logging

"""
    Behavioral Neuron which will treat element
    and return a result of a prices role
"""
class       Neuron:

    identifiers = []

    def     __init__(self, identifier):

        self.last_cycle = 0

        self.connections = {}
        self.identifier = identifier
        self.state = None

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

        print("* Node {}".format(self.identifier))
        for identifier, connection in self.connections.items():
            print("  => {} (weight {})".format(connection.next.identifier, connection.weight))

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
    def     state(self):
        """ State of the Neuron """

        return self._state

    @state.setter
    def     state(self, istate):

        self._state = istate

    @state.deleter
    def     state(self):

        del self._state

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


class       Graph:

    def     __init__(self, filename):

        self.cycle = 0 # Number of call of Chromatic number calculated
        self.neurons = {}

        self.__filename = filename
        self.__graph_loading()

    def     __parse_connections(self, line):

        line = line.rsplit('\n', 1)[0]
        neuron_id, connections_id = line.split(":", 1)
        neuron_left = None
        if neuron_id in self.neurons:
            neuron_left = self.neurons[neuron_id]
        else:
            neuron_left = Neuron(neuron_id)
            self.neurons[neuron_id] = neuron_left
        for neuron_id in connections_id.split(","):
            neuron_right = None
            if neuron_id in self.neurons:
                neuron_right = self.neurons[neuron_id]
            else:
                neuron_right = Neuron(neuron_id)
                self.neurons[neuron_id] = neuron_right
            neuron_left.add_or_update_connection(neuron_right)

    def     __display_neurons(self):

        for neuron in self.neurons.values():
            neuron.display()

    def     __graph_loading(self):

        try:
            with open(self.__filename, 'r') as fd:

                for line in fd:
                    self.__parse_connections(line)
                self.__display_neurons()

        except Exception as err:
            logging.error("{} ({})".format(err, type(err)))

    def     get_chromatic_number(self):

        return 0
