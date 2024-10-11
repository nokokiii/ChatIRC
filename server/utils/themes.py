from typing import List

class Themes:
    def __init__(self):
        self.current_theme = "default"

        self.styles = {
            "input": "\u001b[37m",
            "bold": "\u001b[1m",
            "response": "\u001b[37;1m",
            "end": "\u001b[0m",
            "error": "\u001b[31m",
            "underline": "\u001b[4m"
        }

        self.theme_colors = {
            "default": {"input": "\u001b[37m", "response": "\u001b[37;1m"},
            "pink": {"input": "\u001b[35m", "response": "\u001b[35;1m"},
            "blue": {"input": "\u001b[34m", "response": "\u001b[34;1m"},
            "green": {"input": "\u001b[32m", "response": "\u001b[32;1m"}
        }

    def style(self, text: str, message_type: str) -> str:
        """
        Returns the styled text
        """
        if message_type not in self.styles:
            # ERROR
            return text

        return f"{self.styles[message_type]}{text}{self.styles["end"]}"

    def change_theme(self, new_theme: str) -> None:
        """
        Change theme
        """
        if new_theme not in self.theme_colors:
            # ERROR
            return
        
        self.current_theme = new_theme
        return 


    def themelist(self) -> List[str]:
        return list(self.theme_colors.keys())

    def themelist_styled(self) -> str:
        """
        Returns the available themes
        """
        return "".join(
            (
                f"-> {theme}"
                if theme != self.current_theme
                else f"{self.style.bold} {theme} \n"
            )
            for theme in self.theme_colors.keys()
        )
