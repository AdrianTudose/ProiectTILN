import sys

from algorithms import Preprocesor, SemanticAnalizer, Geolocator


def main():
    if len(sys.argv) < 2:
        raise Exception("A text must be given as a parameter between \"\".")
    if len(sys.argv) > 2:
        raise Exception("Too many arguments for call. Only a text must be given as a parameter between \"\".")

    text = sys.argv[1]

    processed_text = Preprocesor.process(text)

    directions = SemanticAnalizer.analise(processed_text)

    coordinates = Geolocator.get_coordinates(directions)

    return coordinates

if __name__ == "__main__":
    main()
