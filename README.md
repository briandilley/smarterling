# smarterling
Utility for automating tasks with Smartling

## installation and use
Smarterling is in [PyPi](https://pypi.python.org/pypi/smarterling) and can be installed using pip:
```shell
> pip install smarterling
```
or easy_install:
```shell
> easy_install smarterling
```

Then run the smarterling command:
```shell
> smarterling --help
usage: smarterling [options]

Smarterling

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Configuration file
  -u, --upload          Upload files
  -d, --download        Download files
```

- The `-c` argument defines a configuration file to use, this value defaults to `smarterling.config`
- The `-u` argument tells smarterling to upload files
- The `-d` argument tells smarterling to download files
- If neither upload or download is specified smarterling will both upload and download
- Smarterling always uploads before downloading

## configuration
Smartling uses yaml for configuration. You may also set `api-key` and `project-id` through the environment variables `SMARTLING_API_KEY` and `SMARTLING_PROJECT_ID`. Here's a sample that uses all of the options:

```yaml

config:
    api-key: 'your smartling api key'
    project-id: 'your smartling project id'
    sandbox: false
    proxy-settings:
        username:   'proxyuser'
        password:   'proxypass'
        host:       'proxyhost'
        port:       'proxyport'

files:

    'my-java-project/src/main/reources/i18n/messages.properties':
        save-pattern: 'my-project/src/main/reources/i18n/messages_{locale_underscore}.properties'
        save-cmd: 'mv {input_file} > {output_file}'
        file-type: 'javaProperties'
        approve-content: true
        callback-url: 'http://www.whatever.com/smarterling-callback'
        retrieval-type: 'published'
        include-original-strings: false
        directives:
            name: 'value'
            another: 'value2'
            anything: 'goes here'
        filters:
            - 'native2ascii {input_file} > {output_file}'

    'my-nodejs-project/app/resources/locale/en_US/LC_MESSAGES/messages.po':
        save-pattern: 'my-nodejs-project/app/resources/locale/{locale_underscore}/LC_MESSAGES/messages.po'
        file-type:  'gettext'

    'my-android-project/res/values/strings.xml':
        save-pattern: 'my-android-project/res/values-{locale_android_res}/strings.xml'
        file-type:  'android'


```

The configuration file is basically broken into two sections: global configuration and files. The global configuration has things like your api key and project id.  The files section contains configuration about each file that you want translated.

Each file falls beneath the `files` top level configuration and has the following options:

- `save-pattern` (required) the pattern to use for saving the translated files.
  - token: `{locale}` can be used to place the locale into the path, it is in the format: `en-US`
  - token: `{locale_underscore}` can be used to place the locale into the path, it is in the format: `en_US`
  - token: `{locale_android_res}` can be used to place the locale into the path, it is in the format: `en_rUS`
  - token: `{language}` can be used to place the language into the path, it is in the format: `en`
  - token: `{region}` can be used to place the region into the path, it is in the format: `US`
- `file-type` (required) the file type, this must be one of the values supported by [Smartling](https://docs.smartling.com/display/docs/Files+API#FilesAPI-/file/upload(POST))
- `save-cmd` (optional) the command to execute when saving the file, by default the file is just saved to the location defined by `save-pattern`
  - token: `{input_file}` the input file
  - token: `{locale}` can be used to place the locale into the path, it is in the format: `en-US`
  - token: `{locale_underscore}` can be used to place the locale into the path, it is in the format: `en_US`
  - token: `{locale_android_res}` can be used to place the locale into the path, it is in the format: `en_rUS`
  - token: `{language}` can be used to place the language into the path, it is in the format: `en`
  - token: `{region}` can be used to place the region into the path, it is in the format: `US`
- `approve-content` (optional, default: `true`) whether or not to automatically approve uploaded content
- `callback-url` (optional) The calllback url for when the file is 100% translated
- `retrieval-type` (optional, default: `published`) the type of files to download
- `include-original-strings` (optional, default: `false`) whether or not to include original strings in downloaded files
- `directives` (optional) a set of name value pairs to add as directives to the uploaded file
- `filters` (optional) a set of commands to run (in order) on the file after being downloaded
  - token: `{input_file}` the input file
  - token: `{output_file}` the output file

