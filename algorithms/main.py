import sys

from Algorithms.algorithms import Preprocesor, SemanticAnalizer, Geolocator

def execute_algorithms(text):

    processed_text = Preprocesor.process(text)

    directions = SemanticAnalizer.analise(processed_text)

    coordinates = Geolocator.get_coordinates(directions)

    return coordinates