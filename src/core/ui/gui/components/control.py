class CustomControl:
    """Replaces ft.UserControl because of big amount of bugs."""

    overlay = []

    def build(self):
        raise NotImplementedError
