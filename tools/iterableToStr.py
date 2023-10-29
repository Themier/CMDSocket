
import typing

class IterableToStr:

    @classmethod
    def Convert(self, l:typing.Iterable, **d):
        sep = d.get('sep', ' ')
        head = d.get('head', '')
        tail = d.get('tail', '')
        converter = d.get('converter', repr)

        n=len(l)
        i=0
        result = ''
        for item in l:
            if i == n-1:
                result+=converter(item)
            else:
                result+='{}{}'.format(converter(item), sep)
            i+=1
        result = '{}{}{}'.format(head, result, tail)
        return result