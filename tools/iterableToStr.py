
import typing

class IterableToStr:

    @classmethod
    def Convert(self, l:typing.Iterable, **d):
        sep = d.get('sep', ' ')
        head = d.get('head', '')
        tail = d.get('tail', '')
        converter = d.get('converter', repr)

        result = ''
        for item in l[:-1]:
            result+='{}{}'.format(converter(item), sep)
        result+=converter(l[-1])
        result = '{}{}{}'.format(head, result, tail)
        return result