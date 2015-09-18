from graph import Neuron
from random import randint
import logging

ATTEMPTS = 1000
MAX_CHAR_VALUE = 255

class       NeuronChromatic(Neuron):

    def     __init__(self, identifier):

        super(NeuronChromatic, self).__init__(identifier)

        self.color = None

    def     generate_uniq_color(self, graph_colors=set()):

        # Not that much elaborate function. The main purpose isn't here
        attempts = ATTEMPTS
        while attempts > 0:
            color_random = "#{}{}{}".format(
                hex(randint(0, 255)).rsplit('x', 1)[1],
                hex(randint(0, 255)).rsplit('x', 1)[1],
                hex(randint(0, 255)).rsplit('x', 1)[1]
                )
            if color_random not in graph_colors:
                graph_colors.add(color_random)
                return color_random
            attempts -= 1
        raise ValueError("Couldn't generate a uniq color after {} attempts"
                         .format(ATTEMPTS))

    def     perception(self, graph_colors):

        if not isinstance(graph_colors, set):
            raise TypeError(
                "Perception parameter `graph_colors` must be a set."
                )
        neighbours_color = set()
        self.marked = True

        for connection in self.connections.values():

            if not connection.next.marked:
                connection.next.perception(graph_colors)
            color_connection = connection.next.color
            if color_connection:
                neighbours_color.add(color_connection)

        available_colors = graph_colors - neighbours_color
        if not available_colors:
            self.color = self.generate_uniq_color(graph_colors)
            graph_colors.add(self.color)
        else:
            self.color = next(iter(available_colors))

        return len(graph_colors)

    def     display(self):

        print("+ Node {} (color = {})".format(self.identifier, self.color))
        for identifier, connection in self.connections.items():
            print("  => {} (weight = {})".format(
                connection.next.identifier,
                connection.weight))
    """
        Property
    """
    @property
    def     color(self):

        return self._color

    @color.setter
    def     color(self, icolor):

        # TODO: Verify type
        self._color = icolor

class       ChromaticGraph:

    def     __init__(self, filename):

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
            neuron_left = NeuronChromatic(neuron_id)
            self.neurons[neuron_id] = neuron_left
        for neuron_id in connections_id.split(","):
            neuron_right = None
            if neuron_id in self.neurons:
                neuron_right = self.neurons[neuron_id]
            else:
                neuron_right = NeuronChromatic(neuron_id)
                self.neurons[neuron_id] = neuron_right
            neuron_left.add_or_update_connection(neuron_right)

    def     display(self):

        for neuron in self.neurons.values():
            neuron.display()

    def     __graph_loading(self):

        try:
            with open(self.__filename, 'r') as fd:

                for line in fd:
                    self.__parse_connections(line)

        except Exception as err:
            logging.error("{} ({})".format(err, type(err)))

    def     get_chromatic_number(self):

        if self.neurons:

            entry_point = next(iter(self.neurons.values()))
            graph_colors = set()
            chromatic_number = entry_point.perception(graph_colors)
            return chromatic_number

        return 0
