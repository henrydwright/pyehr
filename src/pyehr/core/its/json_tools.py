"""Functions and classes for creating and reading OpenEHR JSON files"""

from json import JSONEncoder

class OpenEHREncoder(JSONEncoder):
    """Implementation of `json.JSONEncoder` that can be used with json.dumps() to produce
    OpenEHR ITS JSON encodings of all base and rm classes. e.g. `json.dumps(my_openehr_object, cls=OpenEHREncoder)`"""
    
    def default(self, o):
        try:
            return o.as_json()
        except:
            return super().default(o)
        
