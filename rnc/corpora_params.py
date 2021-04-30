__all__ = (
    'Mycorp'
)

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

    class Parallel:
        Armenian = arm = 'JSONeyJkb2NfbGFuZyI6IFsiYXJtIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Bashkir = bas = 'JSONeyJkb2NfbGFuZyI6IFsiYmFzaCJdLCAiaXNfcGFyYV9ib3RoX3BhaXJzIjogW3RydWVdfQ=='
        Belarusian = bel = 'JSONeyJkb2NfbGFuZyI6IFsiYmVsIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Bulgarian = bul = 'JSONeyJkb2NfbGFuZyI6IFsiYnVsIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Buryatian = bur = 'JSONeyJkb2NfbGFuZyI6IFsiYnVhIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Chinese = ch = 'JSONeyJkb2NfbGFuZyI6IFsiemhvIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Czech = cz = 'JSONeyJkb2NfbGFuZyI6IFsiY3plIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        English = en = 'JSONeyJkb2NfbGFuZyI6IFsiZW5nIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Estonian = es = 'JSONeyJkb2NfbGFuZyI6IFsiZXN0Il0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Finnish = fin = 'JSONeyJkb2NfbGFuZyI6IFsiZmluIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        French = fr = 'JSONeyJkb2NfbGFuZyI6IFsiZnJhIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        German = ger = 'JSONeyJkb2NfbGFuZyI6IFsiZ2VyIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Italian = it = 'JSONeyJkb2NfbGFuZyI6IFsiaXRhIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Latvian = lat = 'JSONeyJkb2NfbGFuZyI6IFsibGF2Il0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Lithuanian = lit = 'JSONeyJkb2NfbGFuZyI6IFsibGl0Il0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Polish = pol = 'JSONeyJkb2NfbGFuZyI6IFsicG9sIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Spanish = sp = 'JSONeyJkb2NfbGFuZyI6IFsiZXNwIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Swedish = sw = 'JSONeyJkb2NfbGFuZyI6IFsic3ZlIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'
        Ukrainian = ukr = 'JSONeyJkb2NfbGFuZyI6IFsidWtyIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19'

        def __getitem__(self, item: str) -> str:
            """ Get attribute from Parallel.

            :exception KeyError: if the key doesn't exist.
            """
            try:
                return getattr(self, item)
            except AttributeError as e:
                raise KeyError(e)
