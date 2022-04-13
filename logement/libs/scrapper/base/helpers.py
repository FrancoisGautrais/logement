import re

from lxml import etree
class HelperException(Exception):
    pass


def identity(x):
    return x

def not_none_str(x):
    return str(x) if x is not None else ""

def get_range(x, range):
    if not hasattr(x, "__len__"):
        return x

    if len(range) == 1:
        x = x[range[0]] if len(x) > range[0] else None
    elif len(range) == 2:
        if (range[0] is None and range[1] is None):
            a, b = range[0], range[1]
            if a is not None and a >= len(x) or b is not None and b >= len(x):
                return None
            if a is None:
                x = x[:b]
            else:
                x = x[a:]
        elif range[0] is not None and range[1] is not None:
            a, b = range[0], range[1]
            if a >= len(x) or b >= len(x):
                return None
            x = x[a:b]
        else:
            return None
    return None

class BaseHelper:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.after = []
        self.cast = identity
        self.regex = None
        self.concat = lambda x, y: x+y
        if self.kwargs.get("cast"):
            self.cast = self.kwargs.pop("cast")
        if self.kwargs.get("concat"):
            self.cast = self.kwargs.pop("concat")
        if self.kwargs.get("regex"):
            self.regex = self.kwargs.pop("regex")

    def compute(self, *args, **kwargs):
        raise NotImplementedError()


    def get_value(self, *args, **kwargs):
        val = self.cast(self.compute(*args, **kwargs))
        for elem in self.after:
            if isinstance(elem, BaseHelper):
                v = elem.get_value(*args, **kwargs)
            else:
                v = elem
            val = self.concat(val, v)

        if self.regex:
            regexes = self.regex if isinstance(self.regex, (list, tuple)) else [self.regex]
            for regex in regexes:
                x = re.findall(regex, val)
                if x:
                    val=x[0]
                    break

        return val

    def __add__(self, other):
        self.after.append(other)
        return self



class HelperHtml(BaseHelper):

    def __init__(self, selector, target="d", foreach=identity, range=None, methode=None, **kwargs):
        super().__init__(**kwargs)
        self.selector = selector
        self.target = target
        self.foreach = foreach
        self.range = range
        self.methode = methode



    def compute(self, scrapper):
        pq = getattr(scrapper, self.target) if getattr(scrapper, self.target) else None
        if pq is None:
            raise HelperException(f"L'attribut {self.target} n'a pas pu etre trouvé dans l'objet "
                                  f"de type {type(scrapper)}")
        x = [self.foreach(pq(x)) for x in pq(self.selector)]
        if self.range:
            return get_range(x, self.range)
        return x


class HelperHtmlText(HelperHtml):

    def __init__(self, selector, target="d", range=None, cleaned=False, join=" ", foreach_cast=not_none_str, **kwargs):
        super().__init__(selector, target=target, foreach=self._foreach, range=range, method="text", **kwargs)
        self.cleaned = cleaned
        self.join = join
        self.foreach_cast = foreach_cast

    def _foreach(self, x):
        if x is None: return None
        x = self.foreach_cast(x.text())
        if self.cleaned:
            x = x.strip()
        return x

    def compute(self, scrapper):
        x = super().compute(scrapper)
        if x is not None:
            return self.join.join(x)
        return x


class HelperHtmlAttr(HelperHtml):

    def __init__(self, selector, attr, target="d", range=None, cleaned=False, join=" ", foreach_cast=not_none_str, **kwargs):
        super().__init__(selector, target=target, foreach=self._foreach, range=range, **kwargs)
        self.cleaned = cleaned
        self.join = join
        self.foreach_cast = foreach_cast
        self.attr=attr[0] if isinstance(attr, (list,tuple) ) else attr
        self.attrs=attr if isinstance(attr, (list,tuple) ) else [attr]

    def _foreach(self, x):
        if len(self.attrs)>1:
            for attr in self.attrs:
                ret = x.attr(attr)
                if ret is not None:
                    x=ret
                    break
            else:
                x=None
        else:
            x=x.attr(self.attr)

        x = self.foreach_cast(x)
        return x

    def compute(self, scrapper):
        x = super().compute(scrapper)
        if x is not None and self.join is not None:
            return self.join.join(x)
        return x



class HelperJson(BaseHelper):

    def __init__(self, *json_path, target="data", range=None,  **kwargs):
        super().__init__(**kwargs)
        self.json_path = json_path
        self.target = target
        self.range = range

    def compute(self, scrapper):
        data = getattr(scrapper, self.target) if getattr(scrapper, self.target) else None
        if data is None:
            raise HelperException(f"L'attribut {self.target} n'a pas pu etre trouvé dans l'objet "
                                  f"de type {type(scrapper)}")

        curr = data
        for key in self.json_path:
            if key is None: continue
            if isinstance(key, int) and isinstance(curr, list):
                if key >= len(curr): return None
                curr = curr[key]
            elif isinstance(curr, dict):
                if key not in curr: return None
                curr = curr[key]
            else:
                return None
        return curr

class HelperConst(BaseHelper):
    def __init__(self, val, **kwargs):
        super().__init__(**kwargs)
        self.value = val

    def compute(self, scrapper):
        return self.value


class HelperAttr(BaseHelper):

    def __init__(self, *json_path, target="data", range=None,  **kwargs):
        super().__init__(**kwargs)
        self.json_path = json_path
        self.target = target
        self.range = range

    def compute(self, scrapper):
        curr = scrapper
        for key in self.json_path:
            if key is None: continue
            if isinstance(key, int) and isinstance(curr, list):
                if key >= len(curr): return None
                curr = curr[key]
            else:
                if  not hasattr(curr, key): return None
                curr = getattr(curr, key)
        return curr