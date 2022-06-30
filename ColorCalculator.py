
class ColorCalculator:
    def calculate_color(per: float, cool_color: tuple, warm_color: tuple) -> tuple:
        """This method takes any two RGB tuples and plots a radial gradient from the cool
        color (inside) to warm color (outside).

        :param float per: the percent the color is between the cool and warm color (0-1)
        :param tuple cool_color: the (R,G,B) for the color for the inside of the circle
        :param tuple warm_color: the (R,G,B) for the color for the outside of the circle
        :return tuple: the (R,G,B) tuple of the output color
        """
        inverse = 1 - per
        r = int(cool_color[0] * inverse + warm_color[0] * per)
        g = int(cool_color[1] * inverse + warm_color[1] * per)
        b = int(cool_color[2] * inverse + warm_color[2] * per)
        return (r,g,b)
