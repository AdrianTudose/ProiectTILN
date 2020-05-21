import sys

from algorithms.algorithms import Preprocesor, SemanticAnalizer, Geolocator

def execute_algorithms(text,oras):

    processed_text = Preprocesor.process(text)

    directions = SemanticAnalizer.analise(processed_text)

    coordinates = Geolocator.get_coordinates(directions,oras)

    return coordinates