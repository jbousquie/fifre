# Sous-fifre du domaine Winlog
# Chaque module doit implémenter la classe Specialized
# Chaque classe Specialized doit implementer les méthodes :
# - parse_order() -> bool
# - execute_order() 
from typing import Tuple, Union

from pprint import pp as pp

class Specialized:
    def __init__(self) -> None:
        pass

    # dictionnaire : langage de l'ordre <-> langage winlog
    dictionary = {
        'start': 'run',
        'stop': 'stop',
        'reboot': 'reboot'
    }


    def parse_order(self, order: str) -> Tuple[bool, str]:
        checked, msg = self.check(order)
        return checked, msg

    def execute_order(self, order: str):
        pass

    # Vérifie la syntaxe de l'ordre
    def check(self, order: str)-> Tuple[bool, str]:
        order_cleaned = order.replace('\n', '')
        words = order_cleaned.split()
        pp(words)

        action = self.translate(words[0])
        print(action)

        ret = 'ok'
        return True, ret

    def translate(self, word: str) -> Union[str, None]:
        translated = Specialized.dictionary.get(word.lower())
        return translated