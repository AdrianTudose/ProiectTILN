import sys

from algorithms.algorithms import Preprocesor, SemanticAnalizer, Geolocator

<<<<<<< Updated upstream
def execute_algorithms(text):
=======
def execute_algorithms(text,oras):
>>>>>>> Stashed changes

    processed_text = Preprocesor.process(text)

    directions = SemanticAnalizer.analise(processed_text)

<<<<<<< Updated upstream
    coordinates = Geolocator.get_coordinates(directions)
=======
    coordinates = Geolocator.get_coordinates(directions,oras)
>>>>>>> Stashed changes

    return coordinates