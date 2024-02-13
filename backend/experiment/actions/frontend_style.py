from enum import Enum


class EFrontendStyle(Enum):
    EMPTY = ''
    BOOLEAN = 'boolean'
    BOOLEAN_NEGATIVE_FIRST = 'boolean-negative-first'
    NEUTRAL = 'neutral'
    NEUTRAL_INVERTED = 'neutral-inverted'
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    SUCCESS = 'success'
    NEGATIVE = 'negative'
    INFO = 'info'
    WARNING = 'warning'

    @staticmethod
    def is_valid(value):
        return value in EFrontendStyle.__members__.values()


class FrontendStyle:

    VALID_STYLES = EFrontendStyle.__members__.values()

    """
    Initialize the FrontendStyle with a root style, and optionally nested styles.
    :param root_style: The style name for the root element.
    :param nested_styles: A dictionary where keys are element identifiers and values are style names.
    """
    def __init__(self, root_style: EFrontendStyle = EFrontendStyle.EMPTY, **nested_styles):

        if not EFrontendStyle.is_valid(root_style):
            raise ValueError(f"Invalid root style: {root_style}")

        self.styles = {'root': root_style}

        for element, nested_style in nested_styles.items():
            if isinstance(nested_style, FrontendStyle):
                self.styles[element] = nested_style
            else:
                raise ValueError(f"Nested styles must be of type FrontendStyle, got {type(nested_style)} for '{element}'")

    def get_style(self, element: str) -> str:
        """
        Get the style for a specific element.
        :param element: The element identifier for which to get the style.
        :return: The style name for the given element.
        """
        return self.styles.get(element, None)

    def apply_style(self, element: str, style: str) -> None:
        """
        Apply a specific style to an element after validating the style.
        :param element: The element identifier to apply the style to.
        :param style: The style name to apply.
        """
        if EFrontendStyle.is_valid(style):
            self.styles[element] = style
        else:
            valid_styles = ', '.join([str(s) for s in self.VALID_STYLES])
            raise ValueError(f"Invalid style: {style}. Valid styles are {valid_styles}.")

    def to_dict(self) -> dict:
        serialized_styles = {'root': self.styles['root'].value}
        for element, style in self.styles.items():
            if element != 'root':
                if isinstance(style, FrontendStyle):
                    serialized_styles[element] = style.to_dict()
                elif isinstance(style, EFrontendStyle):
                    serialized_styles[element] = style.value
                else:
                    serialized_styles[element] = style

        return serialized_styles
    
    def __str__(self):
        return str(self.to_dict())
    
    def __json__(self):
        return self.to_dict()
