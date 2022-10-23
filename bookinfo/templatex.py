import re
import string
import pprint
from bookinfo.util import Util

class TemplatexError(Exception):
    pass


class Templatex:
    def __init__(self, content):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("Bookstore using debug. start running")
        self.logger.debug("Bookstore finished running")
        self.pp = pprint.PrettyPrinter(indent=4)
        self.content = content
        self.lines = [
            line for line in self.content.splitlines() if len(line.strip()) > 0
        ]

    def substitute_one_item_with_array(
        self, dictx, head, tail, name_str, found, count_x
    ):
        new_lines = []
        n = 2
        ary = dictx[name_str]
        for found_str in found:
            while count_x > 0:
                new_key = "%s_%d" % (name_str, n)
                n += 1
                if dictx.get(new_key, None) is None:
                    xstr = "%s${%s}%s" % (head, new_key, tail)
                    new_lines.append(xstr)
                    dictx[new_key] = found_str
                    count_x -= 1
                    break
                self.logger.debug(f"new_key={new_key} count_x={count_x}")
        return new_lines

    def substitute_one_item(self, dictx, l, result):
        start, end = result.span()
        head = l[0:start]
        tail = l[end:]
        lines = []

        name_str = result.group(1).strip()
        found = dictx.get(name_str, None)
        if found:
            if type(found) == list:
                count_x = len(found)
                if count_x == 0:
                    raise TemplatexError(f"{name_str} don't have a value")
                else:
                    dictx[name_str] = found[0]
                    lines = [l]
                    del found[0]
                    count_x -= 1
                    lines = lines + self.substitute_one_item_with_array(
                        dictx, head, tail, name_str, found, count_x
                    )
            else:
                lines = [l]
        else:
            raise TemplatexError(f"{name_str} not found")

        return lines

    def substitute(self, dictx):
        pattern = r"\${([^$]*)}"
        new_lines = []

        for l in self.lines:
            result = re.search(pattern, l)
            if result:
                new_lines = new_lines + self.substitute_one_item(dictx, l, result)
            else:
                new_lines.append(l)

        content = "\n".join(new_lines)
        new_content = string.Template(content).substitute(dictx)

        return new_content
