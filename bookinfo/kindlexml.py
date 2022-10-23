import xmltodict

from bookinfo.kindlebase import KindleBase, KindleBaseError
from bookinfo.util import Util

class KindlexmlError(KindleBaseError):
    pass


class KindleBaseSubError(KindlexmlError):
    pass


class KindleBaseSub2Error(KindlexmlError):
    pass


class KindleXML(KindleBase):
    def __init__(self, env, env_gcp, cmd):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("using debug. start running")
        self.logger.debug("finished running")

        self.json_file_list = []

        super().__init__(env, env_gcp, cmd)

    def src2db_for_book(self, nary):
        table_name = "book"
        xml_dict = self.specific_env.target.d["xml"]
        xml_path = xml_dict['path']
        nary.extend(self.xmldictarray(xml_path))
        ret = self.dictarray2db(table_name, nary)
        return ret

    def xmldictarray(self, xml_path):
        array = []
        with open(xml_path, encoding="utf-8") as file:
            content = file.read()
            dictx = xmltodict.parse(content)
            array = [ self.get_record_data(item) for item in dictx['response']['add_update_list']['meta_data'] ]
        return array
