class Themes:
    def __init__(self):
        self.current_theme = 'default'

        self.styles = {
            'input': '\u001b[37m',
            'bold': '\u001b[1m',
            'response': '\u001b[37;1m',
            'end': '\u001b[0m',
            'error': '\u001b[31m',
            'underline': '\u001b[4m'
        }

        self.theme_colors = {
            'default': {'input': '\u001b[37m', 'response': '\u001b[37;1m'},
            'pink': {'input': '\u001b[35m', 'response': '\u001b[35;1m'},
            'blue': {'input': '\u001b[34m', 'response': '\u001b[34;1m'},
            'green': {'input': '\u001b[32m', 'response': '\u001b[32;1m'}
        }

    def style(self, text: str, message_type) -> str:
        """
        Returns the styled text
        """
        return f"{self.styles[message_type]}{text}{self.styles['end']}"

    def change_theme(self, theme: str) -> None:
        """
        Changes the theme of the console
        """
        if theme not in self.theme_colors:
            raise ValueError(f"Theme '{theme}' not supported. Available themes are: {', '.join(self.theme_colors.keys())}.")
        
        self.current_theme = theme
        self.styles.update(self.theme_colors[theme])

    def available_themes(self) -> None:
        """
        Returns the available themes
        """
        return list(self.theme_colors.keys()), self.current_theme
