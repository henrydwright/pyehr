"""Functions and classes for creating and reading OpenEHR JSON files"""

from json import JSONEncoder, dumps

import numpy as np

from org.openehr.base.base_types.identification import TerminologyID, ISOOID, UUID, InternetID, VersionTreeID, HierObjectID, ObjectVersionID, ArchetypeID, TemplateID, GenericID, ObjectRef, PartyRef
from org.openehr.base.foundation_types.interval import PointInterval, ProperInterval, MultiplicityInterval
from org.openehr.rm.data_types.text import CodePhrase

class OpenEHREncoder(JSONEncoder):
    """Implementation of `json.JSONEncoder` that can be used with json.dumps() to produce
    OpenEHR ITS JSON encodings of all base and rm classes. e.g. `json.dumps(my_openehr_object, cls=OpenEHREncoder)`"""
    
    def default(self, o):
        try:
            return o.as_json()
        except:
            return super().default(o)
        




# c = CodePhrase(TerminologyID("SNOMED-CT"), "762916009", "Swelling of left foot (finding)")
# pi = PointInterval[np.int32](np.int32(0))
# pri = ProperInterval[np.int32](lower=np.int32(6), lower_included=True)
# mi = MultiplicityInterval(lower=np.int32(0), upper=np.int32(1))

# todo = [c, pi, pri, mi]

# for item in todo:
#     print(dumps(item, cls=OpenEHREncoder))
