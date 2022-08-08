__all__ = (
    'Mycorp'
)

from enum import Enum
from typing import Any


class Page:
    @classmethod
    def e(cls,
          value: int) -> Any:
        """" Get amount of pages exactly equals to the value """
        pass

    @classmethod
    def le(cls,
           value: int) -> Any:
        """ Get amount of pages <= than value """
        pass


class Mycorp:
    def __getitem__(self, item: str) -> str:
        """ Get attribute from Person or from Parallel.

        :exception KeyError: if there is no the item in both them.
        """
        try:
            return getattr(self.Person, item)
        except AttributeError:
            pass
        try:
            return getattr(self.Parallel, item)
        except AttributeError:
            raise KeyError(f"No key '{item}' in either Person or Parallel")

    def __getattr__(self, item: str) -> str:
        """ Get attribute from Person or from Parallel.

        :exception AttributeError: if there is no the item in both them.
        """
        try:
            return getattr(super(), item)
        except AttributeError:
            pass
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError(e)

    class Person:
        Pushkin = 'JSONeyJkb2NfYXV0aG9yIjogWyLQkC7QoS4g0J_Rg9GI0LrQuNC9Il19'
        Dostoyevsky = 'JSONeyJkb2NfYXV0aG9yIjogWyLQpC7QnC4g0JTQvtGB0YLQvtC10LLRgdC60LjQuSJdfQ%3D%3D'
        TolstoyLN = 'JSONeyJkb2NfYXV0aG9yIjogWyLQmy7QnS4g0KLQvtC70YHRgtC-0LkiXX0%3D'
        Chekhov = 'JSONeyJkb2NfYXV0aG9yIjogWyLQkC7Qny4g0KfQtdGF0L7QsiJdfQ%3D%3D'
        Gogol = 'JSONeyJkb2NfYXV0aG9yIjogWyLQnS7Qki4g0JPQvtCz0L7Qu9GMIl19'
        Turgenev = 'JSONeyJkb2NfYXV0aG9yIjogWyLQmC7QoS4g0KLRg9GA0LPQtdC90LXQsiJdfQ%3D%3D'

        def __getitem__(self, item: str) -> str:
            """ Get attribute from Person.

            :exception KeyError: if the key doesn't exist.
            """
            try:
                return getattr(self, item)
            except AttributeError as e:
                raise KeyError(e)

    # TODO: drop this compatibility
    class Parallel:
        Armenian = arm = 'hye'
        Bashkir = bas = 'bak'
        Belarusian = bel = 'bel'
        Bulgarian = bul = 'bul'
        Buryatian = bur = 'bua'
        Chinese = ch = 'zho'
        Czech = cz = 'ces'
        English = en = 'eng'
        Estonian = es = 'est'
        Finnish = fin = 'fin'
        French = fr = 'fra'
        German = ger = 'ger'
        Italian = it = 'ita'
        Latvian = lat = 'lav'
        Lithuanian = lit = 'lit'
        Polish = pol = 'pol'
        Spanish = sp = 'spa'
        Swedish = sw = 'sve'
        Ukrainian = ukr = 'ukr'

        def __getitem__(self, item: str) -> str:
            """ Get attribute from Parallel.

            :exception KeyError: if the key doesn't exist.
            """
            try:
                return getattr(self, item)
            except AttributeError as e:
                raise KeyError(e)


class Languages(Enum):
    Armenian = arm = 'hye'
    Bashkir = bas = 'bak'
    Belarusian = bel = 'bel'
    Bulgarian = bul = 'bul'
    Buryatian = bur = 'bua'
    Chinese = ch = 'zho'
    Czech = cz = 'ces'
    English = en = 'eng'
    Estonian = es = 'est'
    Finnish = fin = 'fin'
    French = fr = 'fra'
    German = ger = 'ger'
    Italian = it = 'ita'
    Latvian = lat = 'lav'
    Lithuanian = lit = 'lit'
    Polish = pol = 'pol'
    Spanish = sp = 'spa'
    Swedish = sw = 'sve'
    Ukrainian = ukr = 'ukr'
