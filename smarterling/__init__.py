
import os
import yaml
from smartlingApiSdk.UploadData import UploadData
from smartlingApiSdk.SmartlingDirective import SmartlingDirective
from smartlingApiSdk.SmartlingFileApi import \
    SmartlingFileApiFactory, \
    ProxySettings

class SmarterlingError(Exception):
    """ Thrown for various errors
    """
    pass

class AttributeDict(dict):
    """ Quick dictionary that allows for getting items
        as attributes in a convenient manner
    """
    __getattr__ = lambda self, key: self.get(key, require_value=True)
    __setattr__ = dict.__setitem__
    def get(self, key, default_val=None, require_value=False):
        """ Returns a dictionary value
        """
        val = dict.get(self, key, default_val)
        if val is None and require_value:
            raise KeyError('key "%s" not found' % key)
        if isinstance(val, dict):
            return AttributeDict(val)
        return val

def file_uri(file_name, conf):
    """ Return the file's uri
    """
    return conf.get('uri') if conf.has_key('uri') else file_name

def download_files(fapi, file_name, conf):
    """ Downloads translated versions of the files
    """
    print("Downloading %s from smartling" % file_name)
    (response, code) = fapi.last_modified(file_uri(file_name, conf))
    retrieval_type = conf.get('retrieval-type', 'published')
    include_original_strings = 'true' if conf.get('include-original-strings', False) else 'false'

    for item in response.data.items:
        item = AttributeDict(item)
        (file_response, code) = fapi.get(file_uri(file_name, conf), item.locale,
            retrievalType=retrieval_type,
            includeOriginalStrings=include_original_strings)
        file_response = str(file_response).strip()
        
        if code != 200 or len(file_response)==0:
            print("%s translation not found for %s" % (item.locale, file_name))
            continue

        # TODO: use conf['save-pattern'] to determine save location
        #       - {locale} (zh-CN)
        #       - {locale_underscore} (zh_CN)
        # TODO: save contents to save location


def get_locales(fapie, file_name, conf):
    """ Returns the locales for a file
    """

def upload_file(fapi, file_name, conf):
    """ Uploads a file to smartling
    """
    print("Uploading %s to smartling" % file_name)
    data = UploadData(
        os.path.dirname(file_name)+os.sep,
        os.path.basename(file_name),
        conf.get('file-type', ''))
    data.setUri(file_uri(file_name, conf))
    if conf.has_key('approve-content'):
        data.setApproveContent("true" if conf.get('approve-content', True) else "false")
    if conf.has_key('callback-url'):
        data.setCallbackUrl(conf.get('callback-url'))
    for name, value in conf.get('directives', {}).items():
        data.addDirective(SmartlingDirective(name, value))
    (response, code) = fapi.upload(data)
    if code!=200:
        print(repr(response))
        raise SmarterlingError("Error uploading file: %s" % file_name)
    else:
        print("Uploaded %s, wordCount: %s, stringCount: %s" % (file_name, response.data.wordCount, response.data.stringCount))

def create_file_api(conf):
    """ Creates a SmartlingFileApi from the given config
    """
    proxy_settings=None
    if conf.config.has_key('proxy-settings'):
        proxy_settings = ProxySettings(
            conf.config.get('proxy-settings').get('username', ''),
            conf.config.get('proxy-settings').get('password', ''),
            conf.config.get('proxy-settings').get('host', ''),
            int(conf.config.get('proxy-settings').get('port', '80')))
    return SmartlingFileApiFactory().getSmartlingTranslationApi(
        not conf.config.get('sandbox', False),
        conf.config.get('api-key', ''),
        conf.config.get('project-id', ''),
        proxySettings=proxy_settings) 

def parse_config(file_name='smarterling.config'):
    """ Parses a smarterling configuration file
    """
    if not os.path.exists(file_name) or not os.path.isfile(file_name):
        raise SmarterlingError('Config file not found: %s' % file_name)
    try:
        contents = None
        with open(file_name, 'r') as f:
            contents = f.read()
        contents_with_environment_variables_expanded = os.path.expandvars(contents)
        return AttributeDict(yaml.load(contents_with_environment_variables_expanded))
    except Exception as e:
        raise SmarterlingError("Error paring config file: %s" % str(e))

